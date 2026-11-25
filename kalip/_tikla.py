#!/usr/bin/env python3
"""Kalıp sunum sayfası · TIKLAMA DENETİMİ (Beyar, 25.11.2026): sayfadaki tıklanabilir her öğe gerçek tarayıcıda (headless Chrome)
tek tek tıklanır, beklenen değişiklik olmuş mu bakılır; her sekme × mecra birleşiminde taşma, ekrana sığmayan kart ve kaydırmada
titreme aranır. Beş genişlikte (1440, 1280, 1024, 768, 390) koşar.

Denenenler: şerit (her alternatif) · şerit okları · mecra düğmeleri · içerik sekmeleri · Güvenli Alan · açılır menüler ve
her seçenek (pasif seçenek gerekçeli mi) · Varsayılan · Bunu Seç · Hepsini Yan Yana Gör.
Tıklama gerçekçi yapılır: öğe görünür olmalı ve tıklama noktasında üstte o öğe bulunmalı (başka bir şeyin altında kalan düğme
"tıklanamaz" sayılır).

Kullanım:  python3 -I kalip/_tikla.py            (yerel)
           python3 -I kalip/_tikla.py --canli    (canlı adres: GitHub Pages'ten aynı kökenli vekil ile)
Çıkış kodu: 0 = hepsi geçti · 1 = kalan var. kalip/_olc.py sonunda bunu da çalıştırır.
"""
import concurrent.futures, shutil, tempfile, functools, html, http.server, json, os, re, socket, subprocess, sys, threading, urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
CANLI = "https://gaviaworks-dev.github.io/dadahaber-panel-prototip/"
GENISLIK = [1440, 1280, 1024, 768, 390]
if '--w' in sys.argv: GENISLIK = [int(sys.argv[sys.argv.index('--w') + 1])]

PROBE = open(sys.argv[sys.argv.index("--probe") + 1]).read() if "--probe" in sys.argv else ""
JS = r"""
(async function(){
const W = +new URLSearchParams(location.search).get('w'), F = document.getElementById('f');
const R = []; const ok = (ad, g, not) => R.push({ad: ad, g: !!g, not: g ? '' : (not || '')});
const bekle = ms => new Promise(r => setTimeout(r, ms));
try {
  for(let i = 0; i < 300; i++){ const dd = F.contentDocument; if(dd && dd.readyState === 'complete' && dd.querySelector('#kpSahne[data-alt]')) break; await bekle(100); }
  const w = F.contentWindow, d = F.contentDocument, HATA = [];
  w.addEventListener('error', e => HATA.push((e.message || '') + ' @' + (e.lineno || '')));
  if(w.document.fonts) await w.document.fonts.ready;
  /* test ortamı: headless sanal zamanda CSS geçişleri ve yumuşak kaydırma ilerlemez → kapatılır (sayfanın davranışı değişmez,
     yalnız animasyonsuz anında olur) */
  const st = d.createElement('style'); st.textContent = '*,*::before,*::after{transition:none!important;animation:none!important;scroll-behavior:auto!important}'; d.head.appendChild(st);
  ['scrollBy', 'scrollTo', 'scrollIntoView'].forEach(f => { const o = w.Element.prototype[f]; w.Element.prototype[f] = function(){ const g = Array.prototype.slice.call(arguments); if(g[0] && typeof g[0] === 'object' && g[0].behavior) g[0] = Object.assign({}, g[0], {behavior: 'auto'}); return o.apply(this, g); }; });
  await bekle(300);
  const S = d.getElementById('kpSahne'), V = JSON.parse(d.getElementById('kpVeri').textContent), K = d.getElementById('kpKontrol');
  const gor = el => !!el && el.getClientRects().length > 0 && w.getComputedStyle(el).visibility !== 'hidden';
  const panel = () => S.querySelector('.sa-form-panel:not([hidden])');
  const tikla = async (el) => {   /* gerçekçi tıklama: görünür ve noktada üstte olmalı */
    if(!gor(el)) return 'görünmüyor';
    el.scrollIntoView({block: 'nearest', inline: 'nearest'}); await bekle(30);
    const r = el.getBoundingClientRect(), x = Math.min(Math.max(r.left + Math.min(r.width / 2, 24), 1), w.innerWidth - 2), y = Math.min(Math.max(r.top + r.height / 2, 1), w.innerHeight - 2);
    const ust = d.elementFromPoint(x, y);
    if(!ust || !(ust === el || el.contains(ust) || ust.contains(el) && ust.closest('label') === ust)) return 'üstünde başka öğe: ' + (ust ? (ust.className || ust.tagName) : 'yok');
    ust.click(); await bekle(60); return '';
  };
  const yerlesim = (ad) => {      /* taşma, ekrana sığmayan kart */
    const de = d.documentElement, p = panel(), pr = p.getBoundingClientRect(), kh = K.getBoundingClientRect().height;
    ok(ad + ' · yatay taşma yok', de.scrollWidth <= w.innerWidth + 1, 'sayfa ' + de.scrollWidth + 'px > ' + w.innerWidth);
    let tas = [], dev = [];
    p.querySelectorAll('.kp-tuval').forEach(t => { if(!gor(t) || t.closest('[hidden]')) return; const r = t.getBoundingClientRect();
      if(r.right > pr.right + 1 || r.left < pr.left - 1) tas.push(t.dataset.tip || '?');
      if(r.height > w.innerHeight - 40 && t.dataset.bicim !== 'uzun') dev.push(Math.round(r.width) + '×' + Math.round(r.height)); });
    ok(ad + ' · kart panelden taşmıyor', !tas.length, tas.slice(0, 3).join(','));
    ok(ad + ' · kart ekrana sığıyor', !dev.length, dev.slice(0, 3).join(','));
  };

  /* sekme dar ekranda "Diğer" menüsüne taşınmış olabilir (çekirdek sekme davranışı): oradan açılır */
  const sekmeAc = async (t) => {
    if(gor(t)) return await tikla(t);
    const db = S.querySelector('.sa-diger-btn'); if(!gor(db)) return 'sekme de Diğer menüsü de görünmüyor';
    await bekle(120); /* çekirdek sekme satırı bir önceki seçimden sonra 0 ms gecikmeyle yeniden dizilir; insan hızında bekle */
    let h = await tikla(db); if(h) return 'Diğer: ' + h;
    const dm = d.getElementById(db.dataset.acilir); await bekle(60);
    if(!dm || !dm.classList.contains('open')) return 'Diğer menüsü açılmadı';
    const it = d.querySelector('.sa-diger-menu [data-sekme-hedef="' + t.dataset.panel + '"]'); if(!it) return 'Diğer menüsünde yok';
    return await tikla(it);
  };
  /* 0 · açılış: motor Seçilen birleşimiyle açılır (Yasin Bey) — şeridin ilk öğesi, "Seçilen" etiketli, bütün seçenekler onun değerinde */
  { const s0 = S.querySelector('.kp-serit-oge'), sv = V.alt.find(a => a.id === V.varsayilan), ac = panel().querySelector('.kp-orn');
    ok('açılış Seçilen', s0 && s0.hasAttribute('data-hazir') && s0.classList.contains('is-on') && /Seçilen/.test(s0.textContent) && S.dataset.alt === V.varsayilan
       && Object.keys(sv.orn).every(g => ac.getAttribute('data-o-' + g) === sv.orn[g]) && !!panel().querySelector('.kp-tuval.kp-' + sv.iskelet), 'ilk öğe ya da açılış değerleri yanlış'); }
  /* 1 · içerik sekmeleri × mecra: tıklama + yerleşim */
  const sekmeler = [...S.querySelectorAll('.sa-form-tab[data-sekme]')], mecralar = [...S.querySelectorAll('[data-kp-mecra]')];
  for(const t of sekmeler){
    const s = t.dataset.sekme, h = await sekmeAc(t);
    ok('sekme ' + s, !h && t.classList.contains('is-on') && panel() && panel().dataset.sekme === s && S.dataset.sekme === s, h || 'panel açılmadı');
    for(const m of mecralar){
      const mk = m.dataset.kpMecra, hm = await tikla(m);
      const bek = V.mecra[mk], yanlis = [...panel().querySelectorAll('.kp-tuval[data-mecrali]')].filter(x => gor(x) && x.dataset.bicim !== bek).length;
      ok('mecra ' + mk + ' (' + s + ')', !hm && m.classList.contains('is-on') && S.dataset.mecra === mk && !yanlis && S.querySelectorAll('[data-kp-mecra].is-on').length === 1, hm || ('biçim yanlış ' + yanlis));
      yerlesim(s + ' × ' + mk);
      /* güvenli alan */
      const gi = d.querySelector('input[data-kp="guvenli"]'), gl = gi && (gi.closest('label') || gi);
      if(gi && !gi.disabled){
        const hg = await tikla(gl); const ac = S.hasAttribute('data-guvenli') && [...panel().querySelectorAll('.kp-guvenli')].some(x => gor(x) && w.getComputedStyle(x).display !== 'none');
        const hg2 = await tikla(gl); ok('güvenli alan (' + s + ' × ' + mk + ')', !hg && !hg2 && ac && !S.hasAttribute('data-guvenli'), hg || hg2 || 'alan görünmedi ya da kapanmadı');
      } else if(gi){ ok('güvenli alan pasif gerekçeli (' + s + ' × ' + mk + ')', !!(d.getElementById('kpGuvAnahtar') || gl).title, 'gerekçe yok'); }
    }
  }
  await tikla(mecralar[0]); await sekmeAc(sekmeler[0]);

  /* 2 · kaydırmada titreme: aşağı in, kompakt hal kararlı mı; yukarı çık, açık hal geri gelsin */
  for(const s of sekmeler){
    await sekmeAc(s); const de = d.documentElement; let deg = 0, onc = K.classList.contains('is-kompakt');
    const mo = new w.MutationObserver(() => { const k = K.classList.contains('is-kompakt'); if(k !== onc){ deg++; onc = k; } }); mo.observe(K, {attributes: true, attributeFilter: ['class']});
    for(let y = 0; y <= de.scrollHeight; y += 37){ w.scrollTo(0, y); w.dispatchEvent(new w.Event('scroll')); await bekle(16); }
    await bekle(150); const altta = K.classList.contains('is-kompakt'), kt = Math.round(K.getBoundingClientRect().top), dipte = w.scrollY >= de.scrollHeight - w.innerHeight - 1;
    for(let y = de.scrollHeight; y >= 0; y -= 37){ w.scrollTo(0, y); w.dispatchEvent(new w.Event('scroll')); await bekle(16); }
    w.scrollTo(0, 0); w.dispatchEvent(new w.Event('scroll')); await bekle(150); mo.disconnect();
    const uzun = de.scrollHeight > w.innerHeight + 60;
    ok('kaydırma ' + s.dataset.sekme + ' · titreme yok', deg <= 2, deg + ' kez gidip geldi');
    const yap = w.getComputedStyle(K).position === 'sticky';
    if(uzun && yap) ok('kaydırma ' + s.dataset.sekme + ' · aşağıda yapışkan ve kompakt', altta && (kt <= 1 || dipte), 'kompakt=' + altta + ' üst=' + kt);
    if(!yap) ok('kaydırma ' + s.dataset.sekme + ' · yapışkan değilken küçülmüyor', !altta, 'küçüldü (içerik zıplar)');
    ok('kaydırma ' + s.dataset.sekme + ' · yukarıda açık hal', !K.classList.contains('is-kompakt'), 'kompakt kaldı');
  }
  await sekmeAc(sekmeler[0]);

  /* 3 · şerit: her alternatif + oklar */
  const serit = d.getElementById('kpSerit');
  for(const b of S.querySelectorAll('.kp-serit-oge')){
    const id = b.dataset.alt, h = await tikla(b);
    const ai = V.alt.find(a => a.id === id), isk = ai.iskelet || id;
    ok('şerit ' + (ai.hazir ? 'Seçilen' : id), !h && b.classList.contains('is-on') && S.dataset.alt === id && !!panel().querySelector('.kp-tuval.kp-' + isk) && (!ai.hazir || Object.keys(ai.orn).every(g => panel().querySelector('.kp-orn').getAttribute('data-o-' + g) === ai.orn[g])), h || 'iskelet ya da süsleme değişmedi');
  }
  const oklar = [...S.querySelectorAll('[data-kp-kaydir]')];
  if(serit.scrollWidth > serit.clientWidth + 2 && oklar.every(o => !gor(o))){
    ok('şerit okları gizli, şerit parmakla kayar', ['auto', 'scroll'].indexOf(w.getComputedStyle(serit).overflowX) > -1, 'kaydırılamıyor');
  } else if(serit.scrollWidth > serit.clientWidth + 2){
    serit.scrollLeft = 0; await bekle(100);
    const sag = oklar.find(o => o.dataset.kpKaydir === '1'), sol = oklar.find(o => o.dataset.kpKaydir === '-1');
    let h = await tikla(sag); await bekle(700); const x1 = serit.scrollLeft; ok('şerit sağ ok', !h && x1 > 0, h || 'kaymadı');
    h = await tikla(sol); await bekle(700); ok('şerit sol ok', !h && serit.scrollLeft < x1, h || 'kaymadı');
  } else ok('şerit okları (kaydırma gerekmiyor, gizli)', oklar.every(o => !gor(o) || o.disabled), 'gerekmediği halde görünür');
  await tikla(S.querySelector('.kp-serit-oge[data-alt="a"]'));

  /* 4 · açılır menüler ve her seçenek (her alternatifte pasif gerekçesi) */
  for(const dd of S.querySelectorAll('[data-kp-acilir]')){
    const g = dd.dataset.kpAcilir, btn = dd.querySelector('.kb-secim-btn'), menu = d.getElementById(btn.dataset.acilir);
    for(const o of dd.querySelectorAll('[data-kp-sec]')){
      const v = o.dataset.v; let h = await tikla(btn); await bekle(220);
      const acik = !h && menu.classList.contains('open') && +w.getComputedStyle(menu).opacity > .9;
      ok('menü ' + g + ' açılıyor', acik, h || 'açılmadı');
      if(!acik) continue;
      if(o.classList.contains('is-pasif')){
        ok('menü ' + g + ' · ' + v + ' pasif gerekçeli', !!o.title, 'gerekçe yok'); await tikla(btn); continue;
      }
      h = await tikla(o); await bekle(60);
      const deger = g === 'kat' ? S.dataset.kat : (panel().querySelector('.kp-orn') || {}).getAttribute && panel().querySelector('.kp-orn').getAttribute('data-o-' + g);
      ok('menü ' + g + ' · ' + v, !h && deger === v && btn.textContent.trim() === o.textContent.trim() && !menu.classList.contains('open'), h || ('değer ' + deger + ', düğme "' + btn.textContent.trim() + '"'));
      const tv = [...panel().querySelectorAll('.kp-tuval')].find(gor);
      if(g === 'islem' && v === 'kgecis' && tv){ const bi = w.getComputedStyle(tv.querySelector('.kp-karart')).backgroundImage;
        ok('Kategori Geçişi görünüyor', /radial-gradient/.test(bi) && /linear-gradient/.test(bi), 'geçiş katmanı yok'); }
      if(g === 'logo' && v === 'beyaz' && tv){ const lm = tv.querySelector('.kp-l-maske'), bc = w.getComputedStyle(lm).backgroundColor;
        ok('Beyaz logo görünüyor', gor(lm) && /255, 255, 255/.test(bc) && !gor(tv.querySelector('.kp-l-sari')), 'logo ' + bc); }
    }
  }
  /* 5 · Varsayılan */
  /* Varsayılan = Seçilen (Yasin Bey): başka iskeletteyken de Seçilen birleşimine döner */
  await tikla(S.querySelector('.kp-serit-oge[data-alt="c"]'));
  const vb = S.querySelector('[data-kp-varsayilan]'); let h = await tikla(vb); const a0 = V.alt.find(a => a.id === V.varsayilan);
  const fark = Object.keys(a0.orn).filter(g => panel().querySelector('.kp-orn').getAttribute('data-o-' + g) !== a0.orn[g]);
  ok('Varsayılan (Seçilen)', !h && S.dataset.alt === V.varsayilan && !fark.length && S.querySelector('.kp-serit-oge.is-on').dataset.alt === V.varsayilan, h || ('alt ' + S.dataset.alt + ' · dönmeyen: ' + fark.join(',')));
  /* 6 · Bunu Seç */
  const si = d.getElementById('kpSec'), sl = si.closest('label') || si, say = d.getElementById('kpSayac');
  h = await tikla(sl); const s1 = si.checked && gor(say) && say.textContent.indexOf('1') > -1;
  const h2 = await tikla(sl); ok('Bunu Seç', !h && !h2 && s1 && !si.checked && !gor(say), h || h2 || 'seçim ya da sayaç tutmadı');
  /* 7 · Hepsini Yan Yana Gör (her sekmede) */
  const hb = S.querySelector('[data-kp-hepsi]');
  for(const t of sekmeler){
    await sekmeAc(t); h = await tikla(hb); await bekle(120);
    const G = panel().querySelector('.kp-hepsi-izgara'), n = G ? [...G.children].filter(gor).length : 0;
    ok('Hepsini Yan Yana Gör (' + t.dataset.sekme + ')', !h && G && !G.hidden && n === V.alt.length && hb.getAttribute('aria-pressed') === 'true', h || (n + ' kart'));
    yerlesim('Hepsini Yan Yana Gör ' + t.dataset.sekme);
    h = await tikla(hb); await bekle(60); ok('Hepsini Yan Yana Gör kapanıyor (' + t.dataset.sekme + ')', !h && G.hidden, h || 'kapanmadı');
  }
  ok('sayfada JS hatası yok', !HATA.length, HATA.slice(0, 3).join(' | '));
} catch(e){ R.push({ad: 'betik hatası', g: false, not: String(e && e.stack || e).slice(0, 300)}); }
document.getElementById('o').textContent = JSON.stringify(R);
})();
"""


def sunucu():
    sk = socket.socket(); sk.bind(("127.0.0.1", 0)); port = sk.getsockname()[1]; sk.close()

    class S(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
        def do_GET(self):
            if self.path.startswith("/__tikla.html"):
                src = ("/canli/" if "canli=1" in self.path else "/") + "kalip/index.html?t=1"
                w = re.search(r"w=(\d+)", self.path).group(1)
                b = (f'<!doctype html><meta charset="utf-8"><iframe id="f" style="width:{w}px;height:900px;border:0" src="{src}"></iframe>'
                     f'<pre id="o"></pre><script>{PROBE or JS}</script>').encode()
                self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers(); self.wfile.write(b); return
            if self.path.startswith("/canli/"):       # canlı adres vekili: aynı köken (iframe içine erişim için)
                yol = self.path[len("/canli/"):]
                try:
                    with urllib.request.urlopen(urllib.request.Request(CANLI + yol, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as r:
                        b, tur = r.read(), r.headers.get("Content-Type", "application/octet-stream")
                    self.send_response(200); self.send_header("Content-Type", tur); self.end_headers(); self.wfile.write(b)
                except Exception:
                    self.send_response(404); self.end_headers()
                return
            return super().do_GET()
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), functools.partial(S, directory=str(KOK)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, port


def kos(port, w, canli):
    prof = tempfile.mkdtemp(prefix="kp-tikla-")
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={prof}",
                        f"--window-size={w + 40},1000", "--virtual-time-budget=600000", "--dump-dom",
                        f"http://127.0.0.1:{port}/__tikla.html?w={w}" + ("&canli=1" if canli else "")],
                       capture_output=True, text=True, timeout=900)
    shutil.rmtree(prof, ignore_errors=True)
    m = re.search(r'<pre id="o">(.*?)</pre>', r.stdout, re.S)
    if not m or not m.group(1).strip():
        return [{"ad": "sonuç alınamadı", "g": False, "not": r.stderr[-200:]}]
    if PROBE: print(html.unescape(m.group(1))); return []
    return json.loads(html.unescape(m.group(1)))


def main():
    canli = "--canli" in sys.argv
    srv, port = sunucu()
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        sonuc = dict(zip(GENISLIK, ex.map(lambda w: kos(port, w, canli), GENISLIK)))
    srv.shutdown()
    toplam = sum(len(v) for v in sonuc.values()); kalan = [(w, x) for w, v in sonuc.items() for x in v if not x["g"]]
    print(f"Tıklama denetimi{' (canlı)' if canli else ''}: {toplam} deneme · 5 genişlik · geçti {toplam - len(kalan)} · kaldı {len(kalan)}")
    for w, x in kalan[: (10**6 if "--hepsi" in sys.argv else 60)]:
        print(f"   {w}px · {x['ad']} · {x['not']}")
    sys.exit(1 if kalan else 0)


if __name__ == "__main__":
    main()
