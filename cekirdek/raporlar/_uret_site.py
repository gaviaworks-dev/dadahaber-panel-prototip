#!/usr/bin/env python3
"""cekirdek/raporlar/site.html üretir (Site İstatistikleri). Çalıştır: python3 -I cekirdek/raporlar/_uret_site.py ; ardından araclar/menu_yaz.py --yalniz cekirdek/raporlar.
 Kabuk parçaları index.html'den alınır; menu_yaz.py sonra yeniler.
Sayılar tek yerde hesaplanır: KPI, tablo ve grafikler birbiriyle tutarlı."""
import re, sys, html, json

import os
KOK = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _yazim, _disa
src = open(KOK + '/cekirdek/raporlar/index.html', encoding='utf-8').read()

def e(s): return html.escape(s, quote=True)

def tr_sayi(v, ond=0):
    s = f'{v:,.{ond}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')

def kisa(v):
    """22_400_000 -> 22,4 Mn · 568_400 -> 568,4 B · 3_482 -> 3.482"""
    if v >= 1e6: return tr_sayi(v / 1e6, 2 if v < 1e7 else 1) + ' Mn'
    if v >= 1e4: return tr_sayi(v / 1e3, 1) + ' B'
    return tr_sayi(v)

def yuzde(v, ond=1): return '%' + tr_sayi(v, ond)

def i(ikon, cls='fa-solid'): return f'<i class="{cls} {ikon}" aria-hidden="true"></i>'

def sure(sn): return f'{sn // 60} dk {sn % 60:02d} sn' if sn >= 60 else f'{sn} sn'

# ---------------------------------------------------------------- veri
GUN = '17 Kas,18,19,20,21,22,23 Kas'
PV = [1330, 1390, 1470, 1540, 2590, 3900, 10180]          # bin, site geneli sayfa görüntüleme (içerik × ~1,27)
PV_ONCE = [2150, 2210, 2290, 2360, 2380, 2410, 2430]       # 10–16.11
pv, pv0 = sum(PV) * 1000, sum(PV_ONCE) * 1000             # 22,4 Mn · 16,23 Mn
KULLANICI, KULLANICI0 = 5_840_000, 4_520_000
OTURUM, OTURUM0 = 9_720_000, 7_310_000
SURE, SURE0 = 161, 172
CIKMA, CIKMA0 = 41.8, 44.6

def deg(a, b): return (a - b) / b * 100

KANAL = [  # ad, ikon, oturum, kullanıcı, süre sn, hemen çıkma, değişim, alt satır, modül
    ('Arama', 'fa-magnifying-glass', 3_940_000, 2_710_000, 156, 43.2, 24, 'Google, Discover, Google Haberler, Yandex, Bing', None),
    ('Doğrudan', 'fa-arrow-right-to-bracket', 2_580_000, 1_490_000, 192, 36.8, 19, 'Adres yazarak, yer imi, uygulama açılışı', None),
    ('Sosyal', 'fa-share-nodes', 1_460_000, 1_120_000, 108, 55.4, 61, 'X, Facebook, WhatsApp, Instagram, TikTok, YouTube Shorts ve diğerleri', None),
    ('Yönlendiren', 'fa-link', 1_080_000, 790_000, 125, 47.9, 35, 'Haber toplayıcılar, forumlar, Ekşi Sözlük, Vikipedi', None),
    ('Bildirim', 'fa-bell', 568_400, 402_100, 142, 39.5, 88, 'Telefon ve web bildirimi · 18 gönderim', 'etkilesim'),
    ('Bülten', 'fa-envelope-open-text', 91_600, 38_400, 245, 28.1, 6, '6 bülten · 48.620 abone', 'etkilesim'),
]
assert abs(sum(k[2] for k in KANAL) - OTURUM) < 1
ARAMA = [('Google Arama', 2_460_000), ('Discover', 1_080_000), ('Google Haberler', 290_000), ('Yandex', 70_000), ('Bing', 40_000)]
SOSYAL = [('X', 520_000), ('Facebook', 380_000), ('WhatsApp', 240_000), ('Instagram', 210_000), ('Telegram', 70_000), ('LinkedIn', 40_000)]
assert sum(x[1] for x in ARAMA) == KANAL[0][2] and sum(x[1] for x in SOSYAL) == KANAL[2][2]

# public sözlükten (araclar/ornek_veri.json, 17–23.11 en çok görüntülenen) — başlık, bölüm › alt konu, yazar, görüntülenme, okuma
ICERIK = [
    ("Marmara'da yoğun kar yağışı: gelişmeler dakika dakika", 'Gündem › Toplum · Mehmet Koçak', 64_300, 228, 71),
    ("İstanbul Valiliği: okullar 24 Kasım'da da tatil", 'Gündem › İstanbul · Sibel Arslan', 52_100, 64, 78),
    ('Kar yağışı nedeniyle okulların tatil edildiği iller listesi güncellendi', 'Gündem · Mehmet Koçak', 45_600, 118, 66),
    ('Kar nedeniyle okulların tatil edildiği iller', 'Gündem · Mehmet Koçak', 45_600, 97, 69),
    ('ÖSYM 2027 sınav takvimini yayımladı', 'Kampüs › Eğitim ve Sınavlar · Selin Koç', 42_700, 176, 58),
    ('BM İklim Konferansı kapanış oturumu', 'Keşfet › İklim · Ozan Er', 41_500, 254, 47),
    ("Marmara'da kar yağışı nedeniyle 14 ilde okullar tatil edildi", 'Gündem › Toplum · Mehmet Koçak', 41_200, 121, 63),
    ('Asgari ücret nasıl belirleniyor? Komisyonun işleyişi 6 dakikada', 'Finans › Çalışma Hayatı · Video · Elif Aras', 38_200, 262, 52),
    ('Benzine 1,20 liralık indirim pompaya yansıdı', 'Finans · Elif Aras', 31_700, 84, 61),
]
ANA_SAYFA = 2_960_000
GRUP = [('İçerik', 17_550_000), ('Ana sayfa', ANA_SAYFA), ('Kategori', 1_120_000), ('Arama ve etiket', 410_000), ('Diğer', 360_000)]
assert sum(g[1] for g in GRUP) == pv, (sum(g[1] for g in GRUP), pv)
KATEGORI = [('Keşfet', 3.68), ('Gündem', 2.80), ('Spor', 2.28), ('Finans', 2.20), ('Savunma', 1.97), ('Dünya', 1.67), ('Kampüs', 1.39), ('Kadın', 1.32)]

YAS = [('18–24', 14.2), ('25–34', 24.8), ('35–44', 23.6), ('45–54', 18.1), ('55–64', 11.9), ('65+', 7.4)]
CINSIYET = [('Erkek', 56.4), ('Kadın', 43.6)]
IL = [('İstanbul', 22.8, 196), ('Ankara', 8.9, 171), ('İzmir', 6.1, 165), ('Bursa', 3.7, 158), ('Antalya', 3.1, 149), ('Kocaeli', 2.6, 162),
      ]
DIGER_IL, YURTDISI = 46.4, 6.4
assert abs(sum(x[1] for x in IL) + DIGER_IL + YURTDISI - 100) < 0.05

CIHAZ = [('Telefon', 72.4), ('Masaüstü', 23.9), ('Tablet', 3.7)]
OS = [('Android', 48.6), ('iOS', 24.9), ('Windows', 19.2), ('macOS', 4.3), ('Diğer', 3.0)]
TARAYICI = [('Chrome', 'fa-chrome', 51.8, 158, 42.6, 'Android %71 · masaüstü %29'), ('Safari', 'fa-safari', 21.4, 167, 40.1, 'iOS %88 · macOS %12'),
            ('Dada Haber uygulaması', None, 12.6, 214, 31.2, 'uygulama içi okuma · Android %58 · iOS %42'), ('Samsung Internet', None, 6.2, 139, 47.8, 'Android'),
            ('Edge', 'fa-edge', 4.1, 176, 44.9, 'Windows %94'), ('Opera', 'fa-opera', 1.6, 131, 49.3, 'Android %61 · masaüstü %39'),
            ('Firefox', 'fa-firefox-browser', 1.3, 149, 46.2, 'Windows %72'), ('Diğer', None, 1.0, 102, 58.4, 'Yandex, UC, DuckDuckGo')]
assert abs(sum(x[2] for x in TARAYICI) - 100) < 0.05 and abs(sum(x[1] for x in OS) - 100) < 0.05

CANLI = [2940, 3010, 3120, 3260, 3390, 3482]
CANLI_ET = ['15.40', '15.45', '15.50', '15.55', '16.00', '16.05']
SIMDI = [  # başlık, alt, şu an, ana kaynak
    ("İstanbul Valiliği: okullar 24 Kasım'da da tatil", 'Gündem › İstanbul · 16.05', 612, 'Bildirim'),
    ("Marmara'da yoğun kar yağışı: gelişmeler dakika dakika", 'Gündem › Toplum · canlı', 488, 'Arama'),
    ('Kar yağışı nedeniyle okulların tatil edildiği iller listesi güncellendi', 'Gündem · 09.10', 341, 'Arama'),
    ('Ana sayfa', 'dadahaber.com', 296, 'Doğrudan'),
    ("AB dışişleri bakanları Brüksel'de genişleme gündemini ele aldı", 'Dünya · 16.05', 118, 'Sosyal'),
]

# reklam: bugünkü gösterimler Reklam alanları ekranından (moduller/etkilesim/reklam.html), 7 güne trafik eğrisiyle yayılır
RK_GUN = [170, 178, 188, 197, 331, 498, 1300]  # bin
ft7 = sum(RK_GUN) / 1300
ft4 = sum(RK_GUN[3:]) / 1300
REKLAM = [  # ad, alt, gösterim, TO, görünürlük
    ('Üst bant · Ad Manager', 'Üst bant · 970×250 / 320×100 · Google Ad Manager', 412_300 * ft7, 0.21, 72),
    ('Haber içi · AdSense', 'Haber içi · 728×90 / 320×100 · Google AdSense', 298_100 * ft7, 0.34, 64),
    ('Liste arası · Ad Manager', 'Liste arası · 300×250 · Google Ad Manager', 268_900 * ft7, 0.18, 58),
    ('Kış lastiği kampanyası', 'Haber içi · Sponsorlu görsel · Yol Lastik · 20.11’den beri', 223_300 * ft4, 0.62, 66),
    ('Yan sütun · AdSense', 'Yan sütun · 300×600 · yalnız masaüstü · Google AdSense', 96_200 * ft7, 0.27, 81),
    ('Kitap günleri', 'Haber içi · Sponsorlu görsel · İstanbul Kitap Günleri · 17.11’de bitti', 61_400, 0.48, 63),
]
rk_gos = sum(r[2] for r in REKLAM)
rk_tik = sum(r[2] * r[3] / 100 for r in REKLAM)
rk_gor = sum(r[2] * r[4] for r in REKLAM) / rk_gos
sp = [r for r in REKLAM if 'Sponsorlu' in r[1]]
sp_to = sum(r[2] * r[3] for r in sp) / sum(r[2] for r in sp)
ALAN = [('Üst bant', 412_300 * ft7), ('Haber içi', 298_100 * ft7 + 223_300 * ft4 + 61_400), ('Liste arası', 268_900 * ft7), ('Yan sütun', 96_200 * ft7)]

# ---------------------------------------------------------------- parçalar
def kpi(ikon, sayi, ad, delta, yon='flat', ton='', dikon=None):
    dikon = dikon or {'up': 'fa-arrow-trend-up', 'down': 'fa-arrow-trend-down', 'flat': 'fa-equals'}[yon]
    return (f'<div class="kpi-card{" " + ton if ton else ""}"><div class="kpi-ico">{i(ikon)}</div><div><div class="kpi-num">{sayi}</div>'
            f'<div class="kpi-lbl">{ad}</div><div class="kpi-delta {yon}">{i(dikon)}{delta}</div></div></div>')

def sutun(ad, veri, bicim):
    mx = max(v for _, v in veri)
    hucre = ''.join(f'<div><b>{bicim(v)}</b><span class="ks-cubuk" style="--h:{round(v / mx * 100)}%"></span><small>{e(a)}</small></div>' for a, v in veri)
    return f'<div class="kb-sutun-grafik" role="img" aria-label="{e(ad)}: {e(", ".join(a + " " + bicim(v) for a, v in veri))}">{hucre}</div>'

def baslik(ikon, ad, ek):
    return f'<div class="form-sec-tt">{i(ikon)}{ad}<span class="fs-ek">{ek}</span></div>'

def bolum_bas(ikon, ad, ek):
    return f'<div class="pc-head"><h2 class="pc-title">{i(ikon)}{ad}</h2><span class="pstat off">{ek}</span></div>'

def hucre_ad(ad, alt, ikon='fa-file-lines', ikon_cls='fa-solid'):
    return (f'<td class="kb-ana"><div class="rcp-cell"><div class="rcp-id"><div class="rcp-name" title="{e(ad)}">{e(ad)}</div>'
            + (f'<div class="rcp-by">{i(ikon, ikon_cls)}{e(alt)}</div>' if alt else '') + '</div></div></td>')

def pay(v, ond=1):
    return f'<td class="say">{yuzde(v, ond)}</td>'  # yatay çubuk bileşeni gelince pay çubuğu buraya (lead'e bildirildi)

def degisim(v):
    return f'<td class="say kb-gizle-t">{"+" if v >= 0 else "−"}%{tr_sayi(abs(v))}</td>'

def tablo(bas, satirlar):
    return f'<div class="ptable-wrap"><table class="ptable"><thead><tr>{bas}</tr></thead><tbody>{"".join(satirlar)}</tbody></table></div>'

# ---------------------------------------------------------------- sekmeler
def kisa1(v): return tr_sayi(v / 1e6, 1) + ' Mn' if v < 1e7 else tr_sayi(v / 1e6) + ' Mn'

def halka(ad, veri, orta, orta_ad):
    return (f'<div class="kb-halka" data-ad="{e(ad)}" data-degerler="{",".join(f"{v:g}" for _, v in veri)}" '
            f'data-etiketler="{e(",".join(a for a, _ in veri))}" data-orta="{orta}" data-orta-ad="{e(orta_ad)}"></div>')

def yatay(ad, veri, ikonlar=None):
    ik = f' data-ikonlar="{",".join(ikonlar)}"' if ikonlar else ''
    return (f'<div class="kb-yatay-cubuk" aria-label="{e(ad)}" data-bicim="kisa" data-degerler="{",".join(str(int(round(v))) for _, v in veri)}" '
            f'data-etiketler="{e(",".join(a for a, _ in veri))}"{ik}></div>')

def sol_sag(sol, sag, sol_modul=''):
    m = f' data-modul="{sol_modul}"' if sol_modul else ''
    return f'<div class="dash-2"><div{m}>{sol}</div><div>{sag}</div></div>'

CANLI30 = [2880, 2905, 2897, 2931, 2940, 2958, 2949, 2987, 3010, 3004, 3036, 3051, 3072, 3120, 3108, 3141, 3166, 3190, 3234, 3260,
           3248, 3281, 3310, 3352, 3390, 3402, 3421, 3447, 3466, 3482]
d_k, d_o, d_p = deg(KULLANICI, KULLANICI0), deg(OTURUM, OTURUM0), deg(pv, pv0)
genel = (
    '<div class="sa-form-panel" id="spGenel" role="tabpanel"><div class="pc-body">'
    '<div class="kpi-grid k5">'
    + kpi('fa-users', kisa(KULLANICI), 'Kullanıcı', f'+%{tr_sayi(d_k)} · %58’i yeni', 'up', 'info')
    + kpi('fa-arrow-right-to-bracket', kisa(OTURUM), 'Oturum', f'+%{tr_sayi(d_o)} önceki 7 gün', 'up')
    + kpi('fa-eye', kisa(pv), 'Sayfa görüntüleme', f'+%{tr_sayi(d_p)} · oturumda {tr_sayi(pv / OTURUM, 1)}', 'up', 'ok')
    + kpi('fa-stopwatch', sure(SURE), 'Ortalama oturum süresi', f'−{SURE0 - SURE} sn önceki 7 gün', 'down')
    + kpi('fa-person-walking-arrow-right', yuzde(CIKMA), 'Hemen çıkma', f'−{tr_sayi(CIKMA0 - CIKMA, 1)} puan (iyi)', 'up', '', 'fa-arrow-trend-down')
    + '</div>'
    + sol_sag(
        baslik('fa-chart-line', 'Günlük sayfa görüntüleme', f'bin · bu dönem {kisa(pv)} · önceki {kisa(pv0)}')
        + f'<div class="kb-cizgi" data-ad="Bu Dönem" data-karsi-ad="Önceki Dönem" data-degerler="{",".join(map(str, PV))}" data-karsi="{",".join(map(str, PV_ONCE))}" data-etiketler="{GUN}"></div>',
        baslik('fa-signal', 'Şu an sitede', 'son 30 dakika · 16.05')
        + kpi('fa-signal', tr_sayi(CANLI30[-1]), 'Okur', '+%14 son 1 saat', 'up', 'ok')
        + '<div class="kb-sutun-grafik is-mini kb-ust-bosluk" role="img" aria-label="Son 30 dakikada dakika dakika sitedeki okur: '
        + f'{tr_sayi(CANLI30[0])} ile {tr_sayi(CANLI30[-1])} arası">'
        + ''.join(f'<div><b>{tr_sayi(v)}</b><span class="ks-cubuk" style="--h:{round(v / max(CANLI30) * 100)}%"></span><small></small></div>' for v in CANLI30)
        + '</div>')
    + '</div>'
    + bolum_bas('fa-bolt', 'Şu an en çok okunan', 'son 30 dakika · 16.05')
    + tablo('<th class="kb-ana">Sayfa</th><th class="say">Şu an</th><th class="kb-gizle-m">Ana kaynak</th><th class="say kb-gizle-t">Okurların payı</th>',
            [f'<tr>{hucre_ad(a, b, "fa-house" if a == "Ana sayfa" else "fa-newspaper")}<td class="say">{tr_sayi(n)}</td><td class="kb-gizle-m">{k}</td>'
             f'<td class="say kb-gizle-t">{yuzde(n / CANLI30[-1] * 100)}</td></tr>' for a, b, n, k in SIMDI])
    + '</div>')

# sosyal mecralar: ad ve sıra sosyal-medya.ayarlar.platformlar kaydından (yalnız açık olanlar); WhatsApp paylaşımı ve diğerleri kayıt dışı
_kayit = json.load(open(KOK + '/moduller.json', encoding='utf-8'))
_kayit = _kayit['moduller'] if isinstance(_kayit, dict) else _kayit
PLATFORM = [p for p in [x for x in _kayit if x.get('id') == 'sosyal-medya'][0]['ayarlar']['platformlar'] if p.get('acik')]
SOSYAL_OTURUM = {'x': 420_000, 'facebook': 310_000, 'instagram': 120_000, 'instagram-reels': 95_000, 'tiktok': 88_000, 'youtube-shorts': 72_000,
                 'telegram': 60_000, 'linkedin': 38_000, 'threads': 14_000, 'bluesky': 6_000}
SOSYAL_IKON = {p['ad']: p.get('ikon', 'fa-solid fa-share-nodes') for p in PLATFORM}
SOSYAL_IKON.update({'WhatsApp paylaşımı': 'fa-brands fa-whatsapp', 'Diğer sosyal ağlar': 'fa-solid fa-share-nodes'})
SOSYAL_ML = sorted([(p['ad'], SOSYAL_OTURUM.get(p['id'], 0)) for p in PLATFORM] + [('WhatsApp paylaşımı', 200_000)], key=lambda z: -z[1])
SOSYAL_ML.append(('Diğer sosyal ağlar', KANAL[2][2] - sum(v for _, v in SOSYAL_ML)))
assert SOSYAL_ML[-1][1] > 0
kaynak = (
    '<div class="sa-form-panel" id="spKaynak" role="tabpanel" hidden><div class="pc-body">'
    + sol_sag(
        baslik('fa-share-nodes', 'Sosyal mecralar', f'oturum · {len(PLATFORM)} mecra · toplam {kisa(KANAL[2][2])}') + yatay('Sosyal mecraya göre oturum', SOSYAL_ML, [SOSYAL_IKON[a] for a, _ in SOSYAL_ML]),
        baslik('fa-chart-pie', 'Kanal payı', 'oturum') + halka('Kanala göre oturum payı', [(k[0], k[2]) for k in KANAL], kisa(OTURUM), 'oturum'))
    + '</div>'
    + bolum_bas('fa-route', 'Kanal dökümü', f'6 kanal · {kisa(OTURUM)} oturum')
    + tablo('<th class="kb-ana">Kanal</th><th class="say">Oturum</th>'
            '<th class="say kb-gizle-m">Kullanıcı</th><th class="say kb-gizle-t">Ort. süre</th><th class="say kb-gizle-t">Hemen çıkma</th><th class="say">Değişim</th>',
            [f'<tr{" data-modul=" + chr(34) + m + chr(34) if m else ""}>{hucre_ad(a, alt, ik)}<td class="say">{kisa(o)}</td>'
             f'<td class="say kb-gizle-m">{kisa(k)}</td><td class="say kb-gizle-t">{sure(s)}</td><td class="say kb-gizle-t">{yuzde(c)}</td>'
             f'<td class="say">+%{tr_sayi(dg)}</td></tr>'
             for a, ik, o, k, s, c, dg, alt, m in KANAL])
    + '</div>')

sayfa_sat = [f'<tr>{hucre_ad("Ana sayfa", "dadahaber.com", "fa-house")}<td class="say">{kisa(ANA_SAYFA)}</td><td class="say kb-gizle-m">{kisa(ANA_SAYFA * 0.31)}</td>'
             f'<td class="say kb-gizle-t">48 sn</td><td class="say kb-gizle-t">%38,4</td></tr>']
sayfa_sat += [f'<tr>{hucre_ad(a, b, "fa-newspaper")}<td class="say">{kisa(v)}</td><td class="say kb-gizle-m">{kisa(v * 0.82)}</td>'
              f'<td class="say kb-gizle-t">{sure(s)}</td><td class="say kb-gizle-t">%{g}</td></tr>' for a, b, v, s, g in ICERIK[:7]]
sayfalar = (
    '<div class="sa-form-panel" id="spSayfa" role="tabpanel" hidden><div class="pc-body">'
    + sol_sag(
        baslik('fa-sitemap', 'Kategoriye göre', '8 ana kategori · köşe yazıları hariç') + yatay('Kategoriye göre içerik görüntüleme', [(a, v * 1e6) for a, v in KATEGORI]),
        baslik('fa-layer-group', 'Sayfa grubu', 'görüntüleme payı') + halka('Sayfa grubuna göre görüntüleme payı', GRUP, kisa(pv), 'görüntüleme'),
        'haberler')
    + '</div>'
    + bolum_bas('fa-fire', 'En çok bakılan sayfalar', 'ilk 8 · sayfa görüntüleme')
    + tablo('<th class="kb-ana">Sayfa</th><th class="say">Görüntüleme</th><th class="say kb-gizle-m">Kullanıcı</th><th class="say kb-gizle-t">Ort. süre</th>'
            '<th class="say kb-gizle-t" title="Oturumun bu sayfayla başladığı görüntülemelerin payı">Giriş sayfası</th>', sayfa_sat)
    + '</div>')

IL_LISTE = [(a, KULLANICI * p / 100) for a, p, _ in IL] + [('Diğer 75 il', KULLANICI * DIGER_IL / 100), ('Yurt dışı', KULLANICI * YURTDISI / 100)]
yd = KULLANICI * YURTDISI / 100
ULKE = [('Almanya', 111_000), ('Hollanda', 46_700), ('ABD', 35_000), ('Azerbaycan', 29_200), ('KKTC', 29_200), ('İngiltere', 23_400)]
ULKE.append(('Diğer 35 ülke', yd - sum(v for _, v in ULKE)))
kitle = (
    '<div class="sa-form-panel" id="spKitle" role="tabpanel" hidden><div class="pc-body">'
    '<div class="kb-bant bilgi">' + i('fa-user-shield') + '<span><b>Yaş ve cinsiyet tahminidir</b> (Google sinyalleri, kullanıcıların %37’si). '
    'Bütün veriler toplu ve anonimdir; 50 kullanıcıdan küçük gruplar gösterilmez.</span></div>'
    + sol_sag(baslik('fa-cake-candles', 'Yaş', 'kullanıcı payı') + sutun('Yaşa göre kullanıcı payı', YAS, yuzde),
              baslik('fa-venus-mars', 'Cinsiyet', 'kullanıcı payı') + halka('Cinsiyete göre kullanıcı payı', CINSIYET, kisa(KULLANICI * 0.37), 'tahmini'))
    + '<div class="kb-ust-bosluk">'
    + sol_sag(baslik('fa-map-location-dot', 'İl', f'kullanıcı · toplam {kisa(KULLANICI)}') + yatay('İle göre kullanıcı', IL_LISTE),
              baslik('fa-earth-europe', 'Yurt dışı', f'kullanıcı · 41 ülke · {kisa(yd)}') + yatay('Ülkeye göre yurt dışı kullanıcı', ULKE))
    + '</div></div></div>')

tar_sat = [f'<tr>{hucre_ad(a, alt, ik or ("fa-mobile-screen" if a.startswith("Dada") else "fa-globe"), "fa-brands" if ik else "fa-solid")}'
           f'<td class="say">{kisa(OTURUM * p / 100)}</td><td class="say kb-gizle-t">{sure(s)}</td><td class="say kb-gizle-t">{yuzde(c)}</td></tr>'
           for a, ik, p, s, c, alt in TARAYICI]
cihaz = (
    '<div class="sa-form-panel" id="spCihaz" role="tabpanel" hidden><div class="pc-body">'
    + sol_sag(baslik('fa-desktop', 'İşletim sistemi', 'oturum') + yatay('İşletim sistemine göre oturum', [(a, OTURUM * p / 100) for a, p in OS]),
              baslik('fa-mobile-screen', 'Cihaz türü', 'oturum payı') + halka('Cihaz türüne göre oturum payı', CIHAZ, kisa(OTURUM), 'oturum'))
    + '</div>'
    + bolum_bas('fa-window-maximize', 'Tarayıcı', f'{kisa(OTURUM)} oturum')
    + tablo('<th class="kb-ana">Tarayıcı</th><th class="say">Oturum</th><th class="say kb-gizle-t">Ort. süre</th><th class="say kb-gizle-t">Hemen çıkma</th>', tar_sat)
    + '</div>')

RK_ONCE = [148, 152, 155, 158, 160, 163, 166]
rk_sat = [f'<tr>{hucre_ad(a, b, "fa-handshake" if "Sponsorlu" in b else "fa-rectangle-ad")}<td class="say">{kisa(g)}</td><td class="say">{tr_sayi(g * t / 100)}</td>'
          f'<td class="say">{yuzde(t, 2)}</td><td class="say kb-gizle-m">%{v}</td></tr>' for a, b, g, t, v in REKLAM]
reklam = (
    '<div class="sa-form-panel" id="spReklam" role="tabpanel" hidden data-modul="etkilesim" data-sayfa-gerek="etkilesim.reklam"><div class="pc-body">'
    '<div class="kpi-grid">'
    + kpi('fa-rectangle-ad', kisa(rk_gos), 'Gösterim', f'+%{tr_sayi(deg(sum(RK_GUN), sum(RK_ONCE)))} · bugün {kisa(1_300_000)}', 'up', 'info')
    + kpi('fa-arrow-pointer', tr_sayi(rk_tik), 'Tıklama', '+%31 önceki 7 gün', 'up')
    + kpi('fa-percent', yuzde(rk_tik / rk_gos * 100, 2), 'Tıklama oranı', f'sponsorlu görselde {yuzde(sp_to, 2)}', 'flat', 'ok', 'fa-handshake')
    + kpi('fa-eye', yuzde(rk_gor, 0), 'Görünür gösterim', 'en az yarısı 1 sn ekranda', 'flat', '', 'fa-circle-info')
    + '</div>'
    + sol_sag(baslik('fa-chart-line', 'Günlük gösterim', 'bin · bütün alanlar')
              + f'<div class="kb-cizgi" data-ad="Bu Dönem" data-karsi-ad="Önceki Dönem" data-degerler="{",".join(map(str, RK_GUN))}" data-karsi="{",".join(map(str, RK_ONCE))}" data-etiketler="{GUN}"></div>',
              baslik('fa-table-cells-large', 'Alana göre gösterim', 'Manşet Altı ve Mobil Alt Bant boş') + halka('Reklam alanına göre gösterim payı', ALAN, kisa(rk_gos), 'gösterim'))
    + '</div>'
    + bolum_bas('fa-bullhorn', 'Reklam dökümü', '6 reklam · Ad Manager ve sponsorlu')
    + tablo('<th class="kb-ana">Reklam</th><th class="say">Gösterim</th><th class="say">Tıklama</th><th class="say">TO</th><th class="say kb-gizle-m">Görünürlük</th>', rk_sat)
    + '</div>')

# ---------------------------------------------------------------- tarih aralığı ve seçimler
def aralik(p):
    return ('<div class="kb-aralik"><div class="ka-hazir" role="group" aria-label="Hazır aralık"><button type="button" data-aralik="bugun">Bugün</button>'
            '<button type="button" data-aralik="7" class="is-on">Son 7 gün</button><button type="button" data-aralik="30">Son 30 gün</button>'
            '<button type="button" data-aralik="ay">Bu ay</button><button type="button" data-aralik="ozel">Özel</button></div>'
            f'<div class="kb-tarih-sec" id="{p}1" data-saatsiz><button type="button" class="kb-tarih-btn" data-acilir="{p}1m" aria-expanded="false" aria-haspopup="dialog" aria-label="Başlangıç tarihi">{i("fa-calendar-days")}<span class="kt-deger"></span></button><div class="pnl-menu kb-tarih-menu" id="{p}1m" role="dialog" aria-label="Başlangıç tarihi"></div></div>'
            '<span class="ka-tire">–</span>'
            f'<div class="kb-tarih-sec" id="{p}2" data-saatsiz><button type="button" class="kb-tarih-btn" data-acilir="{p}2m" aria-expanded="false" aria-haspopup="dialog" aria-label="Bitiş tarihi">{i("fa-calendar-days")}<span class="kt-deger"></span></button><div class="pnl-menu kb-tarih-menu" id="{p}2m" role="dialog" aria-label="Bitiş tarihi"></div></div></div>')

def secim(mid, etk, secenekler, bos, ara=None, sec=None):
    """secenekler: [(deger, ad, alt)]; sec: seçili değer"""
    dolu = sec is not None
    ad = next((a for d, a, _ in secenekler if d == sec), bos)
    ara_html = f'<div class="kb-secim-ara">{i("fa-magnifying-glass")}<input type="search" placeholder="{ara}" aria-label="{ara}"></div>' if ara else ''
    liste = ''.join(f'<button type="button" data-deger="{e(d)}" data-ad="{e(a)}"{" class=" + chr(34) + "is-sec" + chr(34) if d == sec and d else ""}>{e(a)}'
                    f'{"<span class=" + chr(34) + "ks-alt" + chr(34) + ">" + e(alt) + "</span>" if alt else ""}</button>' for d, a, alt in secenekler)
    return (f'<div class="kb-secim{" is-dolu" if dolu and sec else ""}"{" data-deger=" + chr(34) + e(sec) + chr(34) if dolu and sec else ""} data-bos="{e(bos)}">'
            f'<button type="button" class="kb-secim-btn" data-acilir="{mid}" aria-expanded="false" aria-haspopup="listbox">'
            f'{"<span class=" + chr(34) + "ks-etk" + chr(34) + ">" + etk + "</span>" if etk else ""}<span class="ks-deger">{e(ad)}</span>{i("fa-chevron-down")}</button>'
            f'<div class="pnl-menu kb-secim-menu" id="{mid}">{ara_html}<div class="kb-secim-liste" role="listbox">{liste}</div></div></div>')

suzgec = ('<div class="filter-bar">' + aralik('spA')
          + secim('spKars', 'Karşılaştır:', [('onceki', 'Önceki dönem', '10.11–16.11.2026'), ('gecen-yil', 'Geçen yılın aynı dönemi', '17.11–23.11.2025'), ('', 'Karşılaştırma yok', '')], 'Önceki dönem')
          + secim('spAkis', 'Akış:', [('', 'Web ve uygulama', ''), ('web', 'Web', 'dadahaber.com'), ('android', 'Android uygulaması', ''), ('ios', 'iOS uygulaması', '')], 'Web ve uygulama')
          + '</div>')

def sekme(pid, ikon, ad, on=False, ek=''):
    return (f'<button type="button" class="sa-form-tab{" is-on" if on else ""}" role="tab" aria-selected="{"true" if on else "false"}" data-panel="{pid}"{ek}>{i(ikon)}{ad}</button>')

sekmeler = ('<div class="sa-form-tabs" role="tablist" aria-label="Site istatistikleri bölümleri">'
            + sekme('spGenel', 'fa-gauge-high', 'Genel bakış', True) + sekme('spKaynak', 'fa-route', 'Kaynaklar') + sekme('spSayfa', 'fa-file-lines', 'Sayfalar')
            + sekme('spKitle', 'fa-users', 'Kitle') + sekme('spCihaz', 'fa-mobile-screen', 'Cihaz') + sekme('spReklam', 'fa-rectangle-ad', 'Reklam', ek=' data-modul="etkilesim" data-sayfa-gerek="etkilesim.reklam"')
            + '</div>')

AN = 'data-hedef="entegrasyonlar.ayar" data-hedef-ek="?id=analytics" href="../entegrasyonlar/ayar.html?id=analytics"'
main = f'''<main class="pnl-main" id="icerik">
  <div class="pnl-page-head">
    <div>
      <h1>Site istatistikleri</h1>
      <div class="ph-sub" data-durum-gizle="hata yok">Okur ve trafik · Google Analytics 4 · son eşitleme 23.11.2026 16.05 · son 48 saat kesinleşmez</div>
      <div class="ph-sub" data-durum-goster="hata" hidden>Okur ve trafik · Google Analytics 4 · son eşitleme 23.11.2026 15.40 · bağlantı hatalı</div>
      <div class="ph-sub" data-durum-goster="yok" hidden>Okur ve trafik · Google Analytics 4 bağlı değil</div>
    </div>
    <div class="ph-actions" data-durum-gizle="yok">
      <a class="btn btn-ghost btn-sm" data-hedef="raporlar.disa-aktarim" href="disa-aktarim.html">{i("fa-folder-open")}Dışa aktarımlar</a>
      <button type="button" class="btn btn-ghost btn-sm" data-tanim="spDisa">{i("fa-file-export")}Dışa aktar</button>
      <button type="button" class="btn btn-acc btn-sm" data-tanim="spReklamveren" data-modul="etkilesim" data-sayfa-gerek="etkilesim.reklam">{i("fa-handshake")}Reklamveren raporu</button>
    </div>
  </div>

  <div class="kb-bant tehlike dash-row" data-durum-goster="hata" hidden>{i("fa-plug-circle-xmark")}<span><b>Analytics bağlantısı 15.40’tan beri hata veriyor:</b> erişim izninin süresi doldu. Sayılar 15.40’a kadardır; “Şu An Sitede” durdu. Bağlantı yenilenince eksik saatler kendiliğinden tamamlanır.</span><a class="btn btn-ghost btn-sm kb-bant-eylem" {AN}>{i("fa-plug")}Bağlantıya git</a></div>
  <div class="kb-bant uyari dash-row" data-durum-goster="yok" hidden>{i("fa-plug-circle-exclamation")}<span><b>Analytics bağlı değil.</b> Site istatistikleri Entegrasyonlar’daki Google Analytics 4 bağlantısından gelir; bağlantı kurulunca son 30 günün verisi birkaç saat içinde yüklenir.</span><a class="btn btn-ghost btn-sm kb-bant-eylem" {AN}>{i("fa-plug")}Bağlantıya git</a></div>

  <section class="pnl-card" data-sekmeli data-durum-gizle="yok" aria-label="Site istatistikleri">
    {sekmeler}
    {suzgec}
    {genel}
    {kaynak}
    {sayfalar}
    {kitle}
    {cihaz}
    {reklam}
  </section>

  <section class="pnl-card" data-durum-goster="yok" hidden aria-label="Veri yok">
    <div class="pnl-empty"><div class="pe-ico">{i("fa-chart-line")}</div><h2>Henüz istatistik yok</h2><p>Kullanıcı, oturum, trafik kaynakları, kitle ve reklam sayıları Analytics bağlantısı kurulunca burada görünür.</p></div>
  </section>
</main>
</div>
'''

# ---------------------------------------------------------------- dışa aktarım pencereleri (Dışa aktarımlar akışı: başlat → sıraya alındı → Dışa aktarımlar)
SINIR = f'<div class="kb-bant uyari">{i("fa-gauge-high")}<span><b>Sınır: dakikada 3, günde 20 dışa aktarım.</b> Bugün 6 / 20 kullanıldı. 90 günden uzun aralıklar sıraya alınır; hazırlanması birkaç dakika sürebilir.</span></div>'

def kart_sec(alan, ad, secenekler, metin):
    return (f'<div class="kb-kart-sec" data-alan-id="{alan}" data-zorunlu-metin="{metin}">'
            + ''.join(f'<label class="kb-secenek kb-secenek-kart"{ek}><input type="radio" name="{ad}"{" value=" + chr(34) + v + chr(34) if v else ""}{" data-ac=" + chr(34) + ac + chr(34) if ac else ""}{" checked" if c else ""}><span><b>{b}</b><small>{s}</small></span></label>'
                      for v, b, s, c, ac, ek in secenekler) + '</div>')

def kutular(alan, metin, ogeler):
    return (f'<div class="kb-secenek-grup" data-alan-id="{alan}" data-zorunlu-metin="{metin}">'
            + ''.join(f'<label class="kb-secenek"><input type="checkbox"{" checked" if c else ""}>{a}{"<span class=" + chr(34) + "ks-alt" + chr(34) + ">" + alt + "</span>" if alt else ""}</label>' for a, c, alt in ogeler) + '</div>')

disa = f'''<template id="spDisa" data-zorunlu-kayit="raporlar.disa-aktarim" data-baslik="Site istatistiklerini dışa aktar" data-alt="{_disa.BICIM_ALT}">
  {SINIR}
  <div class="kb-fs">
    <div class="kb-fs-tt">Aralık ve biçim</div>
    <div class="frow"><span class="flabel">Tarih aralığı</span>
      <div data-alan-id="aralik">{aralik("sdA")}</div>
      <span class="fhint">Sayfadaki aralıkla başlar; karşılaştırma dönemi dosyada ayrı sütundur.</span></div>
    {_disa.bicim("sdBicim", "sd", "Site İstatistikleri", "17.11–23.11.2026", ["Genel Bakış", "Kaynaklar", "Sayfalar", "Kitle", "Cihaz"], 9)}
  </div>
  <div class="kb-fs">
    <div class="kb-fs-tt">Bölümler</div>
    <div class="frow"><span class="flabel">Dosyaya girecek bölümler</span>
      {kutular("alanlar", "En az bir bölüm seçin", [("Genel bakış", True, ""), ("Kaynaklar", True, ""), ("Sayfalar", True, ""), ("Kitle", True, ""), ("Cihaz", True, ""), ("Önceki dönem", True, "")])}
      <span class="fhint">Sayfalar bölümü ilk 100 sayfayı, Önceki Dönem karşılaştırma sütununu ekler. Veriler toplu ve anonimdir; kişisel veri ya da IP dosyaya girmez.</span></div>
  </div>
  <div class="kb-kap-alt-cubuk">
    <button type="button" class="btn btn-acc btn-sm" data-sablon-ac="spDisaTamam" data-bildir-sonra="PDF hazırlanıyor; hazır olunca bildirim gelecek">{i("fa-file-export")}Başlat</button>
  </div>
</template>
<template id="spDisaTamam" data-baslik="Dışa aktarım hazırlanıyor" data-alt="Hazır olunca bildirim gelir">
  <div class="kb-fs">
    <div class="kb-fs-tt">Site istatistikleri · PDF · 17.11–23.11.2026</div>
    <div class="kb-ilerleme" style="--yuzde:8%"><span></span></div>
    <p class="fhint kb-ust-bosluk">Sırada 1. · yaklaşık 1 dakika · kapak ve 5 bölüm, 9 sayfa. Dosya 7 gün indirilebilir; denetim izine “Site İstatistikleri · PDF dışa aktarıldı” olarak yazılır.</p>
  </div>
  <div class="kb-kap-alt-cubuk">
    <a class="btn btn-acc btn-sm" data-hedef="raporlar.disa-aktarim" href="disa-aktarim.html">{i("fa-file-export")}Dışa aktarımlara git</a>
  </div>
</template>
'''

KAMPANYA = [('kis-lastigi', 'Kış lastiği · Yol Lastik', '20.11–30.11.2026'), ('kitap', 'Kitap günleri · İstanbul Kitap Günleri', 'bitti 17.11'),
            ('yilbasi', 'Yılbaşı · Kent Çarşı', '01.12’de başlıyor')]
ALANLAR = [('ust', 'Üst bant', '970×250 / 320×100'), ('manset', 'Manşet altı', 'boş'), ('liste', 'Liste arası', '300×250'), ('haber', 'Haber içi', '728×90 / 320×100'),
           ('yan', 'Yan sütun', '300×600'), ('mobil', 'Mobil alt bant', 'boş')]
reklamveren = f'''<template id="spReklamveren" data-sayfa-gerek="etkilesim.reklam" data-zorunlu-kayit="raporlar.disa-aktarim" data-baslik="Reklamveren raporu" data-alt="{_disa.BICIM_ALT}">
  {SINIR}
  <div class="kb-fs">
    <div class="kb-fs-tt">Rapor</div>
    <div class="frow"><span class="flabel">Rapor türü</span>
      {kart_sec("rapor", "srTur", [("kampanya", "Kampanya raporu", "Bir sponsorlu kampanyanın sonuçları", True, "srKampanya", ""), ("alan", "Alan raporu", "Bir reklam alanının gösterimi ve kitlesi · teklif için", False, "srAlan", "")], "Bir rapor türü seçin")}</div>
    <div class="frow" id="srKampanya"><span class="flabel">Kampanya</span>
      {secim("srKampSec", "", KAMPANYA, "Kampanya seçin", "Kampanya ya da reklamveren ara", "kis-lastigi")}
      <span class="fhint">Aralık kampanyanın tarihleriyle sınırlanır.</span></div>
    <div class="frow" id="srAlan" hidden><span class="flabel">Reklam alanı</span>
      {secim("srAlanSec", "", ALANLAR, "Alan seçin", "Alan ara", "haber")}</div>
  </div>
  <div class="kb-fs">
    <div class="kb-fs-tt">Aralık ve biçim</div>
    <div class="frow"><span class="flabel">Tarih aralığı</span>
      <div data-alan-id="aralik">{aralik("srA")}</div></div>
    {_disa.bicim("srBicim", "sr", "Reklamveren Raporu · Kış Lastiği", "20.11–23.11.2026", ["Gösterim", "Tıklama", "Görünürlük", "Güne Göre", "Cihaza Göre", "Kitle Özeti"], 7)}
  </div>
  <div class="kb-fs">
    <div class="kb-fs-tt">İçerik</div>
    <div class="frow"><span class="flabel">Rapora girecekler</span>
      {kutular("alanlar", "En az bir alan seçin", [("Gösterim", True, ""), ("Tıklama ve tıklama oranı", True, ""), ("Görünür gösterim", True, ""), ("Güne göre döküm", True, ""), ("Cihaza göre", True, ""), ("Kategoriye göre", False, ""), ("Kitle özeti", True, "toplu"), ("Site özeti", False, "")])}
      <span class="fhint">Rapor toplu sayılar taşır; kişisel veri, IP ve 50 kullanıcıdan küçük kitle grupları rapora girmez.</span></div>
  </div>
  <div class="kb-kap-alt-cubuk">
    <button type="button" class="btn btn-acc btn-sm" data-sablon-ac="spReklamTamam" data-bildir-sonra="Reklamveren raporu PDF hazırlanıyor; hazır olunca bildirim gelecek">{i("fa-file-export")}Başlat</button>
  </div>
</template>
<template id="spReklamTamam" data-sayfa-gerek="etkilesim.reklam" data-baslik="Reklamveren raporu hazırlanıyor" data-alt="Hazır olunca bildirim gelir">
  <div class="kb-fs">
    <div class="kb-fs-tt">Kış lastiği kampanyası · Yol Lastik · PDF · 20.11–23.11.2026</div>
    <div class="kb-ilerleme" style="--yuzde:12%"><span></span></div>
    <p class="fhint kb-ust-bosluk">Sırada 1. · yaklaşık 2 dakika · {kisa(REKLAM[3][2])} gösterim, 6 bölüm. Dosya 7 gün indirilebilir; bağlantıyı Dışa Aktarımlar’dan kopyalayıp reklamverene gönderebilirsiniz.</p>
  </div>
  <div class="kb-kap-alt-cubuk">
    <a class="btn btn-acc btn-sm" data-hedef="raporlar.disa-aktarim" href="disa-aktarim.html">{i("fa-file-export")}Dışa aktarımlara git</a>
  </div>
</template>
'''

# ---------------------------------------------------------------- birleştir
bas = src[:src.index('<main')]
bas = bas.replace('<title>Raporlar · ', '<title>Site istatistikleri · ').replace('<title>Sistem raporu · ', '<title>Site istatistikleri · ').replace('<title>Sistem Raporu · ', '<title>Site istatistikleri · ')
bas = re.sub(r'<body[^>]*>', '<body data-sayfa="raporlar.site">', bas, count=1)
son = src[src.index('<script src="../../cekirdek/js/kabuk.js'):]
yorum = ('\n<!-- SİTE İSTATİSTİKLERİ (raporlar.site): okur ve trafik verisi, kaynak Entegrasyonlar › Analytics (?durum=hata | yok).\n'
         '     Tek kart, altı sekme (?sekme=spGenel|spKaynak|spSayfa|spKitle|spCihaz|spReklam); her sekmede tek tablo. Reklam sekmesi ve\n'
         '     Reklamveren raporu Etkileşim modülüne bağlı (data-modul).\n'
         '     Sayılar birbiriyle tutarlı: 7 günlük görüntüleme Sistem raporuyla, bugünkü reklam gösterimi Reklam alanlarıyla aynı. -->\n')
out = bas.rstrip() + '\n' + yorum + main + disa + reklamveren + son
out = _yazim.isle(out, False)[0]  # panel yazım kuralı
open(KOK + '/cekirdek/raporlar/site.html', 'w', encoding='utf-8').write(out)
print('yazıldı', len(out), 'kullanıcı', kisa(KULLANICI), 'pv', kisa(pv), 'reklam', kisa(rk_gos), tr_sayi(rk_tik), yuzde(rk_tik / rk_gos * 100, 2), yuzde(rk_gor, 0))
