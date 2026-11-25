#!/usr/bin/env python3
"""Kalıp ölçümü (kalip/index.html): her iskelet × kategori × mecra için bütün tuvaller tarayıcıda ölçülür.
Kurallar: başlık kesilmez (en çok 3 satır sığar), hiçbir öğe tuvalden taşmaz, logo metinle ya da etiketle çakışmaz,
9:16'da logo, başlık ve etiket düğmelerin kapattığı alanın dışına çıkmaz (üst %14, alt %35, sol %6, sağ %15).
Kullanım: python3 -I kalip/_olc.py   → "Kalıp ölçümü: … · sorun N"; sorun varsa çıkış 1 ve ilk 40 sorun listelenir.
"""
import functools, http.server, json, os, re, socket, subprocess, sys, threading, html
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
JS = r"""
function ayni(a,b){return !(a.right<=b.left+1||a.left>=b.right-1||a.bottom<=b.top+1||a.top>=b.bottom-1);}
function gor(e){if(!e||!e.getClientRects().length)return false;var s=getComputedStyle(e);return s.visibility!='hidden'&&s.display!='none'&&parseFloat(s.opacity)>0.05;}
function olc(d,kat,mecra,out){
  var n=0;
  d.querySelectorAll('#kpSahne .kp-tuval').forEach(function(t){
    var tr=t.getBoundingClientRect(); if(!tr.width)return; n++;
    var ad=(t.closest('[data-alt]')||{dataset:{}}).dataset.alt+' '+t.dataset.tip+' '+kat+' '+mecra;
    t.querySelectorAll('.kp-baslik').forEach(function(b){if(!gor(b))return; if(b.scrollHeight>b.clientHeight+2)out.push('kesik başlık · '+ad);});
    var parca=[].filter.call(t.querySelectorAll('.kp-logo,.kp-etiket,.kp-etiket-dikey,.kp-baslik,.kp-kaydir,.kp-sdbas,.kp-kim,.kp-aciklama,.kp-liste,.kp-meta,.kp-masthead,.kp-baglanti,.kp-oynat,.kp-glif'),gor);
    parca.forEach(function(x){var r=x.getBoundingClientRect(); if(r.width&&(r.left<tr.left-1||r.right>tr.right+1||r.top<tr.top-1||r.bottom>tr.bottom+1))out.push('taşma '+x.className.split(' ')[0]+' · '+ad);});
    var logo=t.querySelector('.kp-logo'); if(gor(logo)){var lr=logo.getBoundingClientRect();
      parca.forEach(function(x){if(x===logo||logo.contains(x)||x.classList.contains('kp-glif'))return; if(ayni(lr,x.getBoundingClientRect()))out.push('logo çakışma '+x.className.split(' ')[0]+' · '+ad);});}
    var metin=[].filter.call(t.querySelectorAll('.kp-blok > :not(.kp-oge):not(.kp-glif-b)'),gor);
    for(var i=0;i<metin.length;i++)for(var j=i+1;j<metin.length;j++){if(ayni(metin[i].getBoundingClientRect(),metin[j].getBoundingClientRect()))out.push('üst üste '+metin[i].className.split(' ')[0]+'/'+metin[j].className.split(' ')[0]+' · '+ad);}
    if(/hikaye|reels/.test(t.dataset.tip)){var g={t:tr.top+tr.height*.14,b:tr.bottom-tr.height*.35,l:tr.left+tr.width*.06,r:tr.right-tr.width*.15};
      [].forEach.call(t.querySelectorAll('.kp-logo,.kp-baslik,.kp-etiket,.kp-etiket-dikey'),function(x){if(!gor(x))return;var r=x.getBoundingClientRect();
        if(r.top<g.t-1||r.bottom>g.b+1||r.left<g.l-1||r.right>g.r+1)out.push('düğme alanı '+x.className.split(' ')[0]+' · '+ad);});}
  });
  return n;
}
setTimeout(function(){var d=f.contentDocument,out=[],n=0;d.querySelectorAll('.sa-form-panel').forEach(function(p){p.hidden=false;});
 function set(k,v){var i=d.querySelector('input[data-mo="'+k+'"][value="'+v+'"]');i.checked=true;i.dispatchEvent(new Event('change',{bubbles:true}));}
 ['gundem','spor','kadin','finans','savunma'].forEach(function(k){['ig','linkedin','facebook','x'].forEach(function(m){set('kat',k);set('mecra',m);if(f.contentWindow.kpSigdir)f.contentWindow.kpSigdir();n+=olc(d,k,m,out);});});
 o.textContent=JSON.stringify({n:n,sorun:out});},1500);
"""


def main():
    sk = socket.socket(); sk.bind(("127.0.0.1", 0)); port = sk.getsockname()[1]; sk.close()
    class S(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
        def do_GET(self):
            if self.path.startswith("/__olc.html"):
                b = ('<!doctype html><meta charset="utf-8"><iframe id="f" style="width:1440px;height:1800px" src="/kalip/index.html"></iframe><pre id="o"></pre><script>'
                     + JS + '</script>').encode()
                self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers(); self.wfile.write(b); return
            return super().do_GET()
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), functools.partial(S, directory=str(KOK)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=20000", "--dump-dom", f"http://127.0.0.1:{port}/__olc.html"],
                       capture_output=True, text=True, timeout=600)
    srv.shutdown()
    m = re.search(r'<pre id="o">(.*?)</pre>', r.stdout, re.S)
    if not m or not m.group(1).strip():
        print("Kalıp ölçümü: sonuç alınamadı"); sys.exit(1)
    v = json.loads(html.unescape(m.group(1)))
    tekil = sorted(set(v["sorun"]))
    if "--ozet" in sys.argv:
        import collections
        c = collections.Counter(" ".join(x.split(" · ")[0:1] + x.split(" · ")[1].split()[:2]) for x in tekil)
        for k, n in sorted(c.items()): print(f"{n:4d}  {k}")
    print(f"Kalıp ölçümü: {v['n']} tuval (10 iskelet × 5 kategori × 4 mecra) · sorun {len(tekil)}")
    for s in (tekil if "--hepsi" in sys.argv else tekil[:40]): print("   " + s)
    sys.exit(1 if tekil else 0)


if __name__ == "__main__":
    main()
