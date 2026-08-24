"""Reusable Hugging Face training helpers for thesis notebooks."""

from __future__ import annotations

import inspect
import random
from typing import Any

import numpy as np


def set_all_seeds(seed: int = 42) -> None:
    """Set Python, NumPy and Torch random seeds when Torch is available."""

    random.seed(seed)
    np.random.seed(seed)

    try:
        import torch
    except Exception:
        return

    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def trainer_tokenizer_kwargs(trainer_cls: type, tokenizer: Any) -> dict[str, Any]:
    """Return the tokenizer argument supported by the installed Trainer version."""

    signature = inspect.signature(trainer_cls.__init__)

    if "processing_class" in signature.parameters:
        return {"processing_class": tokenizer}
    if "tokenizer" in signature.parameters:
        return {"tokenizer": tokenizer}
    return {}


def prepare_hf_dataset(
    split_df,
    tokenizer,
    *,
    text_col: str,
    label_id_col: str,
    max_length: int = 128,
):
    """Create a tokenized torch Dataset from a dataframe split."""

    from datasets import Dataset

    temp = split_df[[text_col, label_id_col]].copy()
    temp[text_col] = temp[text_col].astype(str)
    temp[label_id_col] = temp[label_id_col].astype(int)
    temp = temp.rename(columns={label_id_col: "labels"})

    dataset = Dataset.from_pandas(temp.reset_index(drop=True))

    def tokenize_fn(batch):
        return tokenizer(
            batch[text_col],
            truncation=True,
            padding="max_length",
            max_length=max_length,
        )

    dataset = dataset.map(tokenize_fn, batched=True)

    keep_cols = ["input_ids", "attention_mask", "labels"]
    if "token_type_ids" in dataset.column_names:
        keep_cols.append("token_type_ids")

    dataset.set_format(type="torch", columns=keep_cols)
    return dataset


def calculate_class_weights(
    labels,
    *,
    num_labels: int = 3,
):
    """Calculate inverse-frequency class weights."""

    label_values = np.asarray(labels, dtype=int)
    counts = np.bincount(label_values, minlength=num_labels)

    weights = []
    for class_id in range(num_labels):
        if counts[class_id] == 0:
            weights.append(1.0)
        else:
            weights.append(len(label_values) / (num_labels * counts[class_id]))

    return np.asarray(weights, dtype=float)


def normalize_finbert_label(value: object) -> str:
    """Map the original FinBERT labels to the project label names."""

    normalized = str(value).lower().strip()
    mapping = {
        "positive": "positive",
        "negative": "negative",
        "neutral": "neutral",
        "label_0": "positive",
        "label_1": "negative",
        "label_2": "neutral",
    }
    return mapping.get(normalized, normalized)


def align_finbert_classifier_to_project_labels(
    model,
    *,
    label2id: dict[str, int],
    id2label: dict[int, str],
):
    """Reorder ProsusAI/finbert classifier rows to match project label ids."""

    import torch

    original_id2label = {
        int(key): normalize_finbert_label(value)
        for key, value in model.config.id2label.items()
    }

    if set(original_id2label.values()) != set(label2id.keys()):
        raise ValueError(f"Unexpected FinBERT label mapping: {original_id2label}")

    if not hasattr(model, "classifier"):
        raise AttributeError("FinBERT model does not expose a classifier layer.")

    classifier = model.classifier
    old_weight = classifier.weight.detach().clone()
    old_bias = classifier.bias.detach().clone() if classifier.bias is not None else None
    source_id_for_label = {
        label: source_id
        for source_id, label in original_id2label.items()
    }

    with torch.no_grad():
        for target_id, target_label in id2label.items():
            source_id = source_id_for_label[target_label]
            classifier.weight[target_id].copy_(old_weight[source_id])
            if old_bias is not None:
                classifier.bias[target_id].copy_(old_bias[source_id])

    model.config.id2label = id2label.copy()
    model.config.label2id = label2id.copy()
    return model
