#!/usr/bin/env python3
"""Sistem Raporu › Sosyal Medya sekmesini (index.html #rpSosyal) yazar. Mecra adı, sırası ve ikonu kayıttan:
moduller.json → sosyal-medya.ayarlar.platformlar (yalnız açık olanlar). Hesap adı ve durumu Sosyal Medya Hesapları ekranıyla aynı.
Çalıştır: python3 -I cekirdek/raporlar/_sosyal_rapor.py ; ardından _yazim.py index.html ve menu_yaz --yalniz cekirdek/raporlar."""
import json, os, re, sys
KOK = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _yazim

kayit = json.load(open(KOK + '/moduller.json', encoding='utf-8'))
kayit = kayit['moduller'] if isinstance(kayit, dict) else kayit
PLATFORM = [p for p in [x for x in kayit if x.get('id') == 'sosyal-medya'][0]['ayarlar']['platformlar'] if p.get('acik')]

# 17–23.11.2026 · gönderi, erişim, etkileşim, siteye tıklama (None: bağlantısız), takipçi değişimi, hesap · durum
VERI = {
    'x':               (58, 1_120_000, 41_800, 18_400, 2140, '@dadahaber · Bağlı'),
    'facebook':        (34, 684_000, 22_100, 12_900, 860, 'Dada Haber · Bağlı'),
    'instagram':       (21, 742_000, 48_600, None, 3310, '@dadahaber · Bağlantı süresi doldu'),
    'linkedin':        (12, 96_400, 3_200, 2_100, 410, 'Dada Haber · Bağlı'),
    'telegram':        (21, 205_000, 1_900, 9_700, 1020, 'Dada Haber kanalı · Bağlı'),
    'threads':         (18, 64_200, 2_600, 1_100, 540, '@dadahaber · Bağlı'),
    'bluesky':         (14, 21_800, 900, 600, 230, '@dadahaber.bsky.social · Bağlı'),
    'youtube-shorts':  (9, 318_000, 14_200, 800, 1180, '@dadahaber · yalnız video · Bağlı'),
    'instagram-reels': (7, 426_000, 31_400, None, None, 'Instagram hesabıyla · bağlantı süresi doldu'),
    'tiktok':          (0, 0, 0, None, None, '@dadahaber · uygulama onayı bekliyor'),
}
GUN = [182, 196, 204, 221, 398, 612, 1034]  # önceki 5 mecranın günlük eğrisi, toplama ölçeklenir

def tr(v, o=1): return f'{v:,.{o}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
def kisa(v): return tr(v / 1e6, 2) + ' Mn' if v >= 1e6 else tr(v / 1e3, 1) + ' B'
def i(c): return f'<i class="{c}" aria-hidden="true"></i>'

sat = [(p, VERI.get(p['id'], (0, 0, 0, None, None, '—'))) for p in PLATFORM]
gon = sum(v[0] for _, v in sat); eri = sum(v[1] for _, v in sat); etk = sum(v[2] for _, v in sat); tik = sum(v[3] or 0 for _, v in sat)
yayinda = [p for p, v in sat if v[1] > 0]
bekleyen = [p['ad'] for p, v in sat if v[1] == 0]
olcek = eri / 1000 / sum(GUN); gunluk = [round(g * olcek) for g in GUN]

def kpi(ikon, sayi, ad, delta, yon='flat', ton='', dikon='fa-solid fa-equals'):
    return (f'<div class="kpi-card{" " + ton if ton else ""}"><div class="kpi-ico">{i("fa-solid " + ikon)}</div><div><div class="kpi-num">{sayi}</div>'
            f'<div class="kpi-lbl">{ad}</div><div class="kpi-delta {yon}">{i(dikon)}{delta}</div></div></div>')

satirlar = ''.join(
    f'<tr><td class="kb-ana"><div class="rcp-cell"><div class="rcp-id"><div class="rcp-name">{p["ad"]}</div><div class="rcp-by">{i(p.get("ikon", "fa-solid fa-share-nodes"))}{v[5]}</div></div></div></td>'
    f'<td class="say">{v[0] or "—"}</td><td class="say">{kisa(v[1]) if v[1] else "—"}</td><td class="say kb-gizle-m">{kisa(v[2]) if v[2] else "—"}</td>'
    f'<td class="say kb-gizle-t">{"%" + tr(v[2] / v[1] * 100) if v[1] else "—"}</td><td class="say">{kisa(v[3]) if v[3] else "—"}</td>'
    f'<td class="say kb-gizle-t">{"+" + tr(v[4], 0) if v[4] else "—"}</td></tr>' for p, v in sat)
yatay = sorted([(p, v[1]) for p, v in sat if v[1]], key=lambda z: -z[1])

panel = (
    '<div class="sa-form-panel" id="rpSosyal" role="tabpanel" hidden data-modul="sosyal-medya">'
    f'<div class="kb-bant uyari dash-row">{i("fa-solid fa-triangle-exclamation")}<span><b>Instagram bağlantısının süresi doldu (15.30).</b> Instagram ve Instagram Reels verileri 15.30’a kadardır; 17.00 gönderisi bekletiliyor. '
    + (f'{", ".join(bekleyen)} uygulama onayı bekliyor; henüz herkese açık gönderi yok.' if bekleyen else '') + '</span>'
    f'<a class="btn btn-ghost btn-sm kb-bant-eylem" data-hedef="sosyal-medya.hesaplar" href="../../moduller/sosyal-medya/hesaplar.html">{i("fa-solid fa-plug")}Hesabı Bağla</a></div>'
    '<div class="kpi-grid">'
    + kpi('fa-share-nodes', tr(gon, 0), 'Gönderi', f'{len(PLATFORM)} platform · {len(yayinda)} yayında', 'flat', 'ok', 'fa-solid fa-layer-group')
    + kpi('fa-users', kisa(eri), 'Erişim', '+%21 önceki 7 gün', 'up', 'info', 'fa-solid fa-arrow-trend-up')
    + kpi('fa-heart', '%' + tr(etk / eri * 100), 'Etkileşim Oranı', f'{kisa(etk)} etkileşim', dikon='fa-solid fa-hand-pointer')
    + kpi('fa-arrow-pointer', kisa(tik), 'Siteye Tıklama', 'Instagram bağlantısız', dikon='fa-solid fa-link')
    + '</div><div class="dash-2">'
    f'<section class="pnl-card"><div class="pc-head"><h2 class="pc-title">{i("fa-solid fa-chart-line")}Günlük Erişim</h2><span class="pstat off">Toplam {kisa(eri)}</span></div>'
    f'<div class="pc-body"><div class="kb-cizgi" data-ad="Günlük sosyal erişim (bin)" data-degerler="{",".join(map(str, gunluk))}" data-etiketler="17 Kas,18,19,20,21,22,23 Kas"></div></div></section>'
    f'<section class="pnl-card"><div class="pc-head"><h2 class="pc-title">{i("fa-solid fa-chart-bar")}Platforma Göre Erişim</h2><span class="pstat off">son 7 gün</span></div>'
    f'<div class="pc-body"><div class="kb-yatay-cubuk" aria-label="Platforma göre erişim" data-bicim="kisa" data-degerler="{",".join(str(v) for _, v in yatay)}" '
    f'data-etiketler="{",".join(p["ad"] for p, _ in yatay)}" data-ikonlar="{",".join(p.get("ikon", "fa-solid fa-share-nodes") for p, _ in yatay)}"></div></div></section></div>'
    f'<section class="pnl-card"><div class="pc-head"><h2 class="pc-title">{i("fa-solid fa-table-list")}Platform Dökümü</h2><span class="pstat off">son 7 gün · {len(PLATFORM)} platform</span></div>'
    '<div class="ptable-wrap"><table class="ptable"><thead><tr><th class="kb-ana">Platform</th><th class="say">Gönderi</th><th class="say">Erişim</th><th class="say kb-gizle-m">Etkileşim</th>'
    f'<th class="say kb-gizle-t">Oran</th><th class="say">Tıklama</th><th class="say kb-gizle-t">Takipçi</th></tr></thead><tbody>{satirlar}</tbody></table></div></section></div>')

p = KOK + '/cekirdek/raporlar/index.html'
s = open(p, encoding='utf-8').read()
a = s.index('<div class="sa-form-panel" id="rpSosyal"'); b = s.index('<div class="sa-form-panel"', a + 10)
s = s[:a] + _yazim.isle(panel, False)[0] + s[b:]
open(p, 'w', encoding='utf-8').write(s)
print('Sosyal Medya sekmesi:', len(PLATFORM), 'platform ·', gon, 'gönderi ·', kisa(eri), 'erişim ·', kisa(tik), 'tıklama')
