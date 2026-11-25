/* =====================================================================
   SOSYAL MEDYA KALIP ALTERNATİFLERİ · yalnız bu sayfanın betiği (ortak dosya değil)
   TEK DURUM NESNESİ (D): seçili alternatif, açık sekme, yan yana görünüm, kategori, mecra, güvenli alan,
   her alternatifin süslemesi, "Bunu Seç" ve notlar. Bütün denetimler D'ye yazar; ciz() sayfayı D'den çizer.
   - Tekli görünüm: sekmelerdeki tuvaller bir kez üretilmiştir; ciz() iskelet sınıfını (kp-a … kp-n), metin/logo zeminini
     (data-yz, data-lz) ve mecraya göre biçimi (data-bicim) yazar; süsleme .kp-orn kaplarına data-o-* olarak iner.
   - Yan yana görünüm: açık sekmenin içeriği bütün alternatifler için kopyalanır; her kart kendi süslemesini taşır.
   - Başlık sığdırma: başlık ya da rakam bloğa sığmıyorsa en çok %54 küçülür (kesilmez).
   Adres satırı: ?alt=c&sekme=haber&kat=spor&mecra=x&guvenli=1&hepsi=1 (sunum ve ölçüm için).
   window.kp: ölçüm (kalip/_olc.py) için durum ve araçlar.
   ===================================================================== */
(function(){
  var S = document.getElementById('kpSahne'), VK = document.getElementById('kpVeri');
  if(!S || !VK) return;
  var V = JSON.parse(VK.textContent), ALT = {}, SIRA = [];
  V.alt.forEach(function(a){ ALT[a.id] = a; SIRA.push(a.id); });
  var GRUP = Object.keys(V.susleme), q = new URLSearchParams(location.search);
  var SEKMELER = Array.prototype.map.call(S.querySelectorAll('.sa-form-tab[data-sekme]'), function(t){ return t.dataset.sekme; });
  var D = {
    alt: ALT[q.get('alt')] ? q.get('alt') : 'a',
    sekme: SEKMELER.indexOf(q.get('sekme')) > -1 ? q.get('sekme') : 'akis',
    hepsi: q.get('hepsi') === '1',
    kat: /^(gundem|spor|kadin|finans|savunma)$/.test(q.get('kat') || '') ? q.get('kat') : 'gundem',
    mecra: V.mecra[q.get('mecra')] ? q.get('mecra') : 'ig',
    guvenli: q.get('guvenli') === '1',
    orn: {}, sec: {}, not: {}
  };
  SIRA.forEach(function(id){ D.orn[id] = Object.assign({}, ALT[id].orn); });
  var arac = document.getElementById('kpArac'), perde = S.querySelector('.kp-perde'), serit = document.getElementById('kpSerit');
  var each = function(l, f){ Array.prototype.forEach.call(l, f); };

  function pasif(id, g, v){ var p = ALT[id].pasif; return p && p[g] && p[g][v]; }
  function zemin(id, tip, bicim){
    var a = ALT[id];
    return [(tip === 'ic' && a.yz.ic) || a.yz._, (tip === 'ic' && a.lz.ic) || a.lz[bicim] || a.lz._];
  }
  function uygula(t, id){
    each(Array.prototype.slice.call(t.classList), function(c){ if(/^kp-[a-n]$/.test(c)) t.classList.remove(c); });
    t.classList.add('kp-' + id);
    if(t.hasAttribute('data-mecrali')) t.setAttribute('data-bicim', V.mecra[D.mecra]);
    var z = zemin(id, t.dataset.tip, t.dataset.bicim);
    t.setAttribute('data-yz', z[0]); t.setAttribute('data-lz', z[1]);
    t.setAttribute('aria-label', ALT[id].harf + ' · ' + ALT[id].ad + ' · ' + t.dataset.tip);
  }
  function ornYaz(k, id){ GRUP.forEach(function(g){ k.setAttribute('data-o-' + g, D.orn[id][g]); }); }

  /* ---------- çizim ---------- */
  var HK = { akis: { _: 300 }, haber: { kare: 380, uzun: 320, yatay: 560 }, sd: { kare: 230, uzun: 190, yatay: 330 }, kaydir: { _: 380 },
             dikey: { _: 320 }, alinti: { kare: 380, uzun: 320, yatay: 560 }, durum: { _: 9999 }, kisi: { _: 9999 } };
  function hepsiKur(){
    var P = document.getElementById('kpT-' + D.sekme); if(!P) return;
    var G = P.querySelector('.kp-hepsi-izgara'), kaynak = P.querySelector('.kp-tek');
    each(S.querySelectorAll('.kp-hepsi-izgara'), function(x){ x.hidden = !D.hepsi || x !== G; });
    if(!D.hepsi || !G) return;
    if(!G._kuruldu){
      G.innerHTML = SIRA.map(function(id){ var a = ALT[id];
        return '<article class="pnl-card kp-hk kp-orn" data-alt="' + id + '"><div class="kp-hk-bas" data-kp-sec-alt="' + id + '" title="Bu alternatifi seç"><span class="kp-harf">' + a.harf + '</span><div><b>' + a.harf + ' · ' + a.ad + '</b><small>' + a.aile + '</small></div>'
          + '<span class="pstat ' + (a.guc === 'guclu' ? 'ok' : 'wait') + '">' + (a.guc === 'guclu' ? 'Güçlü' : 'Orta') + '</span></div><div class="kp-hk-govde"></div></article>'; }).join('');
      each(G.children, function(kart){
        var id = kart.dataset.alt, govde = kart.querySelector('.kp-hk-govde'), parca = [];
        if(D.sekme === 'durum' || D.sekme === 'kisi'){ var x = kaynak.querySelector('[data-alt-icerik="' + id + '"]'); if(x) parca = [x]; }
        else if(D.sekme === 'akis') parca = [kaynak.querySelector('.kp-akis')];
        else parca = kaynak.querySelectorAll('.kp-sekil-kap');
        each(parca, function(p){ var c = p.cloneNode(true); c.hidden = false; c.removeAttribute('id'); each(c.querySelectorAll('[id]'), function(y){ y.removeAttribute('id'); }); govde.appendChild(c); });
      });
      G._kuruldu = true;
    }
    each(G.children, function(kart){
      var id = kart.dataset.alt; ornYaz(kart, id); kart.classList.toggle('is-on', id === D.alt);
      each(kart.querySelectorAll('.kp-tuval'), function(t){ uygula(t, id); });
    });
    var hk = HK[D.sekme] || {}; G.style.setProperty('--hk', (hk[V.mecra[D.mecra]] || hk._ || 320) + 'px');
  }
  function sekmeGoster(){
    each(S.querySelectorAll('.sa-form-tab[data-sekme]'), function(t){ var on = t.dataset.sekme === D.sekme; t.classList.toggle('is-on', on); t.setAttribute('aria-selected', on ? 'true' : 'false'); });
    each(S.querySelectorAll('.sa-form-panel[data-sekme]'), function(p){ p.hidden = p.dataset.sekme !== D.sekme; });
  }
  function ciz(){
    S.dataset.kat = D.kat; S.dataset.mecra = D.mecra; S.dataset.alt = D.alt; S.dataset.sekme = D.sekme;
    if(D.guvenli) S.setAttribute('data-guvenli', ''); else S.removeAttribute('data-guvenli');
    if(D.hepsi) S.setAttribute('data-hepsi', ''); else S.removeAttribute('data-hepsi');
    sekmeGoster();
    each(S.querySelectorAll('.kp-tek.kp-orn, .kp-tek .kp-orn'), function(k){ ornYaz(k, D.alt); });
    each(S.querySelectorAll('.kp-tek .kp-tuval'), function(t){ uygula(t, D.alt); });
    each(S.querySelectorAll('[data-alt-icerik]'), function(x){ if(!x.closest('.kp-hk')) x.hidden = x.getAttribute('data-alt-icerik') !== D.alt; });
    each(S.querySelectorAll('.kp-serit-oge'), function(b){ var id = b.dataset.alt, on = id === D.alt; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', on ? 'true' : 'false');
      var k = b.querySelector('.kp-minik'); ornYaz(k, id); each(k.querySelectorAll('.kp-tuval'), function(t){ uygula(t, id); }); });
    var hb = S.querySelector('[data-kp-hepsi]'); if(hb) hb.setAttribute('aria-pressed', D.hepsi ? 'true' : 'false');
    hepsiKur();
    aracYaz();
    sigdir();
  }

  /* ---------- araç çubuğu ---------- */
  function sec(ad, v){ each(document.querySelectorAll('input[name="' + ad + '"]'), function(i){ i.checked = i.value === v; }); }
  function aracYaz(){
    var a = ALT[D.alt];
    each(document.querySelectorAll('[data-kp-yaz]'), function(x){
      var k = x.dataset.kpYaz;
      if(k === 'guc'){ var g = a.guc === 'guclu'; x.textContent = g ? 'Güçlü' : 'Orta'; x.className = 'pstat ' + (g ? 'ok' : 'wait'); }
      else x.textContent = a[k];
    });
    sec('kpKat', D.kat); sec('kpMecra', D.mecra);
    var gv = document.querySelector('input[data-kp="guvenli"]'); if(gv) gv.checked = D.guvenli;
    GRUP.forEach(function(g){
      var notlar = [];
      each(document.querySelectorAll('input[data-orn="' + g + '"]'), function(i){
        var p = pasif(D.alt, g, i.value), l = i.closest('label');
        i.checked = D.orn[D.alt][g] === i.value; i.disabled = !!p;
        if(l){ if(p){ l.title = p; notlar.push(i.parentNode.textContent.trim() + ': ' + p); } else l.removeAttribute('title'); }
      });
      var n = document.querySelector('[data-pasif-not="' + g + '"]'); if(n){ n.hidden = !notlar.length; n.textContent = notlar.join(' · '); }
    });
    var sn = document.querySelector('[data-kp-sus-not]');
    if(sn) sn.textContent = D.hepsi ? 'Yan yana görünümde süsleme yalnız seçili alternatife (' + a.harf + ' · ' + a.ad + ') uygulanır; başka bir kartın başlığına tıklayarak seçin.' : 'İskelet aynı kalır; yalnız süsleme değişir. Her alternatif kendi varsayılanından başlar.';
    var s = document.getElementById('kpSec'); if(s) s.checked = !!D.sec[D.alt];
    var n2 = document.getElementById('kpNot'); if(n2 && document.activeElement !== n2) n2.value = D.not[D.alt] || '';
    ozetYaz();
  }
  function ozetYaz(){
    var o = document.querySelector('#kpOzet .kp-secilen-metin'); if(!o) return;
    var secili = SIRA.filter(function(id){ return D.sec[id]; });
    if(!secili.length){ o.textContent = 'henüz seçilmedi; “Bunu Seç” ile işaretleyin.'; return; }
    o.textContent = secili.map(function(id){
      var a = ALT[id], degisen = GRUP.filter(function(g){ return D.orn[id][g] !== a.orn[g]; });
      var liste = degisen.map(function(g){ return V.grupad[g] + ' ' + V.ad[g][D.orn[id][g]].toLocaleLowerCase('tr'); });
      return a.harf + ' · ' + a.ad + ' (' + (liste.length ? liste.join(', ') : 'varsayılan süsleme') + ')' + (D.not[id] ? ' — not: ' + D.not[id] : '');
    }).join(' · ');
  }

  /* ---------- olaylar ---------- */
  document.addEventListener('change', function(e){
    var i = e.target;
    if(i.matches('input[data-orn]')){ if(i.checked && !i.disabled){ D.orn[D.alt][i.dataset.orn] = i.value; ciz(); } return; }
    if(i.matches('input[data-kp="kat"]')){ if(i.checked){ D.kat = i.value; ciz(); } return; }
    if(i.matches('input[data-kp="mecra"]')){ if(i.checked){ D.mecra = i.value; ciz(); } return; }
    if(i.matches('input[data-kp="guvenli"]')){ D.guvenli = i.checked; ciz(); return; }
    if(i.id === 'kpSec'){ D.sec[D.alt] = i.checked; ozetYaz(); }
  });
  document.addEventListener('input', function(e){ if(e.target.id === 'kpNot'){ D.not[D.alt] = e.target.value; ozetYaz(); } });
  document.addEventListener('click', function(e){
    var t = e.target.closest && e.target.closest('[data-kp-varsayilan], .kp-serit-oge, [data-kp-hepsi], [data-kp-kaydir], [data-kp-sec-alt], .sa-form-tab[data-sekme], [data-kp-yan-ac], [data-kp-yan-kapat]');
    if(!t) return;
    if(t.matches('[data-kp-varsayilan]')){ e.preventDefault(); D.orn[D.alt] = Object.assign({}, ALT[D.alt].orn); ciz(); return; }
    if(t.matches('.kp-serit-oge')){ D.alt = t.dataset.alt; D.hepsi = false; ciz(); t.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: 'smooth' }); return; }
    if(t.matches('[data-kp-hepsi]')){ D.hepsi = !D.hepsi; ciz(); return; }
    if(t.matches('[data-kp-kaydir]')){ serit.scrollBy({ left: +t.dataset.kpKaydir * serit.clientWidth * .8, behavior: 'smooth' }); return; }
    if(t.matches('[data-kp-sec-alt]')){ D.alt = t.dataset.kpSecAlt; ciz(); return; }
    if(t.matches('.sa-form-tab[data-sekme]')){ D.sekme = t.dataset.sekme; setTimeout(ciz, 0); return; }
    if(t.matches('[data-kp-yan-ac]')){ cekmece(true); return; }
    if(t.matches('[data-kp-yan-kapat]')){ cekmece(false); }
  });
  function cekmece(ac){
    arac.classList.toggle('is-acik', ac); if(perde) perde.hidden = !ac;
    var b = S.querySelector('[data-kp-yan-ac]'); if(b) b.setAttribute('aria-expanded', ac ? 'true' : 'false');
  }
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && arac.classList.contains('is-acik')) cekmece(false); });
  serit.addEventListener('keydown', function(e){
    if(e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    var i = SIRA.indexOf(D.alt) + (e.key === 'ArrowRight' ? 1 : -1); if(i < 0 || i >= SIRA.length) return;
    e.preventDefault(); var b = serit.querySelector('[data-alt="' + SIRA[i] + '"]'); b.click(); b.focus();
  });

  /* ---------- başlık sığdırma: başlık (ya da rakam) bloğa sığmıyorsa küçülür, kesilmez ---------- */
  function gor(x){ return x.getClientRects().length > 0; }
  function sigdir(kok){
    each((kok || S).querySelectorAll('.kp-tuval'), function(t){
      if(!gor(t)) return;
      var b = t.querySelector('.kp-blok'), hs = Array.prototype.filter.call(t.querySelectorAll('.kp-baslik, .kp-sayi'), gor);
      if(!hs.length) return;
      hs.forEach(function(h){ h.style.fontSize = ''; });
      var taban = hs.map(function(h){ return parseFloat(getComputedStyle(h).fontSize); }), k = 1;
      function tasiyor(){
        var r = b.getBoundingClientRect(), cs = getComputedStyle(b), pt = parseFloat(cs.paddingTop), pb = parseFloat(cs.paddingBottom);
        for(var i = 0; i < b.children.length; i++){ var c = b.children[i]; if(!gor(c) || getComputedStyle(c).position === 'absolute') continue; var cr = c.getBoundingClientRect();
          if(cr.top < r.top + pt - 1 || cr.bottom > r.bottom - pb + 1 || cr.right > r.right + 1) return true; }
        return hs.some(function(h){ return h.classList.contains('kp-baslik') && h.scrollHeight > h.clientHeight + 1; });
      }
      while(tasiyor() && k > .46){ k -= .04; hs.forEach(function(h, i){ h.style.fontSize = (taban[i] * k).toFixed(2) + 'px'; }); }
    });
  }

  /* ---------- ölçüm araçları ---------- */
  var ORNEK = { 3: ['Derbide', 'gol', 'yağmuru'], 14: ['Büyükşehir', 'belediyesi', 'yeni', 'toplu', 'taşıma', 'hattı', 'için', 'ihale', 'sürecini', 'başlattığını', 've', 'takvimin', 'netleştiğini', 'açıkladı'] };
  function metin(n){
    each(S.querySelectorAll('.kp-baslik .kp-bi'), function(x){
      if(x._asil === undefined) x._asil = x.innerHTML;
      if(!n){ x.innerHTML = x._asil; return; }
      var w = ORNEK[n].slice(), soz = !!x.closest('.kp-soz'), vi = n === 3 ? 1 : 3;
      w[vi] = '<em class="kp-vurgu">' + w[vi] + (n === 3 ? '' : ' ' + w.splice(vi + 1, 1)[0]) + '</em>';
      x.innerHTML = (soz ? '“' : '') + w.join(' ') + (soz ? '”' : '');
    });
    sigdir();
  }
  window.kp = { D: D, V: V, ciz: ciz, sigdir: sigdir, metin: metin, ayarla: function(o){ Object.assign(D, o); ciz(); }, sira: SIRA };

  if(document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ sigdir(); });
  window.addEventListener('resize', function(){ clearTimeout(sigdir._z); sigdir._z = setTimeout(function(){ sigdir(); }, 120); });
  ciz();
  (function(){ var b = serit.querySelector('.kp-serit-oge.is-on'); if(b && b.offsetLeft + b.offsetWidth > serit.clientWidth) serit.scrollLeft = b.offsetLeft - 12; })();
})();
