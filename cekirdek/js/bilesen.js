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
  ov.innerHTML = '<div class="sa-modal" role="alertdialog" aria-modal="true" aria-labelledby="kbOnayBas"><div class="sa-modal-ico"><i class="fa-solid fa-trash" aria-hidden="true"></i></div>'
    + '<h2 id="kbOnayBas"></h2><p></p><div class="sa-modal-acts"><button type="button" class="btn btn-ghost" data-onay-hayir>Vazgeç</button><button type="button" class="btn btn-danger" data-onay-evet></button></div></div>';
  document.body.appendChild(ov);
  var onayIs = null, onayOnce = null;
  window.kbOnay = function(o){
    ov.querySelector('.sa-modal').classList.toggle('danger', !!o.tehlike);
    ov.querySelector('.sa-modal-ico i').className = 'fa-solid ' + (o.ikon || 'fa-trash');
    ov.querySelector('h2').textContent = o.baslik; ov.querySelector('p').textContent = o.metin;
    ov.querySelector('[data-onay-evet]').textContent = o.evet || 'Onayla';
    ov.querySelector('[data-onay-evet]').className = 'btn ' + (o.tehlike ? 'btn-danger' : 'btn-acc');
    onayIs = o.evetIs; onayOnce = document.activeElement;
    ov.classList.add('open'); ov.querySelector('[data-onay-hayir]').focus();
  };
  function onayKapat(){ ov.classList.remove('open'); if(onayOnce && onayOnce.focus) onayOnce.focus(); }
  ov.addEventListener('click', function(e){
    if(e.target === ov || e.target.closest('[data-onay-hayir]')) onayKapat();
    if(e.target.closest('[data-onay-evet]')){ onayKapat(); if(onayIs) onayIs(); }
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
  window.kbAc = function(sablonId, tur, doldur){
    var s = document.getElementById(sablonId); if(!s) return;
    var k = kaplar[tur] || kaplar.cekmece;
    k.querySelector('h2').textContent = s.dataset.baslik || '';
    k.querySelector('.kb-kap-alt').textContent = s.dataset.alt || '';
    var govde = k.querySelector('.kb-kap-govde'), alt = k.querySelector('.kb-kap-alt-cubuk');
    var parca = s.content.cloneNode(true);
    var ac = parca.querySelector('.kb-kap-alt-cubuk');
    alt.innerHTML = ''; alt.hidden = !ac;
    if(ac){ while(ac.firstChild) alt.appendChild(ac.firstChild); ac.remove(); }
    govde.innerHTML = ''; govde.appendChild(parca);
    if(s.dataset.zorunluKayit) govde.setAttribute('data-zorunlu-kayit', s.dataset.zorunluKayit); else govde.removeAttribute('data-zorunlu-kayit');
    window.kbSecimKur(govde); window.kbSecimKur(alt);
    if(window.kbKur){ window.kbKur(govde); window.kbKur(alt); }
    setTimeout(window.kbPasifGuncelle, 0);
    if(doldur) doldur(k);
    window.kbSayaclar(k);
    if(window.kbAcKapat) window.kbAcKapat();
    if(acikKap && acikKap !== k){ acikKap.classList.remove('open'); acikKap.hidden = true; }
    if(!acikKap) kapOnce = document.activeElement;
    acikKap = k; k._satir = sonSatir;
    k.hidden = false; perde.classList.add('open');
    requestAnimationFrame(function(){ k.classList.add('open'); k.querySelector('.kb-kapat').focus(); });
    document.body.style.overflow = 'hidden';
  };
  window.kbKapat = function(){
    if(!acikKap) return;
    var k = acikKap; acikKap = null;
    k.classList.remove('open'); perde.classList.remove('open'); document.body.style.overflow = '';
    setTimeout(function(){ k.hidden = true; }, 260);
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
    if(!haber){ window.kbOnay({ tehlike:true, baslik:'“' + ad + '” silinsin mi?', metin:'Bu konuda haber yok. Çöpe gider, oradan geri alınabilir; işlem denetim izine yazılır.', evet:'Çöpe taşı', evetIs: function(){ sil(null); } }); return; }
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
  });
  /* sağ sütun sekmeye göre: önizlemesi olan sekmede önizleme en üstte ve yapışkan; data-one-cik kartı kendi sekmesinde üste çıkar */
  function yanDuzen(pid){
    var yan = document.querySelector('.side-card'); if(!yan) return;
    var var_ = false;
    yan.querySelectorAll('[data-panel-icin]').forEach(function(x){ var on = x.getAttribute('data-panel-icin') === pid; x.hidden = !on; if(on) var_ = true; });
    yan.querySelectorAll('[data-one-cik]').forEach(function(x){ x.style.order = x.getAttribute('data-one-cik') === pid ? -1 : ''; });
    yan.classList.toggle('kb-onizlemeli', var_);
  }
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

  /* ---------------- veri tablosu ---------------- */
  var YER_AD = { manset:'manşet', gunun5:'Günün 5\'i', bulten:'Akşam Bülteni' };
  function yerAdlari(r){ return (r.dataset.yerler || '').split(/\s+/).filter(Boolean).map(function(y){ return YER_AD[y] || y; }); }
  document.querySelectorAll('[data-liste]').forEach(function(L){
    /* liste kaydının adı: data-liste-ad="sayfa" (küçük harf, tekil); metinler buna göre yazılır. Varsayılan: haber. */
    var AD = L.dataset.listeAd || 'haber', BAD = AD.charAt(0).toLocaleUpperCase('tr') + AD.slice(1);
    var govde = L.querySelector('tbody[data-satirlar]');
    var satirlar = Array.prototype.slice.call(govde.querySelectorAll('tr[data-satir]'));
    var bosSatir = L.querySelector('tr.kb-bos-satir');
    var sekmeler = L.querySelectorAll('.chip[data-sekme]');
    var ara = L.querySelector('[data-liste-ara]');
    var suzler = L.querySelectorAll('.kb-secim[data-suz]');
    var bilgi = L.querySelector('.pager-info');
    var toplu = L.querySelector('.kb-toplu'), cubuk = L.querySelector('.filter-bar');
    var hepsi = L.querySelector('[data-hepsini-sec]');
    var sayfaBoy = +(L.dataset.sayfaBoy || 25);
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
    L.addEventListener('click', function(e){
      var b = e.target.closest('[data-gez-suz]'); if(!b) return;
      var k = b.dataset.gezSuz, v = b.classList.contains('is-on') ? '' : b.dataset.v, s = L.querySelector('.kb-secim[data-suz="' + k + '"]');
      L.querySelectorAll('[data-gez-suz="' + k + '"]').forEach(function(x){ x.classList.toggle('is-on', x === b && v !== ''); x.setAttribute('aria-pressed', x === b && v !== ''); });
      var o = s && s.querySelector('button[data-deger="' + v + '"]');
      if(s){
        s.dataset.deger = v; s.classList.toggle('is-dolu', v !== '');
        s.querySelectorAll('button[data-deger]').forEach(function(x){ x.classList.toggle('is-sec', x === o && v !== ''); });
        var lbl = s.querySelector('.ks-deger'); if(lbl) lbl.textContent = v === '' ? (s.dataset.bos || 'Tümü') : (o ? (o.getAttribute('data-ad') || o.firstChild.textContent) : v);
        s.dispatchEvent(new CustomEvent('kb-secim', { bubbles:true, detail:{ deger:v } }));
      } else { suzEk[k] = v; uygula(); }
    }); /* data-sekme-ilk: "Tümü" sekmesi olmayan listelerde başlangıç (ör. AI havuzu, K6) */

    function uygula(){
      var v = ara ? tr(ara.value.trim()) : '', n = 0, suzVar = !!v;
      var sz = {}; suzler.forEach(function(s){ if(s.dataset.deger){ sz[s.dataset.suz] = s.dataset.deger; suzVar = true; } });
      Object.keys(suzEk).forEach(function(k){ if(suzEk[k]){ sz[k] = suzEk[k]; coklu[k] = true; suzVar = true; } });
      satirlar.forEach(function(r){
        var d = r.dataset.durum, g = sekme === 'hepsi' ? d !== 'cop' : d === sekme;
        if(g && v) g = tr(r.dataset.ara).indexOf(v) > -1;
        if(g) Object.keys(sz).forEach(function(k){ var rv = r.dataset[k] || ''; if(coklu[k] ? ('|' + rv + '|').indexOf('|' + sz[k] + '|') === -1 : rv !== sz[k]) g = false; });
        if(g && n >= sayfaBoy) g = false;
        r.hidden = !g; if(g) n++;
      });
      if(bosSatir) bosSatir.hidden = n > 0;
      var sk = L.querySelector('.chip[data-sekme="' + sekme + '"]');
      var toplam = suzVar ? n : +(sk && sk.dataset.toplam || n);
      if(bilgi) bilgi.textContent = n ? sayiYaz(toplam) + ' sonuçtan 1–' + sayiYaz(n) + ' gösteriliyor' : 'Sonuç yok';
      L.querySelectorAll('.pager-btns').forEach(function(p){ p.hidden = !n || toplam <= sayfaBoy; });
      var tem = L.querySelector('[data-suz-temizle]'); if(tem) tem.hidden = !suzVar;
      secimGuncelle();
    }
    function secili(){ return satirlar.filter(function(r){ var k = r.querySelector('.kb-onay-kutu'); return k && k.checked && !r.hidden; }); }
    function secimGuncelle(){
      var s = secili();
      satirlar.forEach(function(r){ var k = r.querySelector('.kb-onay-kutu'); r.classList.toggle('is-secili', !!(k && k.checked)); });
      if(toplu){ toplu.hidden = !s.length; var say = toplu.querySelector('[data-secili-say]'); if(say) say.textContent = s.length + ' ' + AD + ' seçildi'; }
      if(cubuk) cubuk.hidden = !!s.length;
      if(hepsi){ var gor = satirlar.filter(function(r){ return !r.hidden; }); hepsi.checked = gor.length > 0 && s.length === gor.length; hepsi.indeterminate = s.length > 0 && s.length < gor.length; }
    }
    function secimTemizle(){ satirlar.forEach(function(r){ var k = r.querySelector('.kb-onay-kutu'); if(k) k.checked = false; }); secimGuncelle(); }
    function sayaclar(){
      sekmeler.forEach(function(c){
        var s = c.dataset.sekme; if(c.dataset.sabit) return;
        var n = satirlar.filter(function(r){ return s === 'hepsi' ? r.dataset.durum !== 'cop' : r.dataset.durum === s; }).length;
        var t = +(c.dataset.taban || 0) + n; c.dataset.toplam = t; var e = c.querySelector('.ch-cnt'); if(e) e.textContent = sayiYaz(t);
      });
    }

    sekmeler.forEach(function(c){
      c.addEventListener('click', function(){
        sekme = c.dataset.sekme;
        sekmeler.forEach(function(x){ x.classList.toggle('is-on', x === c); x.setAttribute('aria-selected', x === c ? 'true' : 'false'); });
        secimTemizle(); uygula();
      });
    });
    if(ara) ara.addEventListener('input', uygula);
    L.addEventListener('kb-secim', uygula);
    L.querySelectorAll('[data-suz-temizle]').forEach(function(b){
      b.addEventListener('click', function(){
        if(ara) ara.value = '';
        suzler.forEach(function(s){ var t = s.querySelector('button[data-deger=""]'); delete s.dataset.deger; s.classList.remove('is-dolu'); var l = s.querySelector('.ks-deger'); if(l) l.textContent = s.dataset.bos || 'Tümü'; s.querySelectorAll('.is-sec').forEach(function(x){ x.classList.remove('is-sec'); }); });
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
          window.kbOnay({ tehlike:true, baslik: s.length + ' ' + AD + ' çöpe taşınsın mı?', metin:(L.dataset.listeCopNot || 'Seçilenler yayından kalkar ve Çöp sekmesine taşınır') + '; oradan geri alınabilir. İşlem denetim izine önceki ve sonraki haliyle yazılır.', evet:'Çöpe taşı',
            evetIs: function(){ var eski = s.map(function(r){ return [r, r.dataset.durum]; }); s.forEach(function(r){ r.dataset.onceki = r.dataset.durum; r.dataset.durum = 'cop'; }); sayaclar(); secimTemizle(); uygula();
              window.kbBildir(s.length + ' ' + AD + ' çöpe taşındı', function(){ eski.forEach(function(x){ x[0].dataset.durum = x[1]; }); sayaclar(); uygula(); }); } });
        } else {
          window.kbBildir(b.dataset.bildir || 'İşlem uygulandı'); secimTemizle();
        }
      });
    });

    /* dışarıdan durum değişince (onay zinciri vb.) sayaçlar ve görünüm yenilenir */
    L.addEventListener('kb-liste-yenile', function(){ satirlar = Array.prototype.slice.call(govde.querySelectorAll('tr[data-satir]')); sayaclar(); uygula(); });

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
        window.kbOnay({ tehlike:true, baslik:BAD + ' çöpe taşınsın mı?', metin:'“' + b + '” ' + (L.dataset.listeCopNot ? L.dataset.listeCopNot.charAt(0).toLocaleLowerCase('tr') + L.dataset.listeCopNot.slice(1) : 'yayından kalkar ve Çöp sekmesine taşınır') + '; oradan geri alınabilir.' + (yer.length ? (r.dataset.kullanim ? ' Kullanım: ' + r.dataset.kullanim + '.' : ' Bu kayıt ' + yer.length + ' yerde kullanılıyor (' + yer.join(', ') + '); oradan da çıkar, geri alınca döner.') : ''), evet:'Çöpe taşı',
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
          dm.classList.add('open');
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
        window.kbOnay({ tehlike:true, ikon:'fa-trash-can', baslik:BAD + ' kalıcı olarak silinsin mi?', metin:'“' + r.dataset.baslik + '” geri alınamayacak biçimde silinir. Bu işlem e-posta koduyla doğrulanır ve denetim izine yazılır.', evet:'Kalıcı olarak sil',
          evetIs: function(){
            var sil = function(){ satirlar = satirlar.filter(function(x){ return x !== r; }); r.remove(); sayaclar(); uygula(); window.kbBildir(BAD + ' kalıcı olarak silindi; denetim izine yazıldı'); };
            if(window.kbKod) window.kbKod({ baslik:'Kalıcı silmeyi doğrulayın', metin:'“' + r.dataset.baslik + '” geri alınamayacak biçimde silinecek.', evet:'Doğrula ve sil', evetIs: sil }); else sil();
          } });
      });
      window.addEventListener('scroll', function(){ if(dmBtn){ dm.classList.remove('open'); dmBtn.setAttribute('aria-expanded', 'false'); dmBtn = null; } }, true);
    }

    L.querySelectorAll('[data-bildir-pg]').forEach(function(b){ b.addEventListener('click', function(){ window.kbBildir('Prototipte yalnızca ilk sayfa gösteriliyor', null, 'bilgi'); }); });

    /* önizleme durumları: ?durum=yukleniyor | hata | bos */
    var dur = q.get('durum');
    if(dur === 'yukleniyor' || dur === 'hata' || dur === 'bos'){
      govde.hidden = true;
      L.querySelectorAll('[data-durum-goster]').forEach(function(el){ el.hidden = el.getAttribute('data-durum-goster') !== dur; });
      L.querySelectorAll('.pager-btns').forEach(function(x){ x.hidden = true; });
      satirlar = [];
    }

    sayaclar(); uygula();
    if(dur === 'yukleniyor' || dur === 'hata' || dur === 'bos'){ L.querySelectorAll('.pager-btns').forEach(function(x){ x.hidden = true; }); if(bilgi) bilgi.textContent = dur === 'yukleniyor' ? 'Yükleniyor…' : '—'; if(bosSatir) bosSatir.hidden = true; }
  });
})();
