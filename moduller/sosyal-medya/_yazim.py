#!/usr/bin/env python3
"""Yazım kuralı (Beyar): etiket, başlık, sekme, düğme, menü öğesi, çekmece/pencere başlığı ve seçenek adlarında
her kelimenin baş harfi büyük; bağlaç ve edatlar küçük. Açıklama, ipucu, bildirim metni ve tablo içeriği cümle düzeninde.

Kullanım:  python3 -I moduller/sosyal-medya/_yazim.py <sayfa.html …>   (dosyayı yerinde düzeltir; _uret.py de çağırır)
Yalnızca metin düğümlerine ve birkaç niteliğe dokunur; işaretleme olduğu gibi kalır.
"""
import re, sys
from html.parser import HTMLParser

KUCUK = {"ve", "veya", "ya", "da", "de", "ile", "için", "ki", "ama", "gibi", "göre", "kadar", "mi", "mı", "mu", "mü"}
BUYUK = str.maketrans({"i": "İ", "ı": "I"})
KORU = {"dadahaber"}  # küçük harfle yazılan özel adlar (hesap adı)


def kelime(w, ilk):
    on = re.match(r"^[(\"“‘'«]*", w).group(0); w = w[len(on):]
    return on + _kelime(w, ilk)


def _kelime(w, ilk):
    if not w or not w[0].isalpha() or not w[0].islower() or w.strip(".,:;!?…)") in KORU: return w
    if any(c.isupper() for c in w) or "@" in w or "." in w.strip(".,:;!?…") or w.startswith("http"): return w
    if not ilk and w.lower().strip(".,:;!?…") in KUCUK: return w
    return w[0].translate(BUYUK).upper() + w[1:] if w[0] not in "iı" else w[0].translate(BUYUK) + w[1:]


def baslik(s, bas=True):
    parca = re.split(r"(\s+)", s); out = []; ilk = bas
    for p in parca:
        if not p or p.isspace(): out.append(p); continue
        out.append(kelime(p, ilk)); ilk = p in ("·", "—", "–", ":", "›")
    return "".join(out)


ETIKET = {"h1", "h2", "h3", "label", "button", "th", "dt"}
SINIF = {"flabel", "form-sec-tt", "kb-fs-tt", "pc-title", "kb-dm-grup", "kpi-lbl", "ks-grup", "ks-deger", "kaa-bas", "kb-entegre-bas"}
HARIC = {"small", "kbd", "code", "textarea", "script", "style"}
HARIC_SINIF = {"ks-alt", "ch-cnt", "fs-ek", "fhint", "kd-etk", "etk", "pstat", "muted", "kp-durum", "kb-ai-durum", "kb-tarih", "kis-m"}
BOS = {"input", "img", "br", "hr", "meta", "link", "source", "col", "area", "base", "wbr", "embed", "param", "track"}
NIT = {"data-ad", "data-onay-evet", "data-yeni-metin"}


class Yazim(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False); self.o = []; self.y = []

    def durum(self):
        return self.y[-1] if self.y else (False, False, False, False)

    def nit(self, ham, tag, attrs, acik):
        a = dict(attrs)
        if tag == "template" and a.get("data-baslik"):
            ham = ham.replace(f'data-baslik="{a["data-baslik"]}"', f'data-baslik="{baslik(a["data-baslik"])}"', 1)
        for n in NIT:
            v = a.get(n)
            if not v or not acik or (n == "data-ad" and (tag != "button" or "data-deger" not in a)): continue
            ham = ham.replace(f'{n}="{v}"', f'{n}="{baslik(v)}"', 1)
        return ham

    def handle_starttag(self, tag, attrs):
        a = dict(attrs); sn = set((a.get("class") or "").split())
        ust_acik, ust_haric, ust_bos, ust_menu = self.durum()
        bos = ust_bos or "pnl-empty" in sn; menu = ust_menu or "kb-diger-menu" in sn
        haric = ust_haric or tag in HARIC or bool(sn & HARIC_SINIF) or a.get("data-alan-id") == "haber" or "data-icerik-sec" in a or "data-sosyal-ad" in a or "data-ai-durum" in a
        acik = ust_acik or tag in ETIKET or (tag == "a" and (bool(sn & {"btn", "pe-tag"}) or menu)) or bool(sn & SINIF) or (tag == "span" and self.ebeveyn_toggle) or (tag == "b" and self.ebeveyn_kart)
        # içerik başlığı taşıyan seçenekler (haber listesi): uzun kısa-ad değerli düğme cümle olarak kalır
        if tag == "h2" and ust_bos: haric = True
        if tag == "button" and "-" in (a.get("data-deger") or "") and len(a.get("data-deger") or "") > 24: haric = True
        self.o.append(self.nit(self.get_starttag_text(), tag, attrs, acik and not haric))
        if tag not in BOS:
            self.y.append((acik, haric, bos, menu)); self.ebeveyn_toggle = "toggle-row" in sn; self.ebeveyn_kart = "kb-secenek-kart" in sn or "kaa-bas" in sn
        else:
            self.ebeveyn_toggle = False

    ebeveyn_toggle = False; ebeveyn_kart = False

    def handle_startendtag(self, tag, attrs):
        self.o.append(self.nit(self.get_starttag_text(), tag, attrs, False))

    def handle_endtag(self, tag):
        self.o.append(f"</{tag}>")
        if tag not in BOS and self.y: self.y.pop()
        self.ebeveyn_toggle = False; self.ebeveyn_kart = False

    def handle_data(self, d):
        acik, haric, _, _ = self.durum()
        if acik and not haric and d.strip():
            if self.o and self.o[-1].startswith("&") and not d[0].isspace():  # "Kadıköy&#x27;de": kelimenin devamı
                bas, kalan = re.match(r"(\S*)(.*)", d, re.S).groups(); d = bas + (baslik(kalan, bas=False) if kalan.strip() else kalan)
            else:
                d = baslik(d)
        self.o.append(d)

    def handle_entityref(self, n): self.o.append(f"&{n};")
    def handle_charref(self, n): self.o.append(f"&#{n};")
    def handle_comment(self, d): self.o.append(f"<!--{d}-->")
    def handle_decl(self, d): self.o.append(f"<!{d}>")
    def handle_pi(self, d): self.o.append(f"<?{d}>")


KAYIT_KONU = re.compile(r'(<div class="kb-fs-tt">)([^<]{8,})(<span class="pstat)')  # kayıt konusu (okur mesajı): içerik, cümle düzeni


def _tek(t):
    sakla = []
    def tut(m): sakla.append(m.group(2)); return m.group(1) + f"\x00{len(sakla) - 1}\x00" + m.group(3)
    t = KAYIT_KONU.sub(tut, t)
    p = Yazim(); p.feed(t); p.close(); o = "".join(p.o)
    return re.sub(r"\x00(\d+)\x00", lambda m: sakla[int(m.group(1))], o)


def duzelt(t):
    """Kabuk parçaları (<!--P:…-->) menu_yaz.py'nindir; onlara dokunulmaz."""
    parca = re.split(r"(<!--P:(\w+)-->.*?<!--/P:\2-->)", t, flags=re.S)
    out = []; i = 0
    while i < len(parca):
        out.append(_tek(parca[i])); i += 1
        if i < len(parca): out.append(parca[i]); i += 2
    return "".join(out)


if __name__ == "__main__":
    for f in sys.argv[1:]:
        t = open(f, encoding="utf-8").read(); y = duzelt(t)
        if y != t: open(f, "w", encoding="utf-8").write(y); print("düzeltildi:", f)
