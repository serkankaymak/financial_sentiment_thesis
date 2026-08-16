"""Normalize thesis notebooks after exploratory work.

Run from the project root:
    python tools/clean_notebooks.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = PROJECT_ROOT / "app"
SHARED_IMPORT = (
    "from thesis_utils import APP_ROOT, DATA_ROOT, PREVIEW_ROWS, PROJECT_ROOT, paths\n"
)
PATH_CONSTANTS = (
    "AGGREGATED_FINANCIAL_NEWS_PATH",
    "PLAIN_SENTIMENT_DATASET_CSV_PATH",
    "PLAIN_SENTIMENT_DATASET_PARQUET_PATH",
    "PLAIN_SENTIMENT_SPLIT_V1_DIR",
    "REUTERS_ANNOTATION_BATCHES_DIR",
    "REUTERS_ANNOTATION_DIR",
    "SP500_ANNOTATION_MASTER_CSV_PATH",
    "SP500_ANNOTATION_MASTER_PARQUET_PATH",
    "SP500_ANNOTATION_MASTER_XLSX_PATH",
    "SP500_ANNOTATION_PREPARATION_BATCHES_DIR",
    "SP500_FINBERT_LABELED_HEADLINES_PATH",
    "SP500_FINBERT_LABELED_HEADLINES_PARQUET_PATH",
    "SP500_FINBERT_LABELED_HEADLINES_XLSX_PATH",
    "SP500_FINBERT_LABELING_PROGRESS_PATH",
    "SP500_HUMAN_REVIEW_BATCHES_DIR",
    "SP500_RAW_HEADLINES_PATH",
    "SYNTHETIC_NEWS_DIR",
    "TRAINING_DATASETS_DIR",
)

PROJECT_PATH = r'Path(r"D:\serkan.kaymak\financial_sentiment_thesis")'
DATA_PATH = r'Path(r"D:\serkan.kaymak\financial_sentiment_thesis\db")'
SP500_ANNOTATION_PATH = (
    r'Path(r"D:\serkan.kaymak\financial_sentiment_thesis\db\annotation_sets")'
)


def normalize_source(source: str) -> str:
    """Apply conservative readability and portability rewrites."""

    source = source.replace(
        "from thesis_utils import DATA_ROOT, PREVIEW_ROWS, PROJECT_ROOT\n",
        "",
    )
    source = source.replace(
        "from thesis_utils import APP_DATA_ROOT, APP_ROOT, DATA_ROOT, PREVIEW_ROWS, PROJECT_ROOT\n"
        "from thesis_utils.paths import REUTERS_ANNOTATION_DIR, SP500_ANNOTATION_DIR, SYNTHETIC_NEWS_DIR\n",
        "",
    )
    source = source.replace(SP500_ANNOTATION_PATH, "SP500_HUMAN_REVIEW_BATCHES_DIR")
    source = source.replace(DATA_PATH, "DATA_ROOT")
    source = source.replace(PROJECT_PATH, "PROJECT_ROOT")
    source = source.replace('PROJECT_DIR / "db"', "DATA_ROOT")
    source = source.replace(
        'PROJECT_DIR / "checkpoints" / "financial_sentiment_multi_model"',
        "paths.MODEL_CHECKPOINT_ROOT",
    )
    source = source.replace(
        'PROJECT_ROOT / "checkpoints" / "financial_sentiment_multi_model"',
        "paths.MODEL_CHECKPOINT_ROOT",
    )
    source = source.replace(
        'BASE_CHECKPOINT_ROOT / "statistical_significance"',
        'paths.MODEL_RESULTS_ROOT / "statistical_significance"',
    )
    source = source.replace(
        'CHECKPOINT_ROOT / "model_dataset_class_analysis"',
        'paths.MODEL_RESULTS_ROOT / "model_dataset_class_analysis"',
    )
    source = source.replace(
        'CHECKPOINT_ROOT / "extended_error_analysis"',
        'paths.MODEL_RESULTS_ROOT / "extended_error_analysis"',
    )
    source = source.replace(
        'CHECKPOINT_ROOT / "model_efficiency"',
        'paths.MODEL_RESULTS_ROOT / "model_efficiency"',
    )
    source = source.replace(
        'CHECKPOINT_ROOT / "results"',
        'paths.MODEL_RESULTS_ROOT / "training_evaluation"',
    )
    source = source.replace(
        'RUN_DIR / "results"',
        'paths.MODEL_RESULTS_ROOT / RUN_NAME / "training_evaluation"',
    )
    source = source.replace(
        'RUN_DIR / "external_evaluation"',
        'paths.MODEL_RESULTS_ROOT / "finbert_target_finetuned_seed42" / "external_evaluation"',
    )
    source = source.replace(
        'MULTISEED_ROOT = BASE_CHECKPOINT_ROOT / "multiseed"\n'
        'MULTISEED_ROOT.mkdir(parents=True, exist_ok=True)',
        'MULTISEED_ROOT = BASE_CHECKPOINT_ROOT / "multiseed"\n'
        'MULTISEED_RESULTS_ROOT = paths.MODEL_RESULTS_ROOT / "multiseed"\n'
        'MULTISEED_ROOT.mkdir(parents=True, exist_ok=True)\n'
        'MULTISEED_RESULTS_ROOT.mkdir(parents=True, exist_ok=True)',
    )
    source = source.replace(
        'ABLATION_ROOT = CHECKPOINT_ROOT / "dataset_ablation_roberta"\n'
        'ABLATION_ROOT.mkdir(parents=True, exist_ok=True)',
        'ABLATION_ROOT = CHECKPOINT_ROOT / "dataset_ablation_roberta"\n'
        'ABLATION_RESULTS_ROOT = paths.MODEL_RESULTS_ROOT / "dataset_ablation_roberta"\n'
        'ABLATION_ROOT.mkdir(parents=True, exist_ok=True)\n'
        'ABLATION_RESULTS_ROOT.mkdir(parents=True, exist_ok=True)',
    )
    source = source.replace(
        '    results_dir = run_dir / "results"',
        '    results_dir = MULTISEED_RESULTS_ROOT / f"{model_cfg[\'model_key\']}_seed{seed}" / "results"',
    )
    if "ABLATION_RESULTS_ROOT" in source:
        source = source.replace(
            '    results_dir = MULTISEED_RESULTS_ROOT / f"{model_cfg[\'model_key\']}_seed{seed}" / "results"',
            '    results_dir = ABLATION_RESULTS_ROOT / exp_name / "results"',
        )
    source = source.replace(
        'AGGREGATE_RESULTS_PATH = MULTISEED_ROOT / "multiseed_results_new_seeds.csv"',
        'AGGREGATE_RESULTS_PATH = MULTISEED_RESULTS_ROOT / "multiseed_results_new_seeds.csv"',
    )
    source = source.replace(
        'all_seed_results_path = MULTISEED_ROOT / "multiseed_results_with_seed42.csv"',
        'all_seed_results_path = MULTISEED_RESULTS_ROOT / "multiseed_results_with_seed42.csv"',
    )
    source = source.replace(
        'summary_path = MULTISEED_ROOT / "multiseed_mean_std_summary.csv"',
        'summary_path = MULTISEED_RESULTS_ROOT / "multiseed_mean_std_summary.csv"',
    )
    source = source.replace(
        'result_path = ABLATION_ROOT / "roberta_dataset_ablation_results.csv"',
        'result_path = ABLATION_RESULTS_ROOT / "roberta_dataset_ablation_results.csv"',
    )
    source = source.replace(
        'difference_path = ABLATION_ROOT / "roberta_dataset_ablation_differences.csv"',
        'difference_path = ABLATION_RESULTS_ROOT / "roberta_dataset_ablation_differences.csv"',
    )
    source = source.replace(
        'CHECKPOINT_ROOT\n    / "finbert_target_finetuned_seed42"\n    / "results"\n    / "finbert_target_finetune_summary.csv"',
        'paths.MODEL_RESULTS_ROOT\n    / "finbert_target_finetuned_seed42"\n    / "training_evaluation"\n    / "finbert_target_finetune_summary.csv"',
    )
    source = source.replace(
        'PROJECT_ROOT / "outputs"',
        "paths.OUTPUTS_ROOT",
    )
    source = source.replace(
        'PROJECT_DIR / "results"',
        "paths.OUTPUTS_ROOT",
    )
    source = source.replace('currentDir / "data"', "APP_DATA_ROOT")
    source = source.replace("currentDir = Path().resolve()", "currentDir = APP_ROOT")
    source = source.replace(
        'DATA_ROOT / "sentetik_finans_haberleri"',
        "SYNTHETIC_NEWS_DIR",
    )
    source = source.replace(
        'DATA_ROOT / "annotation_sets_reuters_5000"',
        "REUTERS_ANNOTATION_DIR",
    )
    source = source.replace(
        'DB_DIR / "annotation_sets_reuters_5000"',
        "REUTERS_ANNOTATION_DIR",
    )
    source = source.replace(
        'DB_DIR / "annotations" / "reuters_5000"',
        "REUTERS_ANNOTATION_DIR",
    )
    source = source.replace(
        'OUT_DIR / "batches_50"',
        "REUTERS_ANNOTATION_BATCHES_DIR",
    )
    source = source.replace(
        'DATA_DIR / "annotation_batches_10_balanced_1500"',
        "SP500_ANNOTATION_PREPARATION_BATCHES_DIR",
    )
    source = source.replace(
        'DATA_ROOT / "model_splits" / "plain_sentiment_split_v1"',
        "PLAIN_SENTIMENT_SPLIT_V1_DIR",
    )
    source = source.replace(
        'DATA_DIR / "sp500_annotation_1500_balanced_master.xlsx"',
        "SP500_ANNOTATION_MASTER_XLSX_PATH",
    )
    source = source.replace(
        'DATA_DIR / "sp500_annotation_1500_balanced_master.csv"',
        "SP500_ANNOTATION_MASTER_CSV_PATH",
    )
    source = source.replace(
        'DATA_DIR / "sp500_annotation_1500_balanced_master.parquet"',
        "SP500_ANNOTATION_MASTER_PARQUET_PATH",
    )
    source = source.replace(
        'list(DB_DIR.rglob("news_final.csv"))',
        "[AGGREGATED_FINANCIAL_NEWS_PATH]",
    )
    source = source.replace(
        'candidate_files = [AGGREGATED_FINANCIAL_NEWS_PATH]\n\n'
        "if not candidate_files:",
        "NEWS_PATH = AGGREGATED_FINANCIAL_NEWS_PATH\n\n"
        "if not NEWS_PATH.exists():",
    )
    source = source.replace("\nNEWS_PATH = candidate_files[0]\n", "\n")
    source = source.replace(
        'OUT_CSV = DATA_DIR / "sp500_headlines_2008_2024_labeled.csv"',
        "OUT_CSV = SP500_FINBERT_LABELED_HEADLINES_PATH",
    )
    source = source.replace(
        'PROGRESS_PARQUET = DATA_DIR / "sp500_headlines_2008_2024_labeled_progress.parquet"',
        "PROGRESS_PARQUET = SP500_FINBERT_LABELING_PROGRESS_PATH",
    )
    source = source.replace(
        "FILE_PATH_OVERRIDE = None",
        "FILE_PATH_OVERRIDE = SP500_RAW_HEADLINES_PATH",
    )
    source = source.replace(
        "OUT_PARQUET = FILE_PATH.with_name(FILE_PATH.stem + \"_labeled.parquet\")",
        "OUT_PARQUET = SP500_FINBERT_LABELED_HEADLINES_PARQUET_PATH",
    )
    source = source.replace(
        "OUT_CSV = FILE_PATH.with_name(FILE_PATH.stem + \"_labeled.csv\")",
        "OUT_CSV = SP500_FINBERT_LABELED_HEADLINES_PATH",
    )
    source = source.replace(
        "OUT_XLSX = FILE_PATH.with_name(FILE_PATH.stem + \"_labeled.xlsx\")",
        "OUT_XLSX = SP500_FINBERT_LABELED_HEADLINES_XLSX_PATH",
    )
    source = source.replace(
        "PROGRESS_PARQUET = FILE_PATH.with_name(FILE_PATH.stem + \"_labeled_progress.parquet\")",
        "PROGRESS_PARQUET = SP500_FINBERT_LABELING_PROGRESS_PATH",
    )
    source = source.replace(
        'DATA_DIR / "annotation_sets"',
        "SP500_HUMAN_REVIEW_BATCHES_DIR",
    )
    source = source.replace("DATA_DIR = APP_DATA_ROOT", "DATA_DIR = TRAINING_DATASETS_DIR")
    source = source.replace(
        'DATA_DIR / "plain_sentiment_df.parquet"',
        "PLAIN_SENTIMENT_DATASET_PARQUET_PATH",
    )
    source = source.replace(
        'DATA_DIR / "plain_sentiment_df.csv"',
        "PLAIN_SENTIMENT_DATASET_CSV_PATH",
    )
    source = source.replace(
        'PROJECT_DIR / "app" / "data" / "plain_sentiment_df.csv"',
        "PLAIN_SENTIMENT_DATASET_CSV_PATH",
    )
    source = source.replace(
        r"D:\serkan.kaymak\financial_sentiment_thesis\db\annotation_sets_reuters_5000",
        "db/annotations/reuters_5000",
    )
    source = source.replace("news_final.csv", "aggregated_financial_news_enriched.csv")
    source = source.replace(
        'RESULT_DIR = ANNOTATION_DIR / "unbiased_eval_results"\n'
        "RESULT_DIR.mkdir(parents=True, exist_ok=True)\n\n",
        "",
    )
    source = source.replace("SAVE_RESULTS = True\n", "")
    source = source.replace('print("SAVE_RESULTS:", SAVE_RESULTS)\n', "")
    source = re.sub(
        r"# ============================================================\n"
        r"# CELL 10 - SONU.*?"
        r"Kaydetmek istersen CELL 1'de SAVE_RESULTS=True yap.*?\n",
        "# ============================================================\n"
        "# CELL 10 - SONUC NOTU\n"
        "# Degerlendirme sonuclari notebook ekraninda gosterilir.\n"
        "# Hizli yeniden uretilebildikleri icin diske kaydedilmez.\n"
        "# ============================================================\n"
        'print("Degerlendirme tamamlandi. Sonuclar diske kaydedilmedi.")\n',
        source,
        flags=re.DOTALL,
    )
    source = source.replace(
        "def evaluate_and_save_report(trainer, dataset, split_name, run_dir, run_name):",
        "def evaluate_model(trainer, dataset, split_name, run_name):",
    )
    source = re.sub(
        r"\n    split_report_dir = run_dir / \"reports\"\n"
        r"    split_report_dir\.mkdir\(parents=True, exist_ok=True\)\n\n"
        r"    with open\(split_report_dir / f\"\{split_name\}_classification_report\.txt\", \"w\", encoding=\"utf-8\"\) as f:\n"
        r"        f\.write\(report_text\)\n\n"
        r"    cm_df\.to_csv\(split_report_dir / f\"\{split_name\}_confusion_matrix\.csv\", encoding=\"utf-8-sig\"\)\n\n"
        r"    with open\(split_report_dir / f\"\{split_name\}_metrics\.json\", \"w\", encoding=\"utf-8\"\) as f:\n"
        r"        json\.dump\(metrics, f, ensure_ascii=False, indent=2\)\n\n"
        r"    pred_df = pd\.DataFrame\(\{\n"
        r"        \"y_true_id\": y_true,\n"
        r"        \"y_pred_id\": y_pred,\n"
        r"        \"y_true\": \[ID2LABEL\[int\(x\)\] for x in y_true\],\n"
        r"        \"y_pred\": \[ID2LABEL\[int\(x\)\] for x in y_pred\],\n"
        r"    \}\)\n\n"
        r"    pred_df\.to_csv\(split_report_dir / f\"\{split_name\}_predictions\.csv\", index=False, encoding=\"utf-8-sig\"\)\n",
        "",
        source,
    )
    source = source.replace('    report_dir = run_dir / "reports"\n', "")
    source = source.replace("    report_dir.mkdir(parents=True, exist_ok=True)\n", "")
    source = source.replace("evaluate_and_save_report(", "evaluate_model(")
    source = source.replace("        run_dir=run_dir,\n", "")
    source = re.sub(
        r"\n    # Her modelden sonra an.*?"
        r"    temp_summary_df\.to_excel\(\n"
        r"        RESULTS_DIR / \"multi_model_results_partial\.xlsx\",\n"
        r"        index=False\n"
        r"    \)\n",
        "",
        source,
        flags=re.DOTALL,
    )
    source = re.sub(
        r"\nsummary_csv = RESULTS_DIR / \"multi_model_results_summary\.csv\"\n"
        r"summary_xlsx = RESULTS_DIR / \"multi_model_results_summary\.xlsx\"\n"
        r"summary_parquet = RESULTS_DIR / \"multi_model_results_summary\.parquet\"\n\n"
        r"summary_df\.to_csv\(summary_csv, index=False, encoding=\"utf-8-sig\"\)\n"
        r"summary_df\.to_excel\(summary_xlsx, index=False\)\n"
        r"summary_df\.to_parquet\(summary_parquet, index=False\)\n",
        "",
        source,
    )
    source = re.sub(
        r"\nprint\(\"\\nSummary kaydedildi:\"\)\n"
        r"print\(summary_csv\)\n"
        r"print\(summary_xlsx\)\n"
        r"print\(summary_parquet\)\n",
        "",
        source,
    )
    source = source.replace("RESULTS_DIR.mkdir(parents=True, exist_ok=True)\n", "")
    for constant in PATH_CONSTANTS:
        source = re.sub(
            rf"(?<![\w.]){constant}\b",
            f"paths.{constant}",
            source,
        )
    source = source.replace(".head()", ".head(PREVIEW_ROWS)")
    source = source.replace(".tail()", ".tail(PREVIEW_ROWS)")
    source = source.replace("[:10]", "[:PREVIEW_ROWS]")
    source = source.replace("[-10:]", "[-PREVIEW_ROWS:]")
    source = source.replace("[:5]", "[:PREVIEW_ROWS]")
    source = source.replace("[-5:]", "[-PREVIEW_ROWS:]")
    source = re.sub(r"\.head\((?:5|10|20|30|50|100)\)", ".head(PREVIEW_ROWS)", source)
    source = re.sub(r"\.tail\((?:5|10|20|30|50|100)\)", ".tail(PREVIEW_ROWS)", source)
    source = re.sub(r"([İi]lk|ilk) (?:5|10|20|30|50)", r"\1 3", source)
    source = re.sub(r"([Ss]on|son) (?:5|10|20|30|50)", r"\1 3", source)
    source = source.replace(
        "def print_annotation_batch(batch_no=1):",
        "def print_annotation_batch(batch_no=1, preview_rows=PREVIEW_ROWS):",
    )
    source = source.replace(
        "temp = annotation_df.iloc[start:end].copy()",
        "temp = annotation_df.iloc[start:end].head(preview_rows).copy()",
    )
    return source


def strip_shared_imports(source: str) -> str:
    """Remove generated shared imports before inserting one canonical block."""

    source = re.sub(
        r"from thesis_utils import APP_DATA_ROOT, APP_ROOT, DATA_ROOT, PREVIEW_ROWS, PROJECT_ROOT\n"
        r"from thesis_utils\.paths import \(\n"
        r"(?:    [A-Z0-9_]+,\n)+"
        r"\)\n",
        "",
        source,
    )
    source = source.replace(
        "from thesis_utils import APP_ROOT, DATA_ROOT, PREVIEW_ROWS, PROJECT_ROOT, paths\n",
        "",
    )
    source = source.replace(
        "from thesis_utils import APP_DATA_ROOT, APP_ROOT, DATA_ROOT, PREVIEW_ROWS, PROJECT_ROOT\n"
        "from thesis_utils.paths import REUTERS_ANNOTATION_DIR, SP500_ANNOTATION_DIR, SYNTHETIC_NEWS_DIR\n",
        "",
    )
    return source


def clean_notebook(path: Path) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]

    for cell in notebook["cells"]:
        source = "".join(cell.get("source", []))
        source = strip_shared_imports(source)
        cell["source"] = normalize_source(source).splitlines(keepends=True)
        if cell["cell_type"] == "code":
            cell["execution_count"] = None
            cell["outputs"] = []

    if code_cells:
        first_source = "".join(code_cells[0].get("source", []))
        code_cells[0]["source"] = (SHARED_IMPORT + first_source).splitlines(keepends=True)

    path.write_text(
        json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    notebooks = sorted(APP_ROOT.glob("*.ipynb"))
    for notebook in notebooks:
        clean_notebook(notebook)
        print(f"cleaned: {notebook.relative_to(PROJECT_ROOT)}")
    print(f"total notebooks: {len(notebooks)}")


if __name__ == "__main__":
    main()
