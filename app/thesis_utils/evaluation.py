"""Shared sentiment evaluation helpers."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)

VALID_LABELS = ("negative", "neutral", "positive")
LABEL2ID = {label: idx for idx, label in enumerate(VALID_LABELS)}
ID2LABEL = {idx: label for label, idx in LABEL2ID.items()}


def labels_to_ids(
    values: Sequence[str | int],
    *,
    label2id: dict[str, int] | None = None,
) -> np.ndarray:
    """Convert string labels to integer ids while preserving integer inputs."""

    label_map = LABEL2ID if label2id is None else label2id
    converted = []

    for value in values:
        if isinstance(value, str):
            converted.append(label_map[value])
        else:
            converted.append(int(value))

    return np.asarray(converted, dtype=int)


def compute_classification_metrics(
    y_true: Sequence[str | int],
    y_pred: Sequence[str | int],
    *,
    model_name: str | None = None,
    test_set_name: str | None = None,
    labels: Sequence[str] = VALID_LABELS,
    label2id: dict[str, int] | None = None,
) -> dict[str, Any]:
    """Return the standard thesis classification metric row."""

    id_map = LABEL2ID if label2id is None else label2id
    true_ids = labels_to_ids(y_true, label2id=id_map)
    pred_ids = labels_to_ids(y_pred, label2id=id_map)
    label_ids = [id_map[label] for label in labels]

    precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
        true_ids,
        pred_ids,
        labels=label_ids,
        average="macro",
        zero_division=0,
    )
    precision_weighted, recall_weighted, f1_weighted, _ = precision_recall_fscore_support(
        true_ids,
        pred_ids,
        labels=label_ids,
        average="weighted",
        zero_division=0,
    )

    metrics: dict[str, Any] = {
        "n_eval": int(len(true_ids)),
        "accuracy": float(accuracy_score(true_ids, pred_ids)),
        "precision_macro": float(precision_macro),
        "recall_macro": float(recall_macro),
        "f1_macro": float(f1_macro),
        "precision_weighted": float(precision_weighted),
        "recall_weighted": float(recall_weighted),
        "f1_weighted": float(f1_weighted),
    }

    if model_name is not None:
        metrics = {"model": model_name, **metrics}
    if test_set_name is not None:
        insert_at = 1 if model_name is not None else 0
        items = list(metrics.items())
        items.insert(insert_at, ("test_set", test_set_name))
        metrics = dict(items)

    return metrics


def make_report_and_confusion_matrices(
    y_true: Sequence[str | int],
    y_pred: Sequence[str | int],
    *,
    labels: Sequence[str] = VALID_LABELS,
    label2id: dict[str, int] | None = None,
) -> tuple[str, pd.DataFrame, pd.DataFrame]:
    """Build a classification report plus raw and row-normalized matrices."""

    id_map = LABEL2ID if label2id is None else label2id
    id2label = {idx: label for label, idx in id_map.items()}
    true_ids = labels_to_ids(y_true, label2id=id_map)
    pred_ids = labels_to_ids(y_pred, label2id=id_map)
    label_ids = [id_map[label] for label in labels]
    target_names = [id2label[idx] for idx in label_ids]

    report_text = classification_report(
        true_ids,
        pred_ids,
        labels=label_ids,
        target_names=target_names,
        digits=4,
        zero_division=0,
    )

    matrix = confusion_matrix(true_ids, pred_ids, labels=label_ids)
    row_totals = matrix.sum(axis=1, keepdims=True)
    normalized = np.divide(
        matrix,
        row_totals,
        out=np.zeros_like(matrix, dtype=float),
        where=row_totals != 0,
    )

    index = [f"true_{label}" for label in labels]
    columns = [f"pred_{label}" for label in labels]

    return (
        report_text,
        pd.DataFrame(matrix, index=index, columns=columns),
        pd.DataFrame(normalized, index=index, columns=columns),
    )


def softmax_numpy(logits: np.ndarray) -> np.ndarray:
    """Compute a numerically stable softmax for numpy logits."""

    shifted = logits - np.max(logits, axis=1, keepdims=True)
    exp_logits = np.exp(shifted)
    return exp_logits / exp_logits.sum(axis=1, keepdims=True)


def chunked(sequence: Sequence[Any], batch_size: int):
    """Yield fixed-size chunks from a sequence."""

    for start in range(0, len(sequence), batch_size):
        yield sequence[start:start + batch_size]


def build_evaluation_report(
    y_true: Sequence[str],
    y_pred: Sequence[str],
    *,
    labels: Sequence[str] = VALID_LABELS,
) -> dict[str, Any]:
    """Build reusable metrics and confusion matrix dataframes."""

    matrix = confusion_matrix(y_true, y_pred, labels=labels)
    row_totals = matrix.sum(axis=1, keepdims=True)
    normalized = np.divide(
        matrix,
        row_totals,
        out=np.zeros_like(matrix, dtype=float),
        where=row_totals != 0,
    )
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "f1_macro": f1_score(y_true, y_pred, labels=labels, average="macro"),
        "f1_weighted": f1_score(y_true, y_pred, labels=labels, average="weighted"),
        "classification_report": classification_report(
            y_true,
            y_pred,
            labels=labels,
            digits=4,
            zero_division=0,
        ),
        "confusion_matrix": pd.DataFrame(matrix, index=labels, columns=labels),
        "confusion_matrix_normalized": pd.DataFrame(
            normalized,
            index=labels,
            columns=labels,
        ),
    }

