from __future__ import annotations

import csv
import shutil
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from xml.etree import ElementTree as ET


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
W = NS["w"]
ET.register_namespace("w", W)


def qn(tag: str) -> str:
    return f"{{{W}}}{tag}"


def el(tag: str, attrs: dict[str, str] | None = None) -> ET.Element:
    node = ET.Element(qn(tag))
    if attrs:
        for key, value in attrs.items():
            node.set(qn(key), value)
    return node


def paragraph(text: str = "", style: str | None = None) -> ET.Element:
    p = el("p")
    if style:
        ppr = el("pPr")
        pstyle = el("pStyle", {"val": style})
        ppr.append(pstyle)
        p.append(ppr)
    if text:
        r = el("r")
        t = el("t")
        t.text = text
        r.append(t)
        p.append(r)
    return p


def set_paragraph_text(p: ET.Element, text: str) -> None:
    ppr = p.find("w:pPr", NS)
    for child in list(p):
        if child is not ppr:
            p.remove(child)
    r = el("r")
    t = el("t")
    t.text = text
    r.append(t)
    p.append(r)


def cell(text: str, width: int = 1200, shade: str | None = None, bold: bool = False) -> ET.Element:
    tc = el("tc")
    tcpr = el("tcPr")
    tcpr.append(el("tcW", {"w": str(width), "type": "dxa"}))
    if shade:
        tcpr.append(el("shd", {"fill": shade}))
    tc.append(tcpr)
    p = el("p")
    r = el("r")
    rpr = el("rPr")
    rpr.append(el("sz", {"val": "16"}))
    if bold:
        rpr.append(el("b"))
    r.append(rpr)
    t = el("t")
    t.text = str(text)
    r.append(t)
    p.append(r)
    tc.append(p)
    return tc


def table(headers: list[str], rows: list[list[str]], widths: list[int]) -> ET.Element:
    tbl = el("tbl")
    tblpr = el("tblPr")
    tblpr.append(el("tblStyle", {"val": "TableGrid"}))
    tblpr.append(el("tblW", {"w": str(sum(widths)), "type": "dxa"}))
    borders = el("tblBorders")
    for side in ["top", "left", "bottom", "right", "insideH", "insideV"]:
        borders.append(el(side, {"val": "single", "sz": "4", "space": "0", "color": "BFBFBF"}))
    tblpr.append(borders)
    tbl.append(tblpr)
    grid = el("tblGrid")
    for w in widths:
        grid.append(el("gridCol", {"w": str(w)}))
    tbl.append(grid)
    tr = el("tr")
    for h, w in zip(headers, widths):
        tr.append(cell(h, w, shade="D9EAF7", bold=True))
    tbl.append(tr)
    for row in rows:
        tr = el("tr")
        for value, w in zip(row, widths):
            tr.append(cell(value, w))
        tbl.append(tr)
    return tbl


def fmt(x: str | float | int) -> str:
    if isinstance(x, float):
        return f"{x:.4f}"
    return str(x)


def load_results() -> list[list[str]]:
    path = Path("outputs/thesis_tables/thesis_single_results_table.csv")
    rows: list[list[str]] = []
    with path.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append(
                [
                    r["dataset"],
                    r["model"],
                    r["n_eval"],
                    fmt(float(r["accuracy"])),
                    fmt(float(r["precision_macro"])),
                    fmt(float(r["recall_macro"])),
                    fmt(float(r["f1_macro"])),
                    fmt(float(r["negative_f1"])),
                    fmt(float(r["neutral_f1"])),
                    fmt(float(r["positive_f1"])),
                ]
            )
    return rows


def main() -> None:
    src = Path("tez/finansal_duygu_analizi_tez_taslagi.docx")
    out = Path("tez/finansal_duygu_analizi_tez_taslagi_guncel.docx")
    tmp = Path("outputs/thesis_tables/_docx_edit_tmp.docx")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, tmp)

    with ZipFile(tmp, "r") as zin:
        parts = {name: zin.read(name) for name in zin.namelist()}

    root = ET.fromstring(parts["word/document.xml"])
    body = root.find("w:body", NS)
    if body is None:
        raise RuntimeError("DOCX body not found")

    for p in body.findall("w:p", NS):
        text = "".join(t.text or "" for t in p.findall(".//w:t", NS))
        if "Dış testte kullanılan nihai set 2.132 geçerli örnek" in text:
            set_paragraph_text(
                p,
                "S&P 500 şirketlerine ilişkin haber başlıkları hazır FinBERT ile ön etiketlenmiş, daha sonra sınıflar dengelenerek anotasyon batch dosyaları oluşturulmuştur. Dış testte kullanılan geçerli değerlendirme seti 1.060 örnekten oluşmaktadır: 323 negative, 339 neutral ve 398 positive. Etiketleme sürecinde manuel inceleme için ChatGPT destekli açıklama alanları kullanılmış; ancak nihai akademik sürümde insan anotatör sayısı ve bağımsız uyum ölçümü ayrıca raporlanmalıdır.",
            )
        if "Sıfır örnekli yaklaşım eğitim gerektirmeyen bir temel model sunmaktadır; nihai metrik tablosu tamamlanmalıdır." in text:
            set_paragraph_text(
                p,
                "Sıfır örnekli yaklaşım eğitim gerektirmeyen bir temel model sunmaktadır; ancak S&P 500 testinde en iyi zero-shot sonuç BART-large-MNLI ile 0,6594 doğruluk ve 0,5580 makro F1 düzeyinde kalmış, denetimli ince ayarlı RoBERTa'nın 0,8145 makro F1 sonucunun belirgin biçimde gerisinde kalmıştır.",
            )

    sect_pr = body.find("w:sectPr", NS)
    insert_at = list(body).index(sect_pr) if sect_pr is not None else len(list(body))

    additions: list[ET.Element] = []
    additions.append(paragraph("EK C. DENEY AYRINTILARI, TOPLU SONUÇLAR VE HATA ANALİZİ", "Heading1"))
    additions.append(paragraph("Bu ek, tez danışmanlığı değerlendirmesinde istenen deney ayrıntılarını mevcut proje dosyalarından çıkarılabildiği ölçüde tek yerde toplar. Sayısal değerler proje klasöründeki split, checkpoint, notebook çıktısı ve prediction CSV dosyalarından alınmıştır; kaydı bulunmayan bilgiler açık sınırlılık olarak belirtilmiştir."))

    additions.append(paragraph("C.1. Deney ve Ortam Ayrıntıları", "Heading2"))
    exp_rows = [
        ["Ana veri", "16.777 örnek; Twitter Financial News Sentiment 11.931, Financial PhraseBank 4.846."],
        ["Split", "Mevcut split dosyaları: train 12.950, validation 1.432, test 2.386. Toplam ana havuza göre yaklaşık %77,19 / %8,54 / %14,22."],
        ["Sınıf dağılımı", "Ana havuz: negative 2.393 (%14,26), neutral 10.623 (%63,32), positive 3.761 (%22,42)."],
        ["Eğitim ayarları", "Seed 42; epoch 4; learning rate 2e-5; train batch size 16; eval batch size 32; max length 128; weight decay 0,01; class weights açık."],
        ["Model sürümleri", "ProsusAI/finbert; bert-base-uncased; distilbert-base-uncased; roberta-base; zero-shot için BART-large-MNLI ve NLI/MNLI model ailesi."],
        ["Yazılım/donanım", "Python 3.14.2, PyTorch 2.11.0+cpu, Transformers 5.8.1, Datasets 4.5.0, scikit-learn 1.8.0. Notebook çıktılarında CUDA false ve cihaz CPU olarak görünmektedir."],
        ["İstatistiksel güvenilirlik", "Mevcut çalıştırmalar tek random seed (42) ile yapılmıştır. Çoklu seed ortalama ve standart sapma bu klasörde mevcut değildir; bu nedenle sonuçlar tek çalıştırma olarak raporlanmıştır."],
    ]
    additions.append(table(["Başlık", "Ayrıntı"], exp_rows, [2200, 6900]))

    additions.append(paragraph("C.2. Veri Seti Büyüklükleri ve Sınıf Dağılımları", "Heading2"))
    dist_rows = [
        ["Ana havuz", "16.777", "2.393", "10.623", "3.761"],
        ["Train", "12.950", "1.820", "8.137", "2.993"],
        ["Validation", "1.432", "215", "929", "288"],
        ["Test", "2.386", "358", "1.549", "479"],
        ["S&P 500 dış test", "1.060", "323", "339", "398"],
        ["Sentetik test", "3.000", "1.000", "1.000", "1.000"],
        ["Reuters dış test", "5.000", "1.579", "1.146", "2.275"],
    ]
    additions.append(table(["Veri seti", "N", "Negative", "Neutral", "Positive"], dist_rows, [2300, 1100, 1500, 1500, 1500]))

    additions.append(paragraph("C.3. Tek Sonuç Tablosu", "Heading2"))
    additions.append(paragraph("Tabloda P-makro ve R-makro sırasıyla makro precision ve makro recall değerlerini gösterir. Internal testte Original FinBERT satırı notebook çıktısından alınmış ve n=2.387 olarak raporlanmıştır; güncel split dosyasında test satır sayısı 2.386'dır."))
    result_headers = ["Veri", "Model", "N", "Acc", "P-makro", "R-makro", "F1-makro", "F1-neg", "F1-neu", "F1-pos"]
    additions.append(table(result_headers, load_results(), [1700, 1900, 800, 800, 850, 850, 900, 800, 800, 800]))

    additions.append(paragraph("C.4. Anotasyon Yöntemi ve Sınırlılık", "Heading2"))
    additions.append(paragraph("S&P 500 setinde haber başlıkları önce FinBERT ile etiketlenmiş, ardından dengeli anotasyon batchleri hazırlanmıştır. Batch yapısında final_label, ChatGPT destekli açıklama, güven ve not alanları bulunmaktadır. Reuters seti 5.000 örnek olarak hazırlanmış; final_label alanı değerlendirme etiketi olarak kullanılmıştır. Kullanılan yönerge özetle positive için yatırımcı açısından olumlu beklenti/gerçekleşme, negative için olumsuz beklenti/risk/kayıp, neutral için olgusal veya yönü belirsiz haber tanımlarını kullanır. Birden fazla hedefte çatışan sentiment varsa target_entity doldurulması veya plain sentiment için örneğin ayrılması önerilmiştir."))
    additions.append(paragraph("Mevcut dosyalarda kaç insan anotatörün görev aldığı ve anotatörler arası uyumun Cohen kappa veya Krippendorff alpha gibi bir ölçütle hesaplandığına ilişkin tamamlanmış kayıt bulunmamaktadır. Bu nedenle çalışma, anotasyon güvenilirliğini ölçülmüş bir bulgu olarak değil, sınırlılık ve gelecek çalışma gereksinimi olarak raporlamalıdır."))

    additions.append(paragraph("C.5. Confusion Matrix ve Hata Analizi", "Heading2"))
    cm_rows = [
        ["Internal RoBERTa", "67 / 1.549", "0,0433"],
        ["Internal BERT", "84 / 1.549", "0,0542"],
        ["Internal DistilBERT", "82 / 1.549", "0,0529"],
        ["S&P 500 Original FinBERT", "36 / 339", "0,1062"],
        ["S&P 500 RoBERTa", "19 / 339", "0,0560"],
        ["S&P 500 BERT", "15 / 339", "0,0442"],
        ["S&P 500 DistilBERT", "16 / 339", "0,0472"],
    ]
    additions.append(table(["Model/test", "Neutral -> negative", "Oran"], cm_rows, [3400, 2600, 1400]))
    additions.append(paragraph("Örnek hata başlıkları özellikle karışık sinyal taşıyan veya piyasa yönü açık olmayan haberlerde yoğunlaşmaktadır: 'S&P 500 Gains and Losses Today: NetApp and GM Rise; Hormel and Las Vegas Sands Fall' hem yükselen hem düşen hisseleri içerdiği için neutral kabul edilmiştir, ancak FinBERT negative tahmin etmiştir. 'Strong corporate earnings are helping the US avoid a recession - but there are 2 big risks facing markets...' olumlu ve riskli unsurları birlikte taşıdığı için neutral/karışık kabul edilmiştir. 'AP Explains: What resignation of New Zealand's leader means' ise finansal yön içermeyen siyasi/açıklayıcı bir başlık olmasına rağmen negative tahmin edilmiştir."))

    additions.append(paragraph("C.6. Zero-Shot ve Sentetik Veri Yorumu", "Heading2"))
    additions.append(paragraph("Zero-shot deneyleri tamamlanmış ve tek sonuç tablosuna eklenmiştir. BART-large-MNLI S&P 500 üzerinde 0,6594 doğruluk ve 0,5580 makro F1 elde ederek zero-shot modeller içinde en iyi sonucu vermiştir. Buna rağmen neutral sınıf F1'i 0,1199 düzeyinde kalmıştır; RoBERTa-base NLI, BERT-base MNLI ve DistilBERT-base MNLI sürümlerinde neutral F1 daha da düşüktür. Bu bulgu, NLI tabanlı zero-shot yaklaşımın finansal neutral tanımını öğrenmeden güçlü bir alternatif olamadığını göstermektedir."))
    additions.append(paragraph("Sentetik veri sonuçları da tabloya eklenmiştir. Tüm modeller sentetik sette 0,9551 ile 0,9957 arasında makro F1 üretmiştir. Bu yüksek değerler, sentetik örneklerde duygu ipuçlarının açık olmasından kaynaklanabilir; bu nedenle sentetik test gerçek Reuters ve S&P 500 dış testlerinin yerine geçmemeli, yalnızca kontrollü bir stres testi olarak yorumlanmalıdır."))

    for offset, node in enumerate(additions):
        body.insert(insert_at + offset, node)

    parts["word/document.xml"] = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    with ZipFile(out, "w", ZIP_DEFLATED) as zout:
        for name, data in parts.items():
            zout.writestr(name, data)
    print(out)


if __name__ == "__main__":
    main()
