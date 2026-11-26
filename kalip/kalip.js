/* =====================================================================
   SOSYAL MEDYA KALIP ALTERNATİFLERİ · yalnız bu sayfanın betiği (ortak dosya değil)
   TEK DURUM NESNESİ (D): seçili alternatif, açık sekme, yan yana görünüm, kategori, mecra, güvenli alan,
   her alternatifin süslemesi, "Bunu Seç" ve notlar. Bütün denetimler D'ye yazar; ciz() sayfayı D'den çizer.
   - Tekli görünüm: sekmelerdeki tuvaller bir kez üretilmiştir; ciz() iskelet sınıfını (kp-a … kp-n), metin/logo zeminini
     (data-yz, data-lz) ve mecraya göre biçimi (data-bicim) yazar; süsleme .kp-orn kaplarına data-o-* olarak iner.
   - Yan yana görünüm: açık sekmenin içeriği bütün alternatifler için kopyalanır; her kart kendi süslemesini taşır.
   - Başlık sığdırma: başlık ya da rakam bloğa sığmıyorsa en çok %54 küçülür (kesilmez).
   Adres satırı: ?alt=c&sekme=haber&kat=spor&mecra=x&guvenli=1&hepsi=1 (sunum ve ölçüm için).
   Kalıp motoru (Yasin Bey, 25.11.2026): iskelet + mecra + süsleme; şeridin ilk öğesi hazır birleşim "Seçilen", Varsayılan ona döner.
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
    alt: ALT[q.get('alt')] ? q.get('alt') : V.varsayilan, /* sayfa motorun Seçilen birleşimiyle açılır (Yasin Bey) */
    sekme: SEKMELER.indexOf(q.get('sekme')) > -1 ? q.get('sekme') : 'akis',
    hepsi: q.get('hepsi') === '1',
    kat: /^(gundem|spor|kadin|finans|savunma)$/.test(q.get('kat') || '') ? q.get('kat') : 'gundem',
    mecra: V.mecra[q.get('mecra')] ? q.get('mecra') : 'ig',
    guvenli: q.get('guvenli') === '1',
    orn: {}, sec: {}, not: {}
  };
  SIRA.forEach(function(id){ D.orn[id] = Object.assign({}, ALT[id].orn); });
  var kontrol = document.getElementById('kpKontrol'), serit = document.getElementById('kpSerit');
  var each = function(l, f){ Array.prototype.forEach.call(l, f); };

  function pasif(id, g, v){ var p = ALT[id].pasif; return p && p[g] && p[g][v]; }
  function zemin(id, tip, bicim){
    var a = ALT[id];
    return [(tip === 'ic' && a.yz.ic) || a.yz._, (tip === 'ic' && a.lz.ic) || a.lz[bicim] || a.lz._];
  }
  function uygula(t, id){
    each(Array.prototype.slice.call(t.classList), function(c){ if(/^kp-[a-n]$/.test(c)) t.classList.remove(c); });
    t.classList.add('kp-' + (ALT[id].iskelet || id)); /* Seçilen gibi hazır birleşim bir iskeleti kullanır */
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
        return '<article class="pnl-card kp-hk kp-orn" data-alt="' + id + '"><div class="kp-hk-bas" data-kp-sec-alt="' + id + '" title="Bu alternatifi seç"><span class="kp-harf">' + a.harf + '</span><div><b>' + (a.hazir ? 'Seçilen · ' : '') + a.harf + ' · ' + a.ad + '</b><small>' + a.aile + '</small></div></div><div class="kp-hk-govde"></div></article>'; }).join('');
      each(G.children, function(kart){
        var id = kart.dataset.alt, govde = kart.querySelector('.kp-hk-govde'), parca = [];
        if(D.sekme === 'durum' || D.sekme === 'kisi'){ var x = kaynak.querySelector('[data-alt-icerik="' + id + '"]') || kaynak.querySelector('.kp-dis'); if(x) parca = [x]; }
        else if(D.sekme === 'akis') parca = [kaynak.querySelector('.kp-akis')];
        else parca = kaynak.querySelectorAll('.kp-sekil-kap:not(.kp-diger)');
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
    each(S.querySelectorAll('.kp-tek [data-kat-sabit]'), function(t){ t.hidden = t.dataset.katSabit === D.kat; });
    each(S.querySelectorAll('[data-alt-icerik]'), function(x){ if(!x.closest('.kp-hk')) x.hidden = x.getAttribute('data-alt-icerik') !== D.alt; });
    each(S.querySelectorAll('.kp-serit-oge'), function(b){ var id = b.dataset.alt, on = id === D.alt; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', on ? 'true' : 'false');
      var k = b.querySelector('.kp-minik'); ornYaz(k, id); each(k.querySelectorAll('.kp-tuval'), function(t){ uygula(t, id); }); });
    var hb = S.querySelector('[data-kp-hepsi]'); if(hb) hb.setAttribute('aria-pressed', D.hepsi ? 'true' : 'false');
    hepsiKur();
    aracYaz();
    sigdir();
  }

  /* ---------- kontrol alanı (üstte, yapışkan) ---------- */
  var DIKEY_SEKME = ['akis', 'dikey', 'durum', 'kisi'];
  function aracYaz(){
    each(S.querySelectorAll('[data-kp-mecra]'), function(b){ var on = b.dataset.kpMecra === D.mecra; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', on ? 'true' : 'false'); });
    var gv = S.querySelector('input[data-kp="guvenli"]'), gl = document.getElementById('kpGuvAnahtar');
    var P0 = document.getElementById('kpT-' + D.sekme), anlamli = !!(P0 && Array.prototype.some.call(P0.querySelectorAll('.kp-tuval[data-bicim="uzun"]'), function(t){ return !t.closest('[hidden]'); }));
    if(gv){ gv.checked = D.guvenli; gv.disabled = !anlamli; }
    if(gl){ gl.classList.toggle('is-pasif', !anlamli); if(anlamli) gl.removeAttribute('title'); else gl.title = 'Bu görünümde 9:16 kart yok: Dikey 9:16 mecrası ya da Hikâye ve Reels sekmesi'; }
    each(S.querySelectorAll('[data-kp-acilir]'), function(dd){
      var g = dd.dataset.kpAcilir, sec = g === 'kat' ? D.kat : D.orn[D.alt][g], ad = '';
      each(dd.querySelectorAll('[data-kp-sec]'), function(b){
        var on = b.dataset.v === sec, p = g === 'kat' ? '' : pasif(D.alt, g, b.dataset.v);
        b.classList.toggle('is-sec', on); b.setAttribute('aria-selected', on ? 'true' : 'false');
        b.classList.toggle('is-pasif', !!p); if(p){ b.setAttribute('aria-disabled', 'true'); b.title = p; } else { b.removeAttribute('aria-disabled'); b.removeAttribute('title'); }
        if(on) ad = b.textContent;
      });
      dd.querySelector('.ks-deger').textContent = ad;
      dd.classList.toggle('is-degisti', g !== 'kat' && D.orn[D.alt][g] !== ALT[D.alt].orn[g]);
    });
    var s = document.getElementById('kpSec'); if(s) s.checked = !!D.sec[D.alt];
    var secili = SIRA.filter(function(id){ return D.sec[id]; }), say = document.getElementById('kpSayac');
    if(say){ say.hidden = !secili.length; say.querySelector('b').textContent = secili.length;
      say.title = secili.map(function(id){ var a = ALT[id], deg = GRUP.filter(function(g){ return D.orn[id][g] !== a.orn[g]; });
        return a.harf + ' · ' + a.ad + (deg.length ? ' (' + deg.map(function(g){ return V.grupad[g] + ' ' + V.ad[g][D.orn[id][g]].toLocaleLowerCase('tr'); }).join(', ') + ')' : ''); }).join(' · '); }
  }

  /* ---------- olaylar ---------- */
  document.addEventListener('change', function(e){
    var i = e.target;
    if(i.matches('input[data-orn]')){ if(i.checked && !i.disabled){ D.orn[D.alt][i.dataset.orn] = i.value; ciz(); } return; }
    if(i.matches('input[data-kp="kat"]')){ if(i.checked){ D.kat = i.value; ciz(); } return; }
    if(i.matches('input[data-kp="mecra"]')){ if(i.checked){ D.mecra = i.value; ciz(); } return; }
    if(i.matches('input[data-kp="guvenli"]')){ D.guvenli = i.checked; ciz(); return; }
    if(i.id === 'kpSec'){ D.sec[D.alt] = i.checked; aracYaz(); }
  });
  document.addEventListener('click', function(e){
    var t = e.target.closest && e.target.closest('[data-kp-varsayilan], .kp-serit-oge, [data-kp-hepsi], [data-kp-kaydir], [data-kp-sec-alt], .sa-form-tab[data-sekme], [data-kp-mecra], [data-kp-sec]');
    if(!t) return;
    if(t.matches('[data-kp-varsayilan]')){ e.preventDefault(); D.alt = V.varsayilan; D.orn[D.alt] = Object.assign({}, ALT[D.alt].orn); ciz(); return; } /* Varsayılan = Seçilen (Yasin Bey) */
    if(t.matches('.kp-serit-oge')){ D.alt = t.dataset.alt; D.hepsi = false; ciz(); t.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: 'smooth' }); return; }
    if(t.matches('[data-kp-hepsi]')){ D.hepsi = !D.hepsi; ciz(); return; }
    if(t.matches('[data-kp-kaydir]')){ serit.scrollBy({ left: +t.dataset.kpKaydir * serit.clientWidth * .8, behavior: 'smooth' }); return; }
    if(t.matches('[data-kp-sec-alt]')){ D.alt = t.dataset.kpSecAlt; ciz(); return; }
    if(t.matches('.sa-form-tab[data-sekme]')){ D.sekme = t.dataset.sekme; setTimeout(ciz, 0); return; }
    if(t.matches('[data-kp-mecra]')){ D.mecra = t.dataset.kpMecra; ciz(); return; }
    if(t.matches('[data-kp-sec]')){
      e.preventDefault(); if(t.getAttribute('aria-disabled') === 'true') return;
      var g = t.dataset.kpSec; if(g === 'kat') D.kat = t.dataset.v; else D.orn[D.alt][g] = t.dataset.v;
      var dd = t.closest('[data-kp-acilir]'), b = dd && dd.querySelector('.kb-secim-btn'); if(b && b.getAttribute('aria-expanded') === 'true') b.click();
      ciz(); return;
    }
  });
  /* yapışkan kompakt hal: sayfa kayınca şerit küçülür; mecra, sekmeler ve süsleme görünür kalır */
  /* eşik gecikmeli: küçülme kontrol alanının boyunu azaltır, tarayıcı kaydırmayı o kadar geri çeker; çıkış eşiği bu farkın altında
     olmazsa açık/kompakt arasında sonsuz gidip gelir (sayfa titrer) */
  var kompaktEsik = 0, kompaktFark = 0;
  function kompakt(){ if(!kontrol) return;
    var acik = kontrol.classList.contains('is-kompakt'), y = window.scrollY;
    if(getComputedStyle(kontrol).position !== 'sticky'){ if(acik) kontrol.classList.remove('is-kompakt'); return; } /* dar ekranda yapışkan değil: küçülme yalnız içeriği zıplatır */
    var k = acik ? y > Math.max(0, kompaktEsik - kompaktFark - 40) : y > kompaktEsik;
    if(k === acik) return;
    var h0 = kontrol.offsetHeight; kontrol.classList.toggle('is-kompakt', k);
    if(k) kompaktFark = Math.max(kompaktFark, h0 - kontrol.offsetHeight); }
  window.addEventListener('scroll', kompakt, { passive: true });
  if(kontrol) kompaktEsik = kontrol.getBoundingClientRect().top + window.scrollY + 8;
  serit.addEventListener('keydown', function(e){
    if(e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    var i = SIRA.indexOf(D.alt) + (e.key === 'ArrowRight' ? 1 : -1); if(i < 0 || i >= SIRA.length) return;
    e.preventDefault(); var b = serit.querySelector('[data-alt="' + SIRA[i] + '"]'); b.click(); b.focus();
  });

  /* ---------- başlık sığdırma: başlık (ya da rakam) bloğa sığmıyorsa küçülür, kesilmez ---------- */
  function gor(x){ return x.getClientRects().length > 0; }
  function satir(h){ var u = {}; Array.prototype.forEach.call(h.querySelector('.kp-bi') ? h.querySelector('.kp-bi').getClientRects() : [], function(r){ if(r.width > 1) u[Math.round(r.top)] = 1; }); return Object.keys(u).length; }
  var KUCUK = .044; /* okunurluk alt sınırı: başlık en az tuvalin kısa kenarının %5'i (dikey ve kare biçimde 5cqw) */
  function sigdir(kok){
    each((kok || S).querySelectorAll('.kp-tuval'), function(t){
      if(!gor(t)) return;
      t.style.setProperty('--tw', t.getBoundingClientRect().width.toFixed(1) + 'px'); /* köşe: tuvalin kendi genişliğinden (kendi cqw'si yok) */
      var b = t.querySelector('.kp-blok'), hs = Array.prototype.filter.call(t.querySelectorAll('.kp-baslik, .kp-sayi'), gor);
      if(!hs.length) return;
      hs.forEach(function(h){ h.style.fontSize = ''; });
      var taban = hs.map(function(h){ return parseFloat(getComputedStyle(h).fontSize); }), k = 1;
      var tr = t.getBoundingClientRect(), alt_ = KUCUK * Math.min(tr.width, tr.height);
      hs.forEach(function(h, i){ if(h.classList.contains('kp-baslik') && taban[i] < alt_){ taban[i] = alt_; h.style.fontSize = alt_.toFixed(2) + 'px'; } }); /* taban ölçü de alt sınırın altına inmez */
      function tasiyor(){
        var r = b.getBoundingClientRect(), cs = getComputedStyle(b), pt = parseFloat(cs.paddingTop), pb = parseFloat(cs.paddingBottom);
        for(var i = 0; i < b.children.length; i++){ var c = b.children[i]; if(!gor(c) || getComputedStyle(c).position === 'absolute') continue; var cr = c.getBoundingClientRect();
          if(cr.top < r.top + pt - 1 || cr.bottom > r.bottom - pb + 1 || cr.right > r.right + 1) return true; }
        return hs.some(function(h){ return h.classList.contains('kp-baslik') && (h.scrollHeight > h.clientHeight + parseFloat(getComputedStyle(h).fontSize) * .3 || (satir(h) > 3 && parseFloat(getComputedStyle(h).fontSize) > alt_ + .01)); }); /* 3 satıra sığmayan başlık küçülür; alt sınırda en çok 4 satır */
      }
      while(tasiyor() && k > .3){ k -= .04; hs.forEach(function(h, i){ var f = taban[i] * k; if(h.classList.contains('kp-baslik')) f = Math.max(f, alt_); h.style.fontSize = f.toFixed(2) + 'px'; });
        if(hs.some(function(h){ return h.classList.contains('kp-baslik'); }) && hs.every(function(h, i){ return !h.classList.contains('kp-baslik') || taban[i] * k <= alt_; })) break; }
    });
    each((kok || S).querySelectorAll('.kp-tuval'), panelSigdir);
  }
  /* PANEL İÇERİĞE GÖRE (Beyar 26.11): iç sayfa ve liste kartlarında satırlar yayılmaz. Sırayla:
     1) liste yazısı boşluk varsa en çok %30 büyür; 2) fotoğraf ÜSTTE şeritse fotoğraf içeriğin üstüne kadar uzar (içerik uzunsa
     panel yukarı büyür); 3) fotoğraf ALTTAysa (C) fotoğraf içeriğin altına kadar uzar (içerik uzunsa panel aşağı büyür). */
  var PANEL = '.kp-liste,.kd-liste,.kd-tablo,.kd-grafik,.kd-secenekler,.kd-akis,.kd-skor,.kd-hava-gunler,.kd-bilgi,.kd-cagri,.kd-ses,.kd-soru-kutu,.kd-zaman';
  function icerik(b){ var u = Infinity, a = -Infinity;
    each(b.children, function(c){ if(!gor(c) || getComputedStyle(c).position === 'absolute') return; var r = c.getBoundingClientRect(); u = Math.min(u, r.top); a = Math.max(a, r.bottom); });
    return u === Infinity ? null : { ust: u, alt: a }; }
  function panelSigdir(t){
    var g = t.querySelector('.kp-gorsel'), kr = t.querySelector('.kp-karart'), sk = t.querySelector('.kp-sekil'), b = t.querySelector('.kp-blok');
    if(!g || !b) return;
    var lis = Array.prototype.filter.call(b.querySelectorAll(':scope > :is(.kp-liste, .kd-liste) li, :scope > .kd-tablo .kd-tr'), gor); /* kategori sarmalının içindekiler dahil, yalnız görünenler */
    g.style.bottom = g.style.top = ''; if(kr) kr.style.bottom = kr.style.top = ''; if(sk){ sk.style.top = ''; sk.style.height = ''; } b.style.top = b.style.bottom = b.style.justifyContent = '';
    each(lis, function(li){ li.style.fontSize = ''; });
    if(!gor(t) || !gor(b)) return;
    var tr = t.getBoundingClientRect(), br = b.getBoundingClientRect(), bs = getComputedStyle(b), ic = icerik(b); if(!ic) return;
    var ici = br.height - parseFloat(bs.paddingTop) - parseFloat(bs.paddingBottom);
    /* 1 · yazı büyür (yalnız gerçekten boş yer varsa; taşırmadan) */
    if(lis.length){
      var taban = Array.prototype.map.call(lis, function(li){ return parseFloat(getComputedStyle(li).fontSize); }), k = 1;
      while(k < 1.3){ var bos = ici - (ic.alt - ic.ust); if(bos < .06 * tr.height) break;
        k += .04; each(lis, function(li, n){ li.style.fontSize = (taban[n] * k).toFixed(2) + 'px'; }); ic = icerik(b);
        if(ic.alt - ic.ust > ici){ k -= .04; each(lis, function(li, n){ li.style.fontSize = (taban[n] * k).toFixed(2) + 'px'; }); ic = icerik(b); break; } }
    }
    if(t.dataset.tip !== 'ic' && !t.querySelector(PANEL)) return; /* iç sayfa ya da panel içeriği (liste, tablo, maç, ses…) taşıyan kart */
    var gr = g.getBoundingClientRect(), pay = .055 * Math.min(tr.width, tr.height), en = .2 * tr.height;
    function kucult(sinir){ /* içerik sınıra sığmıyorsa liste yazısı en çok %30 küçülür */
      if(!lis.length) return; var kk = 1, tb = lis.map(function(li){ return parseFloat(li.style.fontSize || getComputedStyle(li).fontSize); });
      while(ic.alt - ic.ust > sinir && kk > .7){ kk -= .04; lis.forEach(function(li, n){ li.style.fontSize = (tb[n] * kk).toFixed(2) + 'px'; }); ic = icerik(b); } }
    var serit = gr.top <= tr.top + .25 * tr.height && gr.left <= tr.left + .25 * tr.width && gr.right >= tr.right - .12 * tr.width && gr.bottom < tr.bottom - 2 && gr.bottom < tr.top + .75 * tr.height && !/\bkp-[emn]\b/.test(t.className);
    var altta = gr.bottom >= tr.bottom - 2 && gr.top > tr.top + .3 * tr.height;
    if(serit){
      kucult(br.bottom - parseFloat(bs.paddingBottom) - (tr.top + en + pay));
      var icY = br.bottom - parseFloat(bs.paddingBottom) - (ic.alt - ic.ust); /* içerik alta yaslı olduğundaki üst kenarı */
      var yeni = Math.max(icY - pay, tr.top + en);
      if(Math.abs(yeni - gr.bottom) < 1) return;
      var alt = (tr.bottom - yeni).toFixed(1) + 'px', skAyni = sk && gor(sk) && Math.abs(sk.getBoundingClientRect().top - gr.bottom) < 2;
      g.style.bottom = alt; if(kr) kr.style.bottom = alt; if(skAyni){ sk.style.top = 'auto'; sk.style.height = alt; }
      b.style.top = (yeni + pay - tr.top).toFixed(1) + 'px'; b.style.justifyContent = 'flex-start';
    } else if(altta){
      kucult(tr.bottom - en - pay - br.top - parseFloat(bs.paddingTop));
      var icA = br.top + parseFloat(bs.paddingTop) + (ic.alt - ic.ust); /* içerik üste yaslı olduğundaki alt kenarı */
      var yeniU = Math.min(icA + pay, tr.bottom - en);
      if(Math.abs(yeniU - gr.top) < 1) return;
      var ust = (yeniU - tr.top).toFixed(1) + 'px';
      g.style.top = ust; if(kr) kr.style.top = ust;
      b.style.bottom = (tr.bottom - yeniU + pay).toFixed(1) + 'px'; b.style.justifyContent = 'flex-start';
    } else {
      /* fotoğraf şerit değil (kart, çerçeve, mercek, kesik…): içerik sığmıyorsa liste yazısı en çok %30 küçülür; boş yer varsa içerik panelin altına oturur */
      var tamFoto = gr.top <= tr.top + 2 && gr.bottom >= tr.bottom - 2 && gr.left <= tr.left + 2 && gr.right >= tr.right - 2, sekilVar = sk && gor(sk) && getComputedStyle(sk).display !== 'none';
      if(ic.alt - ic.ust > ici && lis.length){ var kk = 1, tb = Array.prototype.map.call(lis, function(li){ return parseFloat(getComputedStyle(li).fontSize); });
        while(ic.alt - ic.ust > ici && kk > .7){ kk -= .04; each(lis, function(li, n){ li.style.fontSize = (tb[n] * kk).toFixed(2) + 'px'; }); ic = icerik(b); } }
      if(ici - (ic.alt - ic.ust) > .06 * tr.height && (!tamFoto || sekilVar)) b.style.justifyContent = 'flex-end';
    }
  }

  /* ---------- ölçüm araçları ---------- */
  var ORNEK = { 3: ['Derbide', 'gol', 'yağmuru'], 14: ['Büyükşehir', 'belediyesi', 'yeni', 'toplu', 'taşıma', 'hattı', 'için', 'ihale', 'sürecini', 'başlattığını', 've', 'takvimin', 'netleştiğini', 'açıkladı'] };
  function metin(n){
    KUCUK = n === 14 ? .038 : .044; /* 14 kelimelik sınama başlığında alt sınır %4,4 (dar dikey yerleşimlerde 3–4 satıra ancak böyle sığar) */
    each(S.querySelectorAll('.kp-baslik .kp-bi'), function(x){
      if(x._asil === undefined) x._asil = x.innerHTML;
      if(!n){ x.innerHTML = x._asil; return; }
      var w = ORNEK[n].slice(), soz = !!x.closest('.kp-soz'), vi = n === 3 ? 1 : 3;
      w[vi] = '<em class="kp-vurgu">' + w[vi] + (n === 3 ? '' : ' ' + w.splice(vi + 1, 1)[0]) + '</em>';
      x.innerHTML = (soz ? '“' : '') + w.join(' ') + (soz ? '”' : '');
    });
    sigdir();
  }
  window.kp = { kucuk: function(){ return KUCUK; }, satir: satir, D: D, V: V, ciz: ciz, sigdir: sigdir, metin: metin, ayarla: function(o){ Object.assign(D, o); ciz(); }, sira: SIRA, KUCUK: KUCUK };

  if(document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ sigdir(); });
  window.addEventListener('resize', function(){ clearTimeout(sigdir._z); sigdir._z = setTimeout(function(){ sigdir(); }, 120); });
  ciz();
  (function(){ var b = serit.querySelector('.kp-serit-oge.is-on'); if(b && b.offsetLeft + b.offsetWidth > serit.clientWidth) serit.scrollLeft = b.offsetLeft - 12; })();
})();
/* Açılır listeler: bu sayfa kabuk.js'i yüklemez; çekirdekteki aç/kapa davranışının aynısı (data-acilir → .pnl-menu.open) */
(function(){
  function kapat(haric){
    document.querySelectorAll('[data-acilir][aria-expanded="true"]').forEach(function(b){
      if(b === haric) return; b.setAttribute('aria-expanded', 'false');
      var m = document.getElementById(b.getAttribute('data-acilir')); if(m) m.classList.remove('open');
    });
  }
  document.addEventListener('click', function(e){
    var b = e.target.closest('[data-acilir]');
    if(b){
      var m = document.getElementById(b.getAttribute('data-acilir')), ac = b.getAttribute('aria-expanded') !== 'true';
      kapat(b); b.setAttribute('aria-expanded', ac ? 'true' : 'false'); if(m) m.classList.toggle('open', ac);
      return;
    }
    if(!e.target.closest('.pnl-menu')) kapat();
  }, true);
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape') kapat(); });
})();
