#!/usr/bin/env python3
"""Kalıp ölçümü (kalip/index.html): sayfa tarayıcıda açılır, window.kp ile her durum kurulur ve tuvaller ölçülür.

Taranan: 14 iskelet × 5 kategori × 5 mecra (Instagram 4:5, Dikey 9:16, LinkedIn, Facebook, X) × 3 başlık boyu
(asıl, 3 kelime, 14 kelime) × bütün içerik çeşitleri (haber, Son Dakika, kaydırmalı kapak ve iç sayfa, hikâye, Reels,
alıntı, veri, akış kartları; varsa Durumlar ve Kişi Haberleri tuvalleri).
Kurallar (hepsi 0 olmalı):
  çakışma          logo, etiket, başlık, kaydır, Son Dakika, künye, rakam, liste vb. parçalar birbirine binmez
  taşma            hiçbir parça tuvalden taşmaz
  kesik başlık     başlık en çok üç satıra sığar (küçülür, kesilmez)
  güvenli alan     9:16'da logo, başlık, etiket, kaydır, Son Dakika ve kişi yüzü birleşik resmî alanın içinde
                   (üst 288, alt 672, sol 65, sağ 192 px @1080×1920); 1 px dışarı = hata
  görsel eksik     her tuvalin fotoğraf katmanında görsel var ve dosya gerçekten yükleniyor
  etkisiz seçenek  her iskelet × süsleme grubu × seçenek, aynı gruptaki diğer seçeneklerden görünür biçimde ayrılır
                   (hesaplanmış stil ve DOM farkı); pasif olarak işaretlenmiş seçenek sayılmaz
  düşük karşıtlık  başlıktaki vurgu metni ile zemini WCAG ≥ 3:1 (bütün başlık vurgusu × görsel işlemi × kategori)
Kullanım: python3 -I kalip/_olc.py [--ozet] [--hepsi]  → "Kalıp ölçümü: …"; sorun varsa çıkış 1.
"""
import functools, http.server, json, os, re, socket, subprocess, sys, threading, html, collections
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
JS = r"""
var W, d, out = {cakisma:[], tasma:[], kesik:[], guvenli:[], gorsel:[], etkisiz:[], karsitlik:[]}, n = 0, url = {};
function gor(e){ if(!e || !e.getClientRects().length) return false; var s = W.getComputedStyle(e); return s.visibility != 'hidden' && parseFloat(s.opacity) > 0.05; }
function kes(a, b){ return !(a.right <= b.left + 1 || a.left >= b.right - 1 || a.bottom <= b.top + 1 || a.top >= b.bottom - 1); }
var PARCA = '.kp-logo,.kp-etiket,.kp-etiket-dikey,.kp-baslik,.kp-kaydir,.kp-sdbas,.kp-kim,.kp-aciklama,.kp-liste,.kp-meta,.kp-masthead,.kp-baglanti,.kp-oynat,.kp-sayi,.kp-ust-not,.kp-ic-bas,.kp-glif,.kp-sayfa-nokta,[data-olc-parca]';
var GUV = '.kp-logo,.kp-baslik,.kp-etiket,.kp-etiket-dikey,.kp-kaydir,.kp-sdbas,.kl-ic,[data-olc-parca="kl-kelime"],[data-olc-yuz]';
function ad(t, ek){ return (t.className.match(/kp-[a-n]\b/) || ['?'])[0].slice(3).toUpperCase() + ' ' + t.dataset.tip + ' ' + t.dataset.bicim + ' ' + ek + (t.closest('[data-alt-icerik]') ? ' [' + (t.closest('#kpT-kisi') ? 'Kişi Haberleri' : 'Durumlar') + ']' : ''); }
function kisa(x){ return (x.className.match(/kp-[a-z-]+/) || [x.getAttribute('data-olc-parca') || x.tagName])[0]; }
function olc(t, ek){
  var tr = t.getBoundingClientRect(); if(!tr.width) return; n++;
  var a = ad(t, ek);
  var g = W.getComputedStyle(t.querySelector('.kp-gorsel'), '::before').backgroundImage, m = /url\("?([^")]+)"?\)/.exec(g);
  if(!m) out.gorsel.push('görsel yok · ' + a); else url[m[1]] = a;
  [].forEach.call(t.querySelectorAll('.kp-baslik'), function(b){ if(gor(b) && b.scrollHeight > b.clientHeight + 2) out.kesik.push('kesik başlık · ' + a); });
  var p = [].filter.call(t.querySelectorAll(PARCA), gor);
  p.forEach(function(x){ var r = x.getBoundingClientRect(); if(r.width && (r.left < tr.left - 1 || r.right > tr.right + 1 || r.top < tr.top - 1 || r.bottom > tr.bottom + 1)) out.tasma.push('taşma ' + kisa(x) + ' · ' + a); });
  for(var i = 0; i < p.length; i++) for(var j = i + 1; j < p.length; j++){
    if(p[i].contains(p[j]) || p[j].contains(p[i])) continue;
    if(kes(p[i].getBoundingClientRect(), p[j].getBoundingClientRect())) out.cakisma.push('çakışma ' + kisa(p[i]) + '/' + kisa(p[j]) + ' · ' + a);
  }
  if(t.dataset.bicim == 'uzun'){
    var s = {t: tr.top + tr.height * 288 / 1920, b: tr.bottom - tr.height * 672 / 1920, l: tr.left + tr.width * 65 / 1080, r: tr.right - tr.width * 192 / 1080};
    [].forEach.call(t.querySelectorAll(GUV), function(x){ if(!gor(x)) return; var r = x.getBoundingClientRect();
      if(r.top < s.t - .5 || r.bottom > s.b + .5 || r.left < s.l - .5 || r.right > s.r + .5) out.guvenli.push('güvenli alan dışı ' + kisa(x) + ' · ' + a); });
  }
}
/* renk: tarayıcıya çözdürülür (lch, color-mix dahil) */
var cv = document.createElement('canvas'); cv.width = cv.height = 1; var cx = cv.getContext('2d', {willReadFrequently: true});
function rgb(c){ cx.clearRect(0, 0, 1, 1); cx.fillStyle = '#000'; cx.fillStyle = c; cx.fillRect(0, 0, 1, 1); var v = cx.getImageData(0, 0, 1, 1).data; return [v[0], v[1], v[2], v[3] / 255]; }
function lum(c){ return c.slice(0, 3).map(function(v){ v /= 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }).reduce(function(s, v, i){ return s + v * [.2126, .7152, .0722][i]; }, 0); }
function oran(a, b){ var x = lum(a), y = lum(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); }
function karsitlik(t, ek){
  [].forEach.call(t.querySelectorAll('.kp-vurgu'), function(v){
    if(!gor(v)) return;
    var fg = rgb(W.getComputedStyle(v).color), bg = null, e = v;
    while(e && e !== t){ var c = rgb(W.getComputedStyle(e).backgroundColor); if(c[3] > .5){ bg = c; break; } e = e.parentElement; }
    if(!bg){ var yz = t.dataset.yz, pr = d.createElement('span'); t.appendChild(pr);
      pr.style.background = yz == 'acik' ? 'var(--paper)' : yz == 'kat' ? 'var(--vr)' : 'rgb(51,51,51)'; bg = rgb(W.getComputedStyle(pr).backgroundColor); pr.remove(); }
    var o = oran(fg, bg); if(o < 3) out.karsitlik.push('düşük karşıtlık ' + o.toFixed(2) + ' · ' + ad(t, ek));
  });
}
function iz(t){
  var s = [], P = ['display','color','background-color','background-image','filter','border-radius','box-shadow','text-decoration-line','text-decoration-color','mix-blend-mode','opacity','padding-top','padding-left','writing-mode','width','height','top','left','transform','font-size','letter-spacing','text-transform'];
  [t].concat([].slice.call(t.querySelectorAll('*'))).forEach(function(e){
    [null, '::before', '::after'].forEach(function(ps){ var c = W.getComputedStyle(e, ps); s.push(P.map(function(k){ return c.getPropertyValue(k); }).join('|')); });
  });
  return s.join('\n');
}
function calis(){
  W = f.contentWindow; d = f.contentDocument; var kp = W.kp, sira = kp.sira, V = kp.V;
  var tek = function(){ return [].slice.call(d.querySelectorAll('.kp-tek .kp-tuval')); };
  function hepsiniAc(){ d.querySelectorAll('.sa-form-panel').forEach(function(p){ p.hidden = false; }); d.querySelectorAll('[data-alt-icerik]').forEach(function(x){ x.hidden = x.getAttribute('data-alt-icerik') !== kp.D.alt; }); kp.sigdir(); }
  ['gundem','spor','kadin','finans','savunma'].forEach(function(kat){
    ['ig','dikey','linkedin','facebook','x'].forEach(function(mecra){
      sira.forEach(function(alt){
        kp.ayarla({alt: alt, kat: kat, mecra: mecra, hepsi: false}); hepsiniAc();
        [0, 3, 14].forEach(function(nk){
          kp.metin(nk);
          tek().forEach(function(t){ if(mecra != 'ig' && !t.hasAttribute('data-mecrali')) return; olc(t, kat + ' ' + mecra + ' ' + (nk || 'asıl')); });
          var ek = [].slice.call(d.querySelectorAll('[data-alt-icerik="' + alt + '"] [data-olc-tuval]'));
          if(mecra == 'ig') ek.forEach(function(t){ var b = t.closest('.sa-form-panel'); olc(t, kat + ' ' + (nk || 'asıl') + ' [' + (b && b.dataset.sekme == 'kisi' ? 'Kişi Haberleri' : 'Durumlar') + (t.dataset.olcTuval ? ' · ' + t.dataset.olcTuval : '') + ']'); });
        });
        kp.metin(0);
      });
    });
  });
  /* etkisiz seçenek ve karşıtlık: haber gönderisi (koyu görsel, 4:5) üzerinde */
  sira.forEach(function(alt){
    kp.ayarla({alt: alt, kat: 'gundem', mecra: 'ig', hepsi: false, sekme: 'haber'}); hepsiniAc();
    var t = d.querySelector('#kpT-haber .kp-tek .kp-tuval'), varsay = Object.assign({}, kp.D.orn[alt]);
    Object.keys(V.susleme).forEach(function(g){
      var izler = {};
      V.susleme[g].forEach(function(v){
        var p = V.alt.filter(function(a){ return a.id == alt; })[0].pasif; if(p && p[g] && p[g][v]) return;
        kp.D.orn[alt][g] = v; kp.ciz(); var k = iz(t);
        Object.keys(izler).forEach(function(v2){ if(izler[v2] === k) out.etkisiz.push('etkisiz seçenek ' + g + ' ' + v2 + '=' + v + ' · ' + alt.toUpperCase()); });
        izler[v] = k;
      });
      kp.D.orn[alt] = Object.assign({}, varsay); kp.ciz();
    });
    ['gundem','spor','kadin','finans','savunma'].forEach(function(kat){
      kp.ayarla({kat: kat});
      V.susleme.bvurgu.forEach(function(bv){ V.susleme.islem.forEach(function(is){
        kp.D.orn[alt].bvurgu = bv; kp.D.orn[alt].islem = is; kp.ciz(); hepsiniAc();
        tek().forEach(function(t2){ if(t2.dataset.tip == 'haber' || t2.dataset.tip == 'sd' || t2.dataset.tip == 'veri' || t2.dataset.tip == 'alinti') karsitlik(t2, kat + ' ' + bv + ' ' + is); });
      }); });
      kp.D.orn[alt] = Object.assign({}, varsay); kp.ciz();
    });
  });
  var us = Object.keys(url), kalan = us.length;
  function bitir(){ o.textContent = JSON.stringify({n: n, sorun: out}); }
  if(!kalan) return bitir();
  us.forEach(function(u){ var im = new Image(); im.onload = function(){ if(!--kalan) bitir(); }; im.onerror = function(){ out.gorsel.push('görsel yüklenmiyor ' + u + ' · ' + url[u]); if(!--kalan) bitir(); }; im.src = new URL(u, f.contentDocument.baseURI).href; });
}
f.onload = function(){ var w = f.contentWindow; (w.document.fonts ? w.document.fonts.ready : Promise.resolve()).then(function(){ setTimeout(function(){ try{ calis(); }catch(ex){ o.textContent = JSON.stringify({hata: String(ex) + ' ' + ex.stack}); } }, 300); }); };
"""
AD = [("cakisma", "çakışma"), ("tasma", "taşma"), ("kesik", "kesik başlık"), ("guvenli", "güvenli alan dışı"), ("gorsel", "görsel eksik"),
      ("etkisiz", "etkisiz seçenek"), ("karsitlik", "düşük karşıtlık")]


def main():
    sk = socket.socket(); sk.bind(("127.0.0.1", 0)); port = sk.getsockname()[1]; sk.close()

    class S(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass

        def do_GET(self):
            if self.path.startswith("/__olc.html"):
                b = ('<!doctype html><meta charset="utf-8"><iframe id="f" style="width:1440px;height:1800px;border:0" src="/kalip/index.html"></iframe><pre id="o"></pre><script>'
                     + JS + '</script>').encode()
                self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers(); self.wfile.write(b); return
            return super().do_GET()
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), functools.partial(S, directory=str(KOK)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--window-size=1600,1900", "--virtual-time-budget=240000", "--dump-dom", f"http://127.0.0.1:{port}/__olc.html"],
                       capture_output=True, text=True, timeout=900)
    srv.shutdown()
    m = re.search(r'<pre id="o">(.*?)</pre>', r.stdout, re.S)
    if not m or not m.group(1).strip():
        print("Kalıp ölçümü: sonuç alınamadı"); sys.exit(1)
    v = json.loads(html.unescape(m.group(1)))
    if "hata" in v:
        print("Kalıp ölçümü: betik hatası ·", v["hata"][:600]); sys.exit(1)
    s = {k: sorted(set(v["sorun"][k])) for k, _ in AD}
    toplam = sum(len(x) for x in s.values())
    print(f"Kalıp ölçümü: {v['n']} tuval (14 iskelet × 5 kategori × 5 mecra × 3 başlık boyu, bütün çeşitler) · "
          + " · ".join(f"{a} {len(s[k])}" for k, a in AD))
    if "--ozet" in sys.argv:
        for k, a in AD:
            c = collections.Counter(re.sub(r" · (\S+ \S+ \S+).*", r" · \1", x) for x in s[k])
            for x, say in c.most_common(25): print(f"  {say:4d}  {x}")
    hepsi = [x for k, _ in AD for x in s[k]]
    for x in (hepsi if "--hepsi" in sys.argv else hepsi[:40]): print("   " + x)
    sys.exit(1 if toplam else 0)


if __name__ == "__main__":
    main()
