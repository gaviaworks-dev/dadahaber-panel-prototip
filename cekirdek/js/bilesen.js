/* =====================================================================
   ÇEKİRDEK · ORTAK BİLEŞEN DAVRANIŞI
   Sayfa yalnızca data- nitelikleriyle bildirir; modül kendi JS'ini yazmaz.
   - kb-secim: aranabilir açılır liste (süzgeçte ve formda aynı)
   - [data-liste]: veri tablosu (sekme, arama, süzgeç, seçim, toplu işlem, sayfalama bilgisi, durumlar)
   - satır tıklama ve küçük tanımlar: etkileşim sözleşmesi (PANEL.etkilesim; önizlemede ?etkilesim=)
   - çekmece / pencere / onay diyaloğu / kısa bildirim
   ===================================================================== */
(function(){
  var P = window.PANEL || {}, q = new URLSearchParams(location.search), doc = document.documentElement;
  var tr = function(s){ return (s || '').toLocaleLowerCase('tr'); };
  var sayiYaz = function(n){ return n.toLocaleString('tr-TR'); };

  /* ---------------- bileşen kurucuları ----------------
     window.kbKurucu(seçici, kur): bileşeni sayfada kurar ve kaydeder. window.kbKur(kök): çekmece, pencere ya da sonradan
     eklenen içerikteki henüz kurulmamış bileşenleri kurar ve rol görünürlüğünü yeniden uygular (kbAc bunu kendiliğinden çağırır). */
  var KURUCULAR = [];
  function kurucuCalistir(kok, sec, fn, i){
    var l = [];
    if(kok.matches && kok.matches(sec)) l.push(kok);
    if(kok.querySelectorAll) Array.prototype.push.apply(l, kok.querySelectorAll(sec));
    l.forEach(function(el){ var k = '_kbKur' + i; if(el[k]) return; el[k] = true; fn(el); });
  }
  window.kbKurucu = function(sec, fn){ KURUCULAR.push([sec, fn]); kurucuCalistir(document, sec, fn, KURUCULAR.length - 1); };
  window.kbKur = function(kok){ if(window.kbZorunluUygula) window.kbZorunluUygula(kok && kok.parentNode || document); KURUCULAR.forEach(function(x, i){ kurucuCalistir(kok || document, x[0], x[1], i); }); if(window.kbRolUygula) window.kbRolUygula(); };

  /* ---------------- zorunlu alan kuralı (sözleşme) ----------------
     Zorunlu alan ([data-zorunlu]) eksikken ana düğme pasif GÖRÜNÜR (.is-pasif) ama tıklanabilir kalır; tıklanınca eksik alanlar
     kırmızı çerçeve ve altında nedenle işaretlenir, ekran ilk eksik alana kayar (kapalı sekmedeyse sekme açılır).
     Ana düğmeler: kaydet çubuğundaki .btn-acc[data-kaydet], çekmece/pencere alt çubuğundaki .btn-acc, [data-dogrula="seçici"] taşıyan düğme. */
  /* zorunlu alanlar modül kaydından (ilke 7): form kabı [data-zorunlu-kayit="modul.form"], alanlar [data-alan-id="…"].
     yayin listesi → data-zorunlu (yayımlarken aranır), taslak listesi → data-zorunlu-taslak (taslak kaydında aranır).
     Etiketteki yıldız (*) da buradan çizilir; sayfada elle yıldız ya da data-zorunlu yazılmaz. */
  window.kbZorunluUygula = function(kok){
    (kok || document).querySelectorAll('[data-zorunlu-kayit]').forEach(function(F){
      var spec = (P.zorunlu || {})[F.getAttribute('data-zorunlu-kayit')]; if(!spec) return;
      F.querySelectorAll('[data-alan-id]').forEach(function(el){
        var id = el.getAttribute('data-alan-id'), y = (spec.yayin || []).indexOf(id) > -1, tz = (spec.taslak || []).indexOf(id) > -1;
        if(y) el.setAttribute('data-zorunlu', ''); else el.removeAttribute('data-zorunlu');
        if(tz) el.setAttribute('data-zorunlu-taslak', ''); else el.removeAttribute('data-zorunlu-taslak');
        var row = el.closest('.frow') || el.closest('.form-sec'), lab = row && row.querySelector(':scope > label, :scope > .flabel, :scope > .form-sec-tt');
        if(!lab) return;
        var s = lab.querySelector('.zorunlu');
        if(y && !s){ s = document.createElement('span'); s.className = 'zorunlu'; s.textContent = '*'; var ek = lab.querySelector('.fs-ek,.fdil,button'); lab.insertBefore(document.createTextNode(' '), ek || null); lab.insertBefore(s, ek || null); }
        if(s) s.hidden = !y;
      });
    });
  };
  window.kbZorunluUygula();

  window.kbAlanBos = function(el){
    if(el.matches('input[type=checkbox],input[type=radio]')) return !el.checked;
    if(el.matches('input,textarea,select')) return !el.value.trim();
    if(el.classList.contains('kb-secim')) return !el.dataset.deger;
    if(el.classList.contains('kb-cip-girdi')) return !el.querySelector('.kb-cip');
    if(el.hasAttribute('data-zorunlu-cip')) return !el.querySelector('.kb-cip');
    if(el.hasAttribute('data-slaytlar')) return !el.querySelector('.kb-slayt');
    if(el.hasAttribute('data-sirali-havuz')) return !el.querySelector('[data-siralanir] > .km-satir');
    if(el.classList.contains('kb-dosya')) return !el.querySelector('.kb-dosya-oge:not(.is-yukleniyor)');
    if(el.hasAttribute('data-gorsel-alan')){ var gb = el.querySelector('[data-gorsel-bos]'); if(gb && !gb.hidden) return true; return Array.prototype.every.call(el.querySelectorAll('[data-gorsel-hedef]'), function(h){ return !h.style.backgroundImage || h.style.backgroundImage === 'none'; }); }
    if(el.classList.contains('kb-tarih-sec')) return !(el.querySelector('.kt-deger') || {}).textContent || !!el.querySelector('.kt-bos');
    if(el.querySelector('input[type=radio],input[type=checkbox]')) return !el.querySelector('input:checked');
    var ed = el.querySelector('.ProseMirror'); if(ed) return !ed.textContent.trim();
    return !el.textContent.trim();
  };
  window.kbEksikler = function(kok, tur){
    return Array.prototype.filter.call((kok || document).querySelectorAll(tur === 'taslak' ? '[data-zorunlu-taslak]' : '[data-zorunlu]'), function(el){
      var g = el.closest('[hidden]'); if(g && !g.classList.contains('sa-form-panel')) return false;
      return window.kbAlanBos(el);
    });
  };
  window.kbEksikGoster = function(liste, sessiz){
    liste = [].concat(liste); if(!liste.length) return;
    liste.forEach(function(el){
      var row = el.closest('.frow') || (el.classList.contains('form-sec') ? el : el.parentNode); row.classList.add('has-error');
      if(!row.querySelector('.ferr')){ var f = document.createElement('div'); f.className = 'ferr'; f.innerHTML = '<i class="fa-solid fa-circle-exclamation" aria-hidden="true"></i><span></span>'; f.querySelector('span').textContent = el.getAttribute('data-zorunlu-metin') || 'Bu alan zorunlu.'; row.appendChild(f); }
      var p = el.closest('.sa-form-panel'); if(p){ var s = document.querySelector('.sa-form-tab[data-panel="' + p.id + '"]'); if(s) s.classList.add('has-error'); }
    });
    var ilk = liste[0], p0 = ilk.closest('.sa-form-panel');
    if(p0 && p0.hidden){ var s0 = document.querySelector('.sa-form-tab[data-panel="' + p0.id + '"]'); if(s0) s0.click(); }
    setTimeout(function(){
      (ilk.closest('.frow') || ilk).scrollIntoView({ block:'center', behavior:'smooth' });
      var od = ilk.matches('input,textarea') ? ilk : ilk.querySelector('input:not([type=hidden]),button,textarea,.ProseMirror');
      if(od && od.focus) od.focus({ preventScroll:true });
    }, 30);
    if(!sessiz) window.kbBildir(liste.length === 1 ? 'Zorunlu alan eksik: işaretli alanı doldurun' : liste.length + ' zorunlu alan eksik; işaretli alanları doldurun', null, 'uyari');
  };
  function dogrulamaKoku(b){
    if(b.dataset.dogrula) return document.querySelector(b.dataset.dogrula);
    var kk = b.closest('.kb-kaydet'); if(kk && b.matches('[data-kaydet]')) return document.getElementById(kk.getAttribute('data-form-icin'));
    var kp = b.closest('.kb-cekmece,.kb-pencere'); if(kp && b.closest('.kb-kap-alt-cubuk')) return kp.querySelector('.kb-kap-govde');
    return null;
  }
  var ANA = '.kb-kaydet .btn-acc[data-kaydet], .kb-kaydet [data-kaydet][data-kaydet-tur="taslak"], .kb-kap-alt-cubuk .btn-acc, .btn-acc[data-dogrula], .btn-danger[data-dogrula]';
  window.kbPasifGuncelle = function(){
    document.querySelectorAll(ANA).forEach(function(b){
      var k = dogrulamaKoku(b); if(!k) return;
      var n = window.kbEksikler(k, b.dataset.kaydetTur).length;
      b.classList.toggle('is-pasif', n > 0); b.setAttribute('aria-disabled', n > 0 ? 'true' : 'false');
      if(n) b.title = n === 1 ? 'Zorunlu alan eksik' : n + ' zorunlu alan eksik'; else b.removeAttribute('title');
    });
  };
  document.addEventListener('click', function(e){
    var b = e.target.closest(ANA); if(!b) return;
    var k = dogrulamaKoku(b); if(!k) return;
    var eks = window.kbEksikler(k, b.dataset.kaydetTur); if(!eks.length) return;
    e.preventDefault(); e.stopImmediatePropagation(); window.kbEksikGoster(eks);
  }, true);
  var pzZ = null;
  function pasifSonra(e){
    var r = e.target.closest && e.target.closest('.frow.has-error,.form-sec.has-error');
    if(r){ var z = r.querySelector('[data-zorunlu]'); if(!z || !window.kbAlanBos(z)) r.classList.remove('has-error'); }
    clearTimeout(pzZ); pzZ = setTimeout(window.kbPasifGuncelle, 60);
  }
  ['input', 'change', 'kb-secim', 'kb-tarih', 'click'].forEach(function(o){ document.addEventListener(o, pasifSonra); });
  window.addEventListener('load', window.kbPasifGuncelle);

  /* dil çubuğu açıklaması (.kfb-not) satıra sığmadığı için ipucuna dönüşür: bilgi ikonu, metin üstüne gelince/odakta görünür */
  window.kbKurucu('.kfb-not', function(n){
    var m = n.textContent.trim(); n.classList.add('is-ipucu'); n.setAttribute('tabindex', '0'); n.setAttribute('role', 'note'); n.setAttribute('aria-label', m);
    n.innerHTML = '<i class="fa-solid fa-circle-info" aria-hidden="true"></i><span class="kfb-balon"></span>'; n.querySelector('.kfb-balon').textContent = m;
  });

  /* ---------------- etkileşim sözleşmesi ---------------- */
  var ETK = Object.assign({ satir:'sayfa', kucuk_tanim:'cekmece', onay:'pencere' }, P.etkilesim || {});
  var on = q.get('etkilesim');
  if(on === 'sayfa') ETK = { satir:'sayfa', kucuk_tanim:'cekmece', onay:'pencere' };
  if(on === 'cekmece') ETK = { satir:'cekmece', kucuk_tanim:'cekmece', onay:'pencere' };
  if(on === 'pencere') ETK = { satir:'sayfa', kucuk_tanim:'pencere', onay:'pencere' };
  doc.dataset.etkSatir = ETK.satir; doc.dataset.etkKucuk = ETK.kucuk_tanim;

  /* ---------------- kısa bildirim ---------------- */
  var tw = document.createElement('div'); tw.className = 'sa-toast-wrap'; tw.setAttribute('aria-live', 'polite');
  document.body.appendChild(tw);
  /* kbBildir(metin, geriAl, tür): tür 'basari' (varsayılan) | 'bilgi' | 'uyari' | 'hata'. Kısa bildirim hiçbir ekranda düğmelerin
     üstüne binmez: alttaki kaydet çubuğu ya da açık çekmece/pencere alt çubuğu sağ altta yer kaplıyorsa onun üstünde açılır. */
  var TUR = { basari:'fa-circle-check', bilgi:'fa-circle-info', uyari:'fa-triangle-exclamation', hata:'fa-circle-xmark' };
  function bildirimYeri(){
    var W = window.innerWidth, H = window.innerHeight, sol = W < 641 ? 0 : W - 24 - 400, alt = 24;
    document.querySelectorAll('.kb-kaydet, .kb-kap-alt-cubuk, .sa-modal-acts').forEach(function(el){
      var r = el.getBoundingClientRect(); if(!r.width || !r.height || r.top >= H || r.bottom <= 0) return;
      if(r.right < sol) return;                      /* bildirim sütunuyla yatayda kesişmiyor */
      if(r.bottom < H - 160) return;                 /* ekranın altında değil */
      alt = Math.max(alt, H - r.top + 12);
    });
    tw.style.bottom = alt + 'px';
  }
  window.kbBildir = function(metin, geriAl, tur){
    tur = TUR[tur] ? tur : 'basari';
    var t = document.createElement('div'); t.className = 'sa-toast ' + tur; t.setAttribute('role', tur === 'hata' || tur === 'uyari' ? 'alert' : 'status');
    t.innerHTML = '<i class="fa-solid ' + TUR[tur] + '" aria-hidden="true"></i><span></span>';
    t.querySelector('span').textContent = metin;
    if(geriAl){
      var b = document.createElement('button'); b.type = 'button'; b.textContent = 'Geri al';
      b.addEventListener('click', function(){ geriAl(); t.remove(); }); t.appendChild(b);
    }
    bildirimYeri();
    tw.appendChild(t); requestAnimationFrame(function(){ t.classList.add('show'); });
    setTimeout(function(){ t.classList.remove('show'); setTimeout(function(){ t.remove(); }, 300); }, tur === 'hata' || tur === 'uyari' ? 6500 : 5000);
  };
  window.addEventListener('scroll', function(){ if(tw.children.length) bildirimYeri(); }, { passive:true });
  window.addEventListener('resize', function(){ if(tw.children.length) bildirimYeri(); });

  /* ---------------- onay diyaloğu ---------------- */
  var ov = document.createElement('div'); ov.className = 'sa-modal-ov';
  ov.innerHTML = '<div class="sa-modal" role="alertdialog" aria-modal="true" aria-labelledby="kbOnayBas"><button type="button" class="kb-kapat sa-modal-kapat" data-onay-hayir aria-label="Kapat" title="Kapat"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button><div class="sa-modal-ico"><i class="fa-solid fa-trash" aria-hidden="true"></i></div>'
    + '<h2 id="kbOnayBas"></h2><p></p><div class="sa-modal-acts"><button type="button" class="btn btn-ghost" data-onay-hayir>Vazgeç</button><button type="button" class="btn btn-ghost" data-onay-ikinci hidden></button><button type="button" class="btn btn-danger" data-onay-evet></button></div></div>';
  document.body.appendChild(ov);
  var onayIs = null, onayIkinci = null, onayOnce = null;
  window.kbOnay = function(o){
    ov.querySelector('.sa-modal').classList.toggle('danger', !!o.tehlike);
    ov.querySelector('.sa-modal-ico i').className = 'fa-solid ' + (o.ikon || 'fa-trash');
    ov.querySelector('h2').textContent = o.baslik; ov.querySelector('p').textContent = o.metin;
    ov.querySelector('[data-onay-evet]').textContent = o.evet || 'Onayla';
    ov.querySelector('[data-onay-evet]').className = 'btn ' + (o.tehlike ? 'btn-danger' : 'btn-acc');
    /* üç seçenekli onay: o.ikinci = { ad, is, tehlike } (ör. "Kaydetmeden Çık"); o.vazgec = vazgeç düğmesinin adı (ör. "Sayfada Kal") */
    var ik = ov.querySelector('[data-onay-ikinci]'); ik.hidden = !o.ikinci; ik.textContent = o.ikinci ? o.ikinci.ad : ''; ik.className = 'btn ' + (o.ikinci && o.ikinci.tehlike ? 'btn-ghost danger' : 'btn-ghost');
    ov.querySelector('.sa-modal-acts [data-onay-hayir]').textContent = o.vazgec || 'Vazgeç';
    ov.querySelector('.sa-modal').classList.toggle('is-uclu', !!o.ikinci);
    onayIs = o.evetIs; onayIkinci = o.ikinci ? o.ikinci.is : null; onayOnce = document.activeElement;
    ov.classList.add('open'); ov.querySelector('.sa-modal-acts [data-onay-hayir]').focus();
  };
  function onayKapat(){ ov.classList.remove('open'); if(onayOnce && onayOnce.focus) onayOnce.focus(); }
  /* KURAL · her pencerede sağ üstte kapat (×): Vazgeç ile aynı iş, hiçbir işlem yapılmaz; Esc de aynı */
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && ov.classList.contains('open')){ e.stopPropagation(); onayKapat(); } }, true);
  ov.addEventListener('click', function(e){
    if(e.target === ov || e.target.closest('[data-onay-hayir]')) onayKapat();
    if(e.target.closest('[data-onay-evet]')){ onayKapat(); if(onayIs) onayIs(); }
    if(e.target.closest('[data-onay-ikinci]')){ onayKapat(); if(onayIkinci) onayIkinci(); }
  });

  /* ---------------- çekmece ve pencere ---------------- */
  var perde = document.createElement('div'); perde.className = 'kb-perde'; document.body.appendChild(perde);
  var kaplar = {};
  ['cekmece','pencere'].forEach(function(tur){
    var k = document.createElement(tur === 'cekmece' ? 'aside' : 'div');
    k.className = 'kb-' + tur; k.setAttribute('role', 'dialog'); k.setAttribute('aria-modal', 'true'); k.hidden = true;
    k.innerHTML = '<div class="kb-kap-bas"><div><h2></h2><div class="kb-kap-alt"></div></div><button type="button" class="kb-kapat" aria-label="Kapat"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button></div><div class="kb-kap-govde"></div><div class="kb-kap-alt-cubuk" hidden></div>';
    document.body.appendChild(k); kaplar[tur] = k;
  });
  var acikKap = null, kapOnce = null;
  /* çekmece/pencere bir satırdan (satır tıklama, görüntüle, ⋯) açıldıysa o satır hatırlanır: içindeki onay zinciri satırın durumunu değiştirebilir */
  var sonSatir = null;
  document.addEventListener('click', function(e){ var r = e.target.closest && e.target.closest('tr[data-satir]'); var m = e.target.closest && e.target.closest('.kb-diger-menu'); sonSatir = r || (m && m._satir) || (e.target.closest && e.target.closest('.kb-cekmece,.kb-pencere') ? sonSatir : null); }, true);
  /* KURAL · kap başlığı: alt satır yalnız kısa bilgi. Kısa = en dar çekmecede (390 px telefon: 390 − 2×22 kenar − 36 kapat − 12 aralık
     = 298 px) başlık genişliğine sığan. Uzun açıklama başlıkta durmaz; gövdenin başına bilgi bandı olarak iner. Dönen: gövdeye inecek metin. */
  var KAP_EN = 298, olcCanvas;
  function kisaMi(metin){
    olcCanvas = olcCanvas || document.createElement('canvas'); var c = olcCanvas.getContext('2d');
    c.font = '500 12.5px ' + (getComputedStyle(document.body).fontFamily || 'sans-serif');
    return c.measureText(metin).width <= KAP_EN;
  }
  window.kbKapBaslik = function(k, baslik, alt){
    var h = k.querySelector('.kb-kap-bas h2'), a = k.querySelector('.kb-kap-bas .kb-kap-alt');
    if(h){ h.textContent = baslik; h.title = baslik; }
    var kisa = !alt || kisaMi(alt);
    if(a){ a.textContent = kisa ? alt : ''; a.title = kisa ? alt : ''; }
    return kisa ? '' : alt;
  };
  /* JS'le kurulan pencereler (etiketleme, medya, kırpma): başlıktaki alt satırı kurala göre yerleştir; gövde = başlığın sonraki kardeşi */
  window.kbKapDuzenle = function(kok){
    Array.prototype.forEach.call((kok || document).querySelectorAll('.kb-kap-bas'), function(b){
      var h = b.querySelector('h2'), a = b.querySelector('.kb-kap-alt'); if(!h) return;
      var m = kbKapBaslik(b, h.textContent, a ? a.textContent : '');
      var es = b.nextElementSibling; if(es && es.classList.contains('kb-kap-not')) es.remove();
      if(m){ var n = document.createElement('div'); n.className = 'kb-bant bilgi kb-kap-not'; n.innerHTML = '<i class="fa-solid fa-circle-info" aria-hidden="true"></i><span></span>'; n.querySelector('span').textContent = m; b.parentNode.insertBefore(n, b.nextSibling); }
    });
  };
  window.kbKapNot = function(govde, metin){
    var eski = govde.querySelector(':scope > .kb-kap-not'); if(eski) eski.remove();
    if(!metin) return;
    var n = document.createElement('div'); n.className = 'kb-bant bilgi kb-kap-not';
    n.innerHTML = '<i class="fa-solid fa-circle-info" aria-hidden="true"></i><span></span>'; n.querySelector('span').textContent = metin;
    var ilk = govde.firstElementChild, dil = ilk && ilk.classList.contains('kb-kap-dil') ? ilk : null; /* dil çubuğu gövdenin en üstünde kalır */
    govde.insertBefore(n, dil ? dil.nextSibling : govde.firstChild);
  };
  /* ---------------- KURAL · seçenek grubu (Beyar 25.11.2026) ----------------
     Tek seçimli (radio): 2–4 kısa seçenek → bölmeli seçici (eşit bölmeler, alanı doldurur, kayan vurgu, satıra kırılmaz);
       açıklamalı (<small> alt satırı olan) → eşit kutular: 2 yan yana, 3 yan yana, 4 → 2×2; 5 ve üzeri → aranabilir açılır liste.
     Çok seçimli (checkbox): eşit kutular; sütun sayısı son satırda tek kutu kalmayacak biçimde seçilir; en çok iki satır,
       aşarsa aranabilir açılır liste (çoklu seçim).
     Dar alanda sığmıyorsa hepsi alt alta tam genişlik (yarım dağılma yok). Girdiler yerinde kalır: form, zorunlu alan ve kayıt
     onları okur; açılır liste seçimi girdilere yazar. Kapsam dışı: araç satırı süzgeç paneli, [data-secenek-serbest]. */
  var SG = '.kb-secenek-grup, .ket-kategori, [data-secenek-grup]', sgNo = 0;
  function sgOgeler(g){ return Array.prototype.filter.call(g.children, function(c){ return c.tagName === 'LABEL' && c.querySelector('input[type=radio],input[type=checkbox]'); }); }
  function sgAd(o){ var b = o.querySelector('b'); return ((b || o).textContent || '').replace(/\s+/g, ' ').trim(); }
  function sgSutun(n){ if(n <= 3) return n; if(n === 4) return 2; for(var c = 4; c >= 2; c--){ if(n % c !== 1 && Math.ceil(n / c) <= 2) return c; } return 0; }
  function sgGuncelle(g){
    var og = sgOgeler(g), i = -1, sec = [];
    og.forEach(function(o, k){ if(o.querySelector('input').checked){ if(i < 0) i = k; sec.push(sgAd(o)); } });
    g.style.setProperty('--sg-i', Math.max(i, 0)); g.classList.toggle('is-bos', i < 0);
    var d = g._sgDd; if(!d) return;
    var l = d.querySelector('.ks-deger'); l.textContent = sec.length ? (sec.length > 2 ? sec.length + ' seçildi' : sec.join(', ')) : (g.getAttribute('data-bos') || 'Seçin');
    d.classList.toggle('is-dolu', sec.length > 0);
    d.querySelectorAll('.kb-secim-liste button').forEach(function(b, k){ var c = og[k] && og[k].querySelector('input').checked; b.classList.toggle('is-sec', !!c); b.setAttribute('aria-selected', c ? 'true' : 'false'); });
  }
  function sgDd(g, og, coklu){
    var id = 'kbSg' + (++sgNo), d = document.createElement('div');
    d.className = 'kb-secim kb-sg-acilir'; d.setAttribute('data-kuruldu', '1');
    d.innerHTML = '<button type="button" class="kb-secim-btn" data-acilir="' + id + '" aria-expanded="false" aria-haspopup="listbox"><span class="ks-deger"></span><i class="fa-solid fa-chevron-down" aria-hidden="true"></i></button>'
      + '<div class="pnl-menu kb-secim-menu" id="' + id + '"><div class="kb-secim-ara"><i class="fa-solid fa-magnifying-glass" aria-hidden="true"></i><input type="search" placeholder="Ara" aria-label="Seçeneklerde ara"></div>'
      + '<div class="kb-secim-liste" role="listbox"' + (coklu ? ' aria-multiselectable="true"' : '') + '></div><div class="kb-secim-bos" hidden>Sonuç yok</div></div>';
    var L = d.querySelector('.kb-secim-liste'), ara = d.querySelector('.kb-secim-ara input'), btn = d.querySelector('.kb-secim-btn');
    og.forEach(function(o){ var b = document.createElement('button'); b.type = 'button'; b.setAttribute('role', 'option'); b.textContent = sgAd(o); var s = o.querySelector('small'); if(s){ var k = document.createElement('small'); k.textContent = s.textContent; b.appendChild(k); } L.appendChild(b); });
    L.addEventListener('click', function(e){
      var b = e.target.closest('button'); if(!b) return; var k = Array.prototype.indexOf.call(L.children, b), inp = og[k] && og[k].querySelector('input'); if(!inp) return;
      if(coklu){ inp.checked = !inp.checked; } else { inp.checked = true; btn.click(); }
      inp.dispatchEvent(new Event('input', { bubbles: true })); inp.dispatchEvent(new Event('change', { bubbles: true }));
    });
    ara.addEventListener('input', function(){ var v = tr(ara.value.trim()), n = 0; Array.prototype.forEach.call(L.children, function(b){ var g2 = !v || tr(b.textContent).indexOf(v) > -1; b.hidden = !g2; if(g2) n++; }); d.querySelector('.kb-secim-bos').hidden = n > 0; });
    btn.addEventListener('click', function(){ setTimeout(function(){ if(btn.getAttribute('aria-expanded') === 'true'){ ara.value = ''; ara.dispatchEvent(new Event('input')); ara.focus(); } }, 0); });
    g.insertBefore(d, og[0]);
    return d;
  }
  window.kbSecenekDuzenle = function(kok){
    (kok || document).querySelectorAll(SG).forEach(function(g){
      if(g.closest('.kb-arac, .kb-arac-filtre-pen, [data-secenek-serbest]')) return;
      var og = sgOgeler(g); if(og.length < 2) return;
      var radyo = og[0].querySelector('input').type === 'radio', acikla = og.some(function(o){ return o.querySelector('small'); }), n = og.length, acilir = false;
      g.classList.remove('is-bolmeli', 'is-kutu', 'is-alt-alta', 'is-acilir', 'is-olcu'); og.forEach(function(o){ o.hidden = false; }); if(g._sgDd) g._sgDd.hidden = true;
      g.style.setProperty('--sg-n', n);
      if(radyo && n >= 5) acilir = true;
      else {
        var c = radyo ? (n <= 3 ? n : 2) : sgSutun(n);
        if(!c) acilir = true;
        else {
          g.style.setProperty('--sg-c', c); g.classList.add(radyo && !acikla ? 'is-bolmeli' : 'is-kutu');
          if(g.getClientRects().length){
            var bol = g.classList.contains('is-bolmeli'); g.classList.add('is-olcu'); /* tek satır kuralı yalnız ölçülen (görünür) grupta */
            function sigmaz(){ return og.some(function(o){ return o.scrollWidth > o.clientWidth + 1 || (!bol && o.getBoundingClientRect().width < 104); }); }
            /* çoklu seçim (onay kutusu): yazı tek satır; sığmıyorsa önce sütun azalır (yalnız kalan kutu olmadan), en son alt alta */
            var yalniz = false;
            if(!radyo && !acikla) while(c > 2 && sigmaz()){ c--; if(n % c === 1){ if(c > 2) c--; else { yalniz = true; break; } } g.style.setProperty('--sg-c', c); }
            var dar = yalniz || sigmaz(); /* bölmeli: yalnız yazı sığmazsa */
            if(dar){ g.classList.remove('is-bolmeli'); g.classList.add('is-kutu', 'is-alt-alta'); }
          }
        }
      }
      if(acilir){ if(!g._sgDd) g._sgDd = sgDd(g, og, !radyo); og.forEach(function(o){ o.hidden = true; }); g._sgDd.hidden = false; g.classList.add('is-acilir'); }
      sgGuncelle(g);
    });
  };
  (function(){
    var bekle; function yap(){ clearTimeout(bekle); bekle = setTimeout(function(){ window.kbSecenekDuzenle(); }, 40); }
    document.addEventListener('change', function(e){ var g = e.target.closest && e.target.closest(SG); if(g) sgGuncelle(g); });
    window.addEventListener('resize', yap); window.addEventListener('load', yap);
    document.addEventListener('click', function(e){ if(e.target.closest && e.target.closest('.sa-form-tab, [data-sekme], [data-tanim], [data-pencere], [data-ac]')) yap(); });
    if(document.readyState !== 'loading') window.kbSecenekDuzenle(); else document.addEventListener('DOMContentLoaded', function(){ window.kbSecenekDuzenle(); });
  })();

  /* KURAL · yapışkan alan: sağ sütun (.side-card) üst bar ile kaydet çubuğu arasına sığmıyorsa yapışkan olmaz (.is-akar).
     Sekme değişince, pencere boyu ya da sütunun içeriği değişince yeniden ölçülür. */
  window.kbYapiskanSigdir = function(){
    var ust = document.querySelector('.pnl-top'), uh = ust ? ust.getBoundingClientRect().height : 64, vh = window.innerHeight;
    var kk = Array.prototype.filter.call(document.querySelectorAll('.kb-kaydet'), function(k){ return k.getClientRects().length && getComputedStyle(k).position === 'sticky'; })[0];
    /* kaydet çubuğunun yapışık haldeki üst kenarı ölçülür (ekranın altına tam oturmayabilir); görünür değilse ekranın altı − çubuk boyu */
    var kr = kk && kk.getBoundingClientRect(), sinir = kk ? Math.min(kr.top < vh && kr.top > 0 ? kr.top : vh - kr.height, vh - kr.height) : vh;
    /* sayfa sonunda kaydet çubuğu yapışıklıktan çıkıp yukarı gelir: sınır onun en yüksek (son) konumu */
    if(kk && kk.previousElementSibling){ /* çubuğun akıştaki (yapışmamış) yeri: önceki kardeşin altı + üst boşluk */
      var de = document.documentElement, dogal = kk.previousElementSibling.getBoundingClientRect().bottom + window.scrollY + parseFloat(getComputedStyle(kk).marginTop);
      var sonUst = vh - (de.scrollHeight - dogal); if(de.scrollHeight > vh + 4) sinir = Math.min(sinir, Math.max(sonUst, uh + 160)); }
    /* KURAL · sağ sütun her düzenleme sayfasında yapışkandır, istisna yok (Beyar, 25.11.2026): üst barın altına yapışır;
       üst bar ile kaydet çubuğu arasına sığmayan sütun yine yapışkan kalır ve kendi içinde kayar (ince kaydırma çubuğu). */
    document.querySelectorAll('.side-card').forEach(function(s){
      s.classList.remove('is-akar'); s.style.top = ''; if(getComputedStyle(s).position !== 'sticky') return;
      s.style.maxHeight = ''; s.classList.remove('is-uzun');
      var bos = parseFloat(getComputedStyle(s).top) || (uh + 24), h = s.scrollHeight;
      if(bos + h + 8 > sinir){ s.style.maxHeight = Math.floor(sinir - 8 - bos) + 'px'; s.classList.add('is-uzun'); } /* uzun sütun yapışkan kalır, kendi içinde kayar */
    });
  };
  (function(){
    var bekle; function yap(){ clearTimeout(bekle); bekle = setTimeout(window.kbYapiskanSigdir, 30); }
    document.addEventListener('kb-sekme', yap);
    window.addEventListener('resize', yap); window.addEventListener('load', yap);
    document.addEventListener('click', function(e){ if(e.target.closest && e.target.closest('.sa-form-tab, [data-sekme], .kb-onizle-sec button')) yap(); });
    if(window.ResizeObserver) document.addEventListener('DOMContentLoaded', function(){ var ro = new ResizeObserver(yap); document.querySelectorAll('.side-card').forEach(function(s){ ro.observe(s); }); });
    if(document.readyState !== 'loading') yap(); else document.addEventListener('DOMContentLoaded', yap);
  })();
  window.kbAc = function(sablonId, tur, doldur){
    var s = document.getElementById(sablonId); if(!s) return;
    var k = kaplar[tur] || kaplar.cekmece;
    var altMetin = kbKapBaslik(k, s.dataset.baslik || '', s.dataset.alt || '');
    var govde = k.querySelector('.kb-kap-govde'), alt = k.querySelector('.kb-kap-alt-cubuk');
    var parca = s.content.cloneNode(true);
    var ac = parca.querySelector('.kb-kap-alt-cubuk');
    alt.innerHTML = ''; alt.hidden = !ac;
    if(ac){ while(ac.firstChild) alt.appendChild(ac.firstChild); ac.remove(); }
    govde.innerHTML = ''; govde.appendChild(parca);
    kbKapNot(govde, altMetin);
    if(s.dataset.zorunluKayit) govde.setAttribute('data-zorunlu-kayit', s.dataset.zorunluKayit); else govde.removeAttribute('data-zorunlu-kayit');
    window.kbSecimKur(govde); window.kbSecimKur(alt);
    if(window.kbKur){ window.kbKur(govde); window.kbKur(alt); }
    window.kbSecenekDuzenle(govde); setTimeout(function(){ window.kbSecenekDuzenle(govde); }, 0); /* görünür olunca ölçü */
    setTimeout(function(){ govde.querySelectorAll('.sa-form-tabs').forEach(sekmeSigdir); }, 0);
    if(window.kbHizala){ var hz = function(){ window.kbTarihHizala && window.kbTarihHizala(); window.kbHizala(govde); }; k.hidden = false; hz(); setTimeout(hz, 0); }
    setTimeout(window.kbPasifGuncelle, 0);
    if(doldur) doldur(k);
    var h2 = k.querySelector('.kb-kap-bas h2'); if(h2) h2.title = h2.textContent; /* doldur başlığı değiştirmiş olabilir */
    window.kbSayaclar(k);
    if(window.kbAcKapat) window.kbAcKapat();
    if(acikKap && acikKap !== k){ acikKap.classList.remove('open'); acikKap.hidden = true; }
    if(!acikKap) kapOnce = document.activeElement;
    acikKap = k; k._satir = sonSatir;
    clearTimeout(k._kbGizle); k.hidden = false; perde.classList.add('open');
    requestAnimationFrame(function(){ k.classList.add('open'); k.querySelector('.kb-kapat').focus(); });
    document.body.style.overflow = 'hidden';
  };
  window.kbKapat = function(){
    if(!acikKap) return;
    var k = acikKap; acikKap = null;
    k.classList.remove('open'); perde.classList.remove('open'); document.body.style.overflow = '';
    clearTimeout(k._kbGizle); k._kbGizle = setTimeout(function(){ if(acikKap !== k) k.hidden = true; }, 260);
    if(kapOnce && kapOnce.focus) kapOnce.focus();
  };
  perde.addEventListener('click', window.kbKapat);
  var acikTur = 'cekmece';
  function degerleriYaz(kaynak, k){
    Object.keys(kaynak.dataset).forEach(function(a){
      if(a.indexOf('deger') !== 0 || a === 'deger') return;
      var alan = (a.charAt(5).toLowerCase() + a.slice(6)).replace(/[A-Z]/g, function(m){ return '-' + m.toLowerCase(); }), v = kaynak.dataset[a];
      k.querySelectorAll('[data-alan="' + alan + '"]').forEach(function(el){
        if(el.matches('input[type=radio]')){ el.checked = el.value === v; }
        else if(el.matches('input,textarea')){ el.value = v; el.dispatchEvent(new Event('input', {bubbles:true})); }
        else if(el.classList.contains('kb-secim')){ var o = el.querySelector('button[data-deger="' + v + '"]'); if(o){ el.dataset.deger = v; el.classList.toggle('is-dolu', v !== ''); var l = el.querySelector('.ks-deger'); if(l) l.textContent = o.getAttribute('data-ad') || o.textContent; } }
        else el.textContent = v;
      });
    });
  }
  Object.keys(kaplar).forEach(function(t){
    kaplar[t].addEventListener('click', function(e){
      if(e.target.closest('.kb-kapat,[data-kapat]')){ window.kbKapat(); return; }
      var sa = e.target.closest('[data-sablon-ac]');
      if(sa){
        e.preventDefault(); e.stopPropagation();
        var bildir = sa.dataset.bildirSonra;
        window.kbAc(sa.getAttribute('data-sablon-ac'), t, function(k){ degerleriYaz(sa, k); if(sa.dataset.baslikYaz) k.querySelector('h2').textContent = sa.dataset.baslikYaz; k.querySelectorAll('[data-yeni-kayitta-gizle]').forEach(function(x){ x.hidden = !sa.dataset.degerAd; }); });
        if(bildir) window.kbBildir(bildir);
      }
    });
  });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape'){ if(ov.classList.contains('open')) onayKapat(); else window.kbKapat(); } });

  /* kategori ağacı (kb-agac): sil düğmesi. Kayıt varsa taşıyarak silme, yoksa ikinci onay; ikisinde de çöp ve geri al (B1). */
  function agacSil(b, agac){
    var ad = b.dataset.ad, ust = b.dataset.ust, haber = +b.dataset.haber || 0, alt = +b.dataset.alt || 0;
    var dugum = ust ? b.closest('li') : b.closest('details');
    function sil(hedef){
      if(dugum) dugum.hidden = true;
      window.kbBildir('“' + (ust ? ust + ' › ' : '') + ad + '” çöpe taşındı' + (hedef ? '; ' + haber.toLocaleString('tr') + ' haber “' + hedef + '” konusuna taşındı' : ''), function(){ if(dugum) dugum.hidden = false; });
    }
    if(!haber){ window.kbOnay({ tehlike:true, baslik:'“' + ad + '” silinsin mi?', metin:'Bu konuda haber yok. Çöpe gider, oradan geri alınabilir; işlem denetim izine yazılır.', evet:'Çöpe Taşı', evetIs: function(){ sil(null); } }); return; }
    var hedefler = [];
    (agac || document).querySelectorAll('details').forEach(function(d){
      var ana = (d.querySelector('summary [data-kat-sil]') || {}).dataset; if(!ana || (!ust && ana.ad === ad)) return;
      d.querySelectorAll('li [data-kat-sil]').forEach(function(x){ if(!(ust && x.dataset.ad === ad && x.dataset.ust === ust)) hedefler.push(ana.ad + ' › ' + x.dataset.ad); });
    });
    window.kbTasiSil({ ad: (ust ? ust + ' › ' : '') + ad, haber: haber, alt: alt, hedefler: hedefler, evetIs: sil });
  }
  document.addEventListener('click', function(e){
    var b = e.target.closest('[data-kat-sil]'); if(b){ e.preventDefault(); e.stopPropagation(); agacSil(b, b.closest('.kb-agac')); return; }
    var f = e.target.closest('[data-kat-sil-form]');
    if(f){ e.preventDefault(); var k = f.closest('.kb-cekmece,.kb-pencere'), adEl = k && k.querySelector('[data-alan="ad"]'), ad = adEl ? adEl.value.trim() : '';
      var sab = document.querySelector('template#hbKategoriler'), kok = sab ? sab.content : document, x = kok.querySelector('[data-kat-sil][data-ad="' + ad.replace(/"/g, '\\"') + '"]');
      if(!x){ window.kbBildir('Kaydedilmemiş kategori; silinecek bir şey yok'); return; }
      window.kbKapat(); agacSil(x, kok); }
  }, true);

  /* küçük tanımlar: [data-tanim="sablonId"] düğmesi sözleşmeye göre çekmece ya da pencere açar;
     sözleşme "sayfa" ise düğmenin href'ine gidilir */
  /* [data-pencere="sablonId"]: şablonu ortada PENCEREDE açar (onaydan büyük, gerekçe isteyen işler: reddet nedeni gibi). Olay yetkilendirmeli. */
  document.addEventListener('click', function(e){
    var b = e.target.closest && e.target.closest('[data-pencere]'); if(!b) return;
    e.preventDefault(); e.stopPropagation();
    document.querySelectorAll('.kb-diger-menu.open').forEach(function(m){ m.classList.remove('open'); });
    var menu = b.closest('.kb-diger-menu'); var satir = b.closest('tr[data-satir],[data-kart]') || (menu && menu._satir) || null;
    window.kbAc(b.getAttribute('data-pencere'), 'pencere', function(k){ degerleriYaz(b, k); });
  }, true);
  document.querySelectorAll('[data-tanim]').forEach(function(b){
    b.addEventListener('click', function(e){
      if(ETK.kucuk_tanim === 'sayfa' && b.getAttribute('href')) return;
      e.preventDefault(); window.kbAc(b.getAttribute('data-tanim'), ETK.kucuk_tanim);
    });
  });

  /* ---------------- sekmeli düzenleme: [data-sekmeli] içinde .sa-form-tab[data-panel] ---------------- */
  document.addEventListener('click', function(e){
    var s = e.target.closest('.sa-form-tab[data-panel]'); if(!s) return;
    var kap = s.closest('[data-sekmeli]') || document;
    kap.querySelectorAll('.sa-form-tab[data-panel]').forEach(function(x){ var on = x === s; x.classList.toggle('is-on', on); x.setAttribute('aria-selected', on ? 'true' : 'false'); });
    kap.querySelectorAll('.sa-form-panel').forEach(function(p){ p.hidden = p.id !== s.getAttribute('data-panel'); });
    yanDuzen(s.getAttribute('data-panel'));
    if(window.kbAracYerlestir) window.kbAracYerlestir(); /* gizli sekmede dar kipte kurulan araç satırı genişler */
    if(window.kbTarihHizala) window.kbTarihHizala(); if(window.kbHizala) window.kbHizala(); /* yeni görünen sekme hemen hizalanır */
  });
  /* KURAL · zaman çizgisi hizası: ilk öğesi tarih (.kb-tarih) olan satırlar (.km-satir) aynı kapta ise tarih sütunu ortak genişlik alır */
  window.kbTarihHizala = function(){
    var kaplar = [];
    document.querySelectorAll('.km-satir > .kb-tarih:first-child').forEach(function(t){ var k = t.parentNode.parentNode; if(kaplar.indexOf(k) < 0) kaplar.push(k); t.parentNode.classList.add('is-zaman'); });
    kaplar.forEach(function(k){
      var en = 0; k.querySelectorAll(':scope > .km-satir > .kb-tarih:first-child').forEach(function(t){ t.style.minWidth = '0'; var g = t.getBoundingClientRect().width; if(g > en) en = g; t.style.minWidth = ''; });
      if(en) k.style.setProperty('--zc-genislik', Math.ceil(en) + 'px');
    });
  };
  (function(){ var b_; function yap(){ clearTimeout(b_); b_ = setTimeout(window.kbTarihHizala, 30); }
    window.addEventListener('load', yap); window.addEventListener('resize', yap); if(document.fonts && document.fonts.ready) document.fonts.ready.then(yap);
    document.addEventListener('click', function(e){ if(e.target.closest && e.target.closest('.sa-form-tab, [data-satir-ekle], [data-satir-sil]')) yap(); });
    document.addEventListener('input', function(e){ if(e.target.closest && e.target.closest('.km-satir')) yap(); });
    window.kbTarihHizala(); })();

  /* KURAL · hiza (Beyar): tekrarlayan satırlarda aynı görevdeki öğe bütün satırlarda aynı kenardan başlar.
     Çekirdek, aynı sınıftan en az üç yatay satırı olan listeleri kendisi hizalar:
       - ızgara satırları (her satır kendi ızgarası): sütun genişlikleri satırlar arasında eşitlenir (esnek sütun esnek kalır);
       - esnek (flex) satırlar: büyüyen öğeden önceki öğeler en genişine göre eşit genişlik alır; bir satırda eksik olan öğenin
         yerine görünmez yer tutucu konur (ör. kapat düğmesi olmayan "bu cihaz" satırı).
     Tablolar, çip ve seçenek grupları, önizlemeler kapsam dışı. Pencere boyu, sekme ve içerik değişince yeniden hesaplanır. */
  var HZ_ATLA = 'table, .chips, .kb-secenek-grup, .ket-kategori, .pager, .kb-arac, .row-acts, .ph-actions, .kb-takvim, [class*="oniz"], .kb-kirp, .pnl-menu, .sa-form-tabs, .kb-cip-girdi, .kit-satir, svg, .kb-kanallar, .kb-log';
  function hzAd(e){ return (typeof e.className === 'string' ? e.className.split(' ').filter(function(s){ return s && !/^is-|^has-|^kb-hiza-/.test(s); })[0] : '') || e.tagName.toLowerCase(); }
  function hzGor(e){ return e.getClientRects().length && !e.hidden; }
  window.kbHizala = function(kok){
    (kok || document).querySelectorAll('.kb-hiza-bos').forEach(function(x){ x.remove(); });
    (kok || document).querySelectorAll('[data-kb-hiza]').forEach(function(x){ x.style.gridTemplateColumns = ''; x.style.minWidth = ''; x.removeAttribute('data-kb-hiza'); });
    Array.prototype.forEach.call((kok || document).querySelectorAll('.pnl-main *, .kb-kap-govde *'), function(P){
      if(P.children.length < 3 || !hzGor(P) || P.closest(HZ_ATLA)) return;
      var R = Array.prototype.filter.call(P.children, hzGor); if(R.length < 3) return;
      var rk = hzAd(R[0]); R = R.filter(function(x){ return hzAd(x) === rk; }); if(R.length < 3) return;
      var L0 = R[0].getBoundingClientRect().left; if(R.some(function(x){ return Math.abs(x.getBoundingClientRect().left - L0) > 1; })) return;
      var cs0 = getComputedStyle(R[0]);
      if(/grid/.test(cs0.display)){
        var cols = R.map(function(x){ return getComputedStyle(x).gridTemplateColumns.split(' ').map(parseFloat); });
        var n = cols[0].length; if(n < 2 || cols.some(function(c){ return c.length !== n; })) return;
        var fark = false; for(var j = 0; j < n; j++){ var v = cols.map(function(c){ return c[j]; }); if(Math.max.apply(null, v) - Math.min.apply(null, v) > 1) fark = true; }
        if(!fark) return;
        var en = []; for(var j2 = 0; j2 < n; j2++) en.push(Math.max.apply(null, cols.map(function(c){ return c[j2]; })));
        var esnek = en.indexOf(Math.max.apply(null, en)); /* en geniş sütun esnek (1fr) kabul edilir */
        var tanim = en.map(function(w, j3){ return j3 === esnek ? 'minmax(0,1fr)' : Math.ceil(Math.min(w, (cols.map(function(c){ return c[j3]; }).sort(function(a, b){ return b - a; })[0]))) + 'px'; }).join(' ');
        R.forEach(function(x){ x.style.gridTemplateColumns = tanim; x.setAttribute('data-kb-hiza', ''); });
        return;
      }
      if(!/flex/.test(cs0.display) || cs0.flexDirection.indexOf('column') > -1 || cs0.flexWrap === 'wrap') return;
      var satirlar = R.map(function(x){ return Array.prototype.filter.call(x.children, function(c){ return hzGor(c) && !/absolute|fixed/.test(getComputedStyle(c).position); }); });
      var gi = satirlar.map(function(c){ for(var i = 0; i < c.length; i++){ if(parseFloat(getComputedStyle(c[i]).flexGrow) > 0) return i; } return -1; });
      if(gi.some(function(i){ return i < 0; })) return;
      /* büyüyen öğeden önceki öğeler: en genişine eşitle */
      var onceAd = {}; satirlar.forEach(function(c, r){ for(var i = 0; i < gi[r]; i++){ var k = hzAd(c[i]); (onceAd[k] = onceAd[k] || []).push(c[i]); } });
      Object.keys(onceAd).forEach(function(k){ var el = onceAd[k]; if(el.length < 2) return; var w = Math.max.apply(null, el.map(function(e){ return e.getBoundingClientRect().width; }));
        if(Math.max.apply(null, el.map(function(e){ return e.getBoundingClientRect().width; })) - Math.min.apply(null, el.map(function(e){ return e.getBoundingClientRect().width; })) > 1) el.forEach(function(e){ e.style.minWidth = Math.ceil(w) + 'px'; e.setAttribute('data-kb-hiza', ''); }); });
      /* büyüyen öğeden sonraki öğeler: aynı türden olanlar en genişine eşitlenir (sağ kenarlar hizalı kalır) */
      var sonraAd = {}; satirlar.forEach(function(c, r){ for(var i = gi[r] + 1; i < c.length; i++){ var k = hzAd(c[i]); (sonraAd[k] = sonraAd[k] || []).push(c[i]); } });
      Object.keys(sonraAd).forEach(function(k){ var el = sonraAd[k]; if(el.length < 2) return; var ws = el.map(function(e){ return e.getBoundingClientRect().width; }), w = Math.max.apply(null, ws);
        if(w - Math.min.apply(null, ws) > 1) el.forEach(function(e){ e.style.minWidth = Math.ceil(w) + 'px'; e.setAttribute('data-kb-hiza', ''); }); });
      /* büyüyen öğeden sonraki öğeler: eksik olana yer tutucu (sırası en kalabalık satırdan) */
      var ornek = satirlar.reduce(function(a, c, r){ var s = c.slice(gi[r] + 1); return s.length > a.length ? s : a; }, []);
      var sira = ornek.map(hzAd);
      if(sira.length) satirlar.forEach(function(c, r){
        var son = c.slice(gi[r] + 1), varAd = son.map(hzAd);
        sira.forEach(function(k, j){ if(varAd.indexOf(k) > -1) return;
          var b = document.createElement('span'); b.className = 'kb-hiza-bos'; b.setAttribute('aria-hidden', 'true'); b.style.width = Math.ceil(ornek[j].getBoundingClientRect().width) + 'px';
          var sonraki = null; for(var q = j + 1; q < sira.length && !sonraki; q++){ var ix = varAd.indexOf(sira[q]); if(ix > -1) sonraki = son[ix]; }
          R[r].insertBefore(b, sonraki || null); });
      });
    });
  };
  (function(){ var b_; function yap(){ clearTimeout(b_); b_ = setTimeout(function(){ window.kbHizala(); }, 60); }
    window.addEventListener('load', yap); window.addEventListener('resize', yap); if(document.fonts && document.fonts.ready) document.fonts.ready.then(yap);
    document.addEventListener('click', function(e){ if(e.target.closest && e.target.closest('.sa-form-tab, [data-tanim], [data-pencere], [data-satir-ekle], [data-satir-sil], .chip[data-sekme], [data-pg]')) yap(); });
    document.addEventListener('kb-liste-suzuldu', yap, true);
    yap(); })();

  /* KURAL · sekme taşması: sekmeler satıra sığmıyorsa kesilmez, kaymaz; sığmayanlar sondaki "Diğer" menüsüne girer (araç satırındaki
     kuralın aynısı). Seçili sekme her zaman görünür kalır. Pencere boyu, yazı tipi ya da sekme değişince yeniden ölçülür. */
  var sdNo = 0;
  function sekmeSigdir(T){
    var tabs = Array.prototype.filter.call(T.children, function(x){ return x.classList.contains('sa-form-tab') && !x.classList.contains('sa-diger-btn'); });
    var dig = T.querySelector(':scope > .sa-form-diger');
    tabs.forEach(function(x){ x.classList.remove('is-tasan'); }); if(dig) dig.hidden = true;
    if(!T.getClientRects().length) return;
    function tasiyor(){ var r = T.getBoundingClientRect(), sag = r.right - parseFloat(getComputedStyle(T).paddingRight) + 1, son = null;
      Array.prototype.forEach.call(T.children, function(x){ if(!x.hidden && x.offsetWidth && !x.classList.contains('is-tasan')) son = x; }); return son && son.getBoundingClientRect().right > sag; }
    if(!tasiyor()) return;
    if(!dig){
      var id = 'kbSekDiger' + (++sdNo); dig = document.createElement('div'); dig.className = 'sa-form-diger';
      dig.innerHTML = '<button type="button" class="sa-form-tab sa-diger-btn" data-acilir="' + id + '" aria-haspopup="menu" aria-expanded="false">Diğer<span class="sd-say"></span><i class="fa-solid fa-chevron-down" aria-hidden="true"></i></button><div class="pnl-menu sa-diger-menu" id="' + id + '" role="menu"></div>';
      T.appendChild(dig);
      dig.querySelector('.pnl-menu').addEventListener('click', function(e){ var b = e.target.closest('[data-sekme-hedef]'); if(!b) return; var h = T.querySelector('.sa-form-tab[data-panel="' + b.dataset.sekmeHedef + '"]'); if(h){ h.click(); setTimeout(function(){ sekmeSigdir(T); }, 0); } });
    }
    dig.hidden = false;
    var gor = tabs.filter(function(x){ return !x.hidden && x.offsetWidth; });
    for(var i = gor.length - 1; i >= 0 && tasiyor(); i--){ if(gor[i].classList.contains('is-on')) continue; gor[i].classList.add('is-tasan'); }
    var tas = tabs.filter(function(x){ return x.classList.contains('is-tasan'); });
    dig.querySelector('.sd-say').textContent = tas.length;
    dig.querySelector('.pnl-menu').innerHTML = tas.map(function(x){ return '<button type="button" role="menuitem" data-sekme-hedef="' + x.dataset.panel + '">' + x.innerHTML + '</button>'; }).join('');
    dig.querySelector('.sa-diger-btn').classList.toggle('has-error', tas.some(function(x){ return x.classList.contains('has-error'); }));
  }
  window.kbSekmeSigdir = function(){ document.querySelectorAll('.sa-form-tabs').forEach(sekmeSigdir); };
  (function(){ var b_; function yap(){ clearTimeout(b_); b_ = setTimeout(window.kbSekmeSigdir, 40); }
    window.addEventListener('resize', yap); window.addEventListener('load', yap); if(document.fonts && document.fonts.ready) document.fonts.ready.then(yap);
    document.addEventListener('click', function(e){ if(e.target.closest && e.target.closest('.sa-form-tab[data-panel], [data-tanim], [data-pencere]')) yap(); });
    if(window.ResizeObserver) new ResizeObserver(yap).observe(document.documentElement);
    window.kbSekmeSigdir(); })();

  /* sağ sütun sekmeye göre: önizlemesi olan sekmede önizleme en üstte ve yapışkan; data-one-cik kartı kendi sekmesinde üste çıkar */
  function yanDuzen(pid){
    /* sayfa başı eylemleri sekmeye göre: .ph-actions [data-panel-icin="p1 p2"] yalnız o sekmede görünür */
    document.querySelectorAll('.ph-actions [data-panel-icin]').forEach(function(x){ x.hidden = x.getAttribute('data-panel-icin').split(' ').indexOf(pid) === -1; });
    var yan = document.querySelector('.side-card'); if(!yan) return;
    var var_ = false;
    yan.querySelectorAll('[data-panel-icin]').forEach(function(x){ var on = x.getAttribute('data-panel-icin') === pid; x.hidden = !on; if(on) var_ = true; });
    /* kart sırası her sekmede aynı: önce sekmenin önizlemesi (varsa), sonra Yayın, sonra SEO Skoru (Beyar, 25.11.2026); data-one-cik artık sıra değiştirmez */
    yan.classList.toggle('kb-onizlemeli', var_);
  }
  /* sayfa içinden sekme açma: [data-sekme-git="panelId"] (ör. "Etiketleri Yönet") — sayfa yenilenmez, sekme açılır, kartın başına kayar */
  document.addEventListener('click', function(e){
    var g = e.target.closest && e.target.closest('[data-sekme-git]'); if(!g) return;
    var s = document.querySelector('.sa-form-tab[data-panel="' + g.getAttribute('data-sekme-git') + '"]'); if(!s) return;
    e.preventDefault(); s.click(); var k = s.closest('.pnl-card') || s; var ust = document.querySelector('.pnl-top');
    window.scrollTo({ top: Math.max(0, k.getBoundingClientRect().top + window.scrollY - (ust ? ust.offsetHeight : 64) - 12), behavior: 'smooth' });
  });
  /* açılışta seçili sekmeye göre sayfa başı eylemleri */
  (function(){ var on = document.querySelector('.sa-form-tab.is-on[data-panel]'); if(on) yanDuzen(on.getAttribute('data-panel')); else document.querySelectorAll('.ph-actions [data-panel-icin]').forEach(function(x){ var ilk = document.querySelector('.sa-form-tab[data-panel]'); if(ilk) x.hidden = x.getAttribute('data-panel-icin').split(' ').indexOf(ilk.getAttribute('data-panel')) === -1; }); })();
  /* sekmeye derin bağlantı: ?sekme=<panel id> (ör. site-ayarlari/index.html?sekme=sIletisim) */
  (function(){ var s = q.get('sekme'); if(!s) return; var b = document.querySelector('.sa-form-tab[data-panel="' + s + '"]'); if(b) setTimeout(function(){ b.click(); }, 0); })();
  var ilkSekme = document.querySelector('[data-sekmeli] > .sa-form-tabs .sa-form-tab.is-on, [data-sekmeli] .sa-form-tab.is-on'); if(ilkSekme) yanDuzen(ilkSekme.getAttribute('data-panel'));

  /* ---------------- karakter sayacı: [data-sayac="önerilen|sınır"] ---------------- */
  function sayacGuncelle(el){
    var m = el.getAttribute('data-sayac').split('|'), oner = +m[0], sinir = +(m[1] || m[0]);
    var n = (el.value !== undefined ? el.value : el.textContent).length;
    var kap = el.closest('.frow,.sc-field'); var cm = kap && kap.querySelector('.char-meter'); if(!cm) return;
    var b = cm.querySelector('b'); if(b) b.textContent = n + ' / ' + oner;
    cm.classList.toggle('warn', n > oner && n <= sinir); cm.classList.toggle('over', n > sinir);
    var cb = kap.querySelector('.kb-cubuk'); if(cb){ cb.querySelector('span').style.width = Math.min(100, n / sinir * 100) + '%'; cb.classList.toggle('warn', n > oner && n <= sinir); cb.classList.toggle('over', n > sinir); }
  }
  document.addEventListener('input', function(e){ if(e.target.matches && e.target.matches('[data-sayac]')) sayacGuncelle(e.target); });
  window.kbSayaclar = function(kok){ (kok || document).querySelectorAll('[data-sayac]').forEach(sayacGuncelle); };

  /* ---------------- adres (slug) üretimi: [data-slug-kaynak="#id"] ---------------- */
  window.kbSlug = function(s){
    var m = {'ç':'c','ğ':'g','ı':'i','ö':'o','ş':'s','ü':'u','â':'a','î':'i','û':'u'};
    return s.toLocaleLowerCase('tr').replace(/[çğıöşüâîû]/g, function(c){ return m[c]; }).replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 80);
  };

  /* adres addan kendiliğinden üretilir (elle değiştirilmediyse); aynı data-alan'lı önizleme metinleri canlı güncellenir */
  document.addEventListener('input', function(e){
    var el = e.target; if(!el.matches) return;
    var kok = el.closest('.kb-kap-govde') || document;
    if(el.matches('[data-slug-hedef]')){
      var h = kok.querySelector('#' + el.getAttribute('data-slug-hedef'));
      if(h && !h.dataset.elle){ h.value = window.kbSlug(el.value); h.dispatchEvent(new Event('input', {bubbles:true})); }
    }
    if(el.matches('[id]') && kok.querySelector('[data-slug-hedef="' + el.id + '"]') && e.isTrusted) el.dataset.elle = '1';
    if(el.matches('input[data-alan],textarea[data-alan]')){
      kok.querySelectorAll('[data-alan="' + el.getAttribute('data-alan') + '"]').forEach(function(x){ if(x !== el && !x.matches('input,textarea,.kb-secim')) x.textContent = el.value; });
    }
  });

  /* ---------------- bildirim önizlemesi (telefon + web) ----------------
     KURAL: önizleme yazılan bildirim başlığını ve metnini gösterir; alan boşsa haberin başlığına ve spotuna düşer.
     Görsel: seçili kapak (kapak alanındaki ilk görsel); "Bildirim Görseli" kapalıysa görsel gizlenir. */
  window.kbPushOnizle = function(){
    var on = document.querySelectorAll('.kb-push, .kb-web-push'); if(!on.length) return;
    function deger(s){ var e = document.querySelector(s); return e && e.value ? e.value.trim() : ''; }
    var is_ = document.querySelector('[data-icerik-sec]'), sc = is_ && is_._kbSecili; /* push: bağlı haber (içerik seçici) */
    var bas = deger('[data-alan="push-baslik"]') || deger('input[data-alan="baslik"],textarea[data-alan="baslik"]') || (sc ? sc.baslik : '');
    var met = deger('[data-alan="push-metin"]') || deger('textarea[data-alan="spot"],input[data-alan="spot"]');
    var pg = document.querySelector('[data-push-gorsel] .kg-resim'), kap = document.querySelector('[data-alan-id="kapak"] .kg-resim, [data-gorsel-alan$=".kapak"] .kg-resim');
    var gorsel = (pg && pg.style.backgroundImage) || (kap ? kap.style.backgroundImage : '') || (sc && sc.gorsel ? 'url(' + sc.gorsel + ')' : '');
    var ac = document.querySelector('[data-push-gorsel], input[aria-label="Bildirim Görseli"]'), goster = !ac || ac.checked;
    on.forEach(function(o){
      var b = o.querySelector('b'), p = o.querySelector('p');
      if(b && bas) { b.textContent = bas; b.title = bas; }
      if(p && met) p.textContent = met;
      var r = o.querySelector('.kp-resim');
      if(!r && o.classList.contains('kb-web-push')){ r = document.createElement('span'); r.className = 'kp-resim'; o.appendChild(r); }
      if(r){ if(gorsel) r.style.backgroundImage = gorsel; r.hidden = !goster || !(gorsel || r.style.backgroundImage); }
    });
  };
  (function(){
    function yap(e){ if(!e || !e.target || !e.target.matches || e.target.matches('[data-alan="push-baslik"],[data-alan="push-metin"],[data-alan="baslik"],[data-alan="spot"],[data-push-gorsel],input[aria-label="Bildirim Görseli"]')) window.kbPushOnizle(); }
    document.addEventListener('input', yap); document.addEventListener('change', yap); document.addEventListener('kb-icerik', function(){ window.kbPushOnizle(); });
    function kur(){ window.kbPushOnizle(); var k = document.querySelector('[data-alan-id="kapak"], [data-gorsel-alan$=".kapak"]');
      if(k && window.MutationObserver) new MutationObserver(function(){ window.kbPushOnizle(); }).observe(k, { attributes: true, subtree: true, attributeFilter: ['style', 'hidden', 'class'] }); }
    if(document.readyState !== 'loading') setTimeout(kur, 0); else document.addEventListener('DOMContentLoaded', kur);
  })();

  /* ---------------- aranabilir açılır liste ---------------- */
  window.kbSecimKur = function(kok){ (kok || document).querySelectorAll('.kb-secim:not([data-kuruldu])').forEach(function(sc){ sc.setAttribute('data-kuruldu', '1');
    var btn = sc.querySelector('.kb-secim-btn'), ara = sc.querySelector('.kb-secim-ara input');
    var ops = sc.querySelectorAll('.kb-secim-liste button[data-deger]');
    var bos = sc.querySelector('.kb-secim-bos');
    if(ara){
      ara.addEventListener('input', function(){
        var v = tr(ara.value.trim()), n = 0;
        ops.forEach(function(o){ var g = !v || tr(o.textContent).indexOf(v) > -1; o.hidden = !g; if(g) n++; });
        sc.querySelectorAll('.ks-grup').forEach(function(g){ g.hidden = !!v; });
        if(bos) bos.hidden = n > 0;
      });
      btn.addEventListener('click', function(){ setTimeout(function(){ if(btn.getAttribute('aria-expanded') === 'true'){ ara.value = ''; ara.dispatchEvent(new Event('input')); ara.focus(); } }, 0); });
    }
    ops.forEach(function(o){
      o.addEventListener('click', function(){
        var d = o.getAttribute('data-deger');
        sc.dataset.deger = d;
        ops.forEach(function(x){ x.classList.toggle('is-sec', x === o && d !== ''); });
        var lbl = sc.querySelector('.ks-deger'); if(lbl) lbl.textContent = d === '' ? (sc.dataset.bos || 'Tümü') : o.getAttribute('data-ad') || o.firstChild.textContent;
        sc.classList.toggle('is-dolu', d !== '');
        var ki = sc.querySelector('.ks-ikon'), oi = o.querySelector('i'); if(ki && oi) ki.className = oi.className + ' ks-ikon';
        btn.click();
        sc.dispatchEvent(new CustomEvent('kb-secim', { bubbles:true, detail:{ deger:d } }));
      });
    });
  }); };
  window.kbSecimKur();

  /* ---------------- LİSTE ARAÇ SATIRI (Beyar kuralı: tek satır, sabit yükseklik, asla ikiye bölünmez) ----------------
     Sayfadaki mevcut işaretleme (.kb-liste-ust > .chips [+ .chip.kb-cop] ve .filter-bar > .fb-search, .kb-secim[data-suz], …)
     çalışma anında tek satıra toplanır: .filter-bar.kb-arac > .kb-arac-sol (durum sekmeleri) + .kb-arac-sag (arama, süzgeçler,
     görünüm değiştirici, diğer düğmeler, Çöp). Kurallar:
       - en çok 5 sekme görünür; fazlası "Diğer" menüsünde;
       - 2'den fazla süzgeç → tek "Filtreler" düğmesi (pencerede seçilir, çoklu seçim; düğmede açık süzgeç sayısı);
       - daralma sırası: (a) süzgeçler Filtreler'e, (b) arama büyüteç ikonuna (tıklanınca satır içinde açılır), (c) sekmeler Diğer'e;
       - açık süzgeçler yalnız varken altta ince etiket şeridinde + "Temizle"; yoksa yer tutmaz.
     Sayfa bir şey yazmaz; kalıba oturmayan (sekmesi chips olmayan, süzgeci kb-secim olmayan) parçalar sağda olduğu gibi kalır. */
  var aracSay = 0;
  function aracKur(ust, fb){
    var kap = (ust || fb).parentNode, n = ++aracSay;
    var satir = fb || document.createElement('div');
    if(!fb){ satir.className = 'filter-bar'; kap.insertBefore(satir, ust.nextSibling); }
    satir.classList.add('kb-arac');
    var eski = Array.prototype.slice.call(satir.childNodes);
    var sol = document.createElement('div'); sol.className = 'kb-arac-sol';
    var sag = document.createElement('div'); sag.className = 'kb-arac-sag';
    var cop = null, chips = null;
    if(ust){
      chips = ust.querySelector('.chips');
      cop = ust.querySelector('.chip.kb-cop') || (chips && chips.querySelector('.chip.kb-cop'));
      Array.prototype.slice.call(ust.childNodes).forEach(function(x){ if(x !== chips && x !== cop && x.nodeType === 1) sag.appendChild(x); });
      ust.remove();
    }
    eski.forEach(function(x){ if(x.nodeType === 1) sag.appendChild(x); });
    if(!chips){ chips = sag.querySelector(':scope > .chips'); }
    if(chips){ sol.appendChild(chips); if(!cop) cop = chips.querySelector('.chip.kb-cop'); }
    if(cop){ sag.appendChild(cop); }
    satir.innerHTML = ''; satir.appendChild(sol); satir.appendChild(sag);
    satir.dataset.arac = n;
    /* tarih aralığı (kb-aralik) satırda tek açılır düğme olur: "Tarih: Son 7 gün" */
    Array.prototype.forEach.call(sag.querySelectorAll(':scope > .kb-aralik'), function(A, k){
      var w = document.createElement('div'); w.className = 'kb-arac-aralik';
      w.innerHTML = '<button type="button" class="chip" data-acilir="kbAracTarih' + n + '_' + k + '" aria-expanded="false" aria-haspopup="dialog"><i class="fa-solid fa-calendar-days" aria-hidden="true"></i><span class="kb-arac-yazi">Tarih: <b></b></span><i class="fa-solid fa-chevron-down" aria-hidden="true"></i></button><div class="pnl-menu kb-arac-aralik-pen" id="kbAracTarih' + n + '_' + k + '" role="dialog" aria-label="Tarih aralığı"></div>';
      A.parentNode.insertBefore(w, A); w.querySelector('.pnl-menu').appendChild(A);
      function etk(){ var on = A.querySelector('.ka-hazir .is-on'), d = Array.prototype.map.call(A.querySelectorAll('.kt-deger'), function(x){ return x.textContent.trim(); }).filter(Boolean);
        w.querySelector('b').textContent = on && on.dataset.aralik !== 'ozel' ? on.textContent.trim() : (d.length ? d.join(' – ') : 'Özel'); }
      ['click', 'kb-tarih', 'kb-aralik'].forEach(function(o){ A.addEventListener(o, function(){ setTimeout(etk, 0); }); });
      etk();
    });
    /* sağdaki chip ve düğmelerin yazısı ayrı sarılır: en dar kipte yalnız ikon ve sayaç kalır */
    Array.prototype.forEach.call(sag.querySelectorAll(':scope > .chip, :scope > .kb-gorunum-sec .chip, :scope > .btn'), function(c){
      Array.prototype.slice.call(c.childNodes).forEach(function(x){ if(x.nodeType === 3 && x.nodeValue.trim()){ var s = document.createElement('span'); s.className = 'kb-arac-yazi'; s.textContent = x.nodeValue.trim(); c.replaceChild(s, x); } });
    });

    /* sekmeler: en çok 5 görünür, fazlası Diğer */
    var diger = document.createElement('div'); diger.className = 'kb-arac-diger'; diger.hidden = true;
    diger.innerHTML = '<button type="button" class="chip" data-acilir="kbAracDiger' + n + '" aria-expanded="false" aria-haspopup="true"><span>Diğer</span><i class="fa-solid fa-chevron-down" aria-hidden="true"></i></button><div class="pnl-menu kb-arac-diger-menu" id="kbAracDiger' + n + '" role="menu"></div>';
    sol.appendChild(diger);
    var digerMenu = diger.querySelector('.pnl-menu'), digerBtn = diger.querySelector('button');
    var sekmeler = chips ? Array.prototype.filter.call(chips.querySelectorAll('.chip[data-sekme]'), function(c){ return !c.classList.contains('kb-cop'); }) : [];

    /* arama: büyüteç kipinde ikona küçülür */
    var ara = sag.querySelector(':scope > .fb-search');
    if(ara){
      var ab = document.createElement('button'); ab.type = 'button'; ab.className = 'ia-btn kb-arac-ara-btn'; ab.setAttribute('aria-label', 'Ara'); ab.innerHTML = '<i class="fa-solid fa-magnifying-glass" aria-hidden="true"></i>';
      ara.parentNode.insertBefore(ab, ara);
      ab.addEventListener('click', function(){ satir.classList.add('is-ara-acik'); var i = ara.querySelector('input'); if(i) i.focus(); });
      var ai = ara.querySelector('input');
      if(ai) ai.addEventListener('blur', function(){ setTimeout(function(){ if(!ai.value.trim() && !ara.contains(document.activeElement)) satir.classList.remove('is-ara-acik'); }, 120); });
      if(ai) ai.addEventListener('keydown', function(e){ if(e.key === 'Escape'){ ai.value = ''; ai.dispatchEvent(new Event('input', { bubbles:true })); ai.blur(); satir.classList.remove('is-ara-acik'); } });
    }

    /* süzgeçler ve Filtreler penceresi */
    var suzler = Array.prototype.slice.call(sag.querySelectorAll(':scope > .kb-secim[data-suz]'));
    var filtre = null, etiket = null;
    if(suzler.length){
      filtre = document.createElement('div'); filtre.className = 'kb-arac-filtre'; filtre.hidden = true;
      filtre.innerHTML = '<button type="button" class="chip" data-acilir="kbAracFiltre' + n + '" aria-expanded="false" aria-haspopup="dialog" aria-label="Filtreler"><i class="fa-solid fa-sliders" aria-hidden="true"></i><span class="kb-arac-yazi">Filtreler</span><b class="ch-cnt" hidden></b></button><div class="pnl-menu kb-arac-filtre-pen" id="kbAracFiltre' + n + '" role="dialog" aria-label="Filtreler"></div>';
      sag.insertBefore(filtre, suzler[0]);
      var pen = filtre.querySelector('.pnl-menu');
      suzler.forEach(function(s){
        var ad = ((s.querySelector('.ks-etk') || {}).textContent || s.dataset.suz).replace(/:\s*$/, '');
        var g = document.createElement('fieldset'); g.className = 'kb-arac-grup'; g.dataset.suz = s.dataset.suz;
        g.innerHTML = '<legend>' + ad + '</legend>';
        Array.prototype.forEach.call(s.querySelectorAll('.kb-secim-liste button[data-deger]'), function(o){
          if(o.dataset.deger === '') return;
          var l = document.createElement('label'); l.className = 'kb-secenek';
          l.innerHTML = '<input type="checkbox" value="' + o.dataset.deger.replace(/"/g, '&quot;') + '"><span></span>';
          l.querySelector('span').textContent = o.getAttribute('data-ad') || o.firstChild.textContent;
          g.appendChild(l);
        });
        pen.appendChild(g);
      });
      var alt = document.createElement('div'); alt.className = 'kb-arac-filtre-alt'; alt.innerHTML = '<button type="button" class="kb-bag" data-arac-temizle>Temizle</button><button type="button" class="btn btn-acc btn-sm" data-arac-kapat>Uygula</button>';
      pen.appendChild(alt);
      pen.addEventListener('change', function(e){
        var g = e.target.closest('.kb-arac-grup'); if(!g) return;
        var s = suzler.filter(function(x){ return x.dataset.suz === g.dataset.suz; })[0]; if(!s) return;
        var vals = Array.prototype.map.call(g.querySelectorAll('input:checked'), function(i){ return i.value; });
        suzAyarla(s, vals);
      });
      pen.addEventListener('click', function(e){
        if(e.target.closest('[data-arac-temizle]')){ suzler.forEach(function(s){ suzAyarla(s, []); }); }
        if(e.target.closest('[data-arac-kapat]')){ filtre.querySelector('button').click(); }
      });
      /* etiket şeridi */
      etiket = document.createElement('div'); etiket.className = 'kb-arac-etiket'; etiket.hidden = true;
      satir.parentNode.insertBefore(etiket, satir.nextSibling);
      etiket.addEventListener('click', function(e){
        var x = e.target.closest('[data-etiket-kaldir]');
        if(x){ var s = suzler.filter(function(y){ return y.dataset.suz === x.dataset.suz; })[0]; var vals = (s.dataset.deger || '').split('|').filter(function(v){ return v && v !== x.dataset.deger; }); suzAyarla(s, vals); }
        if(e.target.closest('[data-arac-temizle]')) suzler.forEach(function(s){ suzAyarla(s, []); });
      });
      suzler.forEach(function(s){ s.addEventListener('kb-secim', function(){ setTimeout(senkron, 0); }); });
    }
    function suzAyarla(s, vals){
      var v = vals.join('|'); s.dataset.deger = v; s.classList.toggle('is-dolu', v !== '');
      var lbl = s.querySelector('.ks-deger');
      if(lbl){ if(!vals.length) lbl.textContent = s.dataset.bos || 'Tümü'; else if(vals.length === 1){ var o = s.querySelector('button[data-deger="' + vals[0].replace(/"/g, '\\"') + '"]'); lbl.textContent = o ? (o.getAttribute('data-ad') || o.firstChild.textContent) : vals[0]; } else lbl.textContent = vals.length + ' seçili'; }
      s.querySelectorAll('button[data-deger]').forEach(function(o){ o.classList.toggle('is-sec', vals.indexOf(o.dataset.deger) > -1); });
      s.dispatchEvent(new CustomEvent('kb-secim', { bubbles:true, detail:{ deger:v } }));
    }
    function senkron(){
      if(!filtre) return;
      var acik = 0, h = '';
      suzler.forEach(function(s){
        var vals = (s.dataset.deger || '').split('|').filter(Boolean), ad = ((s.querySelector('.ks-etk') || {}).textContent || '').replace(/:\s*$/, '');
        var g = filtre.querySelector('.kb-arac-grup[data-suz="' + s.dataset.suz + '"]');
        if(g) g.querySelectorAll('input').forEach(function(i){ i.checked = vals.indexOf(i.value) > -1; });
        vals.forEach(function(v){ acik++; var o = s.querySelector('button[data-deger="' + v.replace(/"/g, '\\"') + '"]'); var t = o ? (o.getAttribute('data-ad') || o.firstChild.textContent) : v;
          h += '<span class="kb-arac-etk"><span>' + ad + ': <b></b></span><button type="button" data-etiket-kaldir data-suz="' + s.dataset.suz + '" data-deger="' + v.replace(/"/g, '&quot;') + '" aria-label="Kaldır"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button></span>';
          h = h.replace('<b></b>', '<b>' + String(t).replace(/</g, '&lt;') + '</b>'); });
      });
      var sb = filtre.querySelector('.ch-cnt'); sb.textContent = acik; sb.hidden = !acik;
      etiket.innerHTML = h + (acik ? '<button type="button" class="kb-bag" data-arac-temizle>Temizle</button>' : '');
      etiket.hidden = !acik;
    }

    /* yerleşim: sığmayana göre kip (0 normal · 1 Filtreler · 2 + arama ikonu · 3 + sekmeler Diğer'e) */
    function yerlestir(){
      var kip = 0;
      function uygula(k, gorunurZorla){
        satir.dataset.kip = k;
        var filtreKip = filtre && (k >= 1 || suzler.length > 2);
        if(filtre){ filtre.hidden = !filtreKip; suzler.forEach(function(s){ s.hidden = filtreKip; }); }
        satir.classList.toggle('is-ara-ikon', k >= 2 && !!ara);
        var gorunur = Math.min(5, sekmeler.length);
        if(k >= 3 && gorunurZorla != null) gorunur = gorunurZorla;
        sekmeler.forEach(function(c, i){ var icerde = i >= gorunur; if(icerde && c.parentNode !== digerMenu) digerMenu.appendChild(c); if(!icerde && c.parentNode !== chips) chips.appendChild(c); });
        if(chips) sekmeler.forEach(function(c, i){ if(i < gorunur) chips.appendChild(c); });
        diger.hidden = !digerMenu.children.length;
        digerGuncelle();
      }
      function sigan(){ var w = sol.clientWidth - (diger.offsetWidth || 90) - 8, t = 0, n2 = 0; for(var i = 0; i < sekmeler.length && i < 5; i++){ t += (sekmeler[i]._kbG || 110) + 8; if(t > w) break; n2++; } return n2; }
      sekmeler.forEach(function(c){ if(c.offsetWidth) c._kbG = c.offsetWidth; });
      /* gerçek ihtiyaç: görünen öğelerin genişliği (kapalı açılır menüler ölçüme girmez) */
      function genislik(kap){ var w = 0, n3 = 0; Array.prototype.forEach.call(kap.children, function(c){ if(c.hidden || c.classList.contains('pnl-menu') || !c.offsetWidth) return; w += (c === chips ? c.scrollWidth : c.offsetWidth); n3++; }); return w + Math.max(0, n3 - 1) * 8; }
      function tasiyor(){ var cs = getComputedStyle(satir), ic = satir.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight); return genislik(sol) + genislik(sag) + 12 > ic + 1 || (chips && chips.offsetWidth > 0 && chips.scrollWidth > chips.clientWidth + 1); }
      satir.classList.remove('is-ikon');
      for(kip = 0; kip <= 2; kip++){ uygula(kip); if(!tasiyor()) break; }
      if(kip > 2){ /* (c) sekmeler Diğer'e: sığana kadar birer birer */
        for(var g = Math.min(5, sekmeler.length); g >= 1; g--){ uygula(3, g); if(!tasiyor()) break; }
        kip = tasiyor() ? 4 : 3;
      }
      if(kip > 3){ /* en dar kip: yalnız ikonlar; sekmelerin hepsi tek açılır düğmede, seçili sekmenin adıyla */
        satir.classList.add('is-ikon'); satir.dataset.kip = 4;
        sekmeler.forEach(function(c){ if(c.parentNode !== digerMenu) digerMenu.appendChild(c); });
        diger.hidden = !sekmeler.length; digerGuncelle();
      }
    }
    function digerGuncelle(){
      var sec = Array.prototype.filter.call(digerMenu.children, function(c){ return c.classList.contains('is-on'); })[0];
      var ad = sec ? ((sec.querySelector('.kb-arac-yazi') || sec.childNodes[0] || {}).textContent || 'Diğer').trim() : 'Diğer';
      var hepsiMenude = chips && !chips.querySelector('.chip[data-sekme]');
      if(hepsiMenude && !sec){ var on = Array.prototype.filter.call(digerMenu.querySelectorAll('.chip'), function(c){ return c.classList.contains('is-on'); })[0]; if(on) ad = (on.childNodes[0].textContent || '').trim(); }
      digerBtn.querySelector('span').textContent = ad;
      digerBtn.classList.toggle('is-on', !!sec || hepsiMenude);
    }
    digerMenu.addEventListener('click', function(e){ if(e.target.closest('.chip')) setTimeout(function(){ digerGuncelle(); digerBtn.click(); }, 0); });
    if(chips) chips.addEventListener('click', function(){ setTimeout(digerGuncelle, 0); });
    var zam; function yeniden(){ clearTimeout(zam); zam = setTimeout(yerlestir, 60); }
    if(window.ResizeObserver) new ResizeObserver(yeniden).observe(satir); else window.addEventListener('resize', yeniden);
    yerlestir(); senkron();
    if(document.fonts && document.fonts.ready) document.fonts.ready.then(yeniden);
    window.addEventListener('load', yeniden);
    satir._kbArac = { yerlestir: yerlestir, senkron: senkron };
  }
  /* sayfadaki bütün liste araç satırları: liste ve kart betikleri bağlanmadan önce toplanır */
  function ardisikBirlestir(fb){ /* aynı listenin art arda süzgeç satırları (tarih aralığı + arama gibi) tek satıra toplanır */
    while(fb && fb.nextElementSibling && fb.nextElementSibling.classList.contains('filter-bar') && !fb.nextElementSibling.classList.contains('kb-arac')){
      var sonraki = fb.nextElementSibling; while(sonraki.firstChild) fb.appendChild(sonraki.firstChild); sonraki.remove();
    }
    return fb;
  }
  function sonrakiSuzgec(u){ /* aynı kapta, tabloya ya da listeye gelmeden önceki ilk süzgeç satırı (arada not bloğu olabilir) */
    for(var e = u.nextElementSibling; e; e = e.nextElementSibling){
      if(e.classList.contains('filter-bar')) return e;
      if(e.matches('.ptable-wrap, table, [data-satirlar], .kb-liste-ust, .pnl-card, .kb-takvim, [data-kart-liste], .kb-entegre-izgara')) return null;
    }
    return null;
  }
  document.querySelectorAll('.kb-liste-ust').forEach(function(u){ var fb = sonrakiSuzgec(u); if(fb && fb !== u.nextElementSibling){ var ara0 = []; for(var e = u.nextElementSibling; e && e !== fb; e = e.nextElementSibling) ara0.push(e); ara0.forEach(function(x){ fb.parentNode.insertBefore(x, fb.nextSibling); }); } if(!fb && !u.querySelector('.chips')) return; /* sınıfı yalnız boşluk için taşıyan öğe (ör. açıklama paragrafı) araç satırı değildir */ aracKur(u, ardisikBirlestir(fb)); });
  document.querySelectorAll('.filter-bar:not(.kb-arac)').forEach(function(fb){ if(fb.isConnected && !fb.classList.contains('kb-arac')) aracKur(null, ardisikBirlestir(fb)); });
  window.kbAracYerlestir = function(){ document.querySelectorAll('.kb-arac').forEach(function(s){ if(s._kbArac) s._kbArac.yerlestir(); }); };

  /* ---------------- sayfalama (ortak: veri tablosu, ızgara, kart listesi) ----------------
     KURAL · sayfalama: alt satır tek, sabit yükseklik; sol "128 sonuçtan 26–50 · 6 sayfa" · orta ilk/önceki/numaralar
     (en çok 5 kutu, seçili sayfanın çevresinde kayan pencere, "…" yok)/sonraki/son (uçta pasif, gizlenmez) · sağ boş. Sayfa boyu sabit 25.
     Tek sayfada düğmeler görünmez, yükseklik aynı. Dar ekranda "26–50 / 128" ve "3 / 12". Sayfa değişince liste başına kayar,
     odak sayfalamada kalır. Kaptaki .pager işaretlemesi ne olursa olsun çekirdek kurar; yoksa ekler.
     kbSayfalaKur(kap, degisti) → { pager, bilgi, bilgiK, boy, sayfa, son, sinirla(toplam), ciz(toplam) } */
  window.kbSayfalaKur = function(L, degisti){
    var S = { boy: +(L.dataset.sayfaBoy || 25), sayfa: 1, son: 1 }; /* sayfa boyu sabit 25 (Beyar); sayfa başına seçimi yok */
    var pager = L.querySelector('.pager');
    if(!pager){ pager = document.createElement('div'); var tw = L.querySelector('.ptable-wrap, [data-kart-izgara]'); if(tw && tw.parentNode) tw.parentNode.insertBefore(pager, tw.nextSibling); else L.appendChild(pager); }
    pager.className = 'pager kb-sayfala';
    pager.innerHTML = '<div class="pager-info" aria-live="polite"><span class="pi-uzun"></span><span class="pi-kisa"></span></div>'
      + '<nav class="pager-btns" aria-label="Sayfalar"><button type="button" class="pg-btn pg-uc" data-pg="ilk" aria-label="İlk sayfa"><i class="fa-solid fa-angles-left" aria-hidden="true"></i></button>'
      + '<button type="button" class="pg-btn pg-uc" data-pg="onceki" aria-label="Önceki sayfa"><i class="fa-solid fa-angle-left" aria-hidden="true"></i></button>'
      + '<span class="pg-sayilar"></span><span class="pg-kisa"></span>'
      + '<button type="button" class="pg-btn pg-uc" data-pg="sonraki" aria-label="Sonraki sayfa"><i class="fa-solid fa-angle-right" aria-hidden="true"></i></button>'
      + '<button type="button" class="pg-btn pg-uc" data-pg="son" aria-label="Son sayfa"><i class="fa-solid fa-angles-right" aria-hidden="true"></i></button></nav>'
      + '<div class="pager-sag" aria-hidden="true"></div>'; /* sağ taraf boş; orta sütun tam ortada kalır */
    S.pager = pager; S.bilgi = pager.querySelector('.pi-uzun'); S.bilgiK = pager.querySelector('.pi-kisa');
    S.sinirla = function(toplam){ S.son = Math.max(1, Math.ceil(toplam / S.boy)); if(S.sayfa > S.son) S.sayfa = S.son; if(S.sayfa < 1) S.sayfa = 1; };
    /* en çok 5 kutu, seçili sayfanın çevresinde kayan pencere; uçta ilk/son numara ve "…" yok (o işi ilk/son düğmeleri görür).
       Kutu sayısı sayfadan sayfaya değişmez (toplam 5'ten azsa toplam kadar). */
    function sayilar(){ var n = S.son, s = S.sayfa, k = Math.min(5, n), bas = Math.max(1, Math.min(s - 2, n - k + 1)), d = [];
      for(var i = 0; i < k; i++) d.push(bas + i); return d; }
    S.ciz = function(toplam){
      var bas = toplam ? (S.sayfa - 1) * S.boy + 1 : 0, son = Math.min(toplam, S.sayfa * S.boy);
      S.bilgi.textContent = toplam ? sayiYaz(toplam) + ' sonuçtan ' + sayiYaz(bas) + '–' + sayiYaz(son) + ' · ' + sayiYaz(S.son) + ' sayfa' : 'Sonuç yok';
      S.bilgiK.textContent = toplam ? sayiYaz(bas) + '–' + sayiYaz(son) + ' / ' + sayiYaz(toplam) : 'Sonuç yok';
      pager.classList.toggle('is-tek', S.son <= 1);
      pager.querySelector('.pg-sayilar').innerHTML = sayilar().map(function(x){ return x === '…' ? '<span class="pg-ara" aria-hidden="true">…</span>' : '<button type="button" class="pg-btn pg-sayi' + (x === S.sayfa ? ' is-on' : '') + '" data-pg="' + x + '"' + (x === S.sayfa ? ' aria-current="page"' : '') + ' aria-label="Sayfa ' + x + '">' + x + '</button>'; }).join('');
      pager.querySelector('.pg-kisa').textContent = S.sayfa + ' / ' + S.son;
      [['ilk', S.sayfa <= 1], ['onceki', S.sayfa <= 1], ['sonraki', S.sayfa >= S.son], ['son', S.sayfa >= S.son]].forEach(function(x){ var b = pager.querySelector('[data-pg="' + x[0] + '"]'); b.disabled = x[1]; b.setAttribute('aria-disabled', x[1] ? 'true' : 'false'); });
    };
    pager.addEventListener('click', function(e){
      var b = e.target.closest('[data-pg]');
      if(!b || b.disabled) return;
      var p = b.dataset.pg, eski = S.sayfa;
      S.sayfa = p === 'ilk' ? 1 : p === 'son' ? S.son : p === 'onceki' ? S.sayfa - 1 : p === 'sonraki' ? S.sayfa + 1 : +p;
      if(S.sayfa === eski) return;
      degisti();
      var ust = document.querySelector('.pnl-top'), uh = ust ? ust.offsetHeight : 64;
      if(L.getBoundingClientRect().top < uh) window.scrollTo({ top: L.getBoundingClientRect().top + window.scrollY - uh - 12, behavior: 'smooth' });
      var oda = /^[0-9]+$/.test(p) ? pager.querySelector('.pg-sayi.is-on') : pager.querySelector('[data-pg="' + p + '"]');
      if(!oda || oda.disabled) oda = pager.querySelector('.pg-sayi.is-on'); if(oda) oda.focus();
    });
    return S;
  };

  /* ---------------- veri tablosu ---------------- */
  var YER_AD = { manset:'manşet', gunun5:'Günün 5\'i', bulten:'Akşam Bülteni' };
  function yerAdlari(r){ return (r.dataset.yerler || '').split(/\s+/).filter(Boolean).map(function(y){ return YER_AD[y] || y; }); }
  document.querySelectorAll('[data-liste]').forEach(function(L){
    /* liste kaydının adı: data-liste-ad="sayfa" (küçük harf, tekil); metinler buna göre yazılır. Varsayılan: haber. */
    var AD = L.dataset.listeAd || 'haber', BAD = AD.charAt(0).toLocaleUpperCase('tr') + AD.slice(1);
    /* gruplu liste: [data-liste][data-grupla] içinde birden çok tbody[data-satirlar][data-grup]; her grubun ilk satırı tr.kb-grup-bas
       (başlık, data-satir yok). Satırlar bütün gruplardan toplanır; görünür satırı kalmayan grup gizlenir. Gruplu listede sayfalama tek sayfa. */
    var govdeler = Array.prototype.slice.call(L.querySelectorAll('tbody[data-satirlar]')), govde = govdeler[0], grupla = L.hasAttribute('data-grupla');
    function satirTopla(){ return Array.prototype.slice.call(L.querySelectorAll('tbody[data-satirlar] tr[data-satir]')); }
    /* kart alanları: thead th[data-kart="ad|durum|neden|zaman|isaret|eylem|sec|…"] ızgara görünümünde hücrenin kart içindeki yerini verir;
       çekirdek değeri aynı sütundaki hücrelere aktarır (sayfa her hücreye yazmaz) */
    var kartTh = Array.prototype.slice.call(L.querySelectorAll('thead th'));
    if(kartTh.some(function(th){ return th.dataset.kart; })){
      L.setAttribute('data-kartli', '');
      L.querySelectorAll('tbody[data-satirlar] tr[data-satir]').forEach(function(r){ Array.prototype.forEach.call(r.children, function(td, i){ if(kartTh[i] && kartTh[i].dataset.kart && !td.dataset.kart) td.dataset.kart = kartTh[i].dataset.kart; }); });
    }
    var satirlar = satirTopla();
    var bosSatir = L.querySelector('tr.kb-bos-satir');
    var sekmeler = L.querySelectorAll('.chip[data-sekme]');
    var ara = L.querySelector('[data-liste-ara]');
    var suzler = L.querySelectorAll('.kb-secim[data-suz]');
    var toplu = L.querySelector('.kb-toplu'), cubuk = L.querySelector('.filter-bar');
    var hepsi = L.querySelector('[data-hepsini-sec]');
    var sayfaBoy, sayfa = 1, sonSayfa = 1, gecenler = [];
    var SY = window.kbSayfalaKur(L, function(){ uygula(); }), pager = SY.pager, bilgi = SY.bilgi, bilgiK = SY.bilgiK;
    sayfaBoy = SY.boy;
    var sekme = L.dataset.sekmeIlk || 'hepsi';
    /* data-suz-coklu: satır değeri "A|B|C" olabilir, süzgeç içerir eşleşmesi yapar (görselin birden çok kişisi gibi) */
    var coklu = {}, suzEk = {}; suzler.forEach(function(s){ if(s.hasAttribute('data-suz-coklu')) coklu[s.dataset.suz] = true; });
    /* görünüm: [data-gorunum-sec] düğmeleri (data-gorunum="izgara|liste") listeyi kart ızgarasına çevirir; seçim hatırlanır */
    var gorKey = 'kbGorunum:' + location.pathname + ':' + (L.id || '');
    function gorunum(g){ L.dataset.gorunum = g; L.querySelectorAll('[data-gorunum-sec] [data-gorunum]').forEach(function(b){ var on = b.dataset.gorunum === g; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', on); }); try{ localStorage.setItem(gorKey, g); }catch(x){} }
    if(L.querySelector('[data-gorunum-sec]')){
      var gk = null; try{ gk = localStorage.getItem(gorKey); }catch(x){}
      gorunum(gk || L.dataset.gorunum || 'liste');
      L.querySelector('[data-gorunum-sec]').addEventListener('click', function(e){ var b = e.target.closest('[data-gorunum]'); if(b) gorunum(b.dataset.gorunum); });
    }
    /* gez: [data-gez-suz="kategori" data-v="Savunma"] düğmesi aynı listedeki kb-secim[data-suz] süzgecini ayarlar; tekrar tıklayınca kaldırır */
    /* dışarıdan gez (sayfa düzeyi, ?suz-): L._kbGez(anahtar, değer) — süzgeç seçimi varsa onu ayarlar, yoksa satırın data-<anahtar> eşitliği */
    L._kbGez = function(k, v){
      var s = L.querySelector('.kb-secim[data-suz="' + k + '"]');
      if(s){ var o = s.querySelector('button[data-deger="' + v + '"]'); s.dataset.deger = v; s.classList.toggle('is-dolu', v !== ''); s.querySelectorAll('button[data-deger]').forEach(function(x){ x.classList.toggle('is-sec', x === o && v !== ''); });
        var lbl = s.querySelector('.ks-deger'); if(lbl) lbl.textContent = v === '' ? (s.dataset.bos || 'Tümü') : (o ? (o.getAttribute('data-ad') || o.firstChild.textContent) : v);
        s.dispatchEvent(new CustomEvent('kb-secim', { bubbles:true, detail:{ deger:v } })); }
      else { suzEk[k] = v; SY.sayfa = 1; uygula(); }
      L.querySelectorAll('[data-gez-suz="' + k + '"]').forEach(function(x){ var on = x.dataset.v === v && v !== ''; x.classList.toggle('is-on', on); x.setAttribute('aria-pressed', on); });
    };
    L._kbSay = function(k, v){ return satirlar.filter(function(r){ return gorunur(r) && r.dataset.durum !== 'cop' && (!v || ('|' + (r.dataset[k] || '') + '|').indexOf('|' + v + '|') > -1); }).length; };
    L.addEventListener('click', function(e){
      var b = e.target.closest('[data-gez-suz]'); if(!b || b.closest('[data-gez-kapsam]')) return;
      var k = b.dataset.gezSuz, v = b.classList.contains('is-on') ? '' : b.dataset.v, s = L.querySelector('.kb-secim[data-suz="' + k + '"]');
      L.querySelectorAll('[data-gez-suz="' + k + '"]').forEach(function(x){ x.classList.toggle('is-on', x === b && v !== ''); x.setAttribute('aria-pressed', x === b && v !== ''); });
      var o = s && s.querySelector('button[data-deger="' + v + '"]');
      if(s){
        s.dataset.deger = v; s.classList.toggle('is-dolu', v !== '');
        s.querySelectorAll('button[data-deger]').forEach(function(x){ x.classList.toggle('is-sec', x === o && v !== ''); });
        var lbl = s.querySelector('.ks-deger'); if(lbl) lbl.textContent = v === '' ? (s.dataset.bos || 'Tümü') : (o ? (o.getAttribute('data-ad') || o.firstChild.textContent) : v);
        s.dispatchEvent(new CustomEvent('kb-secim', { bubbles:true, detail:{ deger:v } }));
      } else { suzEk[k] = v; SY.sayfa = 1; uygula(); }
    }); /* data-sekme-ilk: "Tümü" sekmesi olmayan listelerde başlangıç (ör. AI havuzu, K6) */

    /* satırın kendi görünürlüğü: kapalı modül (data-modul-kapali) ve rol (data-roller) liste süzgecinden önce gelir */
    function gorunur(r){ if(r.hasAttribute('data-modul-kapali')) return false; var rl = r.getAttribute('data-roller'); return !rl || rl.split(' ').indexOf(doc.dataset.rol) > -1; }
    function uygula(){
      var v = ara ? tr(ara.value.trim()) : '', n = 0, suzVar = !!v;
      var sz = {}; suzler.forEach(function(s){ if(s.dataset.deger){ sz[s.dataset.suz] = s.dataset.deger; suzVar = true; } });
      Object.keys(suzEk).forEach(function(k){ if(suzEk[k]){ sz[k] = suzEk[k]; coklu[k] = true; suzVar = true; } });
      function gec(r){ /* arama ve süzgeçlerden geçiyor mu (sekmeden bağımsız) */
        if(v && tr(r.dataset.ara).indexOf(v) < 0) return false;
        return Object.keys(sz).every(function(k){ var rv = r.dataset[k] || '', istek = sz[k].split('|'); return istek.some(function(x){ return coklu[k] ? ('|' + rv + '|').indexOf('|' + x + '|') > -1 : rv === x; }); });
      }
      satirlar.forEach(function(r){
        var d = r.dataset.durum, g = gorunur(r) && (sekme === 'hepsi' ? d !== 'cop' : d === sekme) && gec(r);
        r._kbGecti = g; /* sayfalamadan önce süzgeçten geçti mi (bağlı takvim görünümü bunu okur) */
      });
      /* sekme sayaçları süzgeci izler: süzgeç ya da arama varken her sekme, süzgeçten geçen kayıtları sayar */
      if(suzVar) sekmeler.forEach(function(c){ if(c.dataset.sabit) return; var s = c.dataset.sekme, e = c.querySelector('.ch-cnt'); if(!e) return;
        e.textContent = sayiYaz(satirlar.filter(function(r){ return gorunur(r) && (s === 'hepsi' ? r.dataset.durum !== 'cop' : r.dataset.durum === s) && gec(r); }).length); });
      else if(L._kbSuzSayac) sayaclar();
      L._kbSuzSayac = suzVar;
      gecenler = satirlar.filter(function(r){ return r._kbGecti; });
      if(grupla) SY.boy = Math.max(SY.boy, gecenler.length || 1);
      sayfaBoy = SY.boy; SY.sinirla(gecenler.length); sayfa = SY.sayfa; sonSayfa = SY.son;
      var ilk_ = (sayfa - 1) * sayfaBoy;
      satirlar.forEach(function(r){ r.hidden = true; });
      gecenler.forEach(function(r, i){ var g = i >= ilk_ && i < ilk_ + sayfaBoy; r.hidden = !g; if(g) n++; });
      L.dispatchEvent(new CustomEvent('kb-liste-suzuldu', { detail:{ sekme: sekme } }));
      var ar = L.querySelector('.kb-arac'); if(ar && ar._kbArac && !ar._kbYerZam){ ar._kbYerZam = setTimeout(function(){ ar._kbYerZam = null; ar._kbArac.yerlestir(); }, 30); }
      if(bosSatir) bosSatir.hidden = n > 0;
      SY.ciz(gecenler.length);
      if(grupla) govdeler.forEach(function(g){ if(!g.hasAttribute('data-grup')) return; g.hidden = !g.querySelector('tr[data-satir]:not([hidden])'); var bas = g.querySelector('tr.kb-grup-bas .kgb-say'); if(bas) bas.textContent = g.querySelectorAll('tr[data-satir]:not([hidden])').length; });
      var tem = L.querySelector('[data-suz-temizle]'); if(tem) tem.hidden = !suzVar;
      secimGuncelle();
    }
    function secili(){ return satirlar.filter(function(r){ var k = r.querySelector('.kb-onay-kutu'); return k && k.checked && r._kbGecti; }); } /* sayfa değişince seçim korunur */
    function secimGuncelle(){
      var s = secili();
      satirlar.forEach(function(r){ var k = r.querySelector('.kb-onay-kutu'); r.classList.toggle('is-secili', !!(k && k.checked)); });
      if(toplu){ toplu.hidden = !s.length; var say = toplu.querySelector('[data-secili-say]');
        var sy = {}; s.forEach(function(r){ sy[Math.floor(gecenler.indexOf(r) / sayfaBoy)] = 1; }); var ks = Object.keys(sy).length;
        if(say) say.textContent = ks > 1 ? ks + ' sayfada ' + s.length + ' ' + AD + ' seçildi' : s.length + ' ' + AD + ' seçildi'; }
      if(cubuk) cubuk.hidden = !!s.length;
      if(hepsi){ var gor = satirlar.filter(function(r){ return !r.hidden; }), gs = gor.filter(function(r){ var k = r.querySelector('.kb-onay-kutu'); return k && k.checked; }).length; hepsi.checked = gor.length > 0 && gs === gor.length; hepsi.indeterminate = gs > 0 && gs < gor.length; }
    }
    function secimTemizle(){ satirlar.forEach(function(r){ var k = r.querySelector('.kb-onay-kutu'); if(k) k.checked = false; }); secimGuncelle(); }
    function sayaclar(){
      sekmeler.forEach(function(c){
        var s = c.dataset.sekme; if(c.dataset.sabit) return;
        var n = satirlar.filter(function(r){ return gorunur(r) && (s === 'hepsi' ? r.dataset.durum !== 'cop' : r.dataset.durum === s); }).length;
        var t = +(c.dataset.taban || 0) + n; c.dataset.toplam = t; var e = c.querySelector('.ch-cnt'); if(e) e.textContent = sayiYaz(t);
      });
    }

    sekmeler.forEach(function(c){
      c.addEventListener('click', function(){
        sekme = c.dataset.sekme; SY.sayfa = 1;
        sekmeler.forEach(function(x){ x.classList.toggle('is-on', x === c); x.setAttribute('aria-selected', x === c ? 'true' : 'false'); });
        secimTemizle(); uygula();
      });
    });
    if(ara) ara.addEventListener('input', function(){ SY.sayfa = 1; uygula(); });
    L.addEventListener('kb-secim', function(){ SY.sayfa = 1; uygula(); });
    L.querySelectorAll('[data-suz-temizle]').forEach(function(b){
      b.addEventListener('click', function(){
        if(ara) ara.value = '';
        SY.sayfa = 1; suzler.forEach(function(s){ var t = s.querySelector('button[data-deger=""]'); delete s.dataset.deger; s.classList.remove('is-dolu'); var l = s.querySelector('.ks-deger'); if(l) l.textContent = s.dataset.bos || 'Tümü'; s.querySelectorAll('.is-sec').forEach(function(x){ x.classList.remove('is-sec'); }); });
        uygula();
      });
    });
    if(hepsi) hepsi.addEventListener('change', function(){ satirlar.forEach(function(r){ if(!r.hidden){ var k = r.querySelector('.kb-onay-kutu'); if(k) k.checked = hepsi.checked; } }); secimGuncelle(); });
    L.querySelectorAll('[data-secim-temizle]').forEach(function(b){ b.addEventListener('click', secimTemizle); });

    /* toplu işlemler */
    L.querySelectorAll('[data-toplu]').forEach(function(b){
      b.addEventListener('click', function(){
        var s = secili(), is = b.dataset.toplu; if(!s.length) return;
        if(is === 'cop'){
          window.kbOnay({ tehlike:true, baslik: s.length + ' ' + AD + ' çöpe taşınsın mı?', metin:(L.dataset.listeCopNot || 'Seçilenler yayından kalkar ve Çöp sekmesine taşınır') + '; oradan geri alınabilir. İşlem denetim izine önceki ve sonraki haliyle yazılır.', evet:'Çöpe Taşı',
            evetIs: function(){ var eski = s.map(function(r){ return [r, r.dataset.durum]; }); s.forEach(function(r){ r.dataset.onceki = r.dataset.durum; r.dataset.durum = 'cop'; }); sayaclar(); secimTemizle(); uygula();
              window.kbBildir(s.length + ' ' + AD + ' çöpe taşındı', function(){ eski.forEach(function(x){ x[0].dataset.durum = x[1]; }); sayaclar(); uygula(); }); } });
        } else if(b.dataset.topluDurum){
          /* data-toplu-durum="okundu" [data-toplu-durum-ad] [data-toplu-durum-sinif]: seçili satırların durumu değişir; Geri al */
          var eski2 = s.map(function(r){ var rz = r.querySelector('.pstat'); return [r, r.dataset.durum, rz && rz.textContent, rz && rz.className]; });
          s.forEach(function(r){ r.dataset.durum = b.dataset.topluDurum; var rz = r.querySelector('.pstat'); if(rz){ if(b.dataset.topluDurumAd) rz.textContent = b.dataset.topluDurumAd; if(b.dataset.topluDurumSinif) rz.className = 'pstat ' + b.dataset.topluDurumSinif; } });
          sayaclar(); secimTemizle(); uygula();
          window.kbBildir(b.dataset.bildir || (s.length + ' ' + AD + ' güncellendi'), function(){ eski2.forEach(function(x){ x[0].dataset.durum = x[1]; var rz = x[0].querySelector('.pstat'); if(rz){ rz.textContent = x[2]; rz.className = x[3]; } }); sayaclar(); uygula(); });
        } else {
          window.kbBildir(b.dataset.bildir || 'İşlem uygulandı'); secimTemizle();
        }
      });
    });

    /* dışarıdan durum değişince (onay zinciri vb.) sayaçlar ve görünüm yenilenir */
    document.addEventListener('kb-rol', function(){ sayaclar(); uygula(); });
    L.addEventListener('kb-liste-yenile', function(){ satirlar = satirTopla(); sayaclar(); uygula(); });

    /* satır: tıklama sözleşmeye göre; içindeki düğme ve bağlantılar kendi işini yapar */
    satirlar.forEach(function(r){
      r.addEventListener('click', function(e){
        if(e.target.closest('a,button,input,label,.row-acts')) return;
        /* kendi düzenleme sayfası olmayan küçük kayıt (API anahtarı, cron görevi): satır tıklama "görüntüle" eylemini yapar */
        if(!r.dataset.href){ var g = r.querySelector('.row-acts > :first-child'); if(g && !g.disabled) g.click(); return; }
        if(ETK.satir === 'sayfa'){ location.href = r.dataset.href; return; }
        var sab = L.dataset.ozetSablon; if(!sab) return;
        window.kbAc(sab, ETK.satir, function(k){
          k.querySelector('h2').textContent = r.dataset.turAd ? r.dataset.turAd + ' özeti' : 'Özet';
          k.querySelectorAll('[data-oz]').forEach(function(el){
            var a = el.getAttribute('data-oz'), v = r.dataset[a] || '';
            if(a === 'gorsel'){ el.classList.toggle('kb-yok', !v); el.style.backgroundImage = v ? 'url(' + v + ')' : ''; el.textContent = v ? '' : 'Görsel eksik'; }
            else if(a === 'href'){ el.setAttribute('href', r.dataset.href); }
            else el.textContent = v;
          });
        });
      });
      var k = r.querySelector('.kb-onay-kutu'); if(k) k.addEventListener('change', secimGuncelle);
      var sil = r.querySelector('[data-sil]');
      if(sil) sil.addEventListener('click', function(){
        if(r.dataset.durum === 'cop'){ var k2 = dm && dm.querySelector('[data-kalici-sil]'); if(k2){ dm._satir = r; k2.click(); } return; }
        var b = r.dataset.baslik, yer = r.dataset.kullanim ? [r.dataset.kullanim] : yerAdlari(r);
        window.kbOnay({ tehlike:true, baslik:BAD + ' çöpe taşınsın mı?', metin:'“' + b + '” ' + (L.dataset.listeCopNot ? L.dataset.listeCopNot.charAt(0).toLocaleLowerCase('tr') + L.dataset.listeCopNot.slice(1) : 'yayından kalkar ve Çöp sekmesine taşınır') + '; oradan geri alınabilir.' + (yer.length ? (r.dataset.kullanim ? ' Kullanım: ' + r.dataset.kullanim + '.' : ' Bu kayıt ' + yer.length + ' yerde kullanılıyor (' + yer.join(', ') + '); oradan da çıkar, geri alınca döner.') : ''), evet:'Çöpe Taşı',
          evetIs: function(){ var eski = r.dataset.durum; r.dataset.onceki = eski; r.dataset.durum = 'cop'; sayaclar(); uygula(); window.kbBildir(BAD + ' çöpe taşındı', function(){ r.dataset.durum = eski; sayaclar(); uygula(); }); } });
      });
    });

    /* diğer menüsü: tek ortak menü, düğmenin altında açılır */
    var dm = L.querySelector('.kb-diger-menu');
    if(dm){
      document.body.appendChild(dm); dm.style.position = 'fixed';
      var dmBtn = null;
      L.querySelectorAll('[data-diger]').forEach(function(b){
        b.addEventListener('click', function(e){
          e.stopPropagation();
          if(dmBtn === b && dm.classList.contains('open')){ dm.classList.remove('open'); b.setAttribute('aria-expanded', 'false'); dmBtn = null; return; }
          if(dmBtn) dmBtn.setAttribute('aria-expanded', 'false');
          dmBtn = b; b.setAttribute('aria-expanded', 'true');
          var r = b.getBoundingClientRect();
          var row = b.closest('tr'), dr = row ? row.dataset.durum : '', rol = doc.dataset.rol;
          dm._satir = row;
          dm.querySelectorAll('[data-durum-icin]').forEach(function(x){ x.hidden = x.getAttribute('data-durum-icin').split(' ').indexOf(dr) === -1; });
          dm.querySelectorAll('[data-roller]').forEach(function(x){ if(!x.hidden) x.hidden = x.getAttribute('data-roller').split(' ').indexOf(rol) === -1; });
          /* data-kosul-icin="nitelik:değer1 değer2": satırın data-<nitelik> değeri listede değilse kalem gizlenir (ör. gorsel:temiz kirpildi) */
          dm.querySelectorAll('[data-kosul-icin]').forEach(function(x){ if(x.hidden) return; var k = x.getAttribute('data-kosul-icin').split(':'), v = row ? (row.getAttribute('data-' + k[0]) || '') : ''; x.hidden = (k[1] || '').split(' ').indexOf(v) === -1; });
          dm.querySelectorAll('[data-modul-kapali]').forEach(function(x){ x.hidden = true; });
          var yl = row ? (row.dataset.yerler || '').split(/\s+/) : [];
          dm.querySelectorAll('[data-yer]').forEach(function(x){ var var_ = yl.indexOf(x.dataset.yer) > -1, ad = x.dataset.yerAd; x.classList.toggle('is-cikar', var_);
            x.querySelector('span').textContent = var_ ? ad + (ad === 'Manşet' ? 'ten' : ad === 'Akşam Bülteni' ? 'nden' : 'nden') + ' çıkar' : ad + (ad === 'Manşet' ? 'e' : ad === 'Akşam Bülteni' ? 'ne' : 'ne') + ' ekle'; });
          /* konum açılmadan önce, kalemler süzüldükten sonra hesaplanır: altta yer yoksa doğrudan üstte açılır (zıplama yok) */
          var h = dm.offsetHeight, alt = r.bottom + 6;
          dm.style.left = 'auto'; dm.style.right = (window.innerWidth - r.right) + 'px';
          dm.style.top = (alt + h > window.innerHeight - 8 ? Math.max(8, r.top - h - 6) : alt) + 'px';
          dm.classList.toggle('kb-yukari', alt + h > window.innerHeight - 8);
          dm._kbTetik = b; dm.classList.add('open');
        });
      });
      document.addEventListener('click', function(e){ if(!e.target.closest('.kb-diger-menu') && dmBtn){ dm.classList.remove('open'); dmBtn.setAttribute('aria-expanded', 'false'); dmBtn = null; } });
      dm.querySelectorAll('[data-bildir]').forEach(function(x){ x.addEventListener('click', function(){ dm.classList.remove('open'); window.kbBildir(x.dataset.bildir); }); });
      var dmKapat = function(){ dm.classList.remove('open'); if(dmBtn){ dmBtn.setAttribute('aria-expanded', 'false'); dmBtn = null; } };
      dm.querySelectorAll('[data-yer]').forEach(function(x){ x.addEventListener('click', function(){
        var r = dm._satir; dmKapat(); if(!r) return;
        var yl = (r.dataset.yerler || '').split(/\s+/).filter(Boolean), y = x.dataset.yer, var_ = yl.indexOf(y) > -1, eski = r.dataset.yerler || '';
        r.dataset.yerler = (var_ ? yl.filter(function(z){ return z !== y; }) : yl.concat(y)).join(' ');
        window.kbBildir(var_ ? BAD + ' ' + YER_AD[y] + ' listesinden çıkarıldı' : BAD + ' ' + YER_AD[y] + ' listesine eklendi', function(){ r.dataset.yerler = eski; });
      }); });
      var kopyala = dm.querySelector('[data-kopyala]');
      if(kopyala) kopyala.addEventListener('click', function(){
        var a = dm._satir && dm._satir.querySelector('a.ia-btn[target]'); var u = a ? a.href : location.href;
        if(navigator.clipboard) navigator.clipboard.writeText(u).catch(function(){});
        dmKapat(); window.kbBildir('Bağlantı kopyalandı');
      });
      var geri = dm.querySelector('[data-geri-al]');
      if(geri) geri.addEventListener('click', function(){
        var r = dm._satir; dmKapat(); if(!r) return;
        r.dataset.durum = r.dataset.onceki || 'taslak'; sayaclar(); uygula();
        var dc = L.querySelector('.chip[data-sekme="' + r.dataset.durum + '"]'), dAd = dc ? dc.childNodes[0].textContent.trim().toLocaleLowerCase('tr') : r.dataset.durum;
        window.kbBildir(BAD + ' çöpten geri alındı (' + dAd + ')');
      });
      var kalici = dm.querySelector('[data-kalici-sil]');
      if(kalici) kalici.addEventListener('click', function(){
        var r = dm._satir; dmKapat(); if(!r) return;
        window.kbOnay({ tehlike:true, ikon:'fa-trash-can', baslik:BAD + ' kalıcı olarak silinsin mi?', metin:'“' + r.dataset.baslik + '” geri alınamayacak biçimde silinir. Bu işlem e-posta koduyla doğrulanır ve denetim izine yazılır.', evet:'Kalıcı Olarak Sil',
          evetIs: function(){
            var sil = function(){ satirlar = satirlar.filter(function(x){ return x !== r; }); r.remove(); sayaclar(); uygula(); window.kbBildir(BAD + ' kalıcı olarak silindi; denetim izine yazıldı'); };
            if(window.kbKod) window.kbKod({ baslik:'Kalıcı silmeyi doğrulayın', metin:'“' + r.dataset.baslik + '” geri alınamayacak biçimde silinecek.', evet:'Doğrula ve sil', evetIs: sil }); else sil();
          } });
      });
      window.addEventListener('scroll', function(e){ if(dmBtn && (!window.kbAcilirKaydir || window.kbAcilirKaydir(e, dm, dmBtn))){ dm.classList.remove('open'); dmBtn.setAttribute('aria-expanded', 'false'); dmBtn = null; } }, true);
    }


    /* önizleme durumları: ?durum=yukleniyor | hata | bos */
    var dur = q.get('durum');
    if(dur === 'yukleniyor' || dur === 'hata' || dur === 'bos'){
      govdeler.forEach(function(g){ g.hidden = true; });
      L.querySelectorAll('[data-durum-goster]').forEach(function(el){ el.hidden = el.getAttribute('data-durum-goster') !== dur; });
      satirlar = [];
    }

    sayaclar(); uygula();
    if(dur === 'yukleniyor' || dur === 'hata' || dur === 'bos'){ pager.classList.add('is-tek'); bilgi.textContent = bilgiK.textContent = dur === 'yukleniyor' ? 'Yükleniyor…' : '—'; if(bosSatir) bosSatir.hidden = true; }
  });
  /* ---------------- sayfa düzeyi gez ve adresten süzgeç ----------------
     <nav class="kb-medya-gez kb-gez-sayfa" data-gez-kapsam="#kap"> [data-gez-suz="brans" data-v="Futbol"] …: kapsamdaki BÜTÜN listelere uygulanır
     (sekmelere bölünmüş Kulüpler / Ligler / Maçlar gibi). data-v="" temizler. Düğmedeki <span> sayısı açık sekmedeki listeye göre canlı.
     Adres: ?suz-<anahtar>=<değer> → sayfadaki listeler (ve gez düğmeleri) o süzgeçle açılır; süzgeç etiket şeridinde görünür, Temizle kaldırır. */
  function gezSay(N){
    var kap = document.querySelector(N.getAttribute('data-gez-kapsam')) || document, L = Array.prototype.filter.call(kap.querySelectorAll('[data-liste]'), function(x){ return x.getClientRects().length && x._kbSay; })[0];
    if(!L) return; N.querySelectorAll('[data-gez-suz]').forEach(function(b){ var s = b.querySelector('span'); if(s) s.textContent = sayiYaz(L._kbSay(b.dataset.gezSuz, b.dataset.v || '')); });
  }
  window.kbGezSayfa = function(N, k, v){
    var kap = document.querySelector(N.getAttribute('data-gez-kapsam')) || document;
    kap.querySelectorAll('[data-liste]').forEach(function(L){ if(L._kbGez) L._kbGez(k, v); });
    N.querySelectorAll('[data-gez-suz="' + k + '"]').forEach(function(x){ var on = (x.dataset.v || '') === v; x.classList.toggle('is-on', on && v !== ''); x.setAttribute('aria-pressed', on ? 'true' : 'false'); });
  };
  document.querySelectorAll('[data-gez-kapsam]').forEach(function(N){
    N.addEventListener('click', function(e){ var b = e.target.closest('[data-gez-suz]'); if(!b) return; e.preventDefault();
      var v = b.classList.contains('is-on') ? '' : (b.dataset.v || ''); window.kbGezSayfa(N, b.dataset.gezSuz, v); });
    gezSay(N);
    document.addEventListener('click', function(e){ if(e.target.closest && e.target.closest('.sa-form-tab, .chip[data-sekme]')) setTimeout(function(){ gezSay(N); }, 0); });
  });
  (function(){ /* ?suz-<anahtar>=<değer> */
    var ver = []; q.forEach(function(v, k){ if(k.indexOf('suz-') === 0) ver.push([k.slice(4), v]); }); if(!ver.length) return;
    setTimeout(function(){ ver.forEach(function(x){
      var N = Array.prototype.filter.call(document.querySelectorAll('[data-gez-kapsam]'), function(n){ return n.querySelector('[data-gez-suz="' + x[0] + '"]'); })[0];
      if(N) window.kbGezSayfa(N, x[0], x[1]); else document.querySelectorAll('[data-liste]').forEach(function(L){ if(L._kbGez) L._kbGez(x[0], x[1]); });
    }); }, 0);
  })();


})();
