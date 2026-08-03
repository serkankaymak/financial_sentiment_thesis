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

Bu projede ana eğitim hattı plain sentiment üzerindedir. Şirket/hedef bazlı ayrı etiketleme hattı kullanılmaz.

**Twitter Financial News Sentiment**

- Satır sayısı: 11.931.
- Rolü: Kısa finansal ve piyasa odaklı metinlerde ana eğitim kaynağı.
- Etiket mantığı: `negative`, `neutral`, `positive` sınıflarına dönüştürülür.

**Financial PhraseBank**

- Satır sayısı: 4.846.
- Rolü: Finans haber cümleleriyle eğitim havuzunu zenginleştiren yardımcı kaynak.
- Etiket mantığı: Cümle düzeyinde finansal sentiment etiketi.

**Birleştirilmiş Plain Sentiment Dataset**

- Dosya: `db/processed/training_datasets/plain_sentiment_dataset.parquet`.
- Toplam satır sayısı: 16.777.
- Kullanım: BERT, DistilBERT ve RoBERTa fine-tuning.

**Sınıf Dağılımı**

- Neutral: 10.623 satır, %63,32.
- Positive: 3.761 satır, %22,42.
- Negative: 2.393 satır, %14,26.
- Toplam: 16.777 satır.

Veri setinde `neutral` sınıfı baskındır. Bu nedenle model karşılaştırmalarında yalnızca accuracy değil, sınıfları eşit ağırlıkla değerlendiren macro-F1 metriği de temel alınır.

## 4. Dış Test ve Değerlendirme Kaynakları

**S&P 500 Financial News Headlines 2008-2024**

- Dosya: `db/processed/sp500_headlines_2008_2024_finbert_labeled.csv`.
- Satır sayısı: 17.917.
- Rolü: Ham başlık havuzu ve FinBERT label üretimi.

**S&P 500 Balanced Annotation Master**

- Klasör: `db/annotations/sp500_balanced_1500/`.
- Master dosya: 1.500 satır.
- Rolü: Dengeli anotasyon hazırlığı.

**S&P 500 Human Review Batches**

- Klasör: `db/annotations/sp500_human_review_batches/`.
- Durum: 106 batch dosyası; 1.067 satır okunuyor.
- Rolü: S&P 500 dış test ve anotasyon batchleri.

**S&P 500 Zero-Shot Çıktısı**

- Özet dosya: `outputs/zero_shot_sp500_external_test_model_family/...summary.csv`.
- Değerlendirme satırı: `n_eval=1060`.
- Rolü: NLI/MNLI zero-shot model ailesi karşılaştırması.

**Reuters 5.000 Annotation Set**

- Dosya: `db/annotations/reuters_5000/REUTERS_annotation_all_clean.csv`.
- Satır sayısı: 5.000.
- Rolü: Reuters dış test değerlendirmesi.

**Sentetik Finans Haberleri**

- Klasör: `db/evaluation/synthetic_financial_news/`.
- Rolü: Dengeli sentetik test örnekleri.

## 5. Hazırlanan Ana Veri Tabloları

**Birleştirilmiş Haber Havuzu**

- Dosya: `db/processed/aggregated_financial_news_enriched.csv`.
- Satır sayısı: 943.326.
- Açıklama: Birleştirilmiş ve zenginleştirilmiş finans haber havuzu.

**Piyasa Modelleme Ana Tablosu**

- Dosya: `db/processed/market_sentiment_modeling_master.parquet`.
- Satır sayısı: 42.178.
- Açıklama: Piyasa yönü modellemesi için hazırlanmış ana tablo.

**S&P 500 FinBERT Etiketli Başlıklar**

- Dosya: `db/processed/sp500_headlines_2008_2024_finbert_labeled.csv`.
- Satır sayısı: 17.917.
- Açıklama: FinBERT ile etiketlenen S&P 500 haber başlıkları.

**Pseudo-Label Haberler**

- Dosya: `db/interim/pseudo_labeled_news_confidence_090.parquet`.
- Satır sayısı: 88.342.
- Açıklama: FinBERT güven skoru en az `0.90` olan pseudo-label haberler.

**Plain Sentiment Eğitim Tablosu**

- Dosya: `db/processed/training_datasets/plain_sentiment_dataset.parquet`.
- Satır sayısı: 16.777.
- Açıklama: Genel sentiment sınıflandırması eğitim tablosu.

## 6. Notebook Akışı

Notebookların sırası hocaya anlatılacak mantığa göre düzenlenmiştir. Önce hazırlık, sonra hazır modellerin davranışı, sonra tezin ana fine-tuning deneyleri gelir. `09` en sonda bırakılmıştır.

**Hazırlık**

- `00_setup_requirements.ipynb`: Ortam ve paket hazırlığı.
- `01a_build_reuters_annotation_dataset.ipynb`: Reuters 5.000 dış test anotasyon setinin hazırlanması.
- `01b_build_sp500_annotation_dataset.ipynb`: S&P 500 başlıklarının FinBERT ile etiketlenmesi ve anotasyon batchlerinin hazırlanması.

**Hazır Model ve Zero-Shot Kontrolleri**

- `02_evaluate_finbert_baseline.ipynb`: Hazır FinBERT modelinin hedef veri setinde nasıl davrandığını gösteren baseline ve hata analizi.
- `03a_evaluate_unfinetuned_models_diagnostic.ipynb`: Fine-tune edilmemiş modellerin rastgele classification head ile neden ana baseline olamayacağını gösteren diagnostic kontrol.
- `03b_evaluate_zero_shot_sp500_external_test.ipynb`: BART MNLI ile gerçek zero-shot S&P 500 testi.
- `03c_evaluate_zero_shot_model_family_sp500_external_test.ipynb`: BERT, DistilBERT ve RoBERTa ailelerinin NLI/MNLI zero-shot testi.

**Tezin Ana Fine-Tuning ve Dış Test Akışı**

- `04_train_plain_sentiment_models.ipynb`: BERT, DistilBERT ve RoBERTa modellerinin plain sentiment eğitimi.
- `05_evaluate_sp500_finetuned_models.ipynb`: Fine-tune modellerin S&P 500 dış test değerlendirmesi.
- `06_evaluate_synthetic_finetuned_models.ipynb`: Fine-tune modellerin sentetik finans haberleri üzerinde kontrol testi.
- `07_evaluate_reuters_finetuned_models.ipynb`: Fine-tune modellerin Reuters 5.000 dış test değerlendirmesi.

**Ek Veri Seti Arama**

- `09_search_new_dataset.ipynb`: Hocanın istediği ek veri seti arama ve dış test adayı seçimi.

### 6.1. Baseline, Diagnostic ve Zero-Shot Dosyalarının Farkı

`02`, `03a`, `03b` ve `03c` notebookları bizim fine-tuning deneyinden önceki karşılaştırma ve kontrol katmanını oluşturur. Bu dosyalar aynı şeyi yapmaz.

**`02_evaluate_finbert_baseline.ipynb`**

Hazır `ProsusAI/finbert` modeli test edilir. Finansal sentiment için zaten eğitilmiş bir modelin hedef veri setinde ne kadar uyumlu olduğunu gösterir. Bu dosya ana baseline olarak kullanılabilir.

**`03a_evaluate_unfinetuned_models_diagnostic.ipynb`**

Fine-tune edilmemiş BERT, DistilBERT ve RoBERTa modelleri denenir. Bu modellerin üzerindeki classification head rastgele başladığı için sonuçlar ana başarı sonucu olarak kullanılmaz. Dosyanın amacı şunu göstermektir: modeli göreve eğitmeden doğrudan kullanmak anlamlı bir sentiment sınıflandırması vermez.

**`03b_evaluate_zero_shot_sp500_external_test.ipynb`**

BART MNLI modeliyle gerçek zero-shot classification yapılır. Model fine-tune edilmez; ancak `negative`, `neutral`, `positive` hipotezleri üzerinden NLI mantığıyla karar verir. Bu nedenle rastgele değildir ve zero-shot baseline olarak yorumlanabilir.

**`03c_evaluate_zero_shot_model_family_sp500_external_test.ipynb`**

`03b` deneyinin genişletilmiş halidir. BERT, DistilBERT ve RoBERTa ailelerinin NLI/MNLI sürümleri aynı S&P 500 dış testinde karşılaştırılır. Bu dosya zero-shot modeller arasındaki farkı gösterir.

Kısaca: `03a` uyarı/diagnostic dosyasıdır; `03b` ve `03c` gerçek zero-shot baseline deneyleridir. Asıl tez katkısı `04_train_plain_sentiment_models.ipynb` ile başlar.

## 7. Train / Validation / Test Bölünmesi

`db/splits/plain_sentiment_v1/` altındaki güncel splitler:

- Train: 12.950 satır. Negative 1.820, neutral 8.137, positive 2.993.
- Validation: 1.432 satır. Negative 215, neutral 929, positive 288.
- Test: 2.386 satır. Negative 358, neutral 1.549, positive 479.

Test seti yalnızca Twitter Financial News Sentiment kaynağından gelir. Financial PhraseBank, FinBERT'in eğitim geçmişiyle çakışma riski nedeniyle final baseline karşılaştırmasında test verisi olarak kullanılmaz.

## 8. Eğitim ve Test Veri Seti Eşleşmesi

Bu bölümde her deney dosyasının hangi veri setiyle eğitildiği ve hangi veri setiyle test edildiği açıklanır. Amaç, eğitim verisi, iç test verisi ve bağımsız dış test verilerinin karışmasını önlemektir.

**`02_evaluate_finbert_baseline.ipynb`**

- Eğitim: Bu notebookta yeni eğitim yoktur. Hazır `ProsusAI/finbert` modeli kullanılır.
- Test: `db/splits/plain_sentiment_v1/test_df.parquet`.
- Veri kaynağı: Twitter Financial News Sentiment test bölümü, 2.386 satır.
- Amaç: Hazır FinBERT modelinin hedef plain sentiment veri setindeki başlangıç performansını ölçmek.

**`03a_evaluate_unfinetuned_models_diagnostic.ipynb`**

- Eğitim: Yeni eğitim yoktur. BERT, DistilBERT ve RoBERTa taban modellerine rastgele başlayan classification head takılır.
- Test: `db/annotations/sp500_human_review_batches/`.
- Veri kaynağı: S&P 500 anotasyon batchleri.
- Amaç: Fine-tune edilmemiş modellerin doğrudan kullanılamayacağını gösteren diagnostic kontrol.

**`03b_evaluate_zero_shot_sp500_external_test.ipynb`**

- Eğitim: Yeni eğitim yoktur. BART MNLI zero-shot modeli kullanılır.
- Test: `db/annotations/sp500_human_review_batches/`.
- Çıktı: `outputs/zero_shot_sp500_external_test/`.
- Amaç: Tek bir güçlü NLI modelinin zero-shot sentiment başarısını ölçmek.

**`03c_evaluate_zero_shot_model_family_sp500_external_test.ipynb`**

- Eğitim: Yeni eğitim yoktur. BERT, DistilBERT ve RoBERTa ailelerinin NLI/MNLI sürümleri kullanılır.
- Test: S&P 500 anotasyon batchleri, `n_eval=1060`.
- Çıktı: `outputs/zero_shot_sp500_external_test_model_family/`.
- Amaç: Genel amaçlı zero-shot model ailelerini aynı dış testte karşılaştırmak.

**`04_train_plain_sentiment_models.ipynb`**

- Eğitim: `db/processed/training_datasets/plain_sentiment_dataset.parquet`.
- Eğitim kaynakları: Twitter Financial News Sentiment + Financial PhraseBank, toplam 16.777 satır.
- Validation/Test: `db/splits/plain_sentiment_v1/val_df.parquet` ve `test_df.parquet`.
- Not: Test bölümü yalnızca Twitter Financial News Sentiment kaynaklıdır.
- Amaç: BERT, DistilBERT ve RoBERTa modellerini hedef plain sentiment görevine fine-tune etmek.

**`05_evaluate_sp500_finetuned_models.ipynb`**

- Eğitim: Bu notebookta yeni eğitim yoktur. `04` ile üretilen checkpointler kullanılır.
- Test: `db/annotations/sp500_human_review_batches/`.
- Veri kaynağı: Bağımsız S&P 500 haber başlığı anotasyonları.
- Amaç: Fine-tune edilen modellerin eğitimden farklı finans haber başlıklarına genellemesini ölçmek.

**`06_evaluate_synthetic_finetuned_models.ipynb`**

- Eğitim: Yeni eğitim yoktur. `04` checkpointleri ve hazır FinBERT kullanılır.
- Test: `db/evaluation/synthetic_financial_news/`.
- Veri kaynağı: Her sınıftan 1.000 örnek, toplam 3.000 sentetik finans haberi.
- Amaç: Açık sentiment sinyallerinde modellerin davranışını dengeli veriyle kontrol etmek.

**`07_evaluate_reuters_finetuned_models.ipynb`**

- Eğitim: Yeni eğitim yoktur. `04` checkpointleri ve dosyadaki FinBERT label baselineı kullanılır.
- Test: `db/annotations/reuters_5000/REUTERS_annotation_all_clean.csv`.
- Veri kaynağı: 5.000 Reuters haber başlığı.
- Amaç: Modellerin Reuters haber diline ve farklı etiket dağılımına genellemesini ölçmek.

**`09_search_new_dataset.ipynb`**

- Eğitim: Eğitim yapmaz.
- Test: Henüz final test değildir; yeni aday veri setlerinden örnekler ve karşılaştırma tabloları hazırlar.
- Amaç: Hocanın istediği ek veri setini belirlemek ve ileride dış teste sokulabilecek adayı seçmek.

### 8.1. Ana Eğitim Verisi

Ana fine-tuning verisi `plain_sentiment_dataset.parquet` dosyasıdır. Bu dosya iki kaynaktan oluşur:

- Twitter Financial News Sentiment: 11.931 satır. Kısa finansal/piyasa metinleri ve hedef görev mantığı için kullanılır.
- Financial PhraseBank: 4.846 satır. Finans haber cümleleriyle eğitim havuzunu zenginleştirir.
- Toplam: 16.777 satır plain sentiment fine-tuning verisi.

`test_df.parquet` yalnızca Twitter Financial News Sentiment kaynağından ayrılmıştır. Bunun nedeni, hazır FinBERT modelinin Financial PhraseBank ile önceden ilişkili olma ihtimalidir. Bu seçim final baseline karşılaştırmasında daha temiz bir test alanı sağlar.

### 8.2. Dış Test Verileri

Dış testler modelin sadece eğitim verisini ezberleyip ezberlemediğini değil, farklı haber kaynaklarına genelleyip genelleyemediğini göstermek için kullanılır.

- S&P 500 anotasyon seti: `db/annotations/sp500_human_review_batches/`. Finans haber başlıklarında bağımsız dış testtir.
- Reuters 5.000: `db/annotations/reuters_5000/REUTERS_annotation_all_clean.csv`. Farklı haber kaynağı ve farklı etiket dağılımıyla dış testtir.
- Sentetik finans haberleri: `db/evaluation/synthetic_financial_news/`. Dengeli ve açık sentiment sinyalli kontrol testidir.

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
