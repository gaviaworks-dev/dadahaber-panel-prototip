#!/usr/bin/env python3
"""Sistem Raporu'ndaki alt konu sayılarını tek kaynaktan yazar: public araclar/kategori.json (ağaç) +
moduller.json haberler.ayarlar.servis_sayfalari (servis sütunları/öğeleri alt konu değildir). Kullanım: kategori_say.py <panel kökü>"""
import json, re, sys
import os
KOK = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
k = json.load(open('/Users/gaviaworks/Developer/Projects/dadahaber-prototip/araclar/kategori.json', encoding='utf-8'))
m = json.load(open(KOK + '/moduller.json', encoding='utf-8'))
mods = m['moduller'] if isinstance(m, dict) else m
sv = [x for x in mods if x.get('id') == 'haberler'][0]['ayarlar']['servis_sayfalari']
SUT, OGE = set(sv['sutunlar']), set(sv['ogeler'])
say = {}
for b in k['basliklar']:
    say[b['ad']] = sum(1 for s in b['sutunlar'] if s['ad'] not in SUT for o in s['ogeler'] if o['ad'] not in OGE)
top = sum(say.values()); print(say, top)
p = KOK + '/cekirdek/raporlar/index.html'; s = open(p, encoding='utf-8').read()
s, n = re.subn(r'(<div class="kpi-lbl">Ana Kategori</div><div class="kpi-delta flat"><i class="fa-solid fa-layer-group" aria-hidden="true"></i>)\d+ alt konu', rf'\g<1>{top} alt konu', s); assert n == 1
s, n = re.subn(r'(<div class="kpi-num">)\d+(</div><div class="kpi-lbl">Ana Kategori)', rf'\g<1>{len(say)}\2', s); assert n == 1
for ad, v in say.items():
    s, n = re.subn(r'(<div class="rcp-name">' + re.escape(ad) + r'</div><div class="rcp-by"><i class="fa-solid fa-sitemap" aria-hidden="true"></i>)\d+ alt konu', rf'\g<1>{v} alt konu', s); assert n == 1, ad
s, n = re.subn(r'(<div class="kpi-num">)\d+(</div><div class="kpi-lbl">Alt Konu</div>)', rf'\g<1>{say["Spor"]}\2', s); assert n == 1
open(p, 'w', encoding='utf-8').write(s)
