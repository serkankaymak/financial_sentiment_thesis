"""Canonical project paths shared by notebooks.

The folder on disk is still named ``db`` for compatibility with completed
experiments. In code, use ``DATA_ROOT`` because it contains datasets rather
than a database.
"""

from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = APP_ROOT.parent

DATA_ROOT = PROJECT_ROOT / "db"
CHECKPOINT_ROOT = PROJECT_ROOT / "checkpoints"
APP_DATA_ROOT = APP_ROOT / "data"

RAW_DATA_DIR = DATA_ROOT / "raw"
PROCESSED_DATA_DIR = DATA_ROOT / "processed"
TRAINING_DATASETS_DIR = PROCESSED_DATA_DIR / "training_datasets"
INTERIM_DATA_DIR = DATA_ROOT / "interim"
ANNOTATIONS_DIR = DATA_ROOT / "annotations"
SPLITS_DIR = DATA_ROOT / "splits"
EVALUATION_DATA_DIR = DATA_ROOT / "evaluation"

AGGREGATED_FINANCIAL_NEWS_PATH = (
    PROCESSED_DATA_DIR / "aggregated_financial_news_enriched.csv"
)
MARKET_SENTIMENT_MODELING_MASTER_PATH = (
    PROCESSED_DATA_DIR / "market_sentiment_modeling_master.parquet"
)
PSEUDO_LABELED_NEWS_CONFIDENCE_090_PATH = (
    INTERIM_DATA_DIR / "pseudo_labeled_news_confidence_090.parquet"
)
PLAIN_SENTIMENT_DATASET_CSV_PATH = (
    TRAINING_DATASETS_DIR / "plain_sentiment_dataset.csv"
)
PLAIN_SENTIMENT_DATASET_PARQUET_PATH = (
    TRAINING_DATASETS_DIR / "plain_sentiment_dataset.parquet"
)
TARGET_LEVEL_SENTIMENT_DATASET_CSV_PATH = (
    TRAINING_DATASETS_DIR / "target_level_sentiment_dataset.csv"
)
TARGET_LEVEL_SENTIMENT_DATASET_PARQUET_PATH = (
    TRAINING_DATASETS_DIR / "target_level_sentiment_dataset.parquet"
)

SP500_RAW_HEADLINES_PATH = RAW_DATA_DIR / "sp500_headlines_2008_2024_raw.csv"
SP500_FINBERT_LABELED_HEADLINES_PATH = (
    PROCESSED_DATA_DIR / "sp500_headlines_2008_2024_finbert_labeled.csv"
)
SP500_FINBERT_LABELED_HEADLINES_PARQUET_PATH = (
    PROCESSED_DATA_DIR / "sp500_headlines_2008_2024_finbert_labeled.parquet"
)
SP500_FINBERT_LABELED_HEADLINES_XLSX_PATH = (
    PROCESSED_DATA_DIR / "sp500_headlines_2008_2024_finbert_labeled.xlsx"
)
SP500_FINBERT_LABELING_PROGRESS_PATH = (
    INTERIM_DATA_DIR / "sp500_headlines_2008_2024_finbert_labeling_progress.parquet"
)

SP500_ANNOTATION_DIR = ANNOTATIONS_DIR / "sp500_balanced_1500"
SP500_ANNOTATION_PREPARATION_BATCHES_DIR = (
    SP500_ANNOTATION_DIR / "preparation_batches_10"
)
SP500_HUMAN_REVIEW_BATCHES_DIR = ANNOTATIONS_DIR / "sp500_human_review_batches"
SP500_ANNOTATION_MASTER_CSV_PATH = (
    SP500_ANNOTATION_DIR / "sp500_balanced_1500_annotation_master.csv"
)
SP500_ANNOTATION_MASTER_PARQUET_PATH = (
    SP500_ANNOTATION_DIR / "sp500_balanced_1500_annotation_master.parquet"
)
SP500_ANNOTATION_MASTER_XLSX_PATH = (
    SP500_ANNOTATION_DIR / "sp500_balanced_1500_annotation_master.xlsx"
)

REUTERS_ANNOTATION_DIR = ANNOTATIONS_DIR / "reuters_5000"
REUTERS_ANNOTATION_BATCHES_DIR = REUTERS_ANNOTATION_DIR / "annotation_batches_50"
SYNTHETIC_NEWS_DIR = EVALUATION_DATA_DIR / "synthetic_financial_news"
MODEL_SPLITS_DIR = SPLITS_DIR
PLAIN_SENTIMENT_SPLIT_V1_DIR = SPLITS_DIR / "plain_sentiment_v1"


def ensure_data_directories() -> None:
    """Create the standard writable dataset directories when needed."""

    for path in (
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        TRAINING_DATASETS_DIR,
        INTERIM_DATA_DIR,
        SP500_ANNOTATION_DIR,
        SP500_ANNOTATION_PREPARATION_BATCHES_DIR,
        SP500_HUMAN_REVIEW_BATCHES_DIR,
        REUTERS_ANNOTATION_DIR,
        REUTERS_ANNOTATION_BATCHES_DIR,
        SYNTHETIC_NEWS_DIR,
        PLAIN_SENTIMENT_SPLIT_V1_DIR,
    ):
        path.mkdir(parents=True, exist_ok=True)
