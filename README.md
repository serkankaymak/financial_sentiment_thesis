# Financial Sentiment Thesis

Bu çalışma alanı notebook tabanlı deneyleri ve üretilen veri setlerini içerir.

## Klasörler

| Klasör | İçerik |
| --- | --- |
| `app/` | Sıralı deney ve analiz notebookları |
| `app/thesis_utils/` | Notebooklar arasında paylaşılan Python yardımcıları |
| `db/` | Yaşam döngüsüne göre düzenlenmiş ana veri alanı |
| `checkpoints/` | Eğitilmiş model checkpointleri ve raporları |
| `reports/` | Geçmiş notebook HTML dışa aktarımları |
| `tools/` | Notebook bakım araçları |

`db/` içindeki ayrıntılı veri sözlüğü için [db/README.md](db/README.md)
dosyasına bakın. Notebooklarda dosya yollarını elle birleştirmek yerine
`thesis_utils.paths` sabitleri kullanılmalıdır.

## Kurulum

```powershell
pip install -r requirements.txt
```

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

Test notebookları metrikleri ve örnek tahminleri ekranda gösterir. Yeniden
çalıştırılmaları kısa sürdüğü için prediction CSV, confusion matrix ve özet
rapor dosyaları kalıcı olarak kaydedilmez. Eğitim notebookları yalnızca tekrar
üretimi pahalı olan checkpointleri, final modelleri, splitleri ve
`run_config.json` dosyalarını korur.

Notebooklarda ortak yollar için:

```python
from thesis_utils import DATA_ROOT, PROJECT_ROOT, paths

annotation_dir = paths.SP500_ANNOTATION_DIR
```

Tablo okumak için:

```python
from thesis_utils.data_io import read_first_existing, read_table
```
