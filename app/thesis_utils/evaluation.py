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
)

VALID_LABELS = ("negative", "neutral", "positive")


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

