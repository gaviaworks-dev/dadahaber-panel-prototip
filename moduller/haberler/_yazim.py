"""Haberler modülü · yazım kuralı (Beyar, 25.11.2026): etiket, başlık, sekme, düğme, menü öğesi, pencere başlığı ve seçenek
adlarında her kelimenin baş harfi büyük; bağlaç ve edatlar küçük. Açıklama, ipucu, bildirim, hata ve tablo içeriği olduğu gibi.

Üreticiler (_uret.py, _uret_d2.py) sayfayı yazmadan önce `duzelt(html)` çağırır. Yalnız <main> ve şablonlar işlenir;
<head>, kabuk parçaları (P:menu, P:ust) ve betikler dokunulmaz. İşlem kendini tekrarlar (idempotent).
"""
import html, re

KUCUK = {"ve", "ile", "ya", "da", "de", "veya", "için", "ki", "gibi", "göre", "kadar", "mı", "mi", "mu", "mü"}
_UST = {"i": "İ", "ı": "I"}

def bb(s):
    """Her kelimenin baş harfi büyük (Türkçe), bağlaç ve edatlar küçük; kısaltma, sayı, adres ve özel ad olduğu gibi."""
    parca = re.split(r"(\s+)", s)
    out, ilk = [], True
    for p in parca:
        if not p or p.isspace():
            out.append(p); continue
        m = re.match(r"^([(\"“‘'«]*)(.*)$", p, re.S)
        on, govde = m.group(1), m.group(2)
        cekirdek = govde.rstrip(".,:;!?)”’»\"'").lower()
        if (govde and govde[0].isalpha() and govde[0].islower() and not re.search(r"[./@#]\w", govde)
                and (ilk or cekirdek not in KUCUK)):
            govde = _UST.get(govde[0], govde[0].upper()) + govde[1:]
        out.append(on + govde)
        ilk = False
    return "".join(out)

# hedefler: metnin doğrudan ebeveyni
SINIF = {"flabel", "form-sec-tt", "pc-title", "sa-form-tab", "btn", "kb-dm-grup", "kb-fs-tt", "kmg-tt", "chip", "kb-ekle-btn",
         "kb-suz-temizle", "pe-tag", "kg-etk", "kb-pm-cip", "ks-deger"}
ETIKET = {"label", "th", "h1", "dt"}
LISTE_KAP = {"kb-diger-menu", "kb-secim-liste", "kb-medya-gez", "kb-onizle-sec", "kb-gorunum-sec"}  # içindeki düğme/bağlantı = seçenek ya da menü öğesi
ATTR_HER = ("data-baslik-yaz", "data-onay-evet")  # pencere başlığı, onay düğmesi

_TOK = re.compile(r"<!--.*?-->|<[^>]+>|[^<]+", re.S)
_ATTR = re.compile(r'([\w:-]+)(?:\s*=\s*"([^"]*)")?')
_BOS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "wbr"}

def _sinif(a): return set((a.get("class") or "").split())

def _icerik(a):
    """Seçenek bir içerik kaydı mı (haber başlığı gibi)? Görselli ya da adres kimlikli seçenek içeriktir, olduğu gibi kalır."""
    return "data-gorsel" in a or a.get("data-deger", "").count("-") >= 3

def _hedef(st):
    """Yığının tepesi (doğrudan ebeveyn) yazım hedefi mi?"""
    if not st: return False
    t, a = st[-1]
    c = _sinif(a)
    if _icerik(a): return False
    kap = next((x for x in reversed(st) if "kb-secim" in _sinif(x[1])), None)
    if "ks-deger" in c and kap and _icerik(kap[1]): return False
    ust = st[-2] if len(st) > 1 else (None, {})
    uc = _sinif(ust[1])
    if t in ETIKET or c & SINIF: return True
    if t in ("button", "a") and uc & LISTE_KAP: return True
    if t == "span" and "toggle-row" in uc and not c: return True                         # anahtar başlığı
    if t == "b" and (uc & {"kaa-bas", "kb-pm-bas"} or (ust[0] == "span" and len(st) > 2 and "kb-secenek-kart" in _sinif(st[-3][1]))): return True
    if t == "span" and ust[0] == "div" and len(st) > 2 and "sa-durum" in _sinif(st[-3][1]) and not c: return True  # yan kart etiketi
    if t in ("span", "b") and not c and len(st) > 1:                                    # düğme içindeki sınıfsız span
        return _hedef(st[:-1]) and ust[0] in ("button", "a")
    return False

def _cevir_metin(ham):
    d = html.unescape(ham)
    y = bb(d)
    return ham if y == d else html.escape(y, quote=False)

def _cevir_attr(tag, adlar):
    def r(m):
        ad, v = m.group(1), m.group(2)
        if ad not in adlar or v is None: return m.group(0)
        d = html.unescape(v); y = bb(d)
        return m.group(0) if y == d else f'{ad}="{html.escape(y, quote=True)}"'
    return re.sub(r'([\w:-]+)="([^"]*)"', r, tag)

def _isle(parca):
    out, st = [], []
    for tok in _TOK.findall(parca):
        if tok.startswith("<!--"):
            out.append(tok); continue
        if tok.startswith("</"):
            t = tok[2:-1].strip().lower()
            if any(x[0] == t for x in st):
                while st and st.pop()[0] != t: pass
            out.append(tok); continue
        if tok.startswith("<"):
            m = re.match(r"<([\w-]+)", tok)
            if not m: out.append(tok); continue
            t = m.group(1).lower()
            a = {k: (v if v is not None else "") for k, v in _ATTR.findall(tok[len(t) + 1:].rstrip("/>"))}
            adlar = set(ATTR_HER)
            if t == "template": adlar.add("data-baslik")
            yeni = st + [(t, a)]
            if t in ("button", "a") and st and _sinif(st[-1][1]) & {"kb-secim-liste"} and not _icerik(a): adlar.add("data-ad")
            if "data-yeni-metin" in a and _hedef(yeni) and "ks-deger" not in _sinif(a): adlar.add("data-yeni-metin")
            tok = _cevir_attr(tok, adlar)
            out.append(tok)
            if t not in _BOS and not tok.endswith("/>"): st.append((t, a))
            continue
        if st and _hedef(st) and tok.strip():
            # ks-deger yer tutucusu
            t0, a0 = st[-1]
            if "ks-deger" in _sinif(a0):
                kap = next((x for x in reversed(st) if "kb-secim" in _sinif(x[1])), None)
                if kap and html.unescape(tok.strip()) == html.unescape(kap[1].get("data-bos", "")):
                    out.append(tok); continue
            tok = _cevir_metin(tok)
        out.append(tok)
    return "".join(out)

def duzelt(sayfa):
    """Sayfanın gövdesini yazım kuralına göre düzeltir; head, kabuk parçaları ve betikler olduğu gibi kalır."""
    korunan = re.compile(r"(<head>.*?</head>|<!--P:(menu|ust)-->.*?<!--/P:\2-->|<script\b.*?</script>)", re.S)
    out, i = [], 0
    for m in korunan.finditer(sayfa):
        out.append(_isle(sayfa[i:m.start()])); out.append(m.group(0)); i = m.end()
    out.append(_isle(sayfa[i:]))
    return "".join(out)
