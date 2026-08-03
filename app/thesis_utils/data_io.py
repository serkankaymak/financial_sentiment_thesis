"""Common dataframe loading helpers."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def read_table(path: str | Path) -> pd.DataFrame:
    """Read a parquet, CSV or Excel table based on its extension."""

    table_path = Path(path)
    suffix = table_path.suffix.lower()
    if suffix == ".parquet":
        return pd.read_parquet(table_path)
    if suffix == ".csv":
        return pd.read_csv(table_path, encoding="utf-8-sig")
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(table_path)
    raise ValueError(f"Unsupported table format: {table_path}")


def read_first_existing(*paths: str | Path) -> tuple[pd.DataFrame, Path]:
    """Read the first existing path and return both dataframe and path."""

    for path in map(Path, paths):
        if path.exists():
            return read_table(path), path
    checked = ", ".join(str(Path(path)) for path in paths)
    raise FileNotFoundError(f"No dataset found. Checked: {checked}")

