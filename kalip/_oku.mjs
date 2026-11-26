// Kalıp okunurluk ölçümünün tarayıcı yarısı (kalip/_oku.py çağırır): gerçek zamanlı başsız Chrome (CDP).
// Her görünüm için sayfayı açar, açık sekmedeki kartlarda görünen her yazının satır kutularını, hesaplanmış rengini ve
// etkin saydamlığını toplar, ardından sayfanın o bölgesinin ekran görüntüsünü alır. Çıktı: <dizin>/<n>.png + <n>.json
// Kullanım: node kalip/_oku.mjs <taban-adres> <dizin> <görünümler.json>
import { spawn } from 'node:child_process';
import { writeFileSync, readFileSync, mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
const [taban, dizin, gorFile] = process.argv.slice(2);
const gorunumler = JSON.parse(readFileSync(gorFile, 'utf8'));
const port = 9300 + Math.floor(Math.random() * 500), prof = mkdtempSync(join(tmpdir(), 'kp-oku-'));
const ch = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', ['--headless=new', '--disable-gpu', '--hide-scrollbars', `--remote-debugging-port=${port}`, `--user-data-dir=${prof}`, 'about:blank'], { stdio: 'ignore' });
const bek = ms => new Promise(r => setTimeout(r, ms));
let ws;
for (let i = 0; i < 60; i++) { try { const j = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); const p = j.find(x => x.type === 'page'); if (p) { ws = new WebSocket(p.webSocketDebuggerUrl); break; } } catch (e) {} await bek(200); }
await new Promise(r => ws.addEventListener('open', r));
let id = 0; const bekleyen = {};
ws.addEventListener('message', m => { const d = JSON.parse(m.data); if (d.id && bekleyen[d.id]) { bekleyen[d.id](d.result || d.error); delete bekleyen[d.id]; } });
const gonder = (method, params = {}) => new Promise(r => { const i = ++id; bekleyen[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });
const deger = async (expr) => { const r = await gonder('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true }); return r && r.result && r.result.value; };
await gonder('Page.enable');
await gonder('Emulation.setDeviceMetricsOverride', { width: 1440, height: 1000, deviceScaleFactor: 1, mobile: false });
const TOPLA = `(async () => {
  for (let i = 0; i < 100 && !(window.kp && document.querySelector('#kpSahne[data-alt]')); i++) await new Promise(r => setTimeout(r, 100));
  if (document.fonts) await document.fonts.ready;
  const P = document.querySelector('#kpSahne .sa-form-panel:not([hidden])');
  /* arka plan görselleri gerçekten yüklensin */
  const us = new Set(); P.querySelectorAll('.kp-gorsel').forEach(g => { const m = /url\\("?([^")]+)"?\\)/.exec(getComputedStyle(g, '::before').backgroundImage); if (m) us.add(m[1]); });
  await Promise.all([...us].map(u => new Promise(r => { const im = new Image(); im.onload = im.onerror = r; im.src = u; })));
  await new Promise(r => setTimeout(r, 150)); window.kp.sigdir(); await new Promise(r => setTimeout(r, 80));
  const gor = e => e && e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden';
  /* renk tarayıcıda RGB'ye çevrilir (lch, color-mix, oklch dahil) */
  const cv = document.createElement('canvas'); cv.width = cv.height = 1; const cx = cv.getContext('2d', { willReadFrequently: true });
  const rgb = c => { cx.clearRect(0, 0, 1, 1); cx.fillStyle = '#000'; cx.fillStyle = c; cx.fillRect(0, 0, 1, 1); const v = cx.getImageData(0, 0, 1, 1).data; return [v[0], v[1], v[2], v[3] / 255]; };
  const sy = window.scrollY, sx = window.scrollX, out = [];
  P.querySelectorAll('.kp-tuval').forEach((t, ti) => {
    if (!gor(t) || t.closest('[hidden]')) return;
    const tr = t.getBoundingClientRect(), ad = (t.className.match(/kp-[a-n]\\b/) || ['?'])[0].slice(3).toUpperCase() + ' ' + t.dataset.tip + ' ' + t.dataset.bicim + (t.dataset.durum ? ' [' + t.dataset.durum + ']' : (t.closest('[data-durum]') ? ' [' + t.closest('[data-durum]').dataset.durum + ']' : ''));
    const tw = document.createTreeWalker(t, NodeFilter.SHOW_TEXT); let n; const rg = document.createRange();
    while ((n = tw.nextNode())) {
      if (!n.nodeValue.trim()) continue; const el = n.parentElement; if (!gor(el)) continue;
      const cs = getComputedStyle(el); if (parseFloat(cs.fontSize) < 6) continue;
      let op = 1, e = el; while (e && e !== t.parentElement) { op *= parseFloat(getComputedStyle(e).opacity); e = e.parentElement; }
      rg.selectNodeContents(n);
      [...rg.getClientRects()].forEach(r => { if (r.width < 3 || r.height < 3) return;
        if (r.right < tr.left || r.left > tr.right || r.bottom < tr.top || r.top > tr.bottom) return;
        out.push({ k: ti, ad, s: (el.className && el.className.baseVal === undefined ? el.className : el.tagName).toString().split(' ')[0] || el.tagName, m: n.nodeValue.trim().slice(0, 24), r: [r.left + sx, r.top + sy, r.width, r.height], c: rgb(cs.color), op: op * rgb(cs.color)[3], fs: parseFloat(cs.fontSize), fw: +cs.fontWeight }); });
    }
  });
  const pr = P.getBoundingClientRect();
  return JSON.stringify({ y: pr.top + sy, h: pr.height, w: Math.ceil(document.documentElement.scrollWidth), m: out });
})()`;
/* sayfa BİR KEZ açılır; görünümler sayfa içinden kurulur (kp.ayarla) — hızlı ve aynı durum makinesi */
await gonder('Page.navigate', { url: taban + 'kalip/index.html' });
await bek(1500);
let n = 0;
for (const g of gorunumler) {
  const q = Object.fromEntries(new URLSearchParams(g));
  await deger(`(async () => { for (let i = 0; i < 100 && !window.kp; i++) await new Promise(r => setTimeout(r, 100)); window.scrollTo(0, 0); window.kp.ayarla(${JSON.stringify({ alt: q.alt, sekme: q.sekme, kat: q.kat, mecra: 'ig', hepsi: false })}); return 1; })()`);
  /* görünür alan sayfa boyuna açılır: ölçüm ile ekran görüntüsü aynı yerleşimde (yükseklik ölçüsüne bağlı kartlar oynamaz) */
  await gonder('Emulation.setDeviceMetricsOverride', { width: 1440, height: 1000, deviceScaleFactor: 1, mobile: false }); await bek(80);
  const boy = await deger(`Math.min(16000, document.documentElement.scrollHeight)`);
  await gonder('Emulation.setDeviceMetricsOverride', { width: 1440, height: boy || 1000, deviceScaleFactor: 1, mobile: false }); await bek(250);
  const t0 = Date.now(); const v = await deger(TOPLA); if (process.env.KP_IZ) console.error('topla', g, Date.now() - t0, v ? v.length : 0);
  if (!v) { writeFileSync(join(dizin, `${n}.json`), JSON.stringify({ g, hata: 'sonuç yok' })); n++; continue; }
  const o = JSON.parse(v);
  /* önce yazılı görüntü (harf maskesi için) */
  for (let y = 0, k = 0; y < Math.min(o.h, 16000); y += 2500, k++) {
    const ss = await gonder('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false, clip: { x: 0, y: o.y + y, width: o.w, height: Math.min(2500, o.h - y), scale: 1 } });
    writeFileSync(join(dizin, `${n}_${k}y.png`), Buffer.from(ss.data, 'base64'));
  }
  /* yazısız zemin: yazılar saydam yapılır (yerleşim değişmez); görüntü yalnız zemini (fotoğraf + katmanlar + kutular) taşır */
  await deger(`(() => { const s = document.createElement('style'); s.id = 'kpOkuGizle'; s.textContent = '#kpSahne .kp-tuval, #kpSahne .kp-tuval *{color:transparent!important;-webkit-text-fill-color:transparent!important;text-shadow:none!important;text-decoration-color:transparent!important;caret-color:transparent!important}'; document.head.appendChild(s); return 1; })()`);
  await bek(60);
  /* uzun sekmede tek parça görüntü takılıyor: 2500 px'lik parçalar (Python birleştirir) */
  o.parca = [];
  for (let y = 0, k = 0; y < Math.min(o.h, 16000); y += 2500, k++) {
    const h = Math.min(2500, o.h - y);
    const ss = await gonder('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false, clip: { x: 0, y: o.y + y, width: o.w, height: h, scale: 1 } });
    if (process.env.KP_IZ) console.error('ss', k, Date.now() - t0);
    writeFileSync(join(dizin, `${n}_${k}.png`), Buffer.from(ss.data, 'base64')); o.parca.push(y);
  }
  await deger(`(() => { const s = document.getElementById('kpOkuGizle'); if (s) s.remove(); return 1; })()`);
  writeFileSync(join(dizin, `${n}.json`), JSON.stringify({ g, ...o }));
  n++;
}
ch.kill(); await bek(600); try { rmSync(prof, { recursive: true, force: true }); } catch (e) {} process.exit(0);
