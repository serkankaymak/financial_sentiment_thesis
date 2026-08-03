# Finansal Sentiment Tezi

**Güncel Çalışma Özeti**

Bu dosya, mevcut proje klasöründeki notebook ve veri yapısına göre
hazırlanmış kısa ama açıklayıcı çalışma özetidir.

> Önemli not: Şirket/hedef bazlı ayrı etiketleme hattı hoca tarafından
> istenmediği için projeden kaldırılmıştır. Güncel tez akışı
> plain sentiment sınıflandırması, hazır FinBERT baseline'ı,
> fine-tune edilen Transformer modelleri ve dış test değerlendirmeleri
> üzerindedir.

---

## Kısa Okuma Rehberi

Bu özeti hızlı okumak için sıra şöyledir:

1. **Amaç**: Tezin neyi ölçtüğünü anlatır.
2. **Veriler**: Hangi veri seti nerede kullanıldı gösterir.
3. **Notebook akışı**: Dosyaların hangi sırayla okunacağını verir.
4. **Baseline / zero-shot**: Hazır modellerin ne yaptığını açıklar.
5. **Fine-tuning sonuçları**: Bizim eğittiğimiz modellerin sonuçlarını verir.
6. **Genel sonuç**: Tezde savunulacak ana yorumu özetler.

---

## 1. Çalışmanın Amacı

Bu çalışmada finansal haber başlıkları ve kısa piyasa metinleri
üç sınıfa ayrılır:

- `negative`
- `neutral`
- `positive`

Ana karşılaştırma şudur:

- Hazır `ProsusAI/finbert` modeli baseline olarak test edilir.
- BERT, DistilBERT ve RoBERTa modelleri plain sentiment verisiyle fine-tune edilir.
- Fine-tune edilen modeller iç test ve bağımsız dış testlerde karşılaştırılır.
- Zero-shot modeller ayrı bir baseline katmanı olarak incelenir.

---

## 2. Proje Yapısı

**Ana klasörler**

- `app/`: Sıralı deney, eğitim, değerlendirme ve veri arama notebookları.
- `app/thesis_utils/`: Notebooklar arasında paylaşılan Python yardımcıları.
- `db/`: Ham, işlenmiş, ara, split ve anotasyon verileri.
- `checkpoints/`: Fine-tune edilmiş model checkpointleri.
- `outputs/`: Zero-shot deneylerinden kalıcı CSV çıktıları.
- `reports/`: Eski HTML notebook dışa aktarımları.
- `tools/`: Notebook temizleme ve veri klasörü düzenleme araçları.

**Veri klasörleri**

- `db/raw/`: Ham veri dosyaları.
- `db/interim/`: Ara çıktılar ve pseudo-label tabloları.
- `db/processed/`: İşlenmiş ana veri tabloları.
- `db/processed/training_datasets/`: Plain sentiment eğitim verisi.
- `db/splits/plain_sentiment_v1/`: Train, validation ve test bölünmeleri.
- `db/annotations/`: S&P 500 ve Reuters anotasyon dosyaları.
- `db/evaluation/synthetic_financial_news/`: Sentetik test haberleri.

---

## 3. Kullanılan Veri Setleri

### 3.1. Ana Eğitim Verisi

Ana fine-tuning dosyası:

`db/processed/training_datasets/plain_sentiment_dataset.parquet`

Bu dosya iki kaynaktan oluşur:

**Twitter Financial News Sentiment**

- Satır sayısı: 11.931.
- Rolü: Kısa finansal ve piyasa odaklı metinlerde ana eğitim kaynağı.
- Etiketler: `negative`, `neutral`, `positive` formatına dönüştürülür.

**Financial PhraseBank**

- Satır sayısı: 4.846.
- Rolü: Finans haber cümleleriyle eğitim havuzunu zenginleştirir.
- Not: Hazır FinBERT'in Financial PhraseBank ile önceden ilişkili olma
  ihtimali nedeniyle final test bölümünde ayrıca dikkat edilir.

**Birleştirilmiş veri**

- Toplam satır sayısı: 16.777.
- Kullanım: BERT, DistilBERT ve RoBERTa fine-tuning.

**Sınıf dağılımı**

- Neutral: 10.623 satır, %63,32.
- Positive: 3.761 satır, %22,42.
- Negative: 2.393 satır, %14,26.

> Veri setinde `neutral` sınıfı baskındır. Bu nedenle accuracy tek başına
> yeterli değildir; macro-F1 metriği ana yorumda mutlaka dikkate alınır.

### 3.2. Dış Test ve Kontrol Verileri

**S&P 500 haber başlıkları**

- Ana dosya: `db/processed/sp500_headlines_2008_2024_finbert_labeled.csv`.
- Satır sayısı: 17.917.
- Rolü: S&P 500 haber başlığı havuzu ve FinBERT label üretimi.

**S&P 500 insan değerlendirme batchleri**

- Klasör: `db/annotations/sp500_human_review_batches/`.
- Durum: 106 batch dosyası; 1.067 satır okunuyor.
- Rolü: S&P 500 dış test ve anotasyon değerlendirmesi.

**Reuters 5.000 anotasyon seti**

- Dosya: `db/annotations/reuters_5000/REUTERS_annotation_all_clean.csv`.
- Satır sayısı: 5.000.
- Rolü: Reuters haber dili üzerinde bağımsız dış test.

**Sentetik finans haberleri**

- Klasör: `db/evaluation/synthetic_financial_news/`.
- Yapı: Her sınıftan 1.000 örnek, toplam 3.000 haber.
- Rolü: Açık sentiment sinyallerinde dengeli kontrol testi.

---

## 4. Notebook Akışı

Notebooklar hoca karşısında anlatılacak mantıkla numaralandırılmıştır.

### Hazırlık

- `00_setup_requirements.ipynb`
  - Ortam ve paket hazırlığı.

- `01a_build_reuters_annotation_dataset.ipynb`
  - Reuters 5.000 dış test anotasyon setinin hazırlanması.

- `01b_build_sp500_annotation_dataset.ipynb`
  - S&P 500 başlıklarının FinBERT ile etiketlenmesi.
  - Anotasyon batchlerinin hazırlanması.

### Hazır Model ve Zero-Shot Kontrolleri

- `02_evaluate_finbert_baseline.ipynb`
  - Hazır FinBERT modelinin hedef veri setinde nasıl davrandığını gösterir.

- `03a_evaluate_unfinetuned_models_diagnostic.ipynb`
  - Fine-tune edilmemiş modellerin doğrudan kullanılamayacağını gösteren diagnostic dosyası.

- `03b_evaluate_zero_shot_sp500_external_test.ipynb`
  - BART MNLI ile gerçek zero-shot S&P 500 testi.

- `03c_evaluate_zero_shot_model_family_sp500_external_test.ipynb`
  - BERT, DistilBERT ve RoBERTa ailelerinin NLI/MNLI zero-shot karşılaştırması.

### Tezin Ana Fine-Tuning Akışı

- `04_train_plain_sentiment_models.ipynb`
  - BERT, DistilBERT ve RoBERTa modellerinin plain sentiment eğitimi.

- `05_evaluate_sp500_finetuned_models.ipynb`
  - Fine-tune modellerin S&P 500 dış test değerlendirmesi.

- `06_evaluate_synthetic_finetuned_models.ipynb`
  - Fine-tune modellerin sentetik finans haberleri üzerinde kontrol testi.

- `07_evaluate_reuters_finetuned_models.ipynb`
  - Fine-tune modellerin Reuters 5.000 dış test değerlendirmesi.

### Ek Veri Seti Arama

- `09_search_new_dataset.ipynb`
  - Hocanın istediği ek veri seti arama ve dış test adayı seçimi.

---

## 5. `02`, `03a`, `03b`, `03c` Farkı

Bu dosyalar aynı şeyi yapmaz. Hepsi bizim fine-tuning deneyinden önceki
karşılaştırma ve kontrol katmanına aittir.

**`02`: Hazır FinBERT baseline**

Hazır `ProsusAI/finbert` modeli test edilir. Finansal sentiment için zaten
önceden eğitilmiş bir modelin hedef veri setinde ne kadar uyumlu olduğunu
gösterir. Bu ana baseline olarak kullanılabilir.

**`03a`: Fine-tune edilmemiş model diagnostic dosyası**

BERT, DistilBERT ve RoBERTa taban modelleri denenir. Bu modellerin classification
head kısmı rastgele başladığı için sonuçlar ana başarı sonucu
olarak kullanılmaz. Amaç şunu göstermektir: modeli göreve eğitmeden
doğrudan kullanmak sağlıklı bir sentiment sınıflandırması vermez.

**`03b`: BART MNLI zero-shot baseline**

Model fine-tune edilmez; fakat NLI mantığıyla `negative`, `neutral`,
`positive` hipotezleri üzerinden karar verir. Bu rastgele değildir ve zero-shot
baseline olarak yorumlanabilir.

**`03c`: Zero-shot model ailesi karşılaştırması**

`03b` deneyinin genişletilmiş halidir. BERT, DistilBERT ve RoBERTa ailelerinin
NLI/MNLI sürümleri aynı S&P 500 dış testinde karşılaştırılır.

> Kısaca: `03a` uyarı/diagnostic dosyasıdır. `03b` ve `03c` gerçek
> zero-shot baseline deneyleridir. Asıl tez katkısı `04_train_plain_sentiment_models.ipynb`
> ile başlar.

---

## 6. Eğitim ve Test Eşleşmesi

Bu bölüm hangi notebookun hangi veriyle eğitildiğini ve hangi veriyle test
edildiğini netleştirir.

### `02_evaluate_finbert_baseline.ipynb`

- Eğitim: Yeni eğitim yoktur; hazır `ProsusAI/finbert` kullanılır.
- Test: `db/splits/plain_sentiment_v1/test_df.parquet`.
- Veri: Twitter Financial News Sentiment test bölümü, 2.386 satır.
- Amaç: Hazır FinBERT modelinin başlangıç performansını ölçmek.

### `03a_evaluate_unfinetuned_models_diagnostic.ipynb`

- Eğitim: Yeni eğitim yoktur.
- Model: Fine-tune edilmemiş BERT, DistilBERT ve RoBERTa taban modelleri.
- Test: `db/annotations/sp500_human_review_batches/`.
- Amaç: Rastgele classification head ile doğrudan kullanımın sağlıklı olmadığını göstermek.

### `03b_evaluate_zero_shot_sp500_external_test.ipynb`

- Eğitim: Yeni eğitim yoktur.
- Model: BART MNLI zero-shot modeli.
- Test: `db/annotations/sp500_human_review_batches/`.
- Çıktı: `outputs/zero_shot_sp500_external_test/`.

### `03c_evaluate_zero_shot_model_family_sp500_external_test.ipynb`

- Eğitim: Yeni eğitim yoktur.
- Model: BERT, DistilBERT ve RoBERTa ailelerinin NLI/MNLI sürümleri.
- Test: S&P 500 anotasyon batchleri, `n_eval=1060`.
- Çıktı: `outputs/zero_shot_sp500_external_test_model_family/`.

### `04_train_plain_sentiment_models.ipynb`

- Eğitim: `db/processed/training_datasets/plain_sentiment_dataset.parquet`.
- Veri: Twitter Financial News Sentiment + Financial PhraseBank.
- Toplam: 16.777 satır.
- Validation: `db/splits/plain_sentiment_v1/val_df.parquet`.
- Test: `db/splits/plain_sentiment_v1/test_df.parquet`.
- Not: Test bölümü yalnızca Twitter Financial News Sentiment kaynaklıdır.

### `05_evaluate_sp500_finetuned_models.ipynb`

- Eğitim: Yeni eğitim yoktur; `04` checkpointleri kullanılır.
- Test: `db/annotations/sp500_human_review_batches/`.
- Amaç: Fine-tune modellerin S&P 500 haber başlıklarına genellemesini ölçmek.

### `06_evaluate_synthetic_finetuned_models.ipynb`

- Eğitim: Yeni eğitim yoktur; `04` checkpointleri ve hazır FinBERT kullanılır.
- Test: `db/evaluation/synthetic_financial_news/`.
- Veri: Her sınıftan 1.000 örnek, toplam 3.000 sentetik haber.

### `07_evaluate_reuters_finetuned_models.ipynb`

- Eğitim: Yeni eğitim yoktur; `04` checkpointleri kullanılır.
- Test: `db/annotations/reuters_5000/REUTERS_annotation_all_clean.csv`.
- Veri: 5.000 Reuters haber başlığı.

### `09_search_new_dataset.ipynb`

- Eğitim: Eğitim yapmaz.
- Çıktı: Yeni aday veri setlerinden örnekler ve karşılaştırma tabloları.
- Amaç: Hocanın istediği ek veri setini belirlemek.

---

## 7. Sonuçlar

### 7.1. Hazır FinBERT Baseline

- Model: `ProsusAI/finbert`.
- Test: `db/splits/plain_sentiment_v1/test_df.parquet`.
- Accuracy: `0.7323`.
- Macro-F1: `0.6794`.
- Weighted-F1: `0.7400`.

Yorum: Hazır FinBERT makul bir başlangıç noktasıdır; ancak hedef veri
setindeki kısa piyasa metinlerine tam uyumlu değildir.

### 7.2. Zero-Shot S&P 500 Sonuçları

Dosya:

`outputs/zero_shot_sp500_external_test_model_family/zero_shot_sp500_external_test_model_family_summary.csv`

Değerlendirme satırı: `n_eval=1060`.

| Model | Accuracy | Macro-F1 |
| --- | ---: | ---: |
| Original FinBERT file label | 0.7519 | 0.7521 |
| RoBERTa-base NLI zero-shot | 0.6085 | 0.4913 |
| BERT-base-uncased MNLI zero-shot | 0.5057 | 0.4033 |
| DistilBERT-base-uncased MNLI zero-shot | 0.4679 | 0.3880 |

Yorum: `03a` diagnostic olarak kalır. Ana zero-shot yorum `03b` ve `03c`
üzerinden yapılmalıdır.

### 7.3. Plain Sentiment İç Test

| Model | Accuracy | Macro-F1 |
| --- | ---: | ---: |
| RoBERTa-base | 0.8906 | 0.8651 |
| BERT-base-uncased | 0.8722 | 0.8378 |
| DistilBERT-base-uncased | 0.8583 | 0.8218 |
| Original FinBERT | 0.7323 | 0.6794 |

### 7.4. S&P 500 Fine-Tuned Dış Test

| Model | Accuracy | Macro-F1 |
| --- | ---: | ---: |
| RoBERTa-base | 0.8125 | 0.8138 |
| Original FinBERT | 0.7583 | 0.7585 |
| DistilBERT-base-uncased | 0.7531 | 0.7523 |
| BERT-base-uncased | 0.7521 | 0.7511 |

### 7.5. Sentetik Finans Haberleri

| Model | Accuracy | Macro-F1 |
| --- | ---: | ---: |
| RoBERTa-base | 0.9957 | 0.9957 |
| BERT-base-uncased | 0.9743 | 0.9742 |
| DistilBERT-base-uncased | 0.9583 | 0.9581 |
| Original FinBERT | 0.9550 | 0.9551 |

### 7.6. Reuters 5.000 Dış Test

| Model | Accuracy | Macro-F1 |
| --- | ---: | ---: |
| Original FinBERT file label | 0.6966 | 0.6866 |
| RoBERTa-base | 0.6268 | 0.6388 |
| BERT-base-uncased | 0.6034 | 0.6131 |
| DistilBERT-base-uncased | 0.5766 | 0.5869 |

---

## 8. Genel Sonuç

Bu çalışmada tek bir modelin bütün veri kaynaklarında mutlak üstün
olduğu iddia edilmemelidir. Daha doğru yorum şudur:

- RoBERTa-base, plain sentiment iç testinde en güçlü modeldir.
- RoBERTa-base, S&P 500 dış testinde de en iyi fine-tuned sonucu verir.
- Sentetik testte tüm modeller yüksek başarı gösterir; bu test tek başına
  gerçek dış test yerine geçmez.
- Reuters testinde Original FinBERT file label öne geçer.
- Bu fark, veri kaynağı ve etiket tanımının model performansını
  doğrudan etkilediğini gösterir.

**Tezde kullanılabilecek ana sonuç cümlesi:**

RoBERTa-base, hedef plain sentiment verisine uyum ve S&P 500 genellemesi açısından
en güçlü fine-tuned modeldir. Reuters tarafında ise hazır FinBERT'in
alan ve etiket uyumu avantajı devam etmektedir.

---

## 9. Sonraki Adım

`09_search_new_dataset.ipynb` dosyası hocanın istediği ek veri seti arama
adımı için sonda tutulmuştur. Bu dosyadan seçilecek yeni veri seti,
ileride bağımsız bir ek dış test olarak projeye dahil edilebilir.
