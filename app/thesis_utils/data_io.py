"""Common dataframe loading and cleaning helpers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, Sequence

import pandas as pd

from .paths import PROJECT_ROOT

BLANK_VALUES = ("", "nan", "NaN", "None", "none", "<NA>", "<na>", pd.NA)
NOISE_COLUMN_NAMES = {
    "özet",
    "değer",
    "ozet",
    "deger",
    "field",
    "value",
    "index",
}


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


def normalize_column_name(value: object) -> str:
    """Normalize a spreadsheet column name without changing its meaning."""

    normalized = str(value).strip()
    normalized = normalized.replace("\n", "_").replace("\r", "_")
    return re.sub(r"\s+", "_", normalized)


def normalize_column_key(value: object) -> str:
    """Return a lowercase key suitable for forgiving column-name matching."""

    return re.sub(r"[^a-z0-9]+", "_", str(value).lower()).strip("_")


def make_unique_columns(columns: Iterable[object]) -> list[str]:
    """Normalize column names and suffix duplicates deterministically."""

    seen: dict[str, int] = {}
    output: list[str] = []

    for column in columns:
        normalized = normalize_column_name(column)

        if normalized == "" or normalized.lower() in {"nan", "none", "<na>"}:
            normalized = "unnamed"

        if normalized not in seen:
            seen[normalized] = 0
            output.append(normalized)
        else:
            seen[normalized] += 1
            output.append(f"{normalized}_{seen[normalized]}")

    return output


def clean_string_series(series: pd.Series, *, lowercase: bool = False) -> pd.Series:
    """Strip a pandas Series and convert common empty string markers to NA."""

    cleaned = series.astype("string").str.strip().replace(list(BLANK_VALUES), pd.NA)
    return cleaned.str.lower() if lowercase else cleaned


def clean_label_series(series: pd.Series) -> pd.Series:
    """Normalize sentiment labels to lowercase strings with empty values as NA."""

    return clean_string_series(series, lowercase=True)


def natural_sort_key(value: str | Path) -> list[int | str]:
    """Sort filenames containing numbers in human order."""

    name = Path(value).name
    return [int(token) if token.isdigit() else token.lower() for token in re.split(r"(\d+)", name)]


def extract_number(
    value: object,
    patterns: Sequence[str],
    *,
    default: int,
) -> int:
    """Extract the first integer matched by the supplied regex patterns."""

    text = str(value)
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return int(match.group(1))
    return default


def extract_batch_number(path: str | Path, *, default: int = 999999) -> int:
    """Extract batch number from common annotation batch filenames."""

    stem = Path(path).stem
    return extract_number(
        stem,
        patterns=(
            r"annotation[_\s-]*batch[_\s-]*(\d+)",
            r"batch[_\s-]*(\d+)",
        ),
        default=default,
    )


def extract_annotation_number(value: object, *, default: int = 999999999) -> int:
    """Extract numeric order from an annotation id."""

    return extract_number(value, patterns=(r"(\d+)",), default=default)


def find_header_row(
    raw_df: pd.DataFrame,
    required_cols: Sequence[str] = ("annotation_id",),
    *,
    min_hits: int = 1,
    max_scan_rows: int | None = None,
) -> int | None:
    """Find the row that contains the expected header names."""

    limit = len(raw_df) if max_scan_rows is None else min(max_scan_rows, len(raw_df))
    required = {str(col).strip().lower() for col in required_cols}

    for idx in range(limit):
        row_values = set(raw_df.iloc[idx].astype(str).str.strip().str.lower().tolist())
        if sum(col in row_values for col in required) >= min_hits:
            return idx

    return None


def drop_noise_columns(
    df: pd.DataFrame,
    *,
    extra_noise_names: Sequence[str] = (),
    drop_unnamed: bool = True,
) -> pd.DataFrame:
    """Drop blank spreadsheet helper columns such as Unnamed, Ozet, Field."""

    noise = NOISE_COLUMN_NAMES.union(str(name).lower() for name in extra_noise_names)
    drop_cols = []

    for column in df.columns:
        key = str(column).lower().strip()
        if drop_unnamed and key.startswith("unnamed"):
            drop_cols.append(column)
        elif key in noise:
            drop_cols.append(column)

    return df.drop(columns=drop_cols, errors="ignore")


def read_raw_table_no_header(path: str | Path) -> pd.DataFrame:
    """Read CSV or Excel as a raw table without assuming a header row."""

    table_path = Path(path)
    suffix = table_path.suffix.lower()

    if suffix == ".xlsx":
        return pd.read_excel(table_path, header=None, dtype=object)
    if suffix == ".csv":
        return pd.read_csv(table_path, header=None, encoding="utf-8-sig", dtype=object)
    raise ValueError(f"Unsupported table format: {table_path}")


def read_annotation_excel(
    path: str | Path,
    *,
    required_cols: Sequence[str] = ("annotation_id", "sample_id", "text_en"),
    min_header_hits: int = 2,
    max_header_scan_rows: int = 10,
) -> pd.DataFrame:
    """Read an annotation Excel file with flexible header-row detection."""

    excel_path = Path(path)
    raw = pd.read_excel(excel_path, header=None)
    header_row = find_header_row(
        raw,
        required_cols=required_cols,
        min_hits=min_header_hits,
        max_scan_rows=max_header_scan_rows,
    )

    df = pd.read_excel(excel_path, header=header_row or 0)
    df.columns = [normalize_column_name(column) for column in df.columns]
    df = df.dropna(how="all").copy()
    df = drop_noise_columns(df)
    df["source_file"] = excel_path.name
    df["batch_no"] = extract_batch_number(excel_path)
    return df


def find_files_by_patterns(
    root: str | Path,
    patterns: Sequence[str],
    *,
    recursive: bool = True,
) -> list[Path]:
    """Find non-temporary files under a root for one or more glob patterns."""

    root_path = Path(root)
    found: set[Path] = set()

    if not root_path.exists():
        return []

    for pattern in patterns:
        iterator = root_path.rglob(pattern) if recursive else root_path.glob(pattern)
        found.update(path for path in iterator if path.is_file() and not path.name.startswith("~$"))

    return sorted(found, key=lambda path: (extract_batch_number(path), natural_sort_key(path)))


def find_excel_files(
    annotation_dir: str | Path,
    batch_pattern: str,
    *,
    fallback_roots: Sequence[str | Path] | None = None,
) -> list[Path]:
    """Find annotation Excel files, including project-level fallbacks."""

    annotation_root = Path(annotation_dir)
    candidate_dirs: list[Path] = [annotation_root]

    if fallback_roots is None:
        fallback_roots = (
            Path.cwd(),
            PROJECT_ROOT,
            PROJECT_ROOT / "data",
            PROJECT_ROOT / "datasets",
        )

    for root in fallback_roots:
        root_path = Path(root)
        if root_path not in candidate_dirs:
            candidate_dirs.append(root_path)

    found: set[Path] = set()
    for directory in candidate_dirs:
        if directory.exists():
            found.update(
                path for path in directory.glob(batch_pattern)
                if path.is_file() and not path.name.startswith("~$")
            )

    if not found and PROJECT_ROOT.exists():
        found.update(
            path for path in PROJECT_ROOT.rglob(batch_pattern)
            if path.is_file() and not path.name.startswith("~$")
        )

    return sorted(found, key=lambda path: (extract_batch_number(path), str(path).lower()))

