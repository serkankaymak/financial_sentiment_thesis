"""Small display helpers that keep notebook output readable."""

from __future__ import annotations

from typing import Any

PREVIEW_ROWS = 3


def preview(value: Any, rows: int = PREVIEW_ROWS) -> Any:
    """Return a short notebook-friendly preview when ``head`` is available."""

    head = getattr(value, "head", None)
    return head(rows) if callable(head) else value

