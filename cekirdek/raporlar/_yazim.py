#!/usr/bin/env python3
"""Panel yazım kuralı (Beyar): etiket, başlık, sekme, düğme, menü öğesi, pencere başlığı ve seçenek adlarında her kelimenin
baş harfi büyük; bağlaç/edat küçük; açıklama, ipucu, bant metni ve tablo içeriği cümle düzeninde. Kaynakta değiştirir.
Kullanım: baslik_duzen.py [--goster] dosya.html …"""
import re, sys

KUCUK = {'ve', 'ya', 'da', 'de', 'ile', 'için', 'veya', 'ki', 'mi', 'ya da'}
DAHIL_ETIKET = {'h1', 'h2', 'h3', 'th', 'label', 'title'}
DAHIL_SINIF = {'form-sec-tt', 'kb-fs-tt', 'flabel', 'sa-form-tab', 'chip', 'btn', 'kb-secim-liste', 'ks-deger', 'ks-etk',
               'ka-hazir', 'kpi-lbl', 'kb-diger-menu', 'pc-title'}
HARIC_ETIKET = {'small', 'p', 'td', 'code', 'script', 'style', 'pre'}
HARIC_SINIF = {'ks-alt', 'fs-ek', 'ch-cnt', 'kpi-delta', 'rcp-by', 'fhint', 'pstat', 'kb-bant', 'pnl-empty', 'kt-deger', 'kb-kap-alt', 'kb-dm-not'}
BOS = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
ATTR = re.compile(r'\b(data-bos|data-onay-evet|data-baslik-yaz)="([^"]*)"')
ATTR_DUGME = re.compile(r'\b(data-ad)="([^"]*)"')
TPL_BASLIK = re.compile(r'(<template\b[^>]*\bdata-baslik=")([^"]*)(")')

def buyut(c): return {'i': 'İ', 'ı': 'I'}.get(c, c.upper())

def kelime(w, ilk):
    if not w or w.startswith('&') or any(ch.isupper() for ch in w): return w
    if not ilk and w in KUCUK: return w
    def parca(p):
        j = 0
        while j < len(p) and p[j] in '("“‘\'': j += 1
        return p[:j] + buyut(p[j]) + p[j + 1:] if j < len(p) and p[j].isalpha() else p
    return '/'.join(parca(p) for p in w.split('/'))

def duzen(metin, bas=True):
    out, ilk = [], bas
    for tok in re.split(r'(\s+)', metin):
        if not tok or tok.isspace(): out.append(tok); continue
        out.append(kelime(tok, ilk)); ilk = False
    return ''.join(out)

def karar(yigin):
    for ad, sinif, _ in reversed(yigin):
        if ad in HARIC_ETIKET or sinif & HARIC_SINIF: return False
        if ad in DAHIL_ETIKET or sinif & DAHIL_SINIF: return True
    return False

def isle(s, goster):
    degisen = []
    # işaretli üretim blokları (menü, üst bar) lead'in betiğinden gelir: dokunma
    parcalar = re.split(r'(<!--P:(\w+)-->.*?<!--/P:\2-->)', s, flags=re.S)
    sonuc = []
    k = 0
    while k < len(parcalar):
        p = parcalar[k]
        if p.startswith('<!--P:'): sonuc.append(p); k += 2; continue
        yigin, ilk_metin, sayac = [], {}, [0]
        out = []
        for m in re.finditer(r'<!--.*?-->|<[^>]+>|[^<]+', p, flags=re.S):
            t = m.group(0)
            if t.startswith('<!'): out.append(t); continue
            if t.startswith('</'):
                ad = t[2:-1].strip().lower()
                while yigin:
                    if yigin.pop()[0] == ad: break
                out.append(t); continue
            if t.startswith('<'):
                ad = re.match(r'<\s*([a-zA-Z0-9-]+)', t).group(1).lower()
                cm = re.search(r'\bclass="([^"]*)"', t)
                def a_duz(mm):
                    yeni = duzen(mm.group(2))
                    if yeni != mm.group(2): degisen.append(mm.group(2) + ' → ' + yeni)
                    return f'{mm.group(1)}="{yeni}"'
                t2 = ATTR.sub(a_duz, t)
                if ad == 'button': t2 = ATTR_DUGME.sub(a_duz, t2)
                if ad == 'template': t2 = TPL_BASLIK.sub(lambda mm: mm.group(1) + duzen(mm.group(2)) + mm.group(3), t2)
                out.append(t2)
                if ad not in BOS and not t.endswith('/>'): sayac[0] += 1; yigin.append((ad, set(cm.group(1).split()) if cm else set(), sayac[0]))
                continue
            if t.strip() and karar(yigin):
                # bir öğenin ilk metin parçası cümle başıdır; aynı öğede sonraki parçalar (ikon sonrası değil, iç öğe sonrası) devamdır
                anahtar = yigin[-1][2] if yigin else 0
                bas = anahtar not in ilk_metin; ilk_metin[anahtar] = 1
                yeni = duzen(t, bas)
                if yeni != t: degisen.append(t.strip() + ' → ' + yeni.strip())
                out.append(yeni)
            else: out.append(t)
        sonuc.append(''.join(out)); k += 1
    return ''.join(sonuc), degisen

if __name__ == '__main__':
    goster = '--goster' in sys.argv
    for f in [a for a in sys.argv[1:] if not a.startswith('--')]:
        s = open(f, encoding='utf-8').read()
        y, d = isle(s, goster)
        if not goster: open(f, 'w', encoding='utf-8').write(y)
        print(f, len(d), 'değişiklik')
        if goster:
            for x in sorted(set(d)): print('   ', x)
