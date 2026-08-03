# Finansal Sentiment Tezi - Güncel Çalışma Özeti

Bu özet mevcut proje dosya yapısına göre yeniden düzenlenmiştir. Şirket/hedef bazlı ayrı etiketleme hattı hoca tarafından istenmediği için projeden kaldırılmıştır. Güncel akış plain sentiment sınıflandırması, hazır FinBERT baseline'ı, fine-tune edilen Transformer modelleri ve dış test değerlendirmeleri üzerindedir.

## 1. Çalışmanın Amacı

Bu çalışmada finansal haber başlıkları ve kısa piyasa metinleri `negative`, `neutral`, `positive` sınıflarına ayrılır.

Ana karşılaştırma çizgisi:

- Hazır `ProsusAI/finbert` modeli baseline olarak değerlendirilir.
- `bert-base-uncased`, `distilbert-base-uncased` ve `roberta-base` modelleri plain sentiment veri seti üzerinde fine-tune edilir.
- Fine-tune edilen modeller iç test, S&P 500 dış test, sentetik finans haberleri ve Reuters dış test setlerinde karşılaştırılır.
- `03b` ve `03c` notebookları, eski `03a_evaluate_unfinetuned_models_diagnostic.ipynb` dosyasındaki rastgele classification head problemini düzeltmek için gerçek NLI/MNLI tabanlı zero-shot deneyleri yapar.

## 2. Güncel Proje Yapısı

| Yol | İçerik |
| --- | --- |
| `app/` | Sıralı deney, eğitim, değerlendirme ve veri arama notebookları |
| `app/thesis_utils/` | Ortak path, veri okuma ve değerlendirme yardımcıları |
| `db/raw/` | Ham veri dosyaları |
| `db/interim/` | Ara çıktılar ve pseudo-label tabloları |
| `db/processed/` | İşlenmiş ana veri tabloları |
| `db/processed/training_datasets/` | Model eğitiminde kullanılan plain sentiment veri seti |
| `db/splits/plain_sentiment_v1/` | Train/validation/test bölünmeleri |
| `db/annotations/` | S&P 500 ve Reuters anotasyon dosyaları |
| `db/evaluation/synthetic_financial_news/` | Sentetik değerlendirme haberleri |
| `outputs/zero_shot_sp500_external_test/` | BART MNLI zero-shot S&P 500 tahmin çıktısı |
| `outputs/zero_shot_sp500_external_test_model_family/` | BERT/DistilBERT/RoBERTa NLI zero-shot aile testi çıktıları |
| `checkpoints/financial_sentiment_multi_model/` | Fine-tune edilmiş BERT, DistilBERT ve RoBERTa checkpointleri |
| `reports/historical_notebook_exports/` | Eski HTML notebook dışa aktarımları |
| `tools/` | Notebook temizleme ve veri klasörü düzenleme araçları |

## 3. Kullanılan Eğitim Veri Kaynakları

| Veri seti | Projedeki satır | Kullanım amacı |
| --- | ---: | --- |
| Twitter Financial News Sentiment | 11.931 | Kısa finansal/piyasa metinlerinde ana eğitim kaynağı |
| Financial PhraseBank | 4.846 | Finans haber cümlelerini eğitim havuzuna ekleyen yardımcı kaynak |
| **Plain sentiment dataset** | **16.777** | BERT, DistilBERT ve RoBERTa fine-tuning |

Plain sentiment sınıf dağılımı:

| Sınıf | Adet | Oran |
| --- | ---: | ---: |
| Neutral | 10.623 | %63,32 |
| Positive | 3.761 | %22,42 |
| Negative | 2.393 | %14,26 |
| **Toplam** | **16.777** | **%100** |

Veri setinde `neutral` sınıfı baskındır. Bu nedenle model karşılaştırmalarında yalnızca accuracy değil, sınıfları eşit ağırlıkla değerlendiren macro-F1 metriği de temel alınır.

## 4. Dış Test ve Değerlendirme Kaynakları

| Kaynak | Güncel dosya durumu | Kullanım |
| --- | --- | --- |
| S&P 500 Financial News Headlines 2008-2024 | `db/processed/sp500_headlines_2008_2024_finbert_labeled.csv`, 17.917 satır | Ham başlık havuzu ve FinBERT label üretimi |
| S&P 500 balanced annotation master | `db/annotations/sp500_balanced_1500/`, master 1.500 satır | Dengeli anotasyon hazırlığı |
| S&P 500 human review batches | `db/annotations/sp500_human_review_batches/`, 106 batch dosyası; 1.067 satır okunuyor | Dış test/anotasyon batchleri |
| S&P 500 zero-shot çıktısı | `outputs/zero_shot_sp500_external_test_model_family/...summary.csv`, `n_eval=1060` | NLI/MNLI zero-shot model ailesi karşılaştırması |
| Reuters 5.000 annotation set | `db/annotations/reuters_5000/REUTERS_annotation_all_clean.csv`, 5.000 satır | Reuters dış test değerlendirmesi |
| Sentetik finans haberleri | `db/evaluation/synthetic_financial_news/` | Dengeli sentetik test örnekleri |

## 5. Hazırlanan Ana Veri Tabloları

| Tablo | Satır | Açıklama |
| --- | ---: | --- |
| `db/processed/aggregated_financial_news_enriched.csv` | 943.326 | Birleştirilmiş ve zenginleştirilmiş finans haber havuzu |
| `db/processed/market_sentiment_modeling_master.parquet` | 42.178 | Piyasa yönü modellemesi için hazırlanmış ana tablo |
| `db/processed/sp500_headlines_2008_2024_finbert_labeled.csv` | 17.917 | FinBERT ile etiketlenen S&P 500 haber başlıkları |
| `db/interim/pseudo_labeled_news_confidence_090.parquet` | 88.342 | FinBERT güven skoru en az `0.90` olan pseudo-label haberler |
| `db/processed/training_datasets/plain_sentiment_dataset.parquet` | 16.777 | Genel sentiment sınıflandırması eğitim tablosu |

## 6. Notebook Akışı

| Sıra | Notebook | Güncel rolü |
| ---: | --- | --- |
| 1 | `app/00_setup_requirements.ipynb` | Ortam ve paket hazırlığı |
| 2 | `app/01a_build_reuters_annotation_dataset.ipynb` | Reuters 5.000 dış test anotasyon setinin hazırlanması |
| 3 | `app/01b_build_sp500_annotation_dataset.ipynb` | S&P 500 başlıklarının FinBERT ile etiketlenmesi ve anotasyon batchlerinin hazırlanması |
| 4 | `app/02_evaluate_finbert_baseline.ipynb` | Hazır FinBERT modelinin hedef veri setinde nasıl davrandığını gösteren baseline ve hata analizi |
| 5 | `app/03a_evaluate_unfinetuned_models_diagnostic.ipynb` | Fine-tune edilmemiş modellerin rastgele classification head ile neden ana baseline olamayacağını gösteren diagnostic kontrol |
| 6 | `app/03b_evaluate_zero_shot_sp500_external_test.ipynb` | BART MNLI ile gerçek zero-shot S&P 500 testi |
| 7 | `app/03c_evaluate_zero_shot_model_family_sp500_external_test.ipynb` | BERT/DistilBERT/RoBERTa NLI/MNLI zero-shot aile testi |
| 8 | `app/04_train_plain_sentiment_models.ipynb` | Tezin ana fine-tuning aşaması: BERT, DistilBERT ve RoBERTa plain sentiment eğitimi |
| 9 | `app/05_evaluate_sp500_finetuned_models.ipynb` | Fine-tune modellerin S&P 500 dış test değerlendirmesi |
| 10 | `app/06_evaluate_synthetic_finetuned_models.ipynb` | Fine-tune modellerin sentetik finans haberleri üzerinde kontrol testi |
| 11 | `app/07_evaluate_reuters_finetuned_models.ipynb` | Fine-tune modellerin Reuters 5.000 dış test değerlendirmesi |
| 12 | `app/09_search_new_dataset.ipynb` | Hocanın istediği ek veri seti arama ve dış test adayı seçimi |

### 6.1. Baseline, Diagnostic ve Zero-Shot Dosyalarının Farkı

`02`, `03a`, `03b` ve `03c` notebookları bizim fine-tuning deneyinden önceki karşılaştırma ve kontrol katmanını oluşturur. Bu dosyalar aynı şeyi yapmaz; her biri farklı bir soruya cevap verir.

| Notebook | Ne test ediyor? | Tezdeki anlamı | Ana başarı baseline'ı mı? |
| --- | --- | --- | --- |
| `02_evaluate_finbert_baseline.ipynb` | Hazır `ProsusAI/finbert` modeli | Finansal sentiment için zaten eğitilmiş bir modelin hedef veri setinde ne kadar uyumlu olduğunu gösterir. | Evet |
| `03a_evaluate_unfinetuned_models_diagnostic.ipynb` | Fine-tune edilmemiş BERT/DistilBERT/RoBERTa modelleri ve rastgele başlayan classification head | Modeli göreve eğitmeden doğrudan kullanmanın neden anlamlı bir başarı sonucu vermediğini gösteren diagnostic kontroldür. | Hayır |
| `03b_evaluate_zero_shot_sp500_external_test.ipynb` | BART MNLI ile tek model zero-shot classification | Model fine-tune edilmeden, NLI mantığıyla `negative/neutral/positive` hipotezleri üzerinden sınıflandırma yapar. Rastgele değildir. | Evet, zero-shot baseline |
| `03c_evaluate_zero_shot_model_family_sp500_external_test.ipynb` | BERT, DistilBERT ve RoBERTa ailelerinin NLI/MNLI zero-shot karşılıkları | `03b` deneyini genişletir; farklı genel amaçlı zero-shot model ailelerini aynı S&P 500 dış testinde karşılaştırır. | Evet, zero-shot karşılaştırma |

Bu nedenle `03a`, `03b` ve `03c` aynı deneyin kopyası değildir. `03a` daha çok “modeli eğitmeden rastgele head ile kullanırsak ne olur?” sorusuna cevap veren uyarı/diagnostic dosyasıdır. `03b` ve `03c` ise gerçek zero-shot baseline deneyleridir. Asıl tez katkısı bundan sonra gelen `04_train_plain_sentiment_models.ipynb` ile başlar; burada modeller hedef plain sentiment veri seti üzerinde fine-tune edilir.

## 7. Train / Validation / Test Bölünmesi

`db/splits/plain_sentiment_v1/` altındaki güncel splitler:

| Bölüm | Toplam | Negative | Neutral | Positive |
| --- | ---: | ---: | ---: | ---: |
| Train | 12.950 | 1.820 | 8.137 | 2.993 |
| Validation | 1.432 | 215 | 929 | 288 |
| Test | 2.386 | 358 | 1.549 | 479 |

Test seti yalnızca Twitter Financial News Sentiment kaynağından gelir. Financial PhraseBank, FinBERT'in eğitim geçmişiyle çakışma riski nedeniyle final baseline karşılaştırmasında test verisi olarak kullanılmaz.

## 8. Eğitim ve Test Veri Seti Eşleşmesi

Aşağıdaki tablo, her deney dosyasının hangi veri setini kullandığını açıkça gösterir. Böylece eğitim verisi, iç test verisi ve bağımsız dış test verileri birbirine karıştırılmaz.

| Notebook | Eğitim verisi | Test/değerlendirme verisi | Amaç |
| --- | --- | --- | --- |
| `02_evaluate_finbert_baseline.ipynb` | Yeni eğitim yok; hazır `ProsusAI/finbert` kullanılır. | `db/splits/plain_sentiment_v1/test_df.parquet`; Twitter Financial News Sentiment test bölümü, 2.386 satır. | Hazır FinBERT modelinin hedef plain sentiment veri setindeki başlangıç performansını ölçmek. |
| `03a_evaluate_unfinetuned_models_diagnostic.ipynb` | Yeni eğitim yok; BERT/DistilBERT/RoBERTa taban modellerine rastgele başlayan classification head takılır. | S&P 500 anotasyon batchleri; `db/annotations/sp500_human_review_batches/`. | Fine-tune edilmemiş modellerin doğrudan kullanılamayacağını gösteren diagnostic kontrol. |
| `03b_evaluate_zero_shot_sp500_external_test.ipynb` | Yeni eğitim yok; BART MNLI zero-shot modeli kullanılır. | S&P 500 anotasyon batchleri; çıktı `outputs/zero_shot_sp500_external_test/` altına kaydedilir. | Tek bir güçlü NLI modelinin zero-shot sentiment başarısını ölçmek. |
| `03c_evaluate_zero_shot_model_family_sp500_external_test.ipynb` | Yeni eğitim yok; BERT/DistilBERT/RoBERTa ailelerinin NLI/MNLI sürümleri kullanılır. | S&P 500 anotasyon batchleri; `n_eval=1060`, çıktı `outputs/zero_shot_sp500_external_test_model_family/` altına kaydedilir. | Genel amaçlı zero-shot model ailelerini aynı dış testte karşılaştırmak. |
| `04_train_plain_sentiment_models.ipynb` | `db/processed/training_datasets/plain_sentiment_dataset.parquet`; Twitter Financial News Sentiment + Financial PhraseBank toplam 16.777 satır. | `db/splits/plain_sentiment_v1/val_df.parquet` ve `test_df.parquet`; test bölümü yalnızca Twitter Financial News Sentiment kaynaklıdır. | BERT, DistilBERT ve RoBERTa modellerini hedef plain sentiment görevine fine-tune etmek. |
| `05_evaluate_sp500_finetuned_models.ipynb` | Bu notebookta yeni eğitim yok; `04` ile üretilen checkpointler kullanılır. | S&P 500 bağımsız anotasyon seti; `db/annotations/sp500_human_review_batches/`. | Fine-tune edilen modellerin eğitimden farklı finans haber başlıklarına genellemesini ölçmek. |
| `06_evaluate_synthetic_finetuned_models.ipynb` | Yeni eğitim yok; `04` checkpointleri ve hazır FinBERT kullanılır. | `db/evaluation/synthetic_financial_news/`; her sınıftan 1.000 örnek, toplam 3.000 sentetik haber. | Açık sentiment sinyallerinde modellerin davranışını dengeli veriyle kontrol etmek. |
| `07_evaluate_reuters_finetuned_models.ipynb` | Yeni eğitim yok; `04` checkpointleri ve dosyadaki FinBERT label baselineı kullanılır. | `db/annotations/reuters_5000/REUTERS_annotation_all_clean.csv`; 5.000 Reuters başlığı. | Modellerin Reuters haber diline ve farklı etiket dağılımına genellemesini ölçmek. |
| `09_search_new_dataset.ipynb` | Eğitim yapmaz. | Yeni aday veri setlerinden örnekler ve karşılaştırma tabloları. | Hocanın istediği ek veri setini belirlemek ve ileride dış teste sokulabilecek adayı seçmek. |

### 8.1. Ana Eğitim Verisi

Ana fine-tuning verisi `plain_sentiment_dataset.parquet` dosyasıdır. Bu dosya iki kaynaktan oluşur:

| Kaynak | Satır | Kullanım |
| --- | ---: | --- |
| Twitter Financial News Sentiment | 11.931 | Kısa finansal/piyasa metinleri ve hedef görev mantığı |
| Financial PhraseBank | 4.846 | Finans haber cümleleriyle eğitim havuzunu zenginleştirme |
| **Toplam** | **16.777** | Plain sentiment fine-tuning |

`test_df.parquet` yalnızca Twitter Financial News Sentiment kaynağından ayrılmıştır. Bunun nedeni, hazır FinBERT modelinin Financial PhraseBank ile önceden ilişkili olma ihtimalidir; bu nedenle final baseline karşılaştırmasında daha temiz bir test alanı sağlanır.

### 8.2. Dış Test Verileri

Dış testler modelin sadece eğitim verisini ezberleyip ezberlemediğini değil, farklı haber kaynaklarına genelleyip genelleyemediğini göstermek için kullanılır.

| Dış test | Dosya/klasör | Rol |
| --- | --- | --- |
| S&P 500 anotasyon seti | `db/annotations/sp500_human_review_batches/` | Finans haber başlıklarında bağımsız dış test |
| Reuters 5.000 | `db/annotations/reuters_5000/REUTERS_annotation_all_clean.csv` | Farklı haber kaynağı ve farklı etiket dağılımıyla dış test |
| Sentetik finans haberleri | `db/evaluation/synthetic_financial_news/` | Dengeli ve açık sentiment sinyalli kontrol testi |

## 9. Raporlanan Fine-Tuned Model Sonuçları

### Plain Sentiment İç Test

| Sıra | Model | Accuracy | Macro-F1 | Weighted-F1 |
| ---: | --- | ---: | ---: | ---: |
| 1 | RoBERTa-base | 0.8906 | 0.8651 | 0.8918 |
| 2 | BERT-base-uncased | 0.8722 | 0.8378 | 0.8733 |
| 3 | DistilBERT-base-uncased | 0.8583 | 0.8218 | 0.8593 |
| 4 | Original FinBERT | 0.7323 | 0.6794 | 0.7400 |

### S&P 500 Fine-Tuned Dış Test

| Sıra | Model | Accuracy | Macro-F1 | Weighted-F1 |
| ---: | --- | ---: | ---: | ---: |
| 1 | RoBERTa-base | 0.8125 | 0.8138 | 0.8146 |
| 2 | Original FinBERT | 0.7583 | 0.7585 | 0.7579 |
| 3 | DistilBERT-base-uncased | 0.7531 | 0.7523 | 0.7536 |
| 4 | BERT-base-uncased | 0.7521 | 0.7511 | 0.7524 |

### Sentetik Finans Haberleri

| Sıra | Model | Accuracy | Macro-F1 | Weighted-F1 |
| ---: | --- | ---: | ---: | ---: |
| 1 | RoBERTa-base | 0.9957 | 0.9957 | 0.9957 |
| 2 | BERT-base-uncased | 0.9743 | 0.9742 | 0.9742 |
| 3 | DistilBERT-base-uncased | 0.9583 | 0.9581 | 0.9581 |
| 4 | Original FinBERT | 0.9550 | 0.9551 | 0.9551 |

### Reuters 5.000 Dış Test

| Sıra | Model | Accuracy | Macro-F1 | Weighted-F1 |
| ---: | --- | ---: | ---: | ---: |
| 1 | Original FinBERT file label | 0.6966 | 0.6866 | 0.7016 |
| 2 | RoBERTa-base | 0.6268 | 0.6388 | 0.6486 |
| 3 | BERT-base-uncased | 0.6034 | 0.6131 | 0.6240 |
| 4 | DistilBERT-base-uncased | 0.5766 | 0.5869 | 0.5953 |

## 10. Güncel Zero-Shot S&P 500 Model Ailesi Sonucu

Refactor sonrası asıl güncel zero-shot karşılaştırması `03c` notebooku ve şu dosyada tutulur:

`outputs/zero_shot_sp500_external_test_model_family/zero_shot_sp500_external_test_model_family_summary.csv`

Bu dosyaya göre `n_eval=1060` satır değerlendirilmiştir.

| Sıra | Model | Accuracy | Macro-F1 | Weighted-F1 |
| ---: | --- | ---: | ---: | ---: |
| 1 | Original FinBERT file label | 0.7519 | 0.7521 | 0.7513 |
| 2 | RoBERTa-base NLI zero-shot | 0.6085 | 0.4913 | 0.4989 |
| 3 | BERT-base-uncased MNLI zero-shot | 0.5057 | 0.4033 | 0.4117 |
| 4 | DistilBERT-base-uncased MNLI zero-shot | 0.4679 | 0.3880 | 0.3927 |

Bu tablo, eski `03a_evaluate_unfinetuned_models_diagnostic.ipynb` dosyasındaki rastgele head yaklaşımının yerine kullanılmalıdır. Eski `03a` notebooku metodolojik not/diagnostic olarak kalabilir, ancak tezde ana zero-shot sonucu olarak sunulmamalıdır.

## 11. Genel Sonuç

Mevcut dosyalara göre çalışmanın ana bulgusu şudur:

- Plain sentiment iç testinde fine-tune edilen modeller hazır FinBERT baseline'ını geçmiştir.
- İç test ve S&P 500 fine-tuned dış testte en güçlü model RoBERTa-base olarak raporlanmıştır.
- Reuters dış testinde Original FinBERT file label daha yüksek performans göstermiştir; bu durum veri kaynağı ve etiket tanımının model başarısını ciddi biçimde etkilediğini gösterir.
- Zero-shot tarafta eski unfinetuned taban model deneyi ana sonuç değildir; güncel karşılaştırma NLI/MNLI tabanlı `07b/07c` deneyleridir.

Bu nedenle tezde tek bir modelin her dış veri kaynağında mutlak üstün olduğu iddia edilmemelidir. Daha doğru sonuç cümlesi şudur: RoBERTa-base, hedef plain sentiment verisine uyum ve S&P 500 genellemesi açısından en güçlü fine-tuned modeldir; Reuters tarafında ise hazır FinBERT'in alan/etiket uyumu avantajı devam etmektedir.
