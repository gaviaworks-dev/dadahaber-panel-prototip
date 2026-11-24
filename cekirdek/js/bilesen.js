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
  window.kbBildir = function(metin, geriAl){
    var t = document.createElement('div'); t.className = 'sa-toast';
    t.innerHTML = '<i class="fa-solid fa-circle-check" aria-hidden="true"></i><span></span>';
    t.querySelector('span').textContent = metin;
    if(geriAl){
      var b = document.createElement('button'); b.type = 'button'; b.textContent = 'Geri al';
      b.addEventListener('click', function(){ geriAl(); t.remove(); }); t.appendChild(b);
    }
    tw.appendChild(t); requestAnimationFrame(function(){ t.classList.add('show'); });
    setTimeout(function(){ t.classList.remove('show'); setTimeout(function(){ t.remove(); }, 300); }, 5000);
  };

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
    window.kbSecimKur(govde); window.kbSecimKur(alt);
    if(doldur) doldur(k);
    window.kbSayaclar(k);
    if(window.kbAcKapat) window.kbAcKapat();
    if(acikKap && acikKap !== k){ acikKap.classList.remove('open'); acikKap.hidden = true; }
    if(!acikKap) kapOnce = document.activeElement;
    acikKap = k;
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
        window.kbAc(sa.getAttribute('data-sablon-ac'), t, function(k){ degerleriYaz(sa, k); if(sa.dataset.baslikYaz) k.querySelector('h2').textContent = sa.dataset.baslikYaz; });
        if(bildir) window.kbBildir(bildir);
      }
    });
  });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape'){ if(ov.classList.contains('open')) onayKapat(); else window.kbKapat(); } });

  /* küçük tanımlar: [data-tanim="sablonId"] düğmesi sözleşmeye göre çekmece ya da pencere açar;
     sözleşme "sayfa" ise düğmenin href'ine gidilir */
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
  });

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
    var kok = el.closest('.kb-kap-govde,form,[data-form]') || document;
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
  document.querySelectorAll('[data-liste]').forEach(function(L){
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
    var sekme = 'hepsi';

    function uygula(){
      var v = ara ? tr(ara.value.trim()) : '', n = 0, suzVar = !!v;
      var sz = {}; suzler.forEach(function(s){ if(s.dataset.deger){ sz[s.dataset.suz] = s.dataset.deger; suzVar = true; } });
      satirlar.forEach(function(r){
        var d = r.dataset.durum, g = sekme === 'hepsi' ? d !== 'cop' : d === sekme;
        if(g && v) g = tr(r.dataset.ara).indexOf(v) > -1;
        if(g) Object.keys(sz).forEach(function(k){ if(r.dataset[k] !== sz[k]) g = false; });
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
      if(toplu){ toplu.hidden = !s.length; var say = toplu.querySelector('[data-secili-say]'); if(say) say.textContent = s.length + ' haber seçildi'; }
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
          window.kbOnay({ tehlike:true, baslik: s.length + ' haber çöpe taşınsın mı?', metin:'Haberler sitede yayından kalkar ve Çöp sekmesine taşınır; oradan geri alınabilir. İşlem denetim izine önceki ve sonraki haliyle yazılır.', evet:'Çöpe taşı',
            evetIs: function(){ var eski = s.map(function(r){ return [r, r.dataset.durum]; }); s.forEach(function(r){ r.dataset.onceki = r.dataset.durum; r.dataset.durum = 'cop'; }); sayaclar(); secimTemizle(); uygula();
              window.kbBildir(s.length + ' haber çöpe taşındı', function(){ eski.forEach(function(x){ x[0].dataset.durum = x[1]; }); sayaclar(); uygula(); }); } });
        } else {
          window.kbBildir(b.dataset.bildir || 'İşlem uygulandı'); secimTemizle();
        }
      });
    });

    /* satır: tıklama sözleşmeye göre; içindeki düğme ve bağlantılar kendi işini yapar */
    satirlar.forEach(function(r){
      r.addEventListener('click', function(e){
        if(e.target.closest('a,button,input,label,.row-acts')) return;
        if(ETK.satir === 'sayfa'){ if(r.dataset.href) location.href = r.dataset.href; return; }
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
        var b = r.dataset.baslik;
        window.kbOnay({ tehlike:true, baslik:'Haber çöpe taşınsın mı?', metin:'“' + b + '” sitede yayından kalkar ve Çöp sekmesine taşınır; oradan geri alınabilir.', evet:'Çöpe taşı',
          evetIs: function(){ var eski = r.dataset.durum; r.dataset.onceki = eski; r.dataset.durum = 'cop'; sayaclar(); uygula(); window.kbBildir('Haber çöpe taşındı', function(){ r.dataset.durum = eski; sayaclar(); uygula(); }); } });
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
          dm.style.top = (r.bottom + 6) + 'px'; dm.style.left = 'auto'; dm.style.right = (window.innerWidth - r.right) + 'px';
          var row = b.closest('tr'), dr = row ? row.dataset.durum : '', rol = doc.dataset.rol;
          dm._satir = row;
          dm.querySelectorAll('[data-durum-icin]').forEach(function(x){ x.hidden = x.getAttribute('data-durum-icin').split(' ').indexOf(dr) === -1; });
          dm.querySelectorAll('[data-roller]').forEach(function(x){ if(!x.hidden) x.hidden = x.getAttribute('data-roller').split(' ').indexOf(rol) === -1; });
          dm.classList.add('open');
          var mr = dm.getBoundingClientRect();
          if(mr.bottom > window.innerHeight - 8) dm.style.top = Math.max(8, r.top - mr.height - 6) + 'px';
        });
      });
      document.addEventListener('click', function(e){ if(!e.target.closest('.kb-diger-menu') && dmBtn){ dm.classList.remove('open'); dmBtn.setAttribute('aria-expanded', 'false'); dmBtn = null; } });
      dm.querySelectorAll('[data-bildir]').forEach(function(x){ x.addEventListener('click', function(){ dm.classList.remove('open'); window.kbBildir(x.dataset.bildir); }); });
      var dmKapat = function(){ dm.classList.remove('open'); if(dmBtn){ dmBtn.setAttribute('aria-expanded', 'false'); dmBtn = null; } };
      var kopyala = dm.querySelector('[data-kopyala]');
      if(kopyala) kopyala.addEventListener('click', function(){
        var a = dm._satir && dm._satir.querySelector('a.ia-btn[target]'); var u = a ? a.href : location.href;
        if(navigator.clipboard) navigator.clipboard.writeText(u).catch(function(){});
        dmKapat(); window.kbBildir('Bağlantı kopyalandı');
      });
      var geri = dm.querySelector('[data-geri-al]');
      if(geri) geri.addEventListener('click', function(){
        var r = dm._satir; dmKapat(); if(!r) return;
        r.dataset.durum = r.dataset.onceki || 'taslak'; sayaclar(); uygula(); window.kbBildir('Haber çöpten geri alındı (' + (r.dataset.durum === 'yayinda' ? 'yayında' : 'taslak') + ')');
      });
      var kalici = dm.querySelector('[data-kalici-sil]');
      if(kalici) kalici.addEventListener('click', function(){
        var r = dm._satir; dmKapat(); if(!r) return;
        window.kbOnay({ tehlike:true, ikon:'fa-trash-can', baslik:'Haber kalıcı olarak silinsin mi?', metin:'“' + r.dataset.baslik + '” geri alınamayacak biçimde silinir. Bu işlem e-posta koduyla doğrulanır ve denetim izine yazılır.', evet:'Kalıcı olarak sil',
          evetIs: function(){ satirlar = satirlar.filter(function(x){ return x !== r; }); r.remove(); sayaclar(); uygula(); window.kbBildir('Haber kalıcı olarak silindi'); } });
      });
      window.addEventListener('scroll', function(){ if(dmBtn){ dm.classList.remove('open'); dmBtn.setAttribute('aria-expanded', 'false'); dmBtn = null; } }, true);
    }

    L.querySelectorAll('[data-bildir-pg]').forEach(function(b){ b.addEventListener('click', function(){ window.kbBildir('Prototipte yalnızca ilk sayfa gösteriliyor'); }); });

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
