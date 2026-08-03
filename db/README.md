# Veri Dizini

Bu klasör veri yaşam döngüsüne göre düzenlenmiştir. Notebooklarda yolları elle
yazmak yerine `app/thesis_utils/paths.py` içindeki sabitleri kullanın.

## Klasör Yapısı

| Klasör | Amaç |
| --- | --- |
| `raw/` | Kaynaktan alınan ve değiştirilmeden saklanan ham veriler |
| `processed/` | Temizlenmiş, zenginleştirilmiş veya modellemeye hazır veriler |
| `interim/` | Yeniden üretilebilen ara çıktılar ve yarım kalan işlem kayıtları |
| `annotations/` | İnsan değerlendirmesi ve anotasyon çalışmalarına ait veriler |
| `splits/` | Tekrar üretilebilir train, validation ve test bölmeleri |
| `evaluation/` | Model karşılaştırması için kullanılan bağımsız test verileri |

## Önemli Dosyalar

| Yol | Açıklama |
| --- | --- |
| `raw/sp500_headlines_2008_2024_raw.csv` | Ham SP500 başlık verisi |
| `processed/aggregated_financial_news_enriched.csv` | Birleştirilmiş ve zenginleştirilmiş finans haberleri |
| `processed/market_sentiment_modeling_master.parquet` | Piyasa yönü modellemesi için ana veri seti |
| `processed/sp500_headlines_2008_2024_finbert_labeled.csv` | FinBERT ile etiketlenmiş SP500 başlıkları |
| `processed/training_datasets/` | Plain sentiment eğitim veri setleri |
| `interim/sp500_headlines_2008_2024_finbert_labeling_progress.parquet` | SP500 FinBERT etiketleme devam kaydı |
| `interim/pseudo_labeled_news_confidence_090.parquet` | Güven eşiği 0.90 ile pseudo-label üretilmiş haberler |

## Anotasyon Verileri

| Yol | Açıklama |
| --- | --- |
| `annotations/sp500_balanced_1500/` | Dengeli 1500 örneklik SP500 anotasyon master seti |
| `annotations/sp500_balanced_1500/preparation_batches_10/` | Master set hazırlanırken üretilen 10 satırlık batchler |
| `annotations/sp500_human_review_batches/` | SP500 insan değerlendirme Excel batchleri |
| `annotations/reuters_5000/` | Reuters 5000 örneklik anotasyon seti ve değerlendirme çıktıları |
| `annotations/reuters_5000/annotation_batches_50/` | Reuters için 50 satırlık anotasyon batchleri |

## Değerlendirme Ve Splitler

| Yol | Açıklama |
| --- | --- |
| `splits/plain_sentiment_v1/` | Plain sentiment train, validation ve test splitleri |
| `evaluation/synthetic_financial_news/` | Sentetik finans haberi model değerlendirme seti |

Fine-tuned model değerlendirmelerinde metrikler çoğunlukla notebook ekranında
üretilir. Zero-shot S&P 500 deneylerinin prediction, confusion matrix ve özet
CSV çıktıları ise proje kökündeki `outputs/` klasöründe kalıcı olarak tutulur.
