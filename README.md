# Financial Sentiment Thesis

Bu çalışma alanı notebook tabanlı deneyleri ve üretilen veri setlerini içerir.

## Klasörler

| Klasör | İçerik |
| --- | --- |
| `app/` | Sıralı deney ve analiz notebookları |
| `app/thesis_utils/` | Notebooklar arasında paylaşılan Python yardımcıları |
| `db/` | Yaşam döngüsüne göre düzenlenmiş ana veri alanı |
| `checkpoints/` | Eğitilmiş model checkpointleri ve final model dosyaları |
| `reports/` | Geçmiş notebook HTML dışa aktarımları |
| `outputs/` | Tezde kullanılan kalıcı sonuç, analiz, istatistik ve tablo çıktıları |
| `tools/` | Notebook bakım araçları |

`db/` içindeki ayrıntılı veri sözlüğü için [db/README.md](db/README.md)
dosyasına bakın. Notebooklarda dosya yollarını elle birleştirmek yerine
`thesis_utils.paths` sabitleri kullanılmalıdır.

## Kurulum

```powershell
pip install -r requirements.txt
```

## Notebook Sırası

Notebooklar hocaya anlatılacak akışa göre numaralandırılmıştır:

| Sıra | Notebook | Amaç |
| ---: | --- | --- |
| 00 | `app/00_setup_requirements.ipynb` | Kurulum ve gereksinimler |
| 01a | `app/01a_build_reuters_annotation_dataset.ipynb` | Reuters anotasyon seti hazırlığı |
| 01b | `app/01b_build_sp500_annotation_dataset.ipynb` | S&P 500 FinBERT etiketleme ve anotasyon hazırlığı |
| 02 | `app/02_evaluate_finbert_baseline.ipynb` | Hazır FinBERT baseline ve hata analizi |
| 03a | `app/03a_evaluate_unfinetuned_models_diagnostic.ipynb` | Fine-tune edilmemiş modeller acaba ne yapıyor diagnostic kontrolü |
| 03b | `app/03b_evaluate_zero_shot_sp500_external_test.ipynb` | BART MNLI zero-shot kontrol |
| 03c | `app/03c_evaluate_zero_shot_model_family_sp500_external_test.ipynb` | NLI/MNLI model ailesi zero-shot kontrol |
| 04 | `app/04_train_plain_sentiment_models.ipynb` | Tezin ana fine-tuning deneyi |
| 05 | `app/05_evaluate_sp500_finetuned_models.ipynb` | S&P 500 dış test |
| 06 | `app/06_evaluate_synthetic_finetuned_models.ipynb` | Sentetik haber testi |
| 07 | `app/07_evaluate_reuters_finetuned_models.ipynb` | Reuters dış test |
| 08 | `app/08_finetune_finbert_target_dataset.ipynb` | FinBERT'i hedef veri setinde fine-tune etme |
| 09 | `app/09_search_new_dataset.ipynb` | Ek veri seti arama ve dış test adayı |
| 10 | `app/10_multiseed_training.ipynb` | Ek random seedlerle eğitim tekrarı |
| 11 | `app/11_statistical_significance_tests.ipynb` | İç test için istatistiksel anlamlılık |
| 12 | `app/12_roberta_dataset_ablation_analysis.ipynb` | RoBERTa veri seti ablation analizi |
| 13 | `app/13_model_dataset_class_analysis.ipynb` | Model × veri seti × sınıf analizi |
| 14 | `app/14_extended_error_analysis.ipynb` | Genişletilmiş hata analizi |
| 15 | `app/15_model_efficiency_analysis.ipynb` | Model verimlilik analizi |
| 16 | `app/16_finetuned_finbert_external_evaluation_v2.ipynb` | Fine-tuned FinBERT dış testleri |
| 17 | `app/17_external_statistical_significance_tests_v3.ipynb` | Dış test için istatistiksel anlamlılık |

## Notebook Bakımı

Notebook çıktılarını temizlemek, sabit disk yollarını ortak proje yollarına
çevirmek ve uzun dataframe önizlemelerini üç satırla sınırlamak için proje
kökünde şu komutu çalıştırın:

```powershell
python tools/clean_notebooks.py
```

Eski veri klasör yapısından yeni düzene geçmek için:

```powershell
python tools/organize_data_directory.py
```

Bu taşıma aracı tekrar çalıştırılabilir; veri içeriğini değiştirmez.

## Değerlendirme Sonuçları

Tezde kullanılan sonuç dosyalarının tamamı `outputs/` altında gruplanır:

- `outputs/finetuned_model_results/`
- `outputs/external_statistical_significance/`
- `outputs/thesis_tables/`
- `outputs/zero_shot_sp500_external_test/`
- `outputs/zero_shot_sp500_external_test_model_family/`

Bu klasörlerdeki kalıcı sonuç dosyaları tez çıktısı kabul edilir. Bakım ve
refaktör sırasında bu dosyalar elle düzenlenmemeli, silinmemeli veya yeniden
adlandırılmamalıdır. Yeni sonuç gerekiyorsa ilgili notebook sırasıyla
çalıştırılmalı ve mevcut sonuçlarla farkı ayrıca kontrol edilmelidir.

Eğitim notebookları tekrar üretimi pahalı olan checkpointleri, final modelleri,
splitleri ve `run_config.json` dosyalarını `checkpoints/` altında korur.

Arşiv alırken ağır veya tekrar üretilebilir dosyaları dışarıda bırakmak için
kök dizindeki `checkpoints/` ve `db/` klasörlerini hariç tutabilirsiniz.

Notebooklarda ortak yollar için:

```python
from thesis_utils import DATA_ROOT, PROJECT_ROOT, paths

annotation_dir = paths.SP500_ANNOTATION_DIR
```

Tablo okumak için:

```python
from thesis_utils.data_io import read_first_existing, read_table
```

Tekrarlayan notebook yardımcıları için:

```python
from thesis_utils.data_io import clean_label_series, extract_batch_number
from thesis_utils.evaluation import compute_classification_metrics
from thesis_utils.statistics import holm_adjust, mcnemar_test
```
