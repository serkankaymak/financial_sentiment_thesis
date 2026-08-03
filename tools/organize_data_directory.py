"""Move legacy thesis datasets into a descriptive directory structure.

Run once from the project root:
    python tools/organize_data_directory.py

The migration is idempotent: existing targets are accepted only when the
legacy source no longer exists. No dataset contents are modified.
"""

from __future__ import annotations

from pathlib import Path
from shutil import move

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = PROJECT_ROOT / "db"

MOVES = (
    ("news_final.csv", "processed/aggregated_financial_news_enriched.csv"),
    (
        "final_master_dataset.parquet",
        "processed/market_sentiment_modeling_master.parquet",
    ),
    (
        "pseudo_labeled_news_conf090.parquet",
        "interim/pseudo_labeled_news_confidence_090.parquet",
    ),
    ("sp500_headlines_2008_2024.csv", "raw/sp500_headlines_2008_2024_raw.csv"),
    (
        "sp500_headlines_2008_2024_labeled.csv",
        "processed/sp500_headlines_2008_2024_finbert_labeled.csv",
    ),
    (
        "sp500_headlines_2008_2024_labeled_progress.parquet",
        "interim/sp500_headlines_2008_2024_finbert_labeling_progress.parquet",
    ),
    (
        "sp500_annotation_1500_balanced_master.csv",
        "annotations/sp500_balanced_1500/sp500_balanced_1500_annotation_master.csv",
    ),
    (
        "sp500_annotation_1500_balanced_master.parquet",
        "annotations/sp500_balanced_1500/sp500_balanced_1500_annotation_master.parquet",
    ),
    (
        "annotation_batches_10_balanced_1500",
        "annotations/sp500_balanced_1500/preparation_batches_10",
    ),
    ("annotation_sets", "annotations/sp500_human_review_batches"),
    ("annotation_sets_reuters_5000", "annotations/reuters_5000"),
    (
        "annotations/reuters_5000/batches_50",
        "annotations/reuters_5000/annotation_batches_50",
    ),
    ("model_splits/plain_sentiment_split_v1", "splits/plain_sentiment_v1"),
    ("model_splits", "splits_legacy_empty"),
    ("sentetik_finans_haberleri", "evaluation/synthetic_financial_news"),
)

APP_DATA_MOVES = (
    ("plain_sentiment_df.csv", "plain_sentiment_dataset.csv"),
    ("plain_sentiment_df.parquet", "plain_sentiment_dataset.parquet"),
    ("target_level_sentiment_df.csv", "target_level_sentiment_dataset.csv"),
    ("target_level_sentiment_df.parquet", "target_level_sentiment_dataset.parquet"),
)


def resolve_in_data_root(relative_path: str) -> Path:
    """Resolve a migration path and reject targets outside db/."""

    path = (DATA_ROOT / relative_path).resolve()
    if path != DATA_ROOT.resolve() and DATA_ROOT.resolve() not in path.parents:
        raise ValueError(f"Path leaves DATA_ROOT: {relative_path}")
    return path


def migrate(source_name: str, target_name: str) -> None:
    source = resolve_in_data_root(source_name)
    target = resolve_in_data_root(target_name)

    if not source.exists():
        if target.exists():
            print(f"already migrated: {target.relative_to(DATA_ROOT)}")
            return
        print(f"not found, skipped: {source.relative_to(DATA_ROOT)}")
        return

    if target.exists():
        raise FileExistsError(f"Target already exists: {target}")

    target.parent.mkdir(parents=True, exist_ok=True)
    move(str(source), str(target))
    print(f"moved: {source.relative_to(DATA_ROOT)} -> {target.relative_to(DATA_ROOT)}")


def remove_empty_legacy_directory() -> None:
    legacy_dir = DATA_ROOT / "splits_legacy_empty"
    if legacy_dir.exists() and not any(legacy_dir.iterdir()):
        legacy_dir.rmdir()
        print("removed empty legacy directory: splits_legacy_empty")


def migrate_app_data() -> None:
    """Move datasets out of app/ so that app contains code only."""

    app_data_dir = PROJECT_ROOT / "app" / "data"
    training_data_dir = DATA_ROOT / "processed" / "training_datasets"
    for source_name, target_name in APP_DATA_MOVES:
        source = app_data_dir / source_name
        target = training_data_dir / target_name
        if not source.exists():
            if target.exists():
                print(f"already migrated: {target.relative_to(DATA_ROOT)}")
                continue
            print(f"not found, skipped: {source.relative_to(PROJECT_ROOT)}")
            continue
        if target.exists():
            raise FileExistsError(f"Target already exists: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        move(str(source), str(target))
        print(f"moved: {source.relative_to(PROJECT_ROOT)} -> {target.relative_to(DATA_ROOT)}")

    if app_data_dir.exists() and not any(app_data_dir.iterdir()):
        app_data_dir.rmdir()
        print("removed empty legacy directory: app/data")


def main() -> None:
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    for source_name, target_name in MOVES:
        migrate(source_name, target_name)
    remove_empty_legacy_directory()
    migrate_app_data()


if __name__ == "__main__":
    main()
