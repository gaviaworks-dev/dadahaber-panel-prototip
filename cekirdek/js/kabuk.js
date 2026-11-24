/* =====================================================================
   ÇEKİRDEK · KABUK davranışı (K13: menü HTML'ini betik yazar, bu dosya
   yalnızca etkin kalemi, rolü, izinleri ve grup açık/kapalı durumunu işaretler)
   Kayıt: window.PANEL (cekirdek/js/kayit.js, moduller.json'dan üretilir)
   ===================================================================== */
(function(){
  var P = window.PANEL || {};
  var q = new URLSearchParams(location.search);
  var doc = document.documentElement;

  /* ---- önizleme teması (yalnızca secenekler/ için): ?tema=<ad> ---- */
  var tema = q.get('tema');
  if(tema && /^[a-z0-9-]+$/.test(tema)){
    var link = document.querySelector('link[data-tema]');
    if(link) link.href = link.getAttribute('href').replace(/tema\/[^/?]+\.css(\?v=\w+)?$/, 'secenekler/kabuk-tema/'+tema+'.css');
  }

  /* ---- rol: ?rol= > localStorage > super ---- */
  var ROLLER = P.roller || {};
  function rolOku(){
    var r = q.get('rol');
    if(r && ROLLER[r]){ try{localStorage.setItem('dh_rol', r);}catch(e){} return r; }
    try{ r = localStorage.getItem('dh_rol'); }catch(e){}
    return ROLLER[r] ? r : 'super';
  }

  function izinVar(rol, grup){
    var g = (ROLLER[rol] || {}).izin_gruplari || [];
    return g.indexOf('*') > -1 || g.indexOf(grup) > -1;
  }

  function rolUygula(rol){
    doc.dataset.rol = rol;
    document.querySelectorAll('[data-roller]').forEach(function(el){
      el.hidden = el.getAttribute('data-roller').split(/\s+/).indexOf(rol) === -1;
    });
    document.querySelectorAll('[data-izin]').forEach(function(el){
      el.hidden = !izinVar(rol, el.getAttribute('data-izin'));
    });
    document.querySelectorAll('[data-izin-yok]').forEach(function(el){
      el.hidden = izinVar(rol, el.getAttribute('data-izin-yok'));
    });
    /* kayıttan kapatılan modülün kutusu rolden bağımsız gizli kalır (menu_yaz.py) */
    document.querySelectorAll('[data-modul-kapali]').forEach(function(el){ el.hidden = true; });
    /* hiç kalemi kalmayan grubu gizle */
    document.querySelectorAll('.sa-mgrp').forEach(function(g){
      g.hidden = !g.querySelector('.sa-mlink:not([hidden])');
    });
    /* persona */
    var per = (P.personalar || {})[rol] || {};
    var set = function(id, v){ var el = document.getElementById(id); if(el && v) el.textContent = v; };
    set('pmName', per.ad); set('pmRole', per.unvan); set('pmAva', per.bas_harf);
    set('pmMenuAd', per.ad); set('pmMenuEposta', per.eposta);
    set('krAd', (ROLLER[rol] || {}).ad);
    document.querySelectorAll('[data-rol-sec]').forEach(function(b){
      var on = b.getAttribute('data-rol-sec') === rol;
      b.classList.toggle('is-sec', on);
      b.setAttribute('aria-checked', on ? 'true' : 'false');
    });
    bildirimSay();
    document.querySelectorAll('[data-persona]').forEach(function(el){
      var v = per[el.getAttribute('data-persona')]; if(v) el.textContent = v;
    });
    /* role bağlı bileşenler (okuma onayı vb.) bu olayı dinler */
    document.dispatchEvent(new CustomEvent('kb-rol', { detail: rol }));
  }

  /* ---- etkin kalem ---- */
  var etkin = document.body.dataset.sayfa || '';
  if(document.body.dataset.yakinda) etkin = q.get('s') || '';
  var etkinGrup = null;
  document.querySelectorAll('.sa-mlink[data-sayfa]').forEach(function(a){
    if(a.getAttribute('data-sayfa') === etkin){
      a.classList.add('is-active'); a.setAttribute('aria-current', 'page');
      var g = a.closest('.sa-mgrp'); if(g){ etkinGrup = g; g.classList.add('is-etkin'); }
    }
  });

  /* ---- gruplar: katlanır, etkin grup hep açık, durum hatırlanır (K3) ---- */
  var ayar = P.menu || {};
  var kapali = [];
  if(ayar.durumu_hatirla){ try{ kapali = JSON.parse(localStorage.getItem('dh_menu_kapali') || '[]'); }catch(e){} }
  function grupDurum(g, kapat){
    if(kapat && ayar.etkin_grup_acik && g === etkinGrup) kapat = false;
    g.classList.toggle('is-kapali', kapat);
    var b = g.querySelector('.sa-msec'); if(b) b.setAttribute('aria-expanded', kapat ? 'false' : 'true');
  }
  document.querySelectorAll('.sa-mgrp').forEach(function(g){
    grupDurum(g, ayar.katlanir && kapali.indexOf(g.dataset.grup) > -1);
    var b = g.querySelector('.sa-msec');
    if(!b || !ayar.katlanir) return;
    b.addEventListener('click', function(){
      if(ayar.etkin_grup_acik && g === etkinGrup) return;
      grupDurum(g, !g.classList.contains('is-kapali'));
      kapali = Array.prototype.filter.call(document.querySelectorAll('.sa-mgrp.is-kapali'), function(x){return true;}).map(function(x){ return x.dataset.grup; });
      if(ayar.durumu_hatirla){ try{ localStorage.setItem('dh_menu_kapali', JSON.stringify(kapali)); }catch(e){} }
    });
  });

  /* etkin kalemi menünün görünen alanına getir (açık ya da daraltılmış her halde) */
  function etkiniGoster(){
    var ak = document.querySelector('.sa-mlink.is-active'), nav = document.querySelector('.sa-mnav');
    if(!ak || !nav) return;
    var r = ak.getBoundingClientRect(), n = nav.getBoundingClientRect();
    if(r.top < n.top || r.bottom > n.bottom) nav.scrollTop += (r.top - n.top) - (n.height - r.height) / 2;
  }

  /* ---- menü daraltma (≥1025): biçim ve ilk hal erken.js'te uygulandı ---- */
  var bicim = doc.dataset.daraltma || 'yok';
  var dar = doc.classList.contains('kb-dar');
  var grip = document.getElementById('saDivider');
  function darAyarla(d, kaydet){
    dar = d;
    doc.classList.toggle('kb-dar', d);
    if(grip) grip.setAttribute('aria-label', d ? 'Menüyü genişlet' : 'Menüyü daralt');
    if(grip) grip.setAttribute('aria-expanded', d ? 'false' : 'true');
    if(kaydet){ try{ localStorage.setItem('dh_menu_dar', d ? '1' : '0'); }catch(e){} }
    setTimeout(etkiniGoster, 280);
  }
  darAyarla(dar, false);

  /* menünün kaydırma yeri sayfalar arasında korunur; etkin kalem görünmüyorsa ona getirilir */
  var nav = document.querySelector('.sa-mnav');
  if(nav){
    try{ var k = sessionStorage.getItem('dh_menu_kaydir'); if(k !== null) nav.scrollTop = +k; }catch(e){}
    var sakla = function(){ try{ sessionStorage.setItem('dh_menu_kaydir', String(nav.scrollTop)); }catch(e){} };
    nav.addEventListener('click', sakla);
    window.addEventListener('pagehide', sakla);
  }
  etkiniGoster();
  requestAnimationFrame(function(){ requestAnimationFrame(function(){ doc.classList.remove('kb-yukleniyor'); }); });
  if(grip && bicim !== 'yok'){
    var surukle = false, basX = 0, oynadi = false;
    grip.addEventListener('pointerdown', function(e){ surukle = true; oynadi = false; basX = e.clientX; grip.classList.add('is-drag'); try{ grip.setPointerCapture(e.pointerId); }catch(_){} });
    grip.addEventListener('pointermove', function(e){
      if(!surukle) return;
      var dx = e.clientX - basX; if(Math.abs(dx) > 5) oynadi = true;
      if(dx < -26 && !dar) darAyarla(true, true);
      else if(dx > 26 && dar) darAyarla(false, true);
    });
    var bitir = function(){ if(surukle && !oynadi) darAyarla(!dar, true); surukle = false; grip.classList.remove('is-drag'); };
    grip.addEventListener('pointerup', bitir);
    grip.addEventListener('pointercancel', function(){ surukle = false; grip.classList.remove('is-drag'); });
    grip.addEventListener('keydown', function(e){ if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); darAyarla(!dar, true); } });
  }

  /* ---- ipucu: daraltılmış menüde kalem adı (menü kaydırılabildiği için gövdeye eklenir) ---- */
  var ipucu = document.createElement('div'); ipucu.className = 'kb-ipucu'; ipucu.setAttribute('aria-hidden', 'true');
  document.body.appendChild(ipucu);
  document.querySelectorAll('.sa-menu [data-tip]').forEach(function(el){
    el.addEventListener('mouseenter', function(){
      if(!(dar && bicim === 'ikon') || window.innerWidth <= 1024) return;
      var r = el.getBoundingClientRect();
      ipucu.textContent = el.getAttribute('data-tip');
      ipucu.style.left = (r.right + 12) + 'px';
      ipucu.style.top = (r.top + r.height / 2 - 14) + 'px';
      ipucu.classList.add('on');
    });
    el.addEventListener('mouseleave', function(){ ipucu.classList.remove('on'); });
  });

  /* ---- bildirimler: okunmamış sayısı role göre; tümünü okundu say ---- */
  function bildirimSay(){
    var n = document.querySelectorAll('.kb-bld.is-yeni:not([hidden])').length;
    var s = document.querySelector('.kb-bld-say'); if(s) s.textContent = n ? n + ' okunmamış' : 'Hepsi okundu';
    var dot = document.querySelector('.pnl-bell .pb-dot'); if(dot) dot.hidden = !n;
    var b = document.querySelector('[data-bld-oku]'); if(b) b.hidden = !n;
  }
  try{ if(sessionStorage.getItem('dh_bld_okundu') === '1') document.querySelectorAll('.kb-bld.is-yeni').forEach(function(a){ a.classList.remove('is-yeni'); }); }catch(e){}
  var okuBtn = document.querySelector('[data-bld-oku]');
  if(okuBtn) okuBtn.addEventListener('click', function(e){
    e.stopPropagation();
    document.querySelectorAll('.kb-bld.is-yeni').forEach(function(a){ a.classList.remove('is-yeni'); });
    try{ sessionStorage.setItem('dh_bld_okundu', '1'); }catch(_){}
    bildirimSay();
  });

  /* ---- genel arama: ekranlar (role ve açık modüle göre) + haberlerde ara ---- */
  var ara = document.getElementById('pnlAra'), sonuc = document.getElementById('araSonuc');
  function trKucuk(s){ return (s || '').toLocaleLowerCase('tr'); }
  function araGoster(){
    if(!ara || !sonuc) return;
    var v = trKucuk(ara.value.trim()), rol = doc.dataset.rol, html = '', n = 0;
    document.querySelectorAll('.sa-mlink[data-sayfa]:not([hidden])').forEach(function(a){
      var s = (P.sayfalar || {})[a.getAttribute('data-sayfa')] || {};
      var ad = a.getAttribute('data-tip') || '';
      if(v && trKucuk(ad + ' ' + (s.modul_ad || '')).indexOf(v) === -1) return;
      if(n >= 8) return; n++;
      html += '<a href="' + a.getAttribute('href') + '" role="option"><i class="' + a.querySelector('i').className + '" aria-hidden="true"></i>' + ad.replace(/</g,'&lt;') + '<span class="kb-ara-ek">' + (s.modul_ad || '') + '</span></a>';
    });
    var hb = document.querySelector('.sa-mlink[data-sayfa="haberler.liste"]:not([hidden])');
    var ust = v && hb ? '<div class="kb-ara-grup">Haberler</div><a href="' + hb.getAttribute('href') + '" role="option"><i class="fa-solid fa-magnifying-glass" aria-hidden="true"></i>Haberlerde ara: “' + ara.value.trim().replace(/</g,'&lt;') + '”</a>' : '';
    sonuc.innerHTML = ust + '<div class="kb-ara-grup">' + (v ? 'Ekranlar' : 'Hızlı geçiş') + '</div>' + (html || '<div class="kb-ara-bos">Bu adla bir ekran yok.</div>');
    sonuc.classList.add('open'); ara.setAttribute('aria-expanded', 'true'); ara.parentNode.classList.add('is-acik');
  }
  function araKapat(){ if(sonuc){ sonuc.classList.remove('open'); } if(ara){ ara.setAttribute('aria-expanded', 'false'); ara.parentNode.classList.remove('is-acik'); } }
  if(ara){
    ara.addEventListener('focus', araGoster);
    ara.addEventListener('input', araGoster);
    ara.addEventListener('keydown', function(e){
      var ops = sonuc ? Array.prototype.slice.call(sonuc.querySelectorAll('a')) : [];
      var i = ops.findIndex(function(o){ return o.classList.contains('kb-ara-sec'); });
      if(e.key === 'ArrowDown' || e.key === 'ArrowUp'){
        e.preventDefault(); if(!ops.length) return;
        if(i > -1) ops[i].classList.remove('kb-ara-sec');
        i = e.key === 'ArrowDown' ? (i + 1) % ops.length : (i <= 0 ? ops.length - 1 : i - 1);
        ops[i].classList.add('kb-ara-sec');
      } else if(e.key === 'Enter'){
        var hedef = ops[i > -1 ? i : 0]; if(hedef){ e.preventDefault(); location.href = hedef.href; }
      } else if(e.key === 'Escape'){ araKapat(); ara.blur(); }
    });
    document.addEventListener('click', function(e){ if(!e.target.closest('.pnl-search')) araKapat(); });
  }

  /* ---- açılır menüler (rol, hesap) ---- */
  function kapatHepsi(haric){
    document.querySelectorAll('[data-acilir][aria-expanded="true"]').forEach(function(b){
      if(b === haric) return;
      b.setAttribute('aria-expanded', 'false');
      var m = document.getElementById(b.getAttribute('data-acilir')); if(m) m.classList.remove('open');
    });
  }
  /* açılır kutular: belgeye tek dinleyici (çekmece ya da pencerede sonradan eklenenler de çalışır) */
  document.addEventListener('click', function(e){
    var b = e.target.closest('[data-acilir]');
    if(b){
      e.stopPropagation();
      var m = document.getElementById(b.getAttribute('data-acilir'));
      if(!m){ var kap = b.parentNode; m = kap && kap.querySelector('#' + b.getAttribute('data-acilir')); }
      var ac = b.getAttribute('aria-expanded') !== 'true';
      kapatHepsi(b);
      b.setAttribute('aria-expanded', ac ? 'true' : 'false');
      if(m) m.classList.toggle('open', ac);
      return;
    }
    if(!e.target.closest('.pnl-menu')) kapatHepsi();
  });
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape'){ kapatHepsi(); document.body.classList.remove('nav-open'); }
    if((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k'){
      var s = document.getElementById('pnlAra'); if(s){ e.preventDefault(); s.focus(); }
    }
  });

  /* ---- rol seçimi ---- */
  document.querySelectorAll('[data-rol-sec]').forEach(function(b){
    b.setAttribute('role', 'menuitemradio');
    b.addEventListener('click', function(){
      var r = b.getAttribute('data-rol-sec');
      try{ localStorage.setItem('dh_rol', r); }catch(e){}
      rolUygula(r); kapatHepsi();
    });
  });

  /* ---- çekmece (≤1024) ---- */
  var burger = document.getElementById('pnlBurger'), perde = document.getElementById('pnlOverlay');
  if(burger) burger.addEventListener('click', function(){ document.body.classList.toggle('nav-open'); });
  if(perde) perde.addEventListener('click', function(){ document.body.classList.remove('nav-open'); });
  if(q.get('nav') === '1') document.body.classList.add('nav-open');

  /* ---- yapım aşamasındaki ekran sayfası ---- */
  if(document.body.dataset.yakinda){
    var s = (P.sayfalar || {})[etkin];
    var baslik = s ? s.baslik : ((P.oturum_sayfalari || {})[etkin] || 'Ekran');
    var set2 = function(id, v){ var el = document.getElementById(id); if(el) el.textContent = v; };
    set2('ykBaslik', baslik);
    set2('ykModul', s ? s.modul_ad : 'Kabuk ve oturum');
    document.title = baslik + ' · ' + (P.proje_adi || '') + ' Yönetim Paneli';
  }

  rolUygula(rolOku());

  /* önizleme: ?ac=<menü id> açılır kutuyu açık getirir (seçenek sayfaları ve kontrol için) */
  var ac = q.get('ac');
  if(ac === 'ara' && ara){ ara.value = q.get('q') || ''; araGoster(); }
  else if(ac){ var ab = document.querySelector('[data-acilir="' + ac.replace(/[^a-zA-Z]/g,'') + '"]'); if(ab) ab.click(); }
})();
