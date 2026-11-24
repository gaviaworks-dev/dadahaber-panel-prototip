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
    document.querySelectorAll('[data-persona]').forEach(function(el){
      var v = per[el.getAttribute('data-persona')]; if(v) el.textContent = v;
    });
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
  if(etkinGrup){ var ak = etkinGrup.querySelector('.is-active'); if(ak && ak.scrollIntoView) ak.scrollIntoView({block:'nearest'}); }

  /* ---- açılır menüler (rol, hesap) ---- */
  function kapatHepsi(haric){
    document.querySelectorAll('[data-acilir][aria-expanded="true"]').forEach(function(b){
      if(b === haric) return;
      b.setAttribute('aria-expanded', 'false');
      var m = document.getElementById(b.getAttribute('data-acilir')); if(m) m.classList.remove('open');
    });
  }
  document.querySelectorAll('[data-acilir]').forEach(function(b){
    b.addEventListener('click', function(e){
      e.stopPropagation();
      var m = document.getElementById(b.getAttribute('data-acilir'));
      var ac = b.getAttribute('aria-expanded') !== 'true';
      kapatHepsi(b);
      b.setAttribute('aria-expanded', ac ? 'true' : 'false');
      if(m) m.classList.toggle('open', ac);
    });
  });
  document.addEventListener('click', function(e){ if(!e.target.closest('.pnl-menu')) kapatHepsi(); });
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
})();
