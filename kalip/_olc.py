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
var W, d, out = {cakisma:[], tasma:[], kesik:[], kucuk:[], merkez:[], guvenli:[], gorsel:[], etkisiz:[], karsitlik:[], sayi:[]}, n = 0, url = {};
function gor(e){ if(!e || !e.getClientRects().length) return false; var s = W.getComputedStyle(e); return s.visibility != 'hidden' && parseFloat(s.opacity) > 0.05; }
function kes(a, b){ return !(a.right <= b.left + 1 || a.left >= b.right - 1 || a.bottom <= b.top + 1 || a.top >= b.bottom - 1); }
var PARCA = '.kp-logo,.kp-etiket,.kp-etiket-dikey,.kp-baslik,.kp-kaydir,.kp-sdbas,.kp-kim,.kp-aciklama,.kp-liste,.kp-meta,.kp-masthead,.kp-baglanti,.kp-oynat,.kp-sayi,.kp-ust-not,.kp-ic-bas,.kp-glif,.kp-sayfa-nokta,[data-olc-parca],.kd-rozet,.kd-damga,.kd-ust,.kd-yazar,.kd-program,.kd-skor,.kd-zaman,.kd-bilgi,.kd-tablo,.kd-hava-simdi,.kd-hava-gunler,.kd-akis,.kd-onceki,.kd-eklenen,.kd-not,.kd-yil,.kd-cagri,.kd-ses,.kd-grafik,.kd-secenekler,.kd-soru-kutu,.kd-liste,.ks-yuz';
var GUV = '.kp-logo,.kp-baslik,.kp-etiket,.kp-etiket-dikey,.kp-kaydir,.kp-sdbas,.kl-ic,[data-olc-parca="kl-kelime"],[data-olc-yuz],.ks-yuz';
function ad(t, ek){ return (t.className.match(/kp-[a-n]\b/) || ['?'])[0].slice(3).toUpperCase() + ' ' + t.dataset.tip + ' ' + t.dataset.bicim + ' ' + ek + (t.closest('.kp-dis') ? ' [' + (t.closest('#kpT-kisi') ? 'Kişi Haberleri' : 'Durumlar') + ']' : ''); }
function kisa(x){ return (x.className.match(/kp-[a-z-]+/) || [x.getAttribute('data-olc-parca') || x.tagName])[0]; }
function olc(t, ek){
  var tr = t.getBoundingClientRect(); if(!tr.width) return; n++;
  var a = ad(t, ek);
  var g = W.getComputedStyle(t.querySelector('.kp-gorsel'), '::before').backgroundImage, m = /url\("?([^")]+)"?\)/.exec(g);
  if(!m){ [].some.call(t.querySelectorAll('.kp-gorsel *'), function(x){ var b = W.getComputedStyle(x).backgroundImage; m = /url\("?([^")]+)"?\)/.exec(b) || /url\("?([^")]+)"?\)/.exec(W.getComputedStyle(x, '::before').backgroundImage); return !!m; }); }
  if(!m) out.gorsel.push('görsel yok · ' + a); else url[m[1]] = a;
  [].forEach.call(t.querySelectorAll('.kd-yazar-foto,.kd-onceki-foto'), function(x){ if(!gor(x)) return; var bi = W.getComputedStyle(x).backgroundImage, m2 = /url\("?([^")]+)"?\)/.exec(bi);
    if(!m2) m2 = /url\("?([^")]+)"?\)/.exec(W.getComputedStyle(x, '::before').backgroundImage); if(!m2) out.gorsel.push('görsel yok ' + kisa(x) + ' · ' + a); else url[m2[1]] = a; });
  var bl = t.querySelector('.kp-blok');
  if(bl && gor(bl)){ var br = bl.getBoundingClientRect(), bs = W.getComputedStyle(bl), pt = parseFloat(bs.paddingTop), pb = parseFloat(bs.paddingBottom);
    [].forEach.call(bl.children, function(c){ if(!gor(c) || W.getComputedStyle(c).position == 'absolute') return; var cr = c.getBoundingClientRect();
      if(cr.top < br.top + pt - 1 || cr.bottom > br.bottom - pb + 1 || cr.right > br.right + 1 || cr.left < br.left - 1) out.tasma.push('bloktan taşma ' + kisa(c) + ' · ' + a); }); }
  [].forEach.call(t.querySelectorAll('.kp-baslik'), function(b){ if(!gor(b)) return; var sat = W.kp.satir(b), uzunBaslik = / 14$| 14 /.test(ek); if(b.scrollHeight > b.clientHeight + parseFloat(W.getComputedStyle(b).fontSize) * .3 || sat > (uzunBaslik ? 4 : 3)) out.kesik.push('kesik başlık (' + sat + ' satır) · ' + a);
    var fs = parseFloat(W.getComputedStyle(b).fontSize), alt_ = W.kp.kucuk() * Math.min(tr.width, tr.height); if(fs < alt_ - .3) out.kucuk.push('küçük başlık ' + (fs / Math.min(tr.width, tr.height) * 100).toFixed(1) + 'cqmin · ' + a); });
  var mx = tr.left + tr.width / 2;
  [].forEach.call(t.querySelectorAll('.kp-blok,[data-hiza="orta"]'), function(x){ if(!gor(x)) return; var cs = W.getComputedStyle(x);
    if(cs.textAlign != 'center' && x.getAttribute('data-hiza') != 'orta') return; var r = x.getBoundingClientRect(), k = r.left + r.width / 2 - mx;
    if(Math.abs(k) > 1) out.merkez.push('merkez dışı ' + kisa(x) + ' ' + k.toFixed(1) + 'px · ' + a);
    var lg = t.querySelector('.kp-logo'); if(x.classList.contains('kp-blok') && gor(lg)){ var lr = lg.getBoundingClientRect(), lk = lr.left + lr.width / 2 - mx; if(Math.abs(lk) > 1 && Math.abs(lr.top - tr.top) < tr.height / 2) out.merkez.push('merkez dışı logo ' + lk.toFixed(1) + 'px · ' + a); } });
  var p = [].filter.call(t.querySelectorAll(PARCA), gor);
  p.forEach(function(x){ var r = x.getBoundingClientRect(); if(r.width && (r.left < tr.left - 1 || r.right > tr.right + 1 || r.top < tr.top - 1 || r.bottom > tr.bottom + 1)) out.tasma.push('taşma ' + kisa(x) + ' · ' + a); });
  for(var i = 0; i < p.length; i++) for(var j = i + 1; j < p.length; j++){
    if(p[i].contains(p[j]) || p[j].contains(p[i])) continue;
    if(kes(p[i].getBoundingClientRect(), p[j].getBoundingClientRect())) out.cakisma.push('çakışma ' + kisa(p[i]) + '/' + kisa(p[j]) + ' · ' + a);
  }
  if(t.dataset.bicim == 'uzun'){
    var G = W.kp.V.guvenli, s = {t: tr.top + tr.height * G.ust / G.boy, b: tr.bottom - tr.height * G.alt / G.boy, l: tr.left + tr.width * G.sol / G.en, r: tr.right - tr.width * G.sag / G.en};
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
  /* süsleme çeşitleri: yerleşimi en çok zorlayan logo ve etiket seçenekleriyle yeniden (gündem, 5 mecra, asıl ve 14 kelime) */
  var CES = [{logo: 'rozet'}, {logo: 'plaka'}, {logo: 'renk'}, {etiket: 'dikey'}, {etiket: 'dolu'}];
  sira.forEach(function(alt){
    var a0 = V.alt.filter(function(a){ return a.id == alt; })[0], varsay = Object.assign({}, kp.D.orn[alt]);
    CES.forEach(function(c){
      var g = Object.keys(c)[0]; if(a0.pasif && a0.pasif[g] && a0.pasif[g][c[g]]) return; if(varsay[g] == c[g]) return;
      ['ig','dikey','linkedin','facebook','x'].forEach(function(mecra){
        kp.D.orn[alt] = Object.assign({}, varsay, c); kp.ayarla({alt: alt, kat: 'gundem', mecra: mecra, hepsi: false}); hepsiniAc();
        [0, 14].forEach(function(nk){ kp.metin(nk); tek().forEach(function(t){ if(mecra != 'ig' && !t.hasAttribute('data-mecrali')) return; olc(t, 'gundem ' + mecra + ' ' + (nk || 'asıl') + ' ' + g + '=' + c[g]); }); });
        kp.metin(0);
      });
    });
    kp.D.orn[alt] = Object.assign({}, varsay); kp.ciz();
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
  /* sayfadaki sayılar gerçek sayıyla aynı (elle yazılmaz) */
  var si = d.querySelector('[data-kp-say="iskelet"]'), sk = d.querySelectorAll('.kp-serit-oge').length;
  if(!si || +si.textContent != sk || sk != sira.length) out.sayi.push('iskelet sayısı: başlıkta ' + (si && si.textContent) + ', şeritte ' + sk + ', kayıtta ' + sira.length);
  var dp = d.getElementById('kpT-durum');
  if(dp){ var m3 = /(\d+)\s*durum/i.exec(dp.textContent), ids = {}; [].forEach.call(dp.querySelectorAll('[data-durum]'), function(x){ ids[x.getAttribute('data-durum')] = 1; });
    var nd = Object.keys(ids).length; if(m3 && +m3[1] != nd) out.sayi.push('durum sayısı: yazıda ' + m3[1] + ', kartlarda ' + nd); }
  var us = Object.keys(url), kalan = us.length;
  function bitir(){ o.textContent = JSON.stringify({n: n, sorun: out}); }
  if(!kalan) return bitir();
  us.forEach(function(u){ var im = new Image(); im.onload = function(){ if(!--kalan) bitir(); }; im.onerror = function(){ out.gorsel.push('görsel yüklenmiyor ' + u + ' · ' + url[u]); if(!--kalan) bitir(); }; im.src = new URL(u, f.contentDocument.baseURI).href; });
}
f.onload = function(){ var w = f.contentWindow; (w.document.fonts ? w.document.fonts.ready : Promise.resolve()).then(function(){ setTimeout(function bekle(){ if(!f.contentWindow.kp) return setTimeout(bekle, 200); try{ calis(); }catch(ex){ o.textContent = JSON.stringify({hata: String(ex) + ' ' + ex.stack}); } }, 300); }); };
"""
AD = [("cakisma", "çakışma"), ("tasma", "taşma"), ("kesik", "kesik başlık"), ("kucuk", "küçük başlık"), ("merkez", "merkez dışı"), ("guvenli", "güvenli alan dışı"),
      ("gorsel", "görsel eksik"), ("etkisiz", "etkisiz seçenek"), ("karsitlik", "düşük karşıtlık"), ("sayi", "sayı uyuşmazlığı")]


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
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--window-size=1600,1900", "--virtual-time-budget=900000", "--dump-dom", f"http://127.0.0.1:{port}/__olc.html"],
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
