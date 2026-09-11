# TEZ ÇALIŞMA ÖZETİ — SON KONTROL 2026

## 1. Tez Kimliği

**Başlık:**  
FİNANSAL DUYGU ANALİZİNDE MODEL GENELLEMESİ: FİNBERT VE İNCE AYARLI TRANSFORMER MODELLERİNİN KARŞILAŞTIRMALI İNCELENMESİ

**Araştırma odağı:**  
Hazır alan-özgü FinBERT, hedef veri setine ince ayarlı FinBERT ve genel amaçlı BERT / DistilBERT / RoBERTa modellerinin; iç test başarımı, çoklu seed kararlılığı, dış veri genellemesi, hata örüntüleri, kaynak-bileşimi etkisi ve CPU verimliliği açısından karşılaştırılması.

----

## 2. Ana Araştırma Sorusu

Temel soru yalnızca “hangi model daha yüksek F1 alıyor?” değildir.

Çalışma şu soruları birlikte ele alır:

1. Hedef veri setine özgü fine-tuning performansı ne ölçüde artırır?
2. Alan-özgü ön eğitim, hedefe özgü fine-tuning karşısında tek başına üstünlük sağlar mı?
3. Model sıralaması farklı finansal veri kaynaklarında sabit kalır mı?
4. Veri kaynağı ve etiket semantiği özellikle neutral sınıf hatalarını nasıl etkiler?
5. Sentetik test başarımı gerçek dış-dağılım genellemesini ne ölçüde temsil eder?
6. Financial PhraseBank gibi yardımcı bir kaynak eklemek RoBERTa performansını otomatik olarak artırır mı?
7. En yüksek performanslı model aynı zamanda en verimli model midir?

---

## 3. Veri Setleri

### Ana veri havuzu

Toplam: **16.777 örnek**

- Twitter Financial News Sentiment: **11.931**
- Financial PhraseBank: **4.846**

Güncel split:

- Train: **12.950**
- Validation: **1.432**
- Test: **2.386**

Ana havuz sınıf dağılımı:

- Negative: **2.393 (%14,26)**
- Neutral: **10.623 (%63,32)**
- Positive: **3.761 (%22,42)**

İç test:

- Negative: **358**
- Neutral: **1.549**
- Positive: **479**

Önemli metodolojik nokta: iç test yalnızca ana Twitter veri kaynağından ayrılmıştır. Financial PhraseBank test kümesine alınmamış, eğitim havuzunda yardımcı kaynak olarak kullanılmıştır.

### Dış testler

- S&P 500: **N=1.060** — ana doğrulanmış dış test
- Reuters: **N=5.000**
- Sentetik finansal haber: **N=3.000**

Kaynak-ablasyonu S&P değerlendirmesi ayrı bir loader nedeniyle **N=1.030** kullanmıştır. Bu sonuç yalnız ablation içindeki iki eğitim koşulunu kendi ortak 1.030 örneğinde karşılaştırmak için kullanılmalıdır; ana N=1.060 S&P sonuçlarıyla doğrudan kıyaslanmamalıdır.

---

## 4. Modeller

Ana modeller:

1. Original / off-the-shelf ProsusAI/FinBERT
2. Fine-tuned ProsusAI/FinBERT
3. BERT-base-uncased
4. DistilBERT-base-uncased
5. RoBERTa-base

Tamamlayıcı sıfır örnekli/NLI modeller:

- BART-large-MNLI
- RoBERTa-base NLI
- BERT-base MNLI
- DistilBERT-base MNLI

Zero-shot/NLI kolu ana karşılaştırmanın merkezi değil, tamamlayıcı keşifsel analizdir.

---

## 5. Temel Eğitim Ayarları

Ana fine-tuning protokolü:

- Epoch: **4**
- Learning rate: **2e-5**
- Train batch size: **16**
- Eval batch size: **32**
- Max length: **128**
- Weight decay: **0,01**
- Class weights: açık
- Seedler: **42, 123, 2024**

Yazılım / ortam:

- Python 3.14.2
- PyTorch 2.11.0+cpu
- Transformers 5.8.1
- Datasets 4.5.0
- scikit-learn 1.8.0
- Çalışma ortamı: CPU

Ana başarı ölçütü: **Macro-F1**

Macro-F1 seçilmesinin nedeni neutral sınıfının baskın olmasıdır. Accuracy çoğunluk sınıfından fazla etkilenebilir; Macro-F1 üç sınıfa eşit ağırlık verir.

---

## 6. İç Test — Seed 42 Sonuçları

| Model | Accuracy | Macro-F1 | Weighted-F1 |
|---|---:|---:|---:|
| RoBERTa | 0,8906 | **0,8651** | 0,8918 |
| Fine-tuned FinBERT | 0,8818 | **0,8512** | 0,8829 |
| BERT | 0,8722 | **0,8378** | 0,8733 |
| DistilBERT | 0,8583 | **0,8218** | 0,8593 |
| Original FinBERT | 0,7323 | **0,6794** | 0,7400 |

Fine-tuned FinBERT sınıf F1 değerleri:

- Negative: **0,7968**
- Neutral: **0,9157**
- Positive: **0,8410**

Temel çıkarım:

**Original FinBERT 0,6794 Macro-F1’den hedef veri setine fine-tuning sonrası 0,8512’ye yükselmiştir.** Bu, görev-özel fine-tuning’in çok güçlü etkisini gösterir. Bununla birlikte aynı seed altında RoBERTa **0,8651** ile daha yüksek performans vermiştir.

---

## 7. Çoklu Seed Sonuçları

Seedler: 42, 123, 2024.

| Model | Macro-F1 mean ± std | Accuracy mean ± std |
|---|---:|---:|
| RoBERTa | **0,8728 ± 0,0068** | 0,8975 ± 0,0059 |
| Fine-tuned FinBERT | **0,8480 ± 0,0028** | 0,8790 ± 0,0025 |
| BERT | **0,8396 ± 0,0023** | 0,8736 ± 0,0021 |
| DistilBERT | **0,8231 ± 0,0028** | 0,8601 ± 0,0028 |

Ana sonuç:

**RoBERTa yalnız tek koşuda değil, üç seed ortalamasında da birinci kalmıştır.**

---

## 8. İç Test İstatistiksel Anlamlılık

Seed 123:

- RoBERTa − Fine-tuned FinBERT ΔMacro-F1 = **+0,0294**
- Holm p = **0,000617**
- %95 paired bootstrap GA = **[0,0138; 0,0446]**

Seed 2024:

- RoBERTa − Fine-tuned FinBERT ΔMacro-F1 = **+0,0312**
- Holm p = **0,001410**
- %95 paired bootstrap GA = **[0,0162; 0,0462]**

Fine-tuned FinBERT vs BERT farkı aynı paired testlerde anlamlı değildir.

Dolayısıyla en güçlü istatistiksel iç-test sonucu:

**RoBERTa’nın fine-tuned FinBERT’e üstünlüğü seed 123 ve 2024’te hem Holm-düzeltilmiş McNemar hem paired bootstrap ile desteklenmiştir.**

---

## 9. Ana Dış Test Sonuçları

### S&P 500 — N=1.060

| Model | Macro-F1 |
|---|---:|
| RoBERTa | **0,8145** |
| Fine-tuned FinBERT | **0,7723** |
| BERT | 0,7549 |
| Original FinBERT | 0,7521 |
| DistilBERT | 0,7510 |

Fine-tuned FinBERT ayrıntıları:

- Accuracy: **0,7726**
- Macro Precision: **0,7945**
- Macro Recall: **0,7721**
- Macro-F1: **0,7723**
- F1 negative: **0,7636**
- F1 neutral: **0,7538**
- F1 positive: **0,7995**

Ana yorum:

RoBERTa yakın alan S&P 500 testinde üstünlüğünü korur. Fine-tuned FinBERT Original FinBERT’in sayısal olarak üstüne çıkar fakat bu farkın eşleştirilmiş istatistiksel testi anlamlı değildir.

### Reuters — N=5.000

| Model | Macro-F1 |
|---|---:|
| Original FinBERT | **0,6866** |
| RoBERTa | **0,6388** |
| BERT | 0,6131 |
| Fine-tuned FinBERT | **0,6101** |
| DistilBERT | 0,5869 |

Fine-tuned FinBERT:

- Accuracy: **0,5984**
- Macro Precision: **0,7207**
- Macro Recall: **0,6474**
- Macro-F1: **0,6101**
- F1 negative: **0,6937**
- F1 neutral: **0,5277**
- F1 positive: **0,6090**

Ana yorum:

Reuters’ta model sıralaması değişir ve **Original FinBERT yeniden birinci olur**. Hedef veri setine fine-tuning iç dağılımda güçlü kazanç sağlarken daha uzak editoryal dağılımda Original FinBERT’in alan-genel avantajını azaltabilir.

### Sentetik Finansal Haber — N=3.000

| Model | Macro-F1 |
|---|---:|
| RoBERTa | **0,9957** |
| Fine-tuned FinBERT | **0,9746** |
| BERT | 0,9742 |
| DistilBERT | 0,9581 |
| Original FinBERT | 0,9551 |

Fine-tuned FinBERT:

- Accuracy: **0,9747**
- Macro Precision: **0,9750**
- Macro Recall: **0,9747**
- Macro-F1: **0,9746**
- F1 negative: **0,9658**
- F1 neutral: **0,9876**
- F1 positive: **0,9704**

Sentetik set çok açık ve kolay ayrılabilir örnekler içerdiğinden tek başına gerçek dünya genellemesinin kanıtı olarak görülmemelidir.

---

## 10. Dış Test Eşleştirilmiş İstatistiksel Doğrulama

### S&P 500 — Original FinBERT vs Fine-tuned FinBERT

- Original − FT ΔMacro-F1 = **-0,0201**
- Holm p = **0,1678**
- %95 paired bootstrap GA = **[-0,0492; 0,0080]**

**Fark istatistiksel olarak anlamlı değildir.**

### Reuters — Original FinBERT vs Fine-tuned FinBERT

- Original − FT ΔMacro-F1 = **+0,0765**
- Holm p ≈ **1,37 × 10^-32**
- %95 paired bootstrap GA = **[0,0610; 0,0923]**

**Original FinBERT’in Reuters üstünlüğü güçlü biçimde desteklenmektedir.**

### Notebook 17 kalite kontrolü

Notebook 17’de S&P RoBERTa vs Fine-tuned FinBERT karşılaştırmasında RoBERTa Macro-F1 değeri **0,4913** görülmüştür. Bu değer ana doğrulanmış S&P RoBERTa sonucu **0,8145** ile uyuşmaz ve zero-shot RoBERTa-NLI sonucuyla aynıdır.

Sonuç:

- Otomatik dosya seçimi yanlış prediction CSV’sini eşleştirmiştir.
- Bu S&P RoBERTa paired-test satırı **bilimsel sonuçlardan çıkarılmıştır**.
- Reuters RoBERTa prediction girdisi eşleştirilmiş test için mevcut olmadığından o çift de raporlanmamıştır.

Karıştırılmaması gereken nokta:

**Ana S&P RoBERTa = 0,8145. 0,4913 ana fine-tuned RoBERTa sonucu değildir.**

---

## 11. RoBERTa Kaynak-Bileşimi Ablasyonu — Notebook 12

Kontrollü seed-42 karşılaştırması:

- Koşul A: Twitter-only
- Koşul B: Twitter + Financial PhraseBank

### İç test — N=2.386

| Koşul | Macro-F1 |
|---|---:|
| Twitter-only | **0,8810** |
| Twitter + PhraseBank | **0,8679** |

PhraseBank farkı: **-0,0132**

### Reuters — N=5.000

| Koşul | Macro-F1 |
|---|---:|
| Twitter-only | **0,6465** |
| Twitter + PhraseBank | **0,6305** |

PhraseBank farkı: **-0,0160**

### S&P Ablasyon — N=1.030

| Koşul | Macro-F1 |
|---|---:|
| Twitter-only | **0,7989** |
| Twitter + PhraseBank | **0,7968** |

PhraseBank farkı: **-0,0021**

Ana yorum:

**Daha fazla etiketli veri otomatik olarak daha iyi değildir.** Aynı üç sınıf adı kullanılsa bile Twitter ve Financial PhraseBank’ın dil yapısı ve etiket semantiği farklı olabilir. Heterojen yardımcı veri hedef dağılımının karar sınırını bulanıklaştırabilir.

Sınırlılık:

Bu ablation yalnız **seed 42** ile yapılmıştır. Ana model kararlılığı ayrı üç-seed deneyinde değerlendirilmiştir. Ablation multi-seed tekrarı gelecekte yapılabilir.

---

## 12. Fine-Tuned FinBERT Hata Analizi

Fine-tuned FinBERT iç testte:

- Toplam hata: **282**

En büyük hata geçişleri:

- neutral → positive: **78**
- neutral → negative: **75**
- negative → neutral: **52**
- positive → neutral: **52**
- positive → negative: **17**
- negative → positive: **8**

Neutral → positive ve neutral → negative birlikte:

**153 / 282 = %54,3**

Yüksek güvenli hatalar:

- confidence ≥ 0,90: **217 hata (%77,0)**
- confidence ≥ 0,95: **196 hata (%69,5)**
- confidence ≥ 0,99: **137 hata (%48,6)**

Ana çıkarım:

Hataların önemli kısmı yalnızca düşük güvenli belirsizlikten kaynaklanmamaktadır. Model bazı yanlış kararları çok yüksek güvenle üretmektedir. Bu durum modelin öğrendiği karar sınırı ile veri setinin etiket politikasının / etiket semantiğinin her örnekte tam örtüşmeyebileceğini düşündürmektedir.

Manuel hata kategorileri için 50 örneklik inceleme şablonu hazırlanmıştır; ancak tamamlanmış bağımsız insan kodlaması olmadığı için tezde nitel kategori oranları ölçülmüş sonuç gibi sunulmamaktadır.

---

## 13. Neutral Sınıfı ve Etiket Semantiği

Fine-tuned FinBERT neutral F1:

- Internal: **0,9157**
- S&P 500: **0,7538**
- Reuters: **0,5277**
- Sentetik: **0,9876**

Bu değişim tezdeki ana genelleme savını güçlendirir:

**Neutral karar sınırı veri kaynağı ve etiket semantiğine çok duyarlıdır.**

Finansal metinde “olumsuz kelime” ile “piyasa açısından negative etiket” aynı şey olmayabilir. Özellikle geleneksel finans haber tonu ile bullish/bearish/neutral piyasa-yönelimli etiketleme arasında semantik fark bulunabilir.

---

## 14. Zero-Shot / NLI Sonuçları — S&P 500

| Model | Macro-F1 |
|---|---:|
| BART-large-MNLI | **0,5580** |
| RoBERTa-base NLI | **0,4913** |
| BERT-base MNLI | **0,4033** |
| DistilBERT-base MNLI | **0,3880** |

Neutral F1:

- BART: **0,1199**
- RoBERTa-NLI: **0,0233**
- BERT-MNLI: **0,0058**
- DistilBERT-MNLI: **0,0776**

Ana yorum:

Genel NLI tabanlı zero-shot yaklaşım özellikle neutral sınıfında zayıftır. Bu kol tezde tamamlayıcıdır; ana fine-tuned karşılaştırmanın yerine geçmez.

---

## 15. CPU Verimliliği

| Model | Parametre (M) | Örnek/s | ms/örnek | Internal Macro-F1 |
|---|---:|---:|---:|---:|
| Original FinBERT | 109,48 | 30,81 | 32,46 | 0,6794 |
| Fine-tuned FinBERT | 109,48 | 28,84 | 34,68 | 0,8512 |
| BERT | 109,48 | 31,37 | 31,88 | 0,8378 |
| DistilBERT | **66,96** | **70,30** | **14,23** | 0,8218 |
| RoBERTa | 124,65 | 35,91 | 27,85 | **0,8651** |

DistilBERT, BERT’e göre yaklaşık **2,24× throughput** sağlar.

Ana çıkarım:

- En yüksek F1: RoBERTa
- En iyi hız/model boyutu: DistilBERT

Dolayısıyla gerçek deployment kararı yalnız Macro-F1 ile değil, **performans + genelleme + latency + model boyutu** dengesiyle verilmelidir.

---

## 16. Araştırmanın Ana Bulguları

1. **Target fine-tuning çok güçlüdür.**  
   Original FinBERT 0,6794 → Fine-tuned FinBERT 0,8512.

2. **Domain-specific pretraining tek başına mutlak üstünlük sağlamaz.**  
   İç testte ve üç-seed ortalamasında RoBERTa en iyi modeldir.

3. **Model sıralaması kaynak değişince değişir.**  
   S&P’de RoBERTa, Reuters’ta Original FinBERT birincidir.

4. **Target fine-tuning dış dağılıma otomatik taşınmaz.**  
   Fine-tuned FinBERT Reuters’ta Original FinBERT’in gerisine düşer.

5. **Daha fazla eğitim verisi otomatik kazanç sağlamaz.**  
   RoBERTa source-ablation’da Twitter-only, Twitter + PhraseBank koşulundan daha iyi sonuç verir.

6. **Neutral sınıfı kritik kırılma noktasıdır.**  
   Hata yönleri ve dış testlerdeki F1 düşüşleri özellikle neutral karar sınırına işaret eder.

7. **Sentetik başarı gerçek genellemenin eşdeğeri değildir.**  
   Sentetik sette tüm modeller çok yüksek performans verir.

8. **Performans ve verimlilik aynı modelde birleşmez.**  
   RoBERTa en güçlü performansı, DistilBERT en iyi hız/model-boyutu profilini verir.

---

## 17. Tezin Tek Cümlelik Ana Sonucu

**Hedef veri setine özgü fine-tuning finansal duygu sınıflandırmasında güçlü bir etkendir; ancak alan-özgü ön eğitim, daha fazla heterojen eğitim verisi veya tek bir model mimarisi evrensel üstünlük sağlamaz; model başarısı veri kaynağı, etiket semantiği, görev uyumu ve hesaplama maliyetinin birlikte etkisiyle belirlenir.**

---

## 18. Danışmana / Jüriye Söylenecek Kısa Sonuç

“Hazır FinBERT iç testte 0,6794 Macro-F1 üretirken hedef veri setine fine-tuning sonrası 0,8512’ye çıktı. Buna rağmen RoBERTa üç seed ortalamasında 0,8728 ± 0,0068 ile en güçlü model olarak kaldı. S&P 500’de RoBERTa 0,8145 ile birinci olurken Reuters’ta Original FinBERT 0,6866 ile yeniden öne çıktı ve Original FinBERT’in fine-tuned FinBERT’e Reuters üstünlüğü eşleştirilmiş testlerle desteklendi. Ayrıca kaynak-ablasyonunda Twitter-only RoBERTa’nın Twitter + PhraseBank koşulundan daha iyi sonuç vermesi, veri miktarından çok kaynak ve etiket semantiği uyumunun kritik olduğunu gösterdi.”

---

## 19. Karıştırılmaması Gereken Sonuçlar

- Ana S&P RoBERTa: **0,8145**
- **0,4913 = zero-shot RoBERTa-NLI / Notebook 17’de yanlış seçilen prediction girdisi**
- Fine-tuned FinBERT S&P: **0,7723**
- Fine-tuned FinBERT Reuters: **0,6101**
- Fine-tuned FinBERT sentetik: **0,9746**
- RoBERTa seed 42 internal: **0,8651**
- RoBERTa üç-seed ortalama: **0,8728 ± 0,0068**
- Ablation Twitter-only internal: **0,8810**
- Ablation Twitter + PhraseBank internal: **0,8679**
- Ablation S&P: **N=1.030**
- Ana doğrulanmış S&P: **N=1.060**
- Original FinBERT tarihsel internal baseline: **N=2.387**
- Güncel kaydedilmiş internal split: **N=2.386**

---

## 20. Önemli Sınırlılıklar

- Çalışma İngilizce ve üç sınıflı finansal sentiment ile sınırlıdır.
- Original FinBERT tarihsel baseline N=2.387, güncel saved split N=2.386’dır.
- Source-ablation tek seed (42) ile yapılmıştır.
- Ablation S&P N=1.030, ana S&P N=1.060’dır.
- Notebook 17’de yanlış prediction dosyası seçimi nedeniyle S&P RoBERTa paired karşılaştırması geçersiz sayılmıştır.
- Reuters RoBERTa için uygun paired prediction girdisi bulunmadığından ilgili eşleştirilmiş test raporlanmamıştır.
- Bağımsız anotatörler arası Cohen kappa / Krippendorff alpha ölçümü bulunmamaktadır.
- Manuel hata inceleme şablonu hazırlanmıştır fakat tamamlanmış bağımsız insan kodlamasına dayalı kategori oranı yoktur.
- CPU hız sonuçları kullanılan donanım ortamına özgüdür.
- Sentetik veri gerçek dünya OOD başarısının yerine geçmez.

---

## 21. Gelecek Çalışmalar

- Ablation deneyinin 42/123/2024 gibi çoklu seed ile tekrarlanması.
- Bağımsız anotatörler arası uyum ölçümü.
- Calibration / ECE / reliability analizi.
- Daha geniş zamansal ve kaynak-temelli domain-shift testleri.
- Türkçe / çok dilli finansal sentiment.
- Daha geniş ekonomik geçerlik değerlendirmesi.
- Parameter-efficient fine-tuning / quantization / distillation gibi verimlilik odaklı uzantılar.

---

## 22. Notebook Akışı — Güncel Durum

- 00: ortam / gereksinimler
- 01a: Reuters veri hazırlama
- 01b: S&P veri hazırlama
- 02: Original FinBERT baseline
- 03a: tanısal ince-ayarsız deney
- 03b / 03c: zero-shot NLI
- 04: BERT / DistilBERT / RoBERTa fine-tuning
- 05: S&P dış test
- 06: sentetik dış test
- 07: Reuters dış test
- 08: Fine-tuned FinBERT
- 10: multi-seed eğitim
- 11: internal statistical significance
- 12: **RoBERTa source-ablation — tamamlandı**
- 13: model × veri × sınıf analizi
- 14: genişletilmiş hata analizi
- 15: model verimliliği
- 16: **Fine-tuned FinBERT external evaluation — tamamlandı, S&P N=1.060 doğrulandı**
- 17: external paired significance — **yalnız doğrulanmış girdiler bilimsel sonuca alındı**

---

## 23. Nihai Referans

Tez ve raporlar için esas alınacak güncel dosya:

**finansal_duygu_analizi_tez_FINAL_KONTROL_2026.docx**

Eski notebook markdownları veya tarihsel özetlerde farklı değer görünürse doğrudan kullanılmamalıdır. Öncelik sırası:

1. Güncel doğrulanmış prediction / metric CSV çıktıları
2. FINAL_KONTROL tez
3. Nihai danışman özeti
4. Nihai savunma hazırlık raporu
5. Eski notebook markdownları / tarihsel özetler yalnız geçmiş kayıt olarak değerlendirilir.

**Son güncelleme:** 16 Ağustos 2026
