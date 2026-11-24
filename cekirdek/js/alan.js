/* =====================================================================
   ÇEKİRDEK · ALAN VE ONAY BİLEŞENLERİ (bütün modüllerde aynı)
   - kb-kanallar     : yayın kanalları seçimi (Web · Uygulama · Sosyal Medya; Yasin Bey Y1)
   - kb-okuma-onay   : içerik sonuna kadar okununca etkinleşen onay düğmesi (Y2/Y3)
   - kbKod           : e-posta koduyla doğrulama penceresi (K15; hassas işlemler)
   - .kb-eposta-onizleme : e-posta önizleme kabı (masaüstü / telefon genişliği)
   - kb-maske        : maskeli gizli değer (yalnızca oluşturma anında açık; yenileme e-posta koduyla)
   - kb-tel          : ülke kodlu, maskeli telefon alanı
   - [data-eposta]   : yazılırken doğrulanan e-posta alanı
   - [data-siralanir]: sürükleyerek ya da klavyeyle sıralanan liste
   - [data-anahtar]  : özellik anahtarı (önce/sonra onayı, geri al, denetim izi)
   ===================================================================== */
(function(){
  'use strict';
  var doc = document.documentElement;
  function rol(){ return doc.dataset.rol || 'super'; }
  function ad(){ var el = document.getElementById('pmName'); return el ? el.textContent : ''; }

  /* ---------------- yayın kanalları ---------------- */
  window.kbKurucu('.kb-kanallar', function(K){
    var not = K.parentNode.querySelector('[data-kanal-uyari]');
    function guncelle(){
      var secili = K.querySelectorAll('input:checked').length;
      K.classList.toggle('is-bos', secili === 0);
      if(not) not.hidden = secili !== 0;
    }
    K.addEventListener('change', guncelle); guncelle();
  });

  /* ---------------- okuma onayı ----------------
     <div class="kb-okuma-onay" data-okuma-hedef="#icerik" data-okuma-roller="editor kat-ed">
       <button class="btn btn-acc" data-okuma-btn>Onayla ve Yayınla</button><span class="ko-neden"></span></div>
     Hedef kendi içinde kayıyorsa onu, kaymıyorsa sayfayı izler. Kural rolde geçerli değilse düğme hemen etkindir. */
  window.kbKurucu('.kb-okuma-onay', function(O){
    var hedef = document.querySelector(O.getAttribute('data-okuma-hedef')), btn = O.querySelector('[data-okuma-btn]'), neden = O.querySelector('.ko-neden');
    if(!hedef || !btn) return;
    var okundu = false;
    function gecerli(){ return (O.getAttribute('data-okuma-roller') || '').split(/\s+/).indexOf(rol()) > -1; }
    function oran(){
      if(hedef.scrollHeight > hedef.clientHeight + 2){
        return hedef.scrollHeight - hedef.clientHeight <= 0 ? 1 : hedef.scrollTop / (hedef.scrollHeight - hedef.clientHeight);
      }
      var r = hedef.getBoundingClientRect(), gorunen = window.innerHeight - 90;
      if(r.height <= 0) return 0;
      return Math.max(0, Math.min(1, (gorunen - r.top) / r.height));
    }
    /* içerik ekrana sığıyorsa (kaydırılacak bir şey yoksa) düğme birkaç saniye sonra açılır (YS5) */
    var sure = +(O.getAttribute('data-okuma-sure') || 3), sayacBasladi = false, kalan = sure;
    function sigiyor(){
      if(hedef.scrollHeight > hedef.clientHeight + 2) return false;
      var r = hedef.getBoundingClientRect(); return r.top >= 0 && r.bottom <= window.innerHeight - 90;
    }
    function sayacBaslat(){
      if(sayacBasladi) return; sayacBasladi = true; kalan = sure;
      var z = setInterval(function(){ kalan--; if(kalan <= 0){ clearInterval(z); okundu = true; } ciz(); }, 1000);
    }
    function ciz(){
      if(!gecerli()){
        btn.disabled = false; O.classList.remove('is-bekliyor', 'is-okundu');
        neden.innerHTML = '';
        return;
      }
      var o = oran(); if(o >= .99 && !sigiyor()) okundu = true;
      if(!okundu && sigiyor()){ sayacBaslat(); }
      btn.disabled = !okundu;
      O.classList.toggle('is-bekliyor', !okundu); O.classList.toggle('is-okundu', okundu);
      O.style.setProperty('--ko', (okundu ? 100 : Math.round(o * 100)) + '%');
      neden.innerHTML = okundu
        ? '<i class="fa-solid fa-circle-check" aria-hidden="true"></i>İçerik sonuna kadar okundu'
        : sayacBasladi ? '<i class="fa-solid fa-hourglass-half" aria-hidden="true"></i>İçerik ekrana sığıyor; okumanız için <b>' + kalan + ' sn</b> sonra açılır'
        : '<i class="fa-solid fa-book-open-reader" aria-hidden="true"></i>Onaylamak için içeriği sonuna kadar okuyun <b>%' + Math.round(o * 100) + '</b>';
    }
    btn.setAttribute('aria-describedby', neden.id || (neden.id = 'ko' + Math.random().toString(36).slice(2, 7)));
    hedef.addEventListener('scroll', ciz, { passive:true });
    window.addEventListener('scroll', ciz, { passive:true });
    window.addEventListener('resize', ciz);
    document.addEventListener('kb-rol', function(){ okundu = false; sayacBasladi = false; ciz(); });
    ciz();
  });

  /* ---------------- e-posta kodu (K15) ---------------- */
  var kov = null, kodIs = null, kodOnce = null, sure = null;
  function kodKur(){
    kov = document.createElement('div'); kov.className = 'sa-modal-ov kb-kod-ov';
    kov.innerHTML = '<div class="sa-modal kb-kod" role="alertdialog" aria-modal="true" aria-labelledby="kbKodBas"><div class="sa-modal-ico"><i class="fa-solid fa-envelope-circle-check" aria-hidden="true"></i></div>'
      + '<h2 id="kbKodBas"></h2><p data-kod-metin></p>'
      + '<div class="kb-kod-kutular" role="group" aria-label="6 haneli kod" data-zorunlu-kod>' + [0,1,2,3,4,5].map(function(i){ return '<input inputmode="numeric" maxlength="1" aria-label="' + (i + 1) + '. hane" autocomplete="one-time-code">'; }).join('') + '</div>'
      + '<div class="kb-kod-alt"><span data-kod-sure></span><button type="button" class="kb-bag" data-kod-yeniden disabled>Kodu yeniden gönder</button></div>'
      + '<div class="ferr kb-kod-hata" data-kod-hata><i class="fa-solid fa-circle-exclamation" aria-hidden="true"></i>Kod 6 rakam olmalı.</div>'
      + '<p class="fhint kb-kod-ipucu">Prototip: herhangi 6 rakam kabul edilir.</p>'
      + '<div class="sa-modal-acts"><button type="button" class="btn btn-ghost" data-kod-hayir>Vazgeç</button><button type="button" class="btn btn-acc" data-kod-evet>Doğrula</button></div></div>';
    document.body.appendChild(kov);
    var kutular = kov.querySelectorAll('.kb-kod-kutular input');
    function kodPasif(){ var b = kov.querySelector('[data-kod-evet]'), tam = Array.prototype.every.call(kutular, function(k){ return k.value; }); b.classList.toggle('is-pasif', !tam); b.setAttribute('aria-disabled', !tam); }
    kutular.forEach(function(k, i){
      k.addEventListener('input', function(){ k.value = k.value.replace(/\D/g, '').slice(-1); kov.querySelector('[data-kod-hata]').style.display = ''; kov.querySelector('.kb-kod-kutular').classList.remove('has-error'); if(k.value && kutular[i + 1]) kutular[i + 1].focus(); kodPasif(); });
      k.addEventListener('keydown', function(e){ if(e.key === 'Backspace' && !k.value && kutular[i - 1]) kutular[i - 1].focus(); if(e.key === 'Enter') kov.querySelector('[data-kod-evet]').click(); });
      k.addEventListener('paste', function(e){ var v = (e.clipboardData.getData('text') || '').replace(/\D/g, '').slice(0, 6); if(!v) return; e.preventDefault(); v.split('').forEach(function(c, j){ if(kutular[j]) kutular[j].value = c; }); kutular[Math.min(5, v.length)].focus(); });
    });
    kov.addEventListener('click', function(e){
      if(e.target === kov || e.target.closest('[data-kod-hayir]')){ kodKapat(); return; }
      if(e.target.closest('[data-kod-yeniden]')){ sayac(); window.kbBildir('Yeni kod e-postanıza gönderildi'); return; }
      if(e.target.closest('[data-kod-evet]')){
        var v = Array.prototype.map.call(kutular, function(k){ return k.value; }).join('');
        if(v.length < 6){ kov.querySelector('[data-kod-hata]').style.display = 'flex'; kov.querySelector('.kb-kod-kutular').classList.add('has-error'); var bos = Array.prototype.filter.call(kutular, function(k){ return !k.value; })[0]; if(bos) bos.focus(); return; }
        var is = kodIs; kodKapat(); if(is) is();
      }
    });
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && kov.classList.contains('open')){ e.stopImmediatePropagation(); kodKapat(); } }, true);
  }
  function sayac(){
    var s = 45, el = kov.querySelector('[data-kod-sure]'), b = kov.querySelector('[data-kod-yeniden]');
    clearInterval(sure); b.disabled = true;
    el.textContent = 'Kod 10 dakika geçerli · yeniden gönderme 0.' + s;
    sure = setInterval(function(){ s--; el.textContent = s > 0 ? 'Kod 10 dakika geçerli · yeniden gönderme 0.' + (s < 10 ? '0' + s : s) : 'Kod 10 dakika geçerli'; if(s <= 0){ clearInterval(sure); b.disabled = false; } }, 1000);
  }
  function kodKapat(){ kov.classList.remove('open'); clearInterval(sure); if(kodOnce && kodOnce.focus) kodOnce.focus(); }
  window.kbKod = function(o){
    if(!kov) kodKur();
    var ep = (document.getElementById('pmMenuEposta') || {}).textContent || 'e-posta adresiniz';
    var gizli = ep.replace(/^(.)[^@]*(@.*)$/, '$1•••$2');
    kov.querySelector('h2').textContent = o.baslik || 'E-posta koduyla doğrulayın';
    kov.querySelector('[data-kod-metin]').textContent = (o.metin ? o.metin + ' ' : '') + '6 haneli kod ' + gizli + ' adresine gönderildi.';
    kov.querySelector('[data-kod-evet]').textContent = o.evet || 'Doğrula';
    kov.querySelector('[data-kod-hata]').style.display = '';
    kov.querySelectorAll('.kb-kod-kutular input').forEach(function(k){ k.value = ''; }); kov.querySelector('.kb-kod-kutular').classList.remove('has-error');
    var kb_ = kov.querySelector('[data-kod-evet]'); kb_.classList.add('is-pasif'); kb_.setAttribute('aria-disabled', 'true');
    kodIs = o.evetIs; kodOnce = document.activeElement;
    kov.classList.add('open'); sayac();
    setTimeout(function(){ kov.querySelector('.kb-kod-kutular input').focus(); }, 60);
  };

  /* ---------------- AI ile üret adımı ----------------
     [data-ai-adim data-ai-kaynak="#a,#b"]: kaynak alanlar doluysa işaretli [data-ai-grup] bölümleri üretilir.
     Üretilen bölüm "AI önerisi" etiketi alır; etiket bölümde bir değişiklik yapılınca "gözden geçirildi"ye döner. */
  window.kbKurucu('[data-ai-adim]', function(A){
    var kaynak = (A.getAttribute('data-ai-kaynak') || '').split(',').map(function(s){ return document.querySelector(s.trim()); }).filter(Boolean);
    var btn = A.querySelector('[data-ai-uret]'), neden = A.querySelector('[data-ai-neden]'), durumEl = A.querySelector('[data-ai-durum]');
    function hazir(){ return kaynak.every(function(k){ return k.value.trim().length > 0; }); }
    function bak(){ if(A.classList.contains('is-bitti')) return; var h = hazir() && !!A.querySelector('.kaa-secim input:checked'); btn.disabled = false; btn.classList.toggle('is-pasif', !h); btn.setAttribute('aria-disabled', !h); neden.textContent = hazir() ? 'Başlık ve spot hazır' : 'Önce başlık ve spot'; }
    kaynak.forEach(function(k){ k.addEventListener('input', bak); });
    A.querySelector('.kaa-secim').addEventListener('change', bak); bak();
    function doldur(g){
      g.querySelectorAll('[data-ai-ornek]').forEach(function(el){
        if(el.classList.contains('kz-alan')){ if(window.kbEditorYaz) window.kbEditorYaz(el, el.dataset.aiOrnek); else el.innerHTML = el.dataset.aiOrnek; }
        else if(el.classList.contains('kb-secim')){ var o = el.querySelector('button[data-deger="' + el.dataset.aiOrnek + '"]'); if(o){ el.dataset.deger = el.dataset.aiOrnek; el.classList.add('is-dolu'); var l = el.querySelector('.ks-deger'); if(l) l.textContent = o.getAttribute('data-ad') || o.textContent; } }
        else { el.value = el.dataset.aiOrnek; el.dispatchEvent(new Event('input', { bubbles:true })); }
      });
      g.querySelectorAll('[data-ai-cip]').forEach(function(el){ if(!el.querySelector('.kb-cip')) el.insertAdjacentHTML('afterbegin', el.dataset.aiCip); });
      if(g.querySelector('.kb-platform.is-on')) g.querySelector('.kb-platform.is-on').click();
      var tt = g.querySelector('.form-sec-tt') || g.querySelector('.form-sec-tt, .frow > label');
      g.classList.add('is-ai');
      if(!g.querySelector(':scope .kb-ai-oneri')){
        var et = document.createElement('span'); et.className = 'kb-ai-oneri';
        et.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles" aria-hidden="true"></i>AI önerisi · onay bekliyor<button type="button" data-ai-onayla>Onayla</button>';
        (tt || g).appendChild(et);
      }
      var sekme = g.classList.contains('sa-form-panel') && document.querySelector('.sa-form-tab[data-panel="' + g.id + '"]'); if(sekme) sekme.classList.add('has-ai');
    }
    function bekleyen(){
      var n = document.querySelectorAll('[data-ai-grup].is-ai:not(.is-onayli)').length, kk = document.querySelector('.kb-kaydet .kk-durum');
      if(!kk) return;
      var s = kk.querySelector('.kk-ai'); if(!s){ s = document.createElement('b'); s.className = 'kk-ai'; kk.appendChild(s); }
      s.hidden = !n; s.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles" aria-hidden="true"></i>' + n + ' AI bölümü onay bekliyor';
      document.querySelectorAll('.sa-form-tab.has-ai').forEach(function(sk){ var pn = document.getElementById(sk.getAttribute('data-panel')); sk.classList.toggle('has-ai', !!(pn && (pn.matches('.is-ai:not(.is-onayli)') || pn.querySelector('.is-ai:not(.is-onayli)')))); });
    }
    document.addEventListener('click', function(e){
      var o = e.target.closest('[data-ai-onayla]'); if(!o) return;
      var g = o.closest('[data-ai-grup]'), et = o.closest('.kb-ai-oneri');
      g.classList.add('is-onayli'); et.classList.add('is-bakildi');
      et.innerHTML = '<i class="fa-solid fa-user-check" aria-hidden="true"></i>Editör onayladı · ' + ad();
      bekleyen(); window.kbBildir('AI bölümü onaylandı');
    });
    btn.addEventListener('click', function(){
      if(A.classList.contains('is-bitti')) return;
      var eks = kaynak.filter(function(k){ return !k.value.trim(); });
      if(eks.length){ eks.forEach(function(k){ if(!k.hasAttribute('data-zorunlu-metin')) k.setAttribute('data-zorunlu-metin', (k.closest('.frow').querySelector('label') || {}).textContent ? 'Üretim için ' + k.closest('.frow').querySelector('label').textContent.replace('*', '').trim().toLocaleLowerCase('tr') + ' gerekli' : 'Bu alan gerekli'); }); window.kbEksikGoster(eks); return; }
      if(!A.querySelector('.kaa-secim input:checked')){ window.kbBildir('Üretilecek en az bir bölüm seçin', null, 'uyari'); return; }
      var secilen = Array.prototype.map.call(A.querySelectorAll('.kaa-secim input:checked'), function(i){ return i.value; });
      A.classList.add('is-uretiyor'); btn.disabled = true; btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin" aria-hidden="true"></i>Üretiliyor…';
      setTimeout(function(){
        secilen.forEach(function(g){ document.querySelectorAll('[data-ai-grup="' + g + '"]').forEach(doldur); });
        A.classList.remove('is-uretiyor'); A.classList.add('is-bitti');
        btn.innerHTML = '<i class="fa-solid fa-check" aria-hidden="true"></i>Üretildi'; btn.disabled = true;
        A.querySelector('.kaa-secim').hidden = true; bekleyen();
        durumEl.textContent = secilen.length + ' bölüm üretildi. İşaretli bölümler siz “Onayla” diyene kadar işaretli kalır; kaydet çubuğunda kaç bölümün beklediği yazar. Kapak görseli ve kaynaklar sizde.';
        neden.textContent = '';
        window.kbBildir(secilen.length + ' bölüm AI ile üretildi; gözden geçirmeden yayımlamayın');
      }, 1100);
    });
  });

  /* ---------------- renk seçici ----------------
     .kb-renkler[data-renk-ozel]: hazır renklerin sonuna "+" gelir; açılan kutuda renk alanı, ton şeridi, HEX,
     okunurluk denetimi (beyaz ve koyu yazıyla kontrast, WCAG AA 4,5:1) ve son kullanılanlar vardır. */
  function hexRgb(h){ h = h.replace('#', ''); if(h.length === 3) h = h.split('').map(function(c){ return c + c; }).join(''); var n = parseInt(h, 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }
  function rgbHex(r){ return '#' + r.map(function(x){ return ('0' + Math.round(x).toString(16)).slice(-2); }).join(''); }
  function hsvRgb(h, s, v){ var f = function(n){ var k = (n + h / 60) % 6; return v - v * s * Math.max(0, Math.min(k, 4 - k, 1)); }; return [f(5) * 255, f(3) * 255, f(1) * 255]; }
  function rgbHsv(r){ var R = r[0] / 255, G = r[1] / 255, B = r[2] / 255, mx = Math.max(R, G, B), mn = Math.min(R, G, B), d = mx - mn, h = 0;
    if(d){ h = mx === R ? ((G - B) / d) % 6 : mx === G ? (B - R) / d + 2 : (R - G) / d + 4; h *= 60; if(h < 0) h += 360; }
    return [h, mx ? d / mx : 0, mx]; }
  function parlak(r){ var c = r.map(function(x){ x /= 255; return x <= .03928 ? x / 12.92 : Math.pow((x + .055) / 1.055, 2.4); }); return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]; }
  function kontrast(a, b){ var x = parlak(a), y = parlak(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); }
  var rPop = null, rHedef = null, rHsv = [40, .8, .95], SON = [];
  function rKur(){
    rPop = document.createElement('div'); rPop.className = 'pnl-menu kb-renk-pop'; rPop.setAttribute('role', 'dialog'); rPop.setAttribute('aria-label', 'Özel renk seç');
    rPop.innerHTML = '<div class="krp-alan" data-krp-alan><span class="krp-imlec" data-krp-imlec></span></div>'
      + '<input type="range" class="krp-ton" min="0" max="360" step="1" data-krp-ton aria-label="Ton">'
      + '<div class="krp-satir"><span class="krp-ornek" data-krp-ornek></span><label class="krp-hex"><span>HEX</span><input data-krp-hex maxlength="7" spellcheck="false" aria-label="HEX renk kodu"></label></div>'
      + '<div class="krp-etiket" data-krp-etiket><span>Gündem</span><span>Gündem</span></div>'
      + '<div class="krp-kontrast" data-krp-kontrast></div>'
      + '<div class="krp-son" data-krp-son></div>'
      + '<div class="krp-alt"><button type="button" class="btn btn-ghost btn-sm" data-krp-vazgec>Vazgeç</button><button type="button" class="btn btn-acc btn-sm" data-krp-uygula><i class="fa-solid fa-check" aria-hidden="true"></i>Uygula</button></div>';
    document.body.appendChild(rPop);
    var alan = rPop.querySelector('[data-krp-alan]'), surukle = false;
    function alanYaz(e){ var r = alan.getBoundingClientRect(); rHsv[1] = Math.max(0, Math.min(1, (e.clientX - r.left) / r.width)); rHsv[2] = Math.max(0, Math.min(1, 1 - (e.clientY - r.top) / r.height)); rCiz(); }
    alan.addEventListener('pointerdown', function(e){ surukle = true; alan.setPointerCapture(e.pointerId); alanYaz(e); });
    alan.addEventListener('pointermove', function(e){ if(surukle) alanYaz(e); });
    alan.addEventListener('pointerup', function(){ surukle = false; });
    alan.tabIndex = 0; alan.setAttribute('aria-label', 'Doygunluk ve parlaklık; ok tuşlarıyla değiştirin');
    alan.addEventListener('keydown', function(e){ var m = { ArrowLeft:[-.02,0], ArrowRight:[.02,0], ArrowUp:[0,.02], ArrowDown:[0,-.02] }[e.key]; if(!m) return; e.preventDefault(); rHsv[1] = Math.max(0, Math.min(1, rHsv[1] + m[0])); rHsv[2] = Math.max(0, Math.min(1, rHsv[2] + m[1])); rCiz(); });
    rPop.querySelector('[data-krp-ton]').addEventListener('input', function(e){ rHsv[0] = +e.target.value; rCiz(); });
    rPop.querySelector('[data-krp-hex]').addEventListener('input', function(e){ var v = e.target.value.trim(); if(/^#?([0-9a-f]{3}|[0-9a-f]{6})$/i.test(v)){ rHsv = rgbHsv(hexRgb(v)); rCiz(true); } });
    rPop.addEventListener('click', function(e){
      var s = e.target.closest('[data-krp-renk]'); if(s){ rHsv = rgbHsv(hexRgb(s.dataset.krpRenk)); rCiz(); return; }
      if(e.target.closest('[data-krp-vazgec]')){ rKapat(); return; }
      if(e.target.closest('[data-krp-uygula]')){ rUygula(); }
    });
    document.addEventListener('mousedown', function(e){ if(rPop.classList.contains('open') && !rPop.contains(e.target) && !e.target.closest('[data-renk-ac]')) rKapat(); });
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && rPop.classList.contains('open')){ e.stopImmediatePropagation(); rKapat(); } }, true);
  }
  function rCiz(hexYazma){
    var rgb = hsvRgb(rHsv[0], rHsv[1], rHsv[2]), hex = rgbHex(rgb);
    var alan = rPop.querySelector('[data-krp-alan]'); alan.style.setProperty('--krp-ton', 'hsl(' + rHsv[0] + ',100%,50%)');
    var im = rPop.querySelector('[data-krp-imlec]'); im.style.left = rHsv[1] * 100 + '%'; im.style.top = (1 - rHsv[2]) * 100 + '%'; im.style.background = hex;
    rPop.querySelector('[data-krp-ton]').value = rHsv[0];
    rPop.querySelector('[data-krp-ornek]').style.background = hex;
    if(!hexYazma) rPop.querySelector('[data-krp-hex]').value = hex.toUpperCase();
    var et = rPop.querySelectorAll('[data-krp-etiket] span'); et[0].style.cssText = 'background:' + hex + ';color:#fff'; et[1].style.cssText = 'color:' + hex;
    var kb = kontrast(rgb, [255,255,255]), kz = kontrast(rgb, hexRgb(getComputedStyle(document.documentElement).getPropertyValue('--paper').trim() || '#ffffff'));
    var ok = kb >= 4.5;
    rPop.querySelector('[data-krp-kontrast]').innerHTML = '<span class="' + (ok ? 'is-ok' : 'is-zayif') + '"><i class="fa-solid ' + (ok ? 'fa-circle-check' : 'fa-triangle-exclamation') + '" aria-hidden="true"></i>Beyaz yazıyla ' + kb.toFixed(1).replace('.', ',') + ':1 ' + (ok ? '· okunur (AA)' : '· etikette zor okunur, koyulaştırın') + '</span>';
  }
  function rAc(btn){
    if(!rPop) rKur();
    rHedef = btn.closest('.kb-renkler');
    var sec = rHedef.querySelector('input:checked'), lbl = sec && sec.closest('.kb-renk'), mevcut = lbl ? getComputedStyle(lbl.querySelector('span')).backgroundColor : '';
    var m = mevcut.match(/\d+/g); if(m) rHsv = rgbHsv([+m[0], +m[1], +m[2]]);
    var hazir = Array.prototype.map.call(rHedef.querySelectorAll('.kb-renk:not(.is-ozel) span:not(.sr-only)'), function(s){ var c = getComputedStyle(s).backgroundColor.match(/\d+/g); return c ? rgbHex([+c[0], +c[1], +c[2]]) : null; }).filter(Boolean);
    rPop.querySelector('[data-krp-son]').innerHTML = '<small>' + (SON.length ? 'Son kullanılanlar' : 'Temadaki renkler') + '</small>' + (SON.length ? SON : hazir).slice(0, 10).map(function(h){ return '<button type="button" data-krp-renk="' + h + '" style="background:' + h + '" aria-label="' + h + '"></button>'; }).join('');
    var r = btn.getBoundingClientRect();
    rPop.style.position = 'fixed'; rPop.style.right = 'auto';
    rPop.style.left = Math.max(12, Math.min(r.left, innerWidth - 300)) + 'px';
    rPop.style.top = (r.bottom + 8 + 430 > innerHeight ? Math.max(12, r.top - 438) : r.bottom + 8) + 'px';
    rCiz(); rPop.classList.add('open'); setTimeout(function(){ rPop.querySelector('[data-krp-alan]').focus(); }, 30);
  }
  function rKapat(){ if(rPop) rPop.classList.remove('open'); }
  function rUygula(){
    var hex = rgbHex(hsvRgb(rHsv[0], rHsv[1], rHsv[2])).toUpperCase(), ad = (rHedef.querySelector('input') || {}).name || 'renk';
    var oz = rHedef.querySelector('.kb-renk.is-ozel');
    if(!oz){ oz = document.createElement('label'); oz.className = 'kb-renk is-ozel'; oz.innerHTML = '<input type="radio" name="' + ad + '" value=""><span></span><span class="sr-only"></span>'; rHedef.insertBefore(oz, rHedef.querySelector('[data-renk-ac]')); }
    oz.title = 'Özel renk ' + hex; oz.querySelector('input').value = hex; oz.querySelector('.sr-only').textContent = 'Özel renk ' + hex;
    oz.querySelector('span').style.setProperty('--kat', hex); oz.querySelector('input').checked = true;
    oz.querySelector('input').dispatchEvent(new Event('input', { bubbles:true })); oz.querySelector('input').dispatchEvent(new Event('change', { bubbles:true }));
    SON = [hex].concat(SON.filter(function(x){ return x !== hex; })).slice(0, 10);
    rKapat(); window.kbBildir('Özel renk seçildi: ' + hex);
  }
  function renkKur(kok){
    (kok || document).querySelectorAll('.kb-renkler[data-renk-ozel]:not([data-renk-kuruldu])').forEach(function(R){
      R.setAttribute('data-renk-kuruldu', '');
      var b = document.createElement('button'); b.type = 'button'; b.className = 'kb-renk-ekle'; b.setAttribute('data-renk-ac', ''); b.setAttribute('aria-label', 'Özel renk seç'); b.title = 'Özel renk';
      b.innerHTML = '<i class="fa-solid fa-eye-dropper" aria-hidden="true"></i>'; R.appendChild(b);
    });
  }
  window.kbRenkKur = renkKur; renkKur();
  document.addEventListener('click', function(e){ var b = e.target.closest('[data-renk-ac]'); if(b){ e.preventDefault(); rAc(b); } });
  /* çekmece ya da pencerede açılan şablonlardaki renk alanları */
  new MutationObserver(function(){ renkKur(); }).observe(document.body, { childList:true, subtree:true });

  /* ---------------- taşıyarak silme (B1) ----------------
     kbTasiSil({ ad, tur, haber, alt, hedefler:[…], evetIs(hedef) }): içinde kayıt olan öğe doğrudan silinmez;
     pencere kullanım sayısını yazar ve kayıtların taşınacağı yeri seçtirir; taşıma sonrası öğe çöpe gider. */
  var tsOv = null, tsIs = null;
  window.kbTasiSil = function(o){
    if(!tsOv){
      tsOv = document.createElement('div'); tsOv.className = 'sa-modal-ov kb-tasi-ov';
      tsOv.innerHTML = '<div class="sa-modal danger kb-tasi" role="alertdialog" aria-modal="true" aria-labelledby="kbTasiBas"><div class="sa-modal-ico"><i class="fa-solid fa-folder-minus" aria-hidden="true"></i></div><h2 id="kbTasiBas"></h2><div class="kb-tasi-kullanim" data-ts-kullanim></div>'
        + '<div class="frow"><span class="flabel" data-ts-etk></span><div class="kb-tasi-ara"><i class="fa-solid fa-magnifying-glass" aria-hidden="true"></i><input type="search" placeholder="Ara" aria-label="Taşınacak yeri ara"></div><div class="kb-tasi-liste" role="listbox" data-ts-liste></div><div class="ferr"><i class="fa-solid fa-circle-exclamation" aria-hidden="true"></i>Taşınacak yeri seçin</div></div>'
        + '<p class="fhint" data-ts-not></p><div class="sa-modal-acts"><button type="button" class="btn btn-ghost" data-ts-hayir>Vazgeç</button><button type="button" class="btn btn-danger" data-ts-evet disabled></button></div></div>';
      document.body.appendChild(tsOv);
      tsOv.querySelector('input').addEventListener('input', function(e){ var q = (e.target.value || '').toLocaleLowerCase('tr'); tsOv.querySelectorAll('[data-ts-liste] button').forEach(function(b){ b.hidden = q && b.textContent.toLocaleLowerCase('tr').indexOf(q) === -1; }); });
      tsOv.addEventListener('click', function(e){
        if(e.target === tsOv || e.target.closest('[data-ts-hayir]')){ tsOv.classList.remove('open'); return; }
        var b = e.target.closest('[data-ts-liste] button'); if(b){ tsOv.querySelectorAll('[data-ts-liste] button').forEach(function(x){ x.classList.toggle('is-sec', x === b); x.setAttribute('aria-selected', x === b); }); var ev = tsOv.querySelector('[data-ts-evet]'); ev.classList.remove('is-pasif'); ev.setAttribute('aria-disabled', 'false'); tsOv.querySelector('[data-ts-liste]').closest('.frow').classList.remove('has-error'); tsOv._hedef = b.dataset.v; return; }
        if(e.target.closest('[data-ts-evet]')){
          if(!tsOv._hedef){ var fr = tsOv.querySelector('[data-ts-liste]').closest('.frow'); fr.classList.add('has-error'); fr.querySelector('.kb-tasi-ara input').focus(); return; }
          tsOv.classList.remove('open'); if(tsIs) tsIs(tsOv._hedef); }
      });
    }
    tsIs = o.evetIs; tsOv._hedef = null;
    var bir = o.birim || 'haber';
    tsOv.querySelector('h2').textContent = '“' + o.ad + '” silinmeden önce ' + (o.birimCogul || bir + 'ler') + ' taşınmalı';
    tsOv.querySelector('[data-ts-kullanim]').innerHTML = '<span><i class="fa-solid ' + (o.ikon || 'fa-newspaper') + '" aria-hidden="true"></i><b>' + (o.sayi != null ? o.sayi : o.haber).toLocaleString('tr') + '</b> ' + bir + '</span>' + (o.alt ? '<span><i class="fa-solid fa-sitemap" aria-hidden="true"></i><b>' + o.alt + '</b> alt konu</span>' : '');
    tsOv.querySelector('[data-ts-etk]').textContent = o.soru || ((o.birimCogul || bir + 'ler').charAt(0).toLocaleUpperCase('tr') + (o.birimCogul || bir + 'ler').slice(1) + ' nereye taşınsın?');
    tsOv.querySelector('.kb-tasi-ara input').placeholder = o.araMetin || 'Ara';
    tsOv.querySelector('[data-ts-liste]').closest('.frow').querySelector('.ferr').lastChild.textContent = o.eksikMetin || 'Taşınacak yeri seçin';
    tsOv.querySelector('[data-ts-liste]').innerHTML = o.hedefler.map(function(h){ return '<button type="button" role="option" aria-selected="false" data-v="' + h.replace(/"/g, '&quot;') + '">' + h.replace(/</g, '&lt;') + '</button>'; }).join('');
    tsOv.querySelector('[data-ts-not]').textContent = o.not || ((o.alt ? 'Alt konular da çöpe gider. ' : '') + 'Haberlerin adresi yeni konuya göre değişir, eski adresler yönlendirilir. “' + o.ad + '” çöpe gider ve oradan geri alınabilir; işlem denetim izine yazılır.');
    var tev = tsOv.querySelector('[data-ts-evet]'); tev.textContent = 'Taşı ve çöpe at'; tev.disabled = false; tev.classList.add('is-pasif'); tev.setAttribute('aria-disabled', 'true'); tsOv.querySelector('[data-ts-liste]').closest('.frow').classList.remove('has-error');
    tsOv.querySelector('input').value = '';
    tsOv.classList.add('open'); setTimeout(function(){ tsOv.querySelector('input').focus(); }, 50);
  };

  /* ---------------- satır listesi (formun içindeki tekrarlanan satırlar: kaynaklar vb.) ----------------
     [data-satir-liste]: "ekle" yeni satırı düzenleme halinde açar; kalem satırı düzenler; çöp satırı kaldırır (B8: onaysız + Geri al). */
  window.kbKurucu('[data-satir-liste]', function(L){
    var a1 = L.dataset.satirAlan1 || 'Başlık', a2 = L.dataset.satirAlan2 || 'Açıklama', adx = L.dataset.satirAd || 'Satır';
    function esc2(s){ return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }
    function duzenle(s){
      var y = s.querySelector('.km-yazi'), b = y.firstChild ? (y.firstChild.nodeType === 3 ? y.firstChild.nodeValue : '') : '', k = y.querySelector('small') ? y.querySelector('small').textContent : '';
      s.classList.add('is-duzenle'); s.dataset.eski = y.innerHTML;
      y.innerHTML = '<input class="finput" data-s1 placeholder="' + esc2(a1) + '" value="' + esc2(b.trim()) + '"><input class="finput" data-s2 placeholder="' + esc2(a2) + '" value="' + esc2(k) + '"><span class="km-dz-btn"><button type="button" class="btn btn-acc btn-sm" data-satir-tamam>Tamam</button><button type="button" class="kb-bag" data-satir-vazgec>Vazgeç</button></span>';
      y.querySelector('[data-s1]').focus();
    }
    function bitir(s, kaydet){
      var y = s.querySelector('.km-yazi');
      if(kaydet){ var v1 = y.querySelector('[data-s1]').value.trim(), v2 = y.querySelector('[data-s2]').value.trim();
        if(!v1){ y.querySelector('[data-s1]').classList.add('is-hata'); y.querySelector('[data-s1]').focus(); return; }
        y.innerHTML = esc2(v1) + (v2 ? '<small>' + esc2(v2) + '</small>' : ''); }
      else if(s.dataset.yeni){ s.remove(); return; }
      else y.innerHTML = s.dataset.eski;
      s.classList.remove('is-duzenle'); delete s.dataset.yeni; L.dispatchEvent(new Event('input', { bubbles:true }));
    }
    L.addEventListener('click', function(e){
      var s = e.target.closest('.km-satir');
      if(e.target.closest('[data-satir-ekle]')){
        var n = document.createElement('div'); n.className = 'km-satir'; n.setAttribute('data-sira', ''); n.dataset.yeni = '1';
        n.innerHTML = '<button type="button" class="kb-tutamac" aria-label="Sırayı değiştir"><i class="fa-solid fa-grip-vertical" aria-hidden="true"></i></button><span class="km-yazi"></span><button type="button" class="ia-btn" data-satir-duzenle aria-label="' + adx + ' düzenle"><i class="fa-solid fa-pen" aria-hidden="true"></i></button><button type="button" class="ia-btn danger" data-satir-sil aria-label="' + adx + ' kaldır"><i class="fa-solid fa-trash" aria-hidden="true"></i></button>';
        L.insertBefore(n, e.target.closest('[data-satir-ekle]')); duzenle(n); return;
      }
      if(!s) return;
      if(e.target.closest('[data-satir-duzenle]')){ if(!s.classList.contains('is-duzenle')) duzenle(s); return; }
      if(e.target.closest('[data-satir-tamam]')){ bitir(s, true); return; }
      if(e.target.closest('[data-satir-vazgec]')){ bitir(s, false); return; }
      if(e.target.closest('[data-satir-sil]')){ var sonra = s.nextSibling, ad2 = (s.querySelector('.km-yazi').firstChild || {}).nodeValue || adx; s.remove(); L.dispatchEvent(new Event('input', { bubbles:true }));
        window.kbBildir(adx + ' kaldırıldı: ' + ad2.trim(), function(){ L.insertBefore(s, sonra); }); }
    });
    L.addEventListener('keydown', function(e){ var s = e.target.closest('.km-satir.is-duzenle'); if(!s) return; if(e.key === 'Enter'){ e.preventDefault(); bitir(s, true); } if(e.key === 'Escape'){ e.stopPropagation(); bitir(s, false); } });
  });

  /* ---------------- bakım modu (Site Ayarları; K11, K15) ----------------
     Açma: önce/sonra onayı → e-posta kodu → site bakımda (bant, rozet, kutu). Bitirme: onay. İkisi de denetim izine yazılır. */
  document.querySelectorAll('[data-bakim-kutu]').forEach(function(K){
    var bant = document.querySelector('[data-bakim-bant]'), rozet = document.querySelector('[data-bakim-rozet]');
    function yaz(acik){
      K.classList.toggle('is-bakim', acik);
      K.querySelector('[data-bakim-baslik]').textContent = acik ? 'Site bakımda' : 'Site yayında';
      K.querySelector('[data-bakim-alt]').textContent = acik ? 'Okurlar bakım sayfasını görüyor (503) · 24.11.2026 16.05\'ten beri · ' + ad() : 'Okurlar siteyi ve uygulamayı normal görüyor.';
      var b = K.querySelector('[data-bakim-ac],[data-bakim-bitir]');
      b.outerHTML = acik ? '<button type="button" class="btn btn-ghost btn-sm" data-bakim-bitir><i class="fa-solid fa-circle-play" aria-hidden="true"></i>Bakımı bitir</button>' : '<button type="button" class="btn btn-danger btn-sm" data-bakim-ac><i class="fa-solid fa-person-digging" aria-hidden="true"></i>Bakım modunu aç</button>';
      if(bant){ bant.hidden = !acik; var oz = bant.querySelector('[data-bakim-ozet]'), bt = document.querySelector('#saBakimBitis .kt-deger'); if(oz) oz.textContent = bt && bt.textContent ? 'Planlanan bitiş: ' + bt.textContent + '.' : ''; }
      if(rozet){ rozet.className = 'pstat ' + (acik ? 'warm' : 'ok'); rozet.textContent = acik ? 'Bakımda' : 'Yayında'; }
    }
    document.addEventListener('click', function(e){
      if(e.target.closest('[data-bakim-ac]')){
        window.kbOnay({ tehlike:true, ikon:'fa-person-digging', baslik:'Bakım modu açılsın mı?', metin:'Önce: site yayında → Sonra: okurlar bakım sayfasını görür (503), uygulama bakım ekranı gösterir. İzinli IP\'ler ve ekip önizleme bağlantısı siteyi görmeye devam eder. E-posta koduyla doğrulanır ve denetim izine yazılır.', evet:'Devam et',
          evetIs: function(){ window.kbKod({ baslik:'Bakım modunu doğrulayın', evet:'Doğrula ve aç', evetIs: function(){ yaz(true); window.kbBildir('Bakım modu açıldı; denetim izine yazıldı'); } }); } });
      }
      if(e.target.closest('[data-bakim-bitir]')){
        window.kbOnay({ ikon:'fa-circle-play', baslik:'Bakım bitsin mi?', metin:'Site ve uygulama hemen okurlara açılır. İşlem denetim izine yazılır.', evet:'Bakımı bitir', evetIs: function(){ yaz(false); window.kbBildir('Bakım bitti; site yayında'); } });
      }
    });
  });
  /* açık özellik sayısı (yan kart) */
  var anSay = document.querySelector('[data-anahtar-say]');
  if(anSay){ var anGun = function(){ var h = document.querySelectorAll('input[data-anahtar]'); anSay.textContent = Array.prototype.filter.call(h, function(x){ return x.checked; }).length + ' / ' + h.length; }; document.addEventListener('change', anGun); document.addEventListener('click', function(){ setTimeout(anGun, 50); }); }

  /* ---------------- tarih aralığı ----------------
     .kb-aralik: hazır seçimler (Bugün, Son 7 gün, Son 30 gün, Bu ay) + iki saatsiz tarih seçici (başlangıç, bitiş).
     Elle tarih seçilince hazır seçim "Özel" olur. Değişince 'kb-aralik' olayı (detail: {bas, bit}). */
  var BUGUN = { y:2026, a:10, g:23 };
  window.kbKurucu('.kb-aralik', function(A){
    var t2 = A.querySelectorAll('.kb-tarih-sec'), bas = t2[0], bit = t2[1];
    function gun(n){ var d = new Date(BUGUN.y, BUGUN.a, BUGUN.g - n); return { y:d.getFullYear(), a:d.getMonth(), g:d.getDate(), h:0, m:0 }; }
    function bildir(){ A.dispatchEvent(new CustomEvent('kb-aralik', { bubbles:true, detail:{ bas: bas && bas.dataset.secili, bit: bit && bit.dataset.secili } })); }
    function hazir(k){
      A.querySelectorAll('[data-aralik]').forEach(function(b){ var on = b.dataset.aralik === k; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', on); });
      if(k === 'ozel' || !bas || !bit || !bas.kbAyarla) return;
      var b0 = k === 'ay' ? { y:BUGUN.y, a:BUGUN.a, g:1, h:0, m:0 } : gun(k === 'bugun' ? 0 : +k - 1);
      bas.kbAyarla(b0); bit.kbAyarla(gun(0)); bildir();
    }
    A.addEventListener('click', function(e){ var b = e.target.closest('[data-aralik]'); if(b) hazir(b.dataset.aralik); });
    A.addEventListener('kb-tarih', function(){ hazir('ozel'); bildir(); });
    var on = A.querySelector('[data-aralik].is-on'); setTimeout(function(){ hazir(on ? on.dataset.aralik : '7'); }, 0);
  });

  /* ---------------- izin matrisi ----------------
     table.kb-matris: satır = izin, sütun = rol. Sütun başlığındaki düğme o rolün bütün izinlerini, satır başındaki düğme
     o iznin bütün rollerini açar/kapatır. Kilitli hücre (Süper Admin) değişmez. */
  window.kbKurucu('.kb-matris', function(M){
    function kutular(sec){ return Array.prototype.filter.call(M.querySelectorAll(sec), function(i){ return !i.disabled; }); }
    function topla(liste){ var hepsi = liste.every(function(i){ return i.checked; }); liste.forEach(function(i){ i.checked = !hepsi; }); M.dispatchEvent(new Event('input', { bubbles:true })); say(); }
    function say(){ M.querySelectorAll('[data-matris-say]').forEach(function(s){ var k = s.getAttribute('data-matris-say'); var l = M.querySelectorAll('input[data-rol="' + k + '"]'); s.textContent = Array.prototype.filter.call(l, function(i){ return i.checked; }).length + '/' + l.length; }); }
    M.addEventListener('click', function(e){
      var s = e.target.closest('[data-matris-sutun]'); if(s){ topla(kutular('input[data-rol="' + s.getAttribute('data-matris-sutun') + '"]')); return; }
      var r = e.target.closest('[data-matris-satir]'); if(r){ topla(kutular('tr[data-izin-satir="' + r.getAttribute('data-matris-satir') + '"] input')); }
    });
    M.addEventListener('change', say); say();
  });

  /* ---------------- çizgi grafik ----------------
     .kb-cizgi[data-degerler="12,18,9,…"][data-etiketler="Pzt,Sal,…"][data-birim="haber"]: SVG çizgi + alan, son değer vurgulu. */
  window.kbKurucu('.kb-cizgi[data-degerler]', function(G){
    var v = G.dataset.degerler.split(',').map(Number), et = (G.dataset.etiketler || '').split(','), W = 600, H = 160, p = 8;
    var mx = Math.max.apply(null, v) || 1, mn = Math.min(0, Math.min.apply(null, v));
    var x = function(i){ return p + i * (W - 2 * p) / Math.max(1, v.length - 1); }, y = function(d){ return H - p - (d - mn) / (mx - mn) * (H - 2 * p); };
    var yol = v.map(function(d, i){ return (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(d).toFixed(1); }).join(' ');
    var son = v.length - 1;
    G.innerHTML = '<svg viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="none" role="img" aria-label="' + (G.dataset.ad || 'Grafik') + ': ' + v.join(', ') + '">'
      + [0.25, .5, .75].map(function(k){ return '<line x1="0" x2="' + W + '" y1="' + (p + k * (H - 2 * p)) + '" y2="' + (p + k * (H - 2 * p)) + '" class="kc-izgara"/>'; }).join('')
      + '<path d="' + yol + ' L' + x(son) + ' ' + (H - p) + ' L' + x(0) + ' ' + (H - p) + ' Z" class="kc-alan"/><path d="' + yol + '" class="kc-cizgi"/>'
      + '<circle cx="' + x(son) + '" cy="' + y(v[son]) + '" r="4" class="kc-nokta"/></svg>'
      + (et.length > 1 ? '<div class="kc-etiketler">' + et.map(function(e){ return '<span>' + e + '</span>'; }).join('') + '</div>' : '');
  });

  /* ---------------- e-posta önizleme kabı ----------------
     .kb-eposta-onizleme: [data-eposta-gorunum="masaustu|telefon"] düğmeleri gövdenin genişliğini değiştirir (600 / 360 px). */
  window.kbKurucu('.kb-eposta-onizleme', function(E){
    var d = E.querySelectorAll('[data-eposta-gorunum]');
    d.forEach(function(b){ b.addEventListener('click', function(){
      d.forEach(function(x){ var on = x === b; x.classList.toggle('is-on', on); x.setAttribute('aria-pressed', on); });
      E.classList.toggle('is-telefon', b.dataset.epostaGorunum === 'telefon');
    }); });
  });

  /* ---------------- şifre alanı ----------------
     .kb-sifre: göster/gizle düğmesi; [data-sifre-kural] listesi yazarken işaretlenir (8+ karakter, büyük ve küçük harf, rakam). */
  window.kbKurucu('.kb-sifre', function(S){
    var i = S.querySelector('input'), b = S.querySelector('[data-sifre-goster]'), kural = S.parentNode.querySelector('[data-sifre-kural]');
    if(b) b.addEventListener('click', function(){ var g = i.type === 'password'; i.type = g ? 'text' : 'password'; b.setAttribute('aria-label', g ? 'Şifreyi gizle' : 'Şifreyi göster'); b.innerHTML = '<i class="fa-solid ' + (g ? 'fa-eye-slash' : 'fa-eye') + '" aria-hidden="true"></i>'; });
    function bak(){
      if(!kural) return; var v = i.value, K = { uzun: v.length >= 8, harf: /[a-zçğıöşü]/.test(v) && /[A-ZÇĞİÖŞÜ]/.test(v), rakam: /\d/.test(v) }, n = 0;
      kural.querySelectorAll('[data-kural]').forEach(function(li){ var ok = K[li.dataset.kural]; li.classList.toggle('is-ok', ok); if(ok) n++; });
      var g = kural.querySelector('[data-sifre-guc]'); if(g){ g.style.setProperty('--guc', (n / 3 * 100) + '%'); g.dataset.seviye = n; }
    }
    i.addEventListener('input', bak); bak();
  });

  /* ---------------- sayfa içi kod kutuları (2FA ekranı) ----------------
     [data-kod-kutular] içindeki 6 kutu: rakam yazınca ilerler, yapıştırma dağıtılır; dolunca 'kb-kod-dolu' olayı. */
  window.kbKurucu('[data-kod-kutular]', function(K){
    var k = K.querySelectorAll('input');
    k.forEach(function(x, i){
      x.addEventListener('input', function(){ x.value = x.value.replace(/\D/g, '').slice(-1); if(x.value && k[i + 1]) k[i + 1].focus(); if(Array.prototype.every.call(k, function(y){ return y.value; })) K.dispatchEvent(new CustomEvent('kb-kod-dolu', { bubbles:true })); });
      x.addEventListener('keydown', function(e){ if(e.key === 'Backspace' && !x.value && k[i - 1]) k[i - 1].focus(); });
      x.addEventListener('paste', function(e){ var v = (e.clipboardData.getData('text') || '').replace(/\D/g, '').slice(0, k.length); if(!v) return; e.preventDefault(); v.split('').forEach(function(c, j){ k[j].value = c; }); k[Math.min(k.length - 1, v.length)].focus(); if(v.length === k.length) K.dispatchEvent(new CustomEvent('kb-kod-dolu', { bubbles:true })); });
    });
  });

  /* data-sonra-kaldir: onaydan (ya da taşıyarak silmeden) sonra satır ya da kart listeden kalkar; bildirimde "Geri al" onu yerine koyar.
     Satır: tr[data-satir], [data-kart], .kb-ozk-satir ya da düğmenin [data-sonra-kaldir="seçici"] ile gösterdiği en yakın kap. */
  function satirBul(b){
    var menu = b.closest('.kb-diger-menu'), kap = b.closest('.kb-cekmece,.kb-pencere');
    var sec = b.getAttribute('data-sonra-kaldir');
    return (sec && b.closest(sec)) || b.closest('tr[data-satir],[data-kart],.kb-ozk-satir') || (menu && menu._satir) || (kap && kap._satir) || null;
  }
  function satirKaldir(satir, metin){
    if(!satir || !satir.parentNode) return false;
    var ana = satir.parentNode, sonraki = satir.nextSibling;
    satir.remove(); ana.dispatchEvent(new CustomEvent('kb-liste-yenile', { bubbles:true }));
    window.kbBildir(metin, function(){ ana.insertBefore(satir, sonraki && sonraki.parentNode === ana ? sonraki : null); ana.dispatchEvent(new CustomEvent('kb-liste-yenile', { bubbles:true })); window.kbBildir('Geri alındı'); });
    return true;
  }

  /* bildirimsel tetikleyici: <button data-tasi-sil data-tasi-ad="Editör" data-tasi-sayi="14" data-tasi-birim="kullanıcı"
     data-tasi-hedefler="Genel Yayın Yönetmeni|Kategori Editörü" [data-tasi-not="…"] [data-tasi-ikon="fa-users"] [data-bildir-sonra="…"]>
     Sayı 0 ise normal silme onayı (çöp + geri al). Sonunda düğmede 'kb-tasindi' olayı (detail.hedef). */
  document.addEventListener('click', function(e){
    var b = e.target.closest('[data-tasi-sil]'); if(!b) return;
    e.preventDefault(); e.stopPropagation();
    document.querySelectorAll('.kb-diger-menu.open').forEach(function(m){ m.classList.remove('open'); });
    var adx = b.dataset.tasiAd || 'Kayıt', n = +(b.dataset.tasiSayi || 0), bir = b.dataset.tasiBirim || 'kayıt';
    function bitti(h){ var m = b.dataset.bildirSonra || ('“' + adx + '” çöpe taşındı' + (h ? '; ' + n + ' ' + bir + ' “' + h + '” altına taşındı' : '')); if(!(b.hasAttribute('data-sonra-kaldir') && satirKaldir(satirBul(b), m))) window.kbBildir(m, function(){ window.kbBildir('Geri alındı'); }); b.dispatchEvent(new CustomEvent('kb-tasindi', { bubbles:true, detail:{ hedef:h } })); }
    if(!n){ window.kbOnay({ tehlike:true, baslik:'“' + adx + '” silinsin mi?', metin:'Kullanan ' + bir + ' yok. Çöpe gider, oradan geri alınabilir; işlem denetim izine yazılır.', evet:'Çöpe taşı', evetIs: function(){ bitti(null); } }); return; }
    window.kbTasiSil({ ad: adx, sayi: n, birim: bir, birimCogul: b.dataset.tasiBirimCogul, ikon: b.dataset.tasiIkon, soru: b.dataset.tasiSoru,
      hedefler: (b.dataset.tasiHedefler || '').split('|').filter(Boolean), not: b.dataset.tasiNot || ('“' + adx + '” çöpe gider ve oradan geri alınabilir; işlem denetim izine yazılır.'), evetIs: bitti });
  }, true);

  /* ---------------- maskeli gizli değer ----------------
     Değer hiçbir zaman açık gösterilmez; "Yenile" e-posta koduyla yeni değer üretir ve yalnızca o an bir kez gösterir. */
  /* olay yetkilendirmesiyle bağlanır: çekmece ve pencere şablonlarındaki maskeli alanlar da çalışır.
     data-maske-yeni: değer henüz yok; "Yenile" düğmesi oluşturma düğmesi gibi davranır (API anahtarı oluştur). */
  document.addEventListener('click', function(e){
    var b = e.target.closest('[data-maske-yenile],[data-maske-kopyala],[data-maske-gizle]'); if(!b) return;
    var M = b.closest('.kb-maske'); if(!M) return;
    if(b.hasAttribute('data-maske-kopyala')){
      var v = M.querySelector('.km-acik code').textContent;
      if(navigator.clipboard) navigator.clipboard.writeText(v).catch(function(){});
      window.kbBildir('Kopyalandı; bu değer bir daha gösterilmeyecek'); return;
    }
    if(b.hasAttribute('data-maske-gizle')){ M.classList.remove('is-acik'); M.querySelector('.km-acik').hidden = true; return; }
    var yeni = M.hasAttribute('data-maske-yeni'), adx = M.dataset.ad || 'Değer';
    function uret(){
      var harf = 'abcdefghjkmnpqrstuvwxyz23456789', v = (M.dataset.onEk || '');
      for(var i = 0; i < 24; i++) v += harf.charAt(Math.floor(Math.random() * harf.length));
      M.querySelector('.km-deger').textContent = '•'.repeat(16) + v.slice(-4);
      M.querySelector('.km-acik code').textContent = v;
      M.querySelector('.km-acik').hidden = false; M.classList.add('is-acik'); M.removeAttribute('data-maske-yeni');
      var m = M.querySelector('.km-meta'); if(m) m.textContent = (yeni ? 'Oluşturuldu' : 'Yenilendi') + ' · 24.11.2026 16.05 · ' + ad();
      M.dispatchEvent(new CustomEvent('kb-maske', { bubbles:true, detail:{ yeni: yeni } }));
      window.kbBildir(adx + (yeni ? ' oluşturuldu' : ' yenilendi') + '; denetim izine yazıldı');
    }
    var kod = function(){ window.kbKod({ baslik: yeni ? 'Oluşturmayı doğrulayın' : 'Yenilemeyi doğrulayın', evet: yeni ? 'Doğrula ve oluştur' : 'Doğrula ve yenile', evetIs: uret }); };
    if(yeni){ kod(); return; }
    window.kbOnay({ ikon:'fa-rotate', baslik: adx + ' yenilensin mi?', metin: M.dataset.yenileMetin || 'Eski değer hemen geçersiz olur; onu kullanan yerler yeni değerle güncellenmelidir. İşlem e-posta koduyla doğrulanır ve denetim izine yazılır.', evet:'Yenile', evetIs: kod });
  });

  /* ---------------- bildirimsel onay zinciri ----------------
     <button data-onay-baslik="…" data-onay-metin="…" data-onay-evet="Yayına al" [data-onay-tehlike] [data-onay-ikon="fa-…"]
             [data-kod] [data-kod-baslik="…"] [data-bildir-sonra="…"]>
     Onay penceresi → (data-kod varsa) e-posta kodu → kısa bildirim; sonunda düğmede 'kb-onaylandi' olayı. Açık ⋯ menüsü kapanır. */
  document.addEventListener('click', function(e){
    var b = e.target.closest('[data-onay-baslik],[data-onaysiz]'); if(!b || b.disabled) return;
    e.preventDefault(); e.stopPropagation();
    document.querySelectorAll('.kb-diger-menu.open').forEach(function(m){ m.classList.remove('open'); });
    /* data-sonra-durum="iptal" [data-sonra-durum-ad="İptal edildi"] [data-sonra-durum-sinif="off"]: onaydan sonra satırın durumu değişir
       (satırdaki ya da satırın ⋯ menüsündeki düğme); durum rozeti güncellenir, liste sayaçları yenilenir.
       data-sonra-kaldir: satır listeden kalkar (oturum kapatma, bağlantı kaldırma); bildirimde Geri al.
       data-sonra-kapat: çekmece ya da pencerenin içinden tetiklenince iş bitince kap kapanır.
       data-onaysiz (data-onay-baslik yerine): onay penceresi açılmaz, sonrası aynı (okundu say gibi hafif işler). */
    var menu = b.closest('.kb-diger-menu'), kap = b.closest('.kb-cekmece,.kb-pencere'), satir = b.closest('tr[data-satir]') || (menu && menu._satir) || (kap && kap._satir) || null;
    function bitir(){
      if(satir && b.dataset.sonraDurum){
        satir.dataset.durum = b.dataset.sonraDurum;
        var rz = satir.querySelector('.pstat'); if(rz){ if(b.dataset.sonraDurumAd) rz.textContent = b.dataset.sonraDurumAd; if(b.dataset.sonraDurumSinif) rz.className = 'pstat ' + b.dataset.sonraDurumSinif; }
        satir.dispatchEvent(new CustomEvent('kb-liste-yenile', { bubbles:true }));
      }
      if(b.hasAttribute('data-sonra-kaldir') && satirKaldir(satirBul(b), b.dataset.bildirSonra || 'Kaldırıldı')){ if(kap && window.kbKapat) window.kbKapat(); }
      else if(b.dataset.bildirSonra) window.kbBildir(b.dataset.bildirSonra);
      if(b.hasAttribute('data-sonra-kapat') && kap && window.kbKapat) window.kbKapat(); /* çekmece/pencere içinden: iş bitince kapanır */
      b.dispatchEvent(new CustomEvent('kb-onaylandi', { bubbles:true, detail:{ satir: satir } }));
    }
    if(b.hasAttribute('data-onaysiz')){ bitir(); return; } /* hafif işlem (okundu say): onay sorulmaz, sonrası aynı (sonra-durum, bildirim) */
    window.kbOnay({ tehlike: b.hasAttribute('data-onay-tehlike'), ikon: b.dataset.onayIkon || (b.hasAttribute('data-onay-tehlike') ? 'fa-triangle-exclamation' : 'fa-circle-check'),
      baslik: b.dataset.onayBaslik, metin: b.dataset.onayMetin || '', evet: b.dataset.onayEvet || 'Onayla',
      evetIs: function(){ if(b.hasAttribute('data-kod')) window.kbKod({ baslik: b.dataset.kodBaslik || 'E-posta koduyla doğrulayın', evet: 'Doğrula', evetIs: bitir }); else bitir(); } });
  }, true);

  /* ---------------- kart ızgarası süzgeci ----------------
     [data-kart-liste]: içindeki .chip[data-sekme] kartları ([data-kart][data-durum]) süzer; [data-liste-ara] adla arar;
     sayaçlar (.ch-cnt) kendiliğinden; sonuç yoksa [data-kart-bos] görünür. */
  window.kbKurucu('[data-kart-liste]', function(K){
    var kartlar = K.querySelectorAll('[data-kart]'), ara = K.querySelector('[data-liste-ara]'), bos = K.querySelector('[data-kart-bos]'), sekme = 'hepsi';
    var tr = function(s){ return (s || '').toLocaleLowerCase('tr'); };
    function uygula(){
      var q = ara ? tr(ara.value.trim()) : '', n = 0;
      kartlar.forEach(function(k){ var g = (sekme === 'hepsi' || k.dataset.durum === sekme) && (!q || tr(k.textContent).indexOf(q) > -1); k.hidden = !g; if(g) n++; });
      if(bos) bos.hidden = n > 0;
      K.querySelectorAll('.chip[data-sekme]').forEach(function(c){ var s = c.dataset.sekme, on = s === sekme; c.classList.toggle('is-on', on); c.setAttribute('aria-selected', on);
        var cnt = c.querySelector('.ch-cnt'); if(cnt) cnt.textContent = Array.prototype.filter.call(kartlar, function(k){ return s === 'hepsi' || k.dataset.durum === s; }).length; });
    }
    K.addEventListener('click', function(e){ var c = e.target.closest('.chip[data-sekme]'); if(c){ sekme = c.dataset.sekme; uygula(); } });
    if(ara) ara.addEventListener('input', uygula);
    uygula();
  });

  /* ---------------- telefon (ülke kodu + maske) ---------------- */
  var MASKE = { '90':'### ### ## ##', '49':'#### #######', '44':'#### ######', '1':'### ### ####', '994':'## ### ## ##' };
  window.kbKurucu('.kb-tel', function(T){
    var giris = T.querySelector(':scope > input') || T.querySelector('input.finput'), ulke = T.querySelector('.kb-secim'), row = T.closest('.frow');
    function kod(){ return (ulke && ulke.dataset.deger) || '90'; }
    function bicim(){
      var m = MASKE[kod()] || '### ### ####', r = giris.value.replace(/\D/g, '').slice(0, (m.match(/#/g) || []).length), o = '', j = 0;
      for(var i = 0; i < m.length && j < r.length; i++) o += m[i] === '#' ? r[j++] : m[i];
      giris.value = o; giris.placeholder = m.replace(/#/g, '0');
      return r.length === (m.match(/#/g) || []).length;
    }
    giris.addEventListener('input', bicim);
    giris.addEventListener('blur', function(){ var tam = bicim(); if(row) row.classList.toggle('has-error', !!giris.value && !tam); });
    if(ulke) ulke.addEventListener('kb-secim', function(){ bicim(); });
    bicim();
  });

  /* ---------------- e-posta: yazılırken doğrulanır ---------------- */
  var EPOSTA = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  window.kbKurucu('input[data-eposta]', function(i){
    var row = i.closest('.frow');
    function bak(son){
      var v = i.value.trim(), ok = EPOSTA.test(v);
      i.classList.toggle('is-gecerli', ok);
      if(row && (son || ok || !v)) row.classList.toggle('has-error', !!v && !ok);
    }
    i.addEventListener('input', function(){ bak(false); });
    i.addEventListener('blur', function(){ bak(true); });
    bak(false);
  });

  /* ---------------- sıralanan liste ----------------
     [data-siralanir] içindeki [data-sira] satırları tutamaçtan (.kb-tutamac) sürüklenir; tutamaç odaktayken ↑/↓ ile taşınır. */
  window.kbKurucu('[data-siralanir]', function(L){
    /* olay yetkilendirmeli: sonradan eklenen [data-sira] öğeleri de sürüklenir; sıra değişince .km-no yeniden numaralanır, 'kb-sira' olayı */
    var tasinan = null;
    function bitti(){
      L.querySelectorAll(':scope > [data-sira] .km-no').forEach(function(n, i){ n.textContent = i + 1; });
      L.dispatchEvent(new Event('input', { bubbles:true })); L.dispatchEvent(new CustomEvent('kb-sira', { bubbles:true }));
    }
    L._kbSiraBitti = bitti;
    L.addEventListener('pointerdown', function(e){ var t = e.target.closest('.kb-tutamac'), s = t && t.closest('[data-sira]'); if(s && s.parentNode === L) s.draggable = true; });
    L.addEventListener('dragstart', function(e){ var s = e.target.closest && e.target.closest('[data-sira]'); if(!s || s.parentNode !== L) return; tasinan = s; s.classList.add('is-tasiniyor'); e.dataTransfer.effectAllowed = 'move'; try{ e.dataTransfer.setData('text/plain', ''); }catch(x){} });
    L.addEventListener('dragend', function(){ if(!tasinan) return; tasinan.classList.remove('is-tasiniyor'); tasinan.draggable = false; tasinan = null; bitti(); });
    L.addEventListener('keydown', function(e){
      var t = e.target.closest('.kb-tutamac'), s = t && t.closest('[data-sira]'); if(!s || s.parentNode !== L) return;
      var onceki = s.previousElementSibling, sonraki = s.nextElementSibling;
      if(e.key === 'ArrowUp' && onceki && onceki.hasAttribute('data-sira')){ e.preventDefault(); L.insertBefore(s, onceki); t.focus(); bitti(); }
      if(e.key === 'ArrowDown' && sonraki && sonraki.hasAttribute('data-sira')){ e.preventDefault(); L.insertBefore(sonraki, s); t.focus(); bitti(); }
    });
    L.addEventListener('dragover', function(e){
      if(!tasinan) return; e.preventDefault();
      var digerleri = Array.prototype.filter.call(L.querySelectorAll(':scope > [data-sira]'), function(x){ return x !== tasinan; });
      var alt = digerleri.filter(function(x){ var r = x.getBoundingClientRect(); return e.clientY < r.top + r.height / 2; })[0];
      if(alt) L.insertBefore(tasinan, alt); else { var son = digerleri[digerleri.length - 1]; if(son) L.insertBefore(tasinan, son.nextSibling); }
    });
  });

  /* ---------------- özellik anahtarı ----------------
     <label class="toggle"><input type="checkbox" data-anahtar="Yorumlar" data-anahtar-etki="haber detayı, canlı anlatım"></label>
     Değişiklik önce/sonra onayıyla uygulanır, hemen yayına yansır, geri alınabilir ve denetim izine yazılır. */
  window.kbKurucu('input[data-anahtar]', function(i){
    i.addEventListener('click', function(e){
      e.preventDefault();
      var yeni = !i.checked === false ? true : false; /* tıklamada i.checked yeni değeri gösterir */
      yeni = i.checked; i.checked = !yeni;
      var adx = i.dataset.anahtar, etki = i.dataset.anahtarEtki;
      window.kbOnay({ tehlike: !yeni, ikon: yeni ? 'fa-toggle-on' : 'fa-toggle-off',
        baslik: adx + (yeni ? ' açılsın mı?' : ' kapatılsın mı?'),
        metin: 'Önce: ' + (yeni ? 'kapalı' : 'açık') + ' → Sonra: ' + (yeni ? 'açık' : 'kapalı') + '. Değişiklik hemen sitede ve uygulamada geçerli olur' + (etki ? ' (etkilenen: ' + etki + ')' : '') + '; önbellek yenilenir ve denetim izine yazılır.',
        evet: yeni ? 'Aç' : 'Kapat',
        evetIs: function(){
          i.checked = yeni;
          var satir = i.closest('[data-anahtar-satir]'), m = satir && satir.querySelector('.kb-ozk-meta');
          if(m) m.textContent = (yeni ? 'Açıldı' : 'Kapatıldı') + ' · 24.11.2026 16.05 · ' + ad();
          if(satir) satir.classList.toggle('is-kapali', !yeni);
          window.kbBildir(adx + (yeni ? ' açıldı' : ' kapatıldı') + '; önbellek yenilendi', function(){ i.checked = !yeni; if(satir) satir.classList.toggle('is-kapali', yeni); if(m) m.textContent = 'Geri alındı · 24.11.2026 16.05 · ' + ad(); window.kbBildir('Geri alındı'); });
        } });
    });
  });
  /* =====================================================================
     DALGA 2 BİLEŞENLERİ (lead): güven skoru, eşik kaydırıcı, dosya yükleme, takvim. Kaynak teyidi yalnız CSS.
     ===================================================================== */
  var AYLAR = ['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık'];
  var GUNLER = ['Pazartesi','Salı','Çarşamba','Perşembe','Cuma','Cumartesi','Pazar'], GUNK = ['Pzt','Sal','Çar','Per','Cum','Cmt','Paz'];
  function iki(n){ return (n < 10 ? '0' : '') + n; }
  function sayiTr(n){ return Number(n).toLocaleString('tr'); }

  /* ---------------- güven skoru ----------------
     <span class="kb-guven" data-guven="86" [data-esik="80"]></span> · büyük: class="kb-guven k-lg"
     Seviye: 85+ yüksek, 60–84 orta, 60 altı düşük (CC, kararlar §4). Eşik verilirse ipucunda üstünde/altında yazar. */
  window.kbKurucu('[data-guven]', function(G){
    var s = Math.max(0, Math.min(100, +G.dataset.guven || 0)), esik = +(G.dataset.esik || 0);
    var sev = s >= 85 ? 'yuksek' : s >= 60 ? 'orta' : 'dusuk', ad = { yuksek:'yüksek', orta:'orta', dusuk:'düşük' }[sev];
    G.classList.add('kb-guven'); G.dataset.seviye = sev; G.style.setProperty('--skor', s);
    var not = 'Güven skoru %' + s + ' · ' + ad + (esik ? (s >= esik ? ' · otomatik yayın eşiğinin (%' + esik + ') üstünde' : ' · eşiğin (%' + esik + ') altında, editör onayı bekler') : '');
    if(G.classList.contains('k-lg')) G.innerHTML = '<span class="kb-guven-halka" aria-hidden="true"><b>' + s + '</b></span><span class="kb-guven-ad">Güven <b>' + ad + '</b>' + (esik ? '<small>' + (s >= esik ? 'eşik üstü' : 'eşik altı') + ' · eşik %' + esik + '</small>' : '') + '</span>';
    else G.innerHTML = '<i aria-hidden="true"></i><b>' + s + '</b>';
    G.setAttribute('role', 'img'); G.setAttribute('aria-label', not); G.title = not;
  });

  /* ---------------- eşik kaydırıcı ----------------
     <div class="kb-esik" data-dagilim="4,6,9,…" [data-donem="Son 7 gün"]> <label for=…>…</label><output></output> <input type="range" min max step value> </div>
     Dağılım: aralığı eşit dilimlere bölen haber sayıları. Üstündeki dilimler "otomatik yayımlanır", altı "kuyrukta kalır". */
  window.kbKurucu('.kb-esik', function(E){
    var r = E.querySelector('input[type=range]'); if(!r) return;
    var o = E.querySelector('output'), min = +r.min || 0, max = +(r.max || 100);
    var d = (E.dataset.dagilim || '').split(',').map(Number).filter(function(x){ return !isNaN(x); });
    var top = d.reduce(function(a, b){ return a + b; }, 0), enb = Math.max.apply(null, d.concat(1)), adim = d.length ? (max - min) / d.length : 1;
    var g = E.querySelector('.kb-esik-grafik'), n = E.querySelector('.kb-esik-not');
    if(d.length && !g){ g = document.createElement('div'); g.className = 'kb-esik-grafik'; g.setAttribute('aria-hidden', 'true'); r.parentNode.insertBefore(g, r); }
    if(g) g.innerHTML = d.map(function(v){ return '<i style="--h:' + Math.max(4, v / enb * 100) + '%"></i>'; }).join('');
    if(!E.querySelector('.kb-esik-olcek')){ var olc = document.createElement('div'); olc.className = 'kb-esik-olcek'; olc.setAttribute('aria-hidden', 'true'); olc.innerHTML = '<span>%' + min + '</span><span>Kuyrukta kalır ← → Otomatik yayımlanır</span><span>%' + max + '</span>'; r.parentNode.insertBefore(olc, r.nextSibling); }
    if(d.length && !n){ n = document.createElement('p'); n.className = 'kb-esik-not'; n.setAttribute('aria-live', 'polite'); E.appendChild(n); }
    function guncelle(){
      var v = +r.value, ust = 0;
      if(o) o.textContent = '%' + v;
      r.style.setProperty('--yuzde', ((v - min) / (max - min) * 100) + '%');
      d.forEach(function(x, i){ var bas = min + i * adim, pay = Math.max(0, Math.min(1, (bas + adim - v) / adim)); ust += x * pay; if(g && g.children[i]) g.children[i].classList.toggle('is-ust', bas + adim / 2 >= v); });
      ust = Math.round(ust);
      if(n && top) n.innerHTML = '<b>' + (E.dataset.donem || 'Son 7 gün') + ':</b> ' + sayiTr(top) + ' AI haberinin <b>' + sayiTr(ust) + ' tanesi (%' + Math.round(ust / top * 100) + ')</b> bu eşikle otomatik yayımlanırdı; ' + sayiTr(top - ust) + ' tanesi editör onayı beklerdi.';
      r.setAttribute('aria-valuetext', '%' + v);
    }
    r.addEventListener('input', guncelle); guncelle();
  });

  /* ---------------- dosya yükleme (video, ses, belge) ----------------
     <div class="kb-dosya" data-tur="video|ses|belge" [data-sinir="500"] (MB) [data-coklu] [data-kabul=".pdf,…"] [data-alan-id]>
       [hazır dosya için: <div class="kb-dosya-oge" data-ad data-boyut data-sure>…]</div>
     Sürükle-bırak ya da "Dosya seç"; ilerleme, ad, boyut, süre (video ve seste). Kaldır: onaysız + "Geri al" (B8).
     Tekli alanda dosya varken bırakma alanı gizlenir, satırda "Değiştir" çıkar. Zorunlu alanda boşluk kbAlanBos ile denetlenir. */
  var DOSYA = {
    video: { ikon:'fa-file-video', kabul:'video/mp4,video/quicktime,video/webm', yazi:'MP4, MOV ya da WEBM', sinir:500 },
    ses:   { ikon:'fa-file-audio', kabul:'audio/mpeg,audio/mp4,audio/x-m4a,audio/wav,audio/ogg', yazi:'MP3, M4A, WAV ya da OGG', sinir:200 },
    belge: { ikon:'fa-file-lines', kabul:'.pdf,.doc,.docx,.xls,.xlsx,.csv,.ppt,.pptx', yazi:'PDF, Word, Excel ya da PowerPoint', sinir:50 }
  };
  function boyutYaz(b){ return b >= 1073741824 ? (b / 1073741824).toLocaleString('tr', { maximumFractionDigits:1 }) + ' GB' : b >= 1048576 ? (b / 1048576).toLocaleString('tr', { maximumFractionDigits:1 }) + ' MB' : Math.max(1, Math.round(b / 1024)) + ' KB'; }
  function sureYaz(s){ s = Math.round(s); var sa = Math.floor(s / 3600), dk = Math.floor(s % 3600 / 60), sn = s % 60; return (sa ? sa + ' sa ' : '') + (dk ? dk + ' dk ' : '') + (sa ? '' : sn + ' sn'); }
  window.kbKurucu('.kb-dosya', function(D){
    var tur = DOSYA[D.dataset.tur] ? D.dataset.tur : 'belge', T = DOSYA[tur], coklu = D.hasAttribute('data-coklu');
    var sinir = +(D.dataset.sinir || T.sinir), kabul = D.dataset.kabul || T.kabul;
    var bos = document.createElement('label'); bos.className = 'kb-dosya-bos';
    bos.innerHTML = '<input type="file" accept="' + kabul + '"' + (coklu ? ' multiple' : '') + '><i class="fa-solid ' + (tur === 'ses' ? 'fa-microphone-lines' : tur === 'video' ? 'fa-film' : 'fa-file-arrow-up') + '" aria-hidden="true"></i><b>' + (coklu ? 'Dosyaları' : 'Dosyayı') + ' sürükleyip bırakın</b><span>' + T.yazi + ' · en fazla ' + sayiTr(sinir) + ' MB</span><span class="btn btn-ghost btn-sm"><i class="fa-solid fa-upload" aria-hidden="true"></i>Dosya seç</span>';
    var inp = bos.querySelector('input'); inp.setAttribute('aria-label', (D.dataset.ad || 'Dosya') + ' yükle');
    var liste = D.querySelector('.kb-dosya-liste'); if(!liste){ liste = document.createElement('div'); liste.className = 'kb-dosya-liste'; Array.prototype.slice.call(D.querySelectorAll(':scope > .kb-dosya-oge')).forEach(function(x){ liste.appendChild(x); }); D.appendChild(liste); }
    D.insertBefore(bos, liste);
    function durum(){ var var_ = !!liste.querySelector('.kb-dosya-oge'); bos.hidden = !coklu && var_; D.classList.toggle('is-dolu', var_); D.dispatchEvent(new Event('input', { bubbles:true })); if(window.kbPasifGuncelle) window.kbPasifGuncelle(); }
    function satir(ad, boyut, sure, hazir){
      var s = document.createElement('div'); s.className = 'kb-dosya-oge' + (hazir ? '' : ' is-yukleniyor');
      s.innerHTML = '<span class="kb-dosya-ikon"><i class="fa-solid ' + T.ikon + '" aria-hidden="true"></i></span><div class="kb-dosya-bilgi"><b></b><span class="kb-dosya-meta"></span><div class="kb-ilerleme"><span></span></div></div><div class="kb-dosya-eylem">' + (coklu ? '' : '<button type="button" class="btn btn-ghost btn-sm" data-dosya-degistir>Değiştir</button>') + '<button type="button" class="ia-btn danger" data-dosya-kaldir aria-label="Dosyayı kaldır" title="Kaldır"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button></div>';
      s.querySelector('b').textContent = ad; s.dataset.ad = ad; s.dataset.boyut = boyut; if(sure) s.dataset.sure = sure;
      meta(s); return s;
    }
    function meta(s){ var m = s.querySelector('.kb-dosya-meta'); if(!m) return; m.textContent = [s.dataset.boyut && boyutYaz(+s.dataset.boyut), s.dataset.sure && sureYaz(+s.dataset.sure), s.classList.contains('is-yukleniyor') ? 'yükleniyor…' : 'yüklendi'].filter(Boolean).join(' · '); }
    function ekle(f){
      var hata = f.size > sinir * 1048576 ? f.name + ': ' + sayiTr(sinir) + ' MB sınırını aşıyor (' + boyutYaz(f.size) + ')' : null;
      if(!hata && tur !== 'belge' && f.type && f.type.indexOf(tur === 'ses' ? 'audio' : 'video') !== 0) hata = f.name + ': ' + T.yazi + ' bekleniyor';
      if(hata){ window.kbBildir(hata, null, 'hata'); return; }
      if(!coklu) liste.innerHTML = '';
      var s = satir(f.name, f.size, 0, false); liste.appendChild(s); durum();
      if(tur !== 'belge' && window.URL){ var m = document.createElement(tur === 'ses' ? 'audio' : 'video'); m.preload = 'metadata'; m.src = URL.createObjectURL(f); m.onloadedmetadata = function(){ if(isFinite(m.duration)){ s.dataset.sure = m.duration; meta(s); } URL.revokeObjectURL(m.src); }; }
      var y = 0, cubuk = s.querySelector('.kb-ilerleme span'), t = setInterval(function(){ y = Math.min(100, y + 12 + Math.random() * 18); cubuk.style.setProperty('--yuzde', y + '%'); if(y >= 100){ clearInterval(t); s.classList.remove('is-yukleniyor'); meta(s); durum(); D.dispatchEvent(new CustomEvent('kb-dosya', { bubbles:true, detail:{ ad:f.name, boyut:f.size } })); } }, 160);
    }
    liste.querySelectorAll('.kb-dosya-oge').forEach(function(s){ if(!s.children.length){ var y = satir(s.dataset.ad || 'dosya', s.dataset.boyut, s.dataset.sure, true); s.replaceWith(y); } });
    inp.addEventListener('change', function(){ Array.prototype.forEach.call(inp.files, ekle); inp.value = ''; });
    ['dragenter', 'dragover'].forEach(function(ev){ D.addEventListener(ev, function(e){ e.preventDefault(); D.classList.add('is-surukle'); }); });
    ['dragleave', 'drop'].forEach(function(ev){ D.addEventListener(ev, function(e){ e.preventDefault(); if(ev === 'dragleave' && D.contains(e.relatedTarget)) return; D.classList.remove('is-surukle'); }); });
    D.addEventListener('drop', function(e){ var fs = e.dataTransfer && e.dataTransfer.files; if(!fs || !fs.length) return; Array.prototype.slice.call(fs, 0, coklu ? fs.length : 1).forEach(ekle); });
    liste.addEventListener('click', function(e){
      var s = e.target.closest('.kb-dosya-oge'); if(!s) return;
      if(e.target.closest('[data-dosya-degistir]')){ inp.click(); return; }
      if(e.target.closest('[data-dosya-kaldir]')){
        var sonraki = s.nextSibling; s.remove(); durum();
        window.kbBildir((s.dataset.ad || 'Dosya') + ' kaldırıldı', function(){ liste.insertBefore(s, sonraki && sonraki.parentNode === liste ? sonraki : null); durum(); });
      }
    });
    durum();
  });

  /* ---------------- takvim görünümü ----------------
     <div class="kb-takvim" [data-baslangic="24.11.2026"] [data-gorunum="ay|hafta|liste"] [data-gun-ac="sablonId"]>
       <div class="kb-takvim-veri" hidden> <a href="…" data-tarih="24.11.2026 14.30" [data-ton="marka|bilgi|ok|uyari|tehlike|notr"] [data-ikon="fa-brands fa-x-twitter"]>Metin</a> … </div>
     </div>
     Olay bağlantısı kendi sayfasını açar (satır → sayfa); data-tanim taşıyan olay çekmece açar. Boş güne tıklamak
     data-gun-ac şablonunu çekmecede açar ve içindeki tarih seçiciye o günü yazar. Telefonda Ay ve Hafta Liste olur. */
  window.kbKurucu('.kb-takvim', function(T){
    /* Listeye bağlı takvim (tek veri görünümü kuralı): [data-liste] içindeki .kb-takvim olaylarını listenin satırlarından
       (tr[data-satir][data-tarih]) okur; listenin sekme, arama ve süzgeci takvime de uygulanır. "Liste" düğmesi listenin
       kendi tablosunu (Çöp, toplu seçim, satır eylemleri) gösterir; Ay/Hafta takvimi gösterir. L[data-gorunum="takvim|liste"]. */
    var BL = T.closest('[data-liste]');
    var veri = T.querySelector('.kb-takvim-veri');
    if(BL){ if(!veri){ veri = document.createElement('div'); veri.className = 'kb-takvim-veri'; veri.hidden = true; T.appendChild(veri); } }
    if(!veri) return;
    function listedenOku(){
      veri.innerHTML = '';
      BL.querySelectorAll('tr[data-satir][data-tarih]').forEach(function(r){
        if(r._kbGecti === false || r.dataset.durum === 'cop') return;
        var a = document.createElement('a'), ilk = r.querySelector('.row-acts a[href]:not([href="#"]), .row-acts [data-tanim], [data-hedef]');
        a.dataset.tarih = r.dataset.tarih; if(r.dataset.ton) a.dataset.ton = r.dataset.ton; if(r.dataset.ikon) a.dataset.ikon = r.dataset.ikon;
        if(r.dataset.not) a.dataset.not = r.dataset.not;
        if(r.dataset.href) a.href = r.dataset.href; else if(ilk && ilk.getAttribute('href') && ilk.getAttribute('href') !== '#') a.href = ilk.getAttribute('href'); else if(ilk && ilk.hasAttribute('data-tanim')) a.setAttribute('data-tanim', ilk.getAttribute('data-tanim'));
        a._kbSatir = r;
        a.textContent = r.dataset.ad || ((r.querySelector('.rcp-name') || r.querySelector('td.kb-ana') || r).textContent || '').trim();
        veri.appendChild(a);
      });
    }
    if(BL) listedenOku();
    function coz(s){ var m = (s || '').match(/(\d{1,2})\.(\d{1,2})\.(\d{4})(?:\s+(\d{1,2})\.(\d{2}))?/); return m ? { g:+m[1], a:+m[2] - 1, y:+m[3], h:m[4] ? +m[4] : null, m:m[5] ? +m[5] : 0 } : null; }
    var olaylar = [];
    function olaylariOku(){ olaylar = Array.prototype.map.call(veri.querySelectorAll('[data-tarih]'), function(el){ var t = coz(el.dataset.tarih); return t ? { t:t, el:el, d:new Date(t.y, t.a, t.g, t.h || 0, t.m) } : null; }).filter(Boolean).sort(function(a, b){ return a.d - b.d; }); }
    olaylariOku();
    var bugun = coz(T.dataset.bugun || T.dataset.baslangic) || (function(){ var n = new Date(); return { y:n.getFullYear(), a:n.getMonth(), g:n.getDate() }; })();
    var odak = new Date(bugun.y, bugun.a, bugun.g), gorunum = T.dataset.gorunum || 'ay', dar = window.matchMedia('(max-width:640px)');
    var ust = document.createElement('div'); ust.className = 'kb-takvim-ust';
    ust.innerHTML = '<div class="kb-takvim-gez"><button type="button" class="ia-btn" data-takvim="geri" aria-label="Önceki"><i class="fa-solid fa-chevron-left" aria-hidden="true"></i></button><button type="button" class="ia-btn" data-takvim="ileri" aria-label="Sonraki"><i class="fa-solid fa-chevron-right" aria-hidden="true"></i></button><span class="kb-takvim-baslik" aria-live="polite"></span><button type="button" class="btn btn-ghost btn-sm" data-takvim="bugun">Bugün</button></div><div class="chips kb-takvim-gorunum" role="group" aria-label="Görünüm"><button type="button" class="chip" data-gorunum="ay">Ay</button><button type="button" class="chip" data-gorunum="hafta">Hafta</button><button type="button" class="chip" data-gorunum="liste">Liste</button></div>';
    var govde = document.createElement('div'); govde.className = 'kb-takvim-govde';
    T.insertBefore(ust, veri); T.insertBefore(govde, veri);
    function ayni(a, b){ return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate(); }
    var bugunD = new Date(bugun.y, bugun.a, bugun.g);
    function gunOlay(d){ return olaylar.filter(function(o){ return ayni(o.d, d); }); }
    function olayHtml(o, uzun){
      var el = o.el, ton = el.dataset.ton || 'marka', ikon = el.dataset.ikon, saat = o.t.h != null ? iki(o.t.h) + '.' + iki(o.t.m) : '';
      var c = el.cloneNode(true); c.removeAttribute('data-tarih'); c.className = 'kb-takvim-olay ton-' + ton + (el.className ? ' ' + el.className : '');
      c.innerHTML = (ikon ? '<i class="' + ikon + '" aria-hidden="true"></i>' : '') + (saat ? '<time>' + saat + '</time>' : '') + '<span>' + el.innerHTML + '</span>' + (uzun && el.dataset.not ? '<small>' + el.dataset.not + '</small>' : '');
      if(!c.getAttribute('href') && c.tagName === 'A') c.setAttribute('href', '#');
      return c.outerHTML;
    }
    function gunBtn(d, metin, sinif){ return '<button type="button" class="' + sinif + '" data-takvim-gun="' + iki(d.getDate()) + '.' + iki(d.getMonth() + 1) + '.' + d.getFullYear() + '" aria-label="' + d.getDate() + ' ' + AYLAR[d.getMonth()] + ' ' + GUNLER[(d.getDay() + 6) % 7] + (T.dataset.gunAc ? ', yeni ekle' : '') + '">' + metin + '</button>'; }
    function ciz(){
      var g = gorunum !== 'liste' && dar.matches ? 'liste' : gorunum; /* telefonda Ay ve Hafta Liste olur */
      if(BL){ BL.dataset.gorunum = g === 'liste' ? 'liste' : 'takvim'; if(g === 'liste'){ ust.querySelectorAll('[data-gorunum]').forEach(function(b){ var on = b.dataset.gorunum === 'liste'; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', on); }); T.dataset.etkin = 'liste'; govde.innerHTML = ''; return; } }
      ust.querySelectorAll('[data-gorunum]').forEach(function(b){ var on = b.dataset.gorunum === g; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', on); });
      T.dataset.etkin = g; var h = '', bas, d, i;
      if(g === 'hafta'){
        bas = new Date(odak); bas.setDate(bas.getDate() - (bas.getDay() + 6) % 7);
        var son = new Date(bas); son.setDate(son.getDate() + 6);
        ust.querySelector('.kb-takvim-baslik').textContent = bas.getDate() + (bas.getMonth() !== son.getMonth() ? ' ' + AYLAR[bas.getMonth()] : '') + ' – ' + son.getDate() + ' ' + AYLAR[son.getMonth()] + ' ' + son.getFullYear();
        h = '<div class="kb-takvim-hafta">';
        for(i = 0; i < 7; i++){ d = new Date(bas); d.setDate(bas.getDate() + i); var ol = gunOlay(d);
          h += '<div class="kb-takvim-sutun' + (ayni(d, bugunD) ? ' is-bugun' : '') + '"><div class="kb-takvim-sbas">' + gunBtn(d, '<span>' + GUNK[i] + '</span><b>' + d.getDate() + '</b>', 'kb-takvim-no') + '</div><div class="kb-takvim-olaylar">' + (ol.length ? ol.map(function(o){ return olayHtml(o, true); }).join('') : '<span class="kb-takvim-bos">—</span>') + '</div></div>'; }
        h += '</div>';
      } else if(g === 'liste'){
        ust.querySelector('.kb-takvim-baslik').textContent = AYLAR[odak.getMonth()] + ' ' + odak.getFullYear();
        var ayO = olaylar.filter(function(o){ return o.d.getMonth() === odak.getMonth() && o.d.getFullYear() === odak.getFullYear(); }), son2 = null;
        h = '<div class="kb-takvim-liste">';
        ayO.forEach(function(o){ if(!son2 || !ayni(son2, o.d)){ if(son2) h += '</div></div>'; son2 = o.d; h += '<div class="kb-takvim-lgun' + (ayni(o.d, bugunD) ? ' is-bugun' : '') + '"><div class="kb-takvim-lbas"><b>' + o.d.getDate() + ' ' + AYLAR[o.d.getMonth()] + '</b><span>' + GUNLER[(o.d.getDay() + 6) % 7] + '</span></div><div class="kb-takvim-olaylar">'; } h += olayHtml(o, true); });
        h += ayO.length ? '</div></div>' : '<div class="pnl-empty kb-takvim-liste-bos"><div class="pe-ico"><i class="fa-regular fa-calendar" aria-hidden="true"></i></div><b>Bu ay kayıt yok</b></div>';
        h += '</div>';
      } else {
        ust.querySelector('.kb-takvim-baslik').textContent = AYLAR[odak.getMonth()] + ' ' + odak.getFullYear();
        var ilk = new Date(odak.getFullYear(), odak.getMonth(), 1); bas = new Date(ilk); bas.setDate(1 - (ilk.getDay() + 6) % 7);
        var hucre = Math.ceil(((ilk.getDay() + 6) % 7 + new Date(odak.getFullYear(), odak.getMonth() + 1, 0).getDate()) / 7) * 7;
        h = '<div class="kb-takvim-ay"><div class="kb-takvim-gunler" aria-hidden="true">' + GUNK.map(function(x){ return '<span>' + x + '</span>'; }).join('') + '</div><div class="kb-takvim-izgara">';
        for(i = 0; i < hucre; i++){ d = new Date(bas); d.setDate(bas.getDate() + i); var o2 = gunOlay(d), fazla = o2.length - 3;
          h += '<div class="kb-takvim-gun' + (d.getMonth() !== odak.getMonth() ? ' is-diger' : '') + (ayni(d, bugunD) ? ' is-bugun' : '') + '">' + gunBtn(d, d.getDate(), 'kb-takvim-no') + '<div class="kb-takvim-olaylar">' + o2.slice(0, 3).map(function(o){ return olayHtml(o); }).join('') + (fazla > 0 ? '<button type="button" class="kb-takvim-fazla" data-takvim-hafta="' + d.getTime() + '">+' + fazla + ' daha</button>' : '') + '</div></div>'; }
        h += '</div></div>';
      }
      govde.innerHTML = h;
    }
    ust.addEventListener('click', function(e){
      var b = e.target.closest('[data-takvim],[data-gorunum]'); if(!b) return;
      if(b.dataset.gorunum){ gorunum = b.dataset.gorunum; ciz(); return; }
      var k = b.dataset.takvim, g = T.dataset.etkin;
      if(k === 'bugun') odak = new Date(bugunD);
      else if(g === 'hafta') odak.setDate(odak.getDate() + (k === 'ileri' ? 7 : -7));
      else odak = new Date(odak.getFullYear(), odak.getMonth() + (k === 'ileri' ? 1 : -1), 1);
      ciz();
    });
    govde.addEventListener('click', function(e){
      var f = e.target.closest('[data-takvim-hafta]'); if(f){ odak = new Date(+f.dataset.takvimHafta); gorunum = 'hafta'; ciz(); return; }
      var o = e.target.closest('.kb-takvim-olay');
      if(o){ if(o.hasAttribute('data-tanim')){ e.preventDefault(); window.kbAc(o.getAttribute('data-tanim'), 'cekmece'); } else if(o.getAttribute('href') === '#'){ e.preventDefault(); if(BL){ var ad0 = o.textContent.trim(); var r0 = Array.prototype.filter.call(BL.querySelectorAll('tr[data-satir]'), function(r){ return (r.dataset.ad || '').trim() === ad0 || ((r.querySelector('.rcp-name') || {}).textContent || '').trim() === ad0; })[0]; var td = r0 && r0.querySelector('td.kb-ana, td:nth-child(2)'); if(td) td.click(); } } return; }
      var gb = e.target.closest('[data-takvim-gun]');
      if(gb && T.dataset.gunAc){ var t = coz(gb.dataset.takvimGun); window.kbAc(T.dataset.gunAc, 'cekmece', function(k){ var kt = k.querySelector('.kb-tarih-sec'); if(kt && kt.kbAyarla) kt.kbAyarla({ y:t.y, a:t.a, g:t.g, h:10, m:0 }); }); }
    });
    if(dar.addEventListener) dar.addEventListener('change', ciz);
    if(BL){
      BL.addEventListener('kb-liste-suzuldu', function(e){
        /* Çöp yalnız liste görünümünde (sözleşme) */
        if(e.detail && e.detail.sekme === 'cop' && gorunum !== 'liste'){ gorunum = 'liste'; }
        listedenOku(); olaylariOku(); ciz();
      });
    }
    ciz();
  });
  /* =====================================================================
     DALGA 2 · teammate bildirimleriyle eklenenler (lead)
     ===================================================================== */
  function escH(s){ return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); }

  /* ---------------- havuzdan seçilen sıralı liste ----------------
     <div class="kb-sirali" data-sirali-havuz [data-sinir="5"] [data-sirali-ad="Haber"] [data-alan-id]>
       <div class="kb-madde" data-siralanir> <div class="km-satir" data-sira data-deger="…" data-ad="…" [data-alt] [data-gorsel]>…</div> … </div>
       <div class="kb-secim" data-sirali-kaynak …> (seçenekler: button[data-deger][data-ad][data-alt][data-gorsel]) </div>
     </div>
     Aranabilir listeden seçilen kayıt sona eklenir (aynısı iki kez eklenmez; sınır dolunca uyarı); sürükle-bırak sıra;
     × onaysız kaldırır + Geri al (B8). Satırları hazır yazmak yerine yalnız data-* verip boş bırakabilirsin; bileşen doldurur. */
  function siraliSatir(o){
    var s = document.createElement('div'); s.className = 'km-satir'; s.setAttribute('data-sira', '');
    ['deger', 'ad', 'alt', 'gorsel'].forEach(function(k){ if(o[k]) s.dataset[k] = o[k]; });
    s.innerHTML = siraliIc(o); return s;
  }
  function siraliIc(o){
    return '<button type="button" class="kb-tutamac" aria-label="Sırayı değiştir (ok tuşları)"><i class="fa-solid fa-grip-vertical" aria-hidden="true"></i></button><span class="km-no"></span>'
      + (o.gorsel ? '<span class="rcp-thumb" style="background-image:url(' + escH(o.gorsel) + ')"></span>' : '')
      + '<span class="km-yazi">' + escH(o.ad) + (o.alt ? '<small>' + escH(o.alt) + '</small>' : '') + '</span>'
      + '<button type="button" class="ia-btn danger" data-sirali-sil aria-label="Listeden çıkar" title="Listeden çıkar"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button>';
  }
  window.kbKurucu('[data-sirali-havuz]', function(K){
    var liste = K.querySelector('[data-siralanir]'), sec = K.querySelector('.kb-secim'), sinir = +(K.dataset.sinir || 0), adx = K.dataset.siraliAd || 'Kayıt';
    if(!liste) return;
    liste.querySelectorAll(':scope > .km-satir').forEach(function(s){ if(!s.children.length) s.innerHTML = siraliIc(s.dataset); });
    function numara(){ if(liste._kbSiraBitti) liste._kbSiraBitti(); else liste.querySelectorAll('.km-no').forEach(function(n, i){ n.textContent = i + 1; }); K.classList.toggle('is-dolu', sinir && liste.querySelectorAll(':scope > .km-satir').length >= sinir); }
    if(sec) sec.addEventListener('kb-secim', function(e){
      var d = e.detail && e.detail.deger; if(!d) return;
      var o = sec.querySelector('button[data-deger="' + d + '"]');
      var sifirla = function(){ sec.dataset.deger = ''; sec.classList.remove('is-dolu'); var l = sec.querySelector('.ks-deger'); if(l) l.textContent = sec.dataset.yer || (adx + ' ekle'); };
      if(liste.querySelector(':scope > .km-satir[data-deger="' + d + '"]')){ window.kbBildir('Bu ' + adx.toLocaleLowerCase('tr') + ' listede zaten var', null, 'uyari'); sifirla(); return; }
      if(sinir && liste.querySelectorAll(':scope > .km-satir').length >= sinir){ window.kbBildir('Liste dolu (' + sinir + '); önce birini çıkarın', null, 'uyari'); sifirla(); return; }
      liste.appendChild(siraliSatir({ deger:d, ad: o ? (o.dataset.ad || o.textContent.trim()) : d, alt: o && o.dataset.alt, gorsel: o && o.dataset.gorsel }));
      sifirla(); numara(); e.stopPropagation();
    });
    K.addEventListener('click', function(e){
      var b = e.target.closest('[data-sirali-sil]'); if(!b) return;
      var s = b.closest('.km-satir'), sonra = s.nextSibling; s.remove(); numara();
      window.kbBildir(adx + ' çıkarıldı: ' + (s.dataset.ad || ''), function(){ liste.insertBefore(s, sonra && sonra.parentNode === liste ? sonra : null); numara(); });
    });
    numara();
  });

  /* ---------------- galeri sıralayıcı (slaytlar) ----------------
     <div class="kb-slaytlar" data-slaytlar data-gorsel-alan="multimedya.galeri" [data-kirp-sonra] [data-alan-id="slaytlar"]>
       <div class="kb-slayt-liste" data-siralanir> <div class="kb-slayt" data-sira data-gorsel="url" [data-altyazi] [data-kaynak] [data-kapak]></div> … </div>
       <div class="kb-slayt-ekle"><button data-medya-sec data-gorsel-kapsam="yeni" data-slayt-ekle>Havuzdan ekle</button>
         <button data-gorsel-yukle data-gorsel-kapsam="yeni" data-slayt-ekle>Yükle</button><span hidden data-gorsel-hedef="yeni"></span></div>
     </div>
     Havuzdan seçilen ya da yüklenen (etiketle → kırp) görsel yeni slayt olur; slaytta altyazı ve kaynak, kapak seçimi, sıra, kaldır (B8). */
  function slaytIc(o, i, ad){
    return '<button type="button" class="kb-tutamac" aria-label="Sırayı değiştir (ok tuşları)"><i class="fa-solid fa-grip-vertical" aria-hidden="true"></i></button>'
      + '<span class="km-no"></span><span class="kb-slayt-resim" style="background-image:url(' + escH(o.gorsel) + ')"></span>'
      + '<div class="kb-slayt-alan"><input class="finput" data-slayt-altyazi placeholder="Altyazı" aria-label="Altyazı" value="' + escH(o.altyazi || '') + '"><input class="finput" data-slayt-kaynak placeholder="Kaynak (ör. AA, Dada Haber)" aria-label="Kaynak" value="' + escH(o.kaynak || '') + '"></div>'
      + '<label class="kb-slayt-kapak"><input type="radio" name="' + ad + '"' + (o.kapak ? ' checked' : '') + '><span>Kapak</span></label>'
      + '<button type="button" class="ia-btn danger" data-slayt-sil aria-label="Slaytı kaldır" title="Kaldır"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button>';
  }
  var slaytSay = 0;
  window.kbKurucu('[data-slaytlar]', function(K){
    var liste = K.querySelector('.kb-slayt-liste'), ad = 'kbKapak' + (++slaytSay), yeni = K.querySelector('[data-gorsel-hedef="yeni"]');
    if(!liste) return;
    liste.querySelectorAll(':scope > .kb-slayt').forEach(function(s){ if(!s.children.length) s.innerHTML = slaytIc({ gorsel:s.dataset.gorsel, altyazi:s.dataset.altyazi, kaynak:s.dataset.kaynak, kapak:s.hasAttribute('data-kapak') }, 0, ad); });
    function guncelle(){
      var ss = liste.querySelectorAll(':scope > .kb-slayt');
      if(ss.length && !liste.querySelector('input[type=radio]:checked')) ss[0].querySelector('input[type=radio]').checked = true;
      if(liste._kbSiraBitti) liste._kbSiraBitti(); else ss.forEach(function(s, i){ s.querySelector('.km-no').textContent = i + 1; });
      var say = K.querySelector('[data-slayt-say]'); if(say) say.textContent = ss.length + ' slayt';
      K.classList.toggle('is-bos', !ss.length);
    }
    K.addEventListener('kb-gorsel', function(e){
      if(!e.target.closest('[data-slayt-ekle]') || !yeni) return;
      e.stopPropagation();
      var url = (yeni.style.backgroundImage || '').replace(/^url\(["']?/, '').replace(/["']?\)$/, ''); if(!url) return;
      var s = document.createElement('div'); s.className = 'kb-slayt'; s.setAttribute('data-sira', ''); s.dataset.gorsel = url;
      s.innerHTML = slaytIc({ gorsel:url }, 0, ad); liste.appendChild(s); yeni.style.backgroundImage = '';
      guncelle(); s.querySelector('[data-slayt-altyazi]').focus();
      K.dispatchEvent(new Event('input', { bubbles:true }));
    }, true);
    K.addEventListener('click', function(e){
      var b = e.target.closest('[data-slayt-sil]'); if(!b) return;
      var s = b.closest('.kb-slayt'), sonra = s.nextSibling, kapakti = s.querySelector('input[type=radio]').checked; s.remove(); guncelle();
      K.dispatchEvent(new Event('input', { bubbles:true }));
      window.kbBildir('Slayt kaldırıldı' + (kapakti ? '; kapak ilk slayta geçti' : ''), function(){ liste.insertBefore(s, sonra && sonra.parentNode === liste ? sonra : null); guncelle(); K.dispatchEvent(new Event('input', { bubbles:true })); });
    });
    guncelle();
  });

  /* ---------------- sıraya bağlı önizleme (vitrin / manşet) ----------------
     <div class="kb-vitrin-oniz" data-sira-onizleme="#listeId"> … [data-oniz-yer] öğeleri (sırayla) …
       her yerde [data-oniz-gorsel] (arka plan) ve [data-oniz-baslik] (metin) </div>
     Listedeki [data-sira] satırlarının data-ad ve data-gorsel değerleri sırayla yerlere yazılır; sıra değişince güncellenir. */
  window.kbKurucu('[data-sira-onizleme]', function(O){
    var L = document.querySelector(O.dataset.siraOnizleme); if(!L) return;
    function ciz(){
      var ss = L.querySelectorAll(':scope > [data-sira]'), yerler = O.querySelectorAll('[data-oniz-yer]');
      yerler.forEach(function(y, i){
        var s = ss[i], g = y.querySelector('[data-oniz-gorsel]'), b = y.querySelector('[data-oniz-baslik]');
        y.classList.toggle('is-bos', !s);
        if(g) g.style.backgroundImage = s && s.dataset.gorsel ? 'url(' + s.dataset.gorsel + ')' : '';
        if(b) b.textContent = s ? (s.dataset.ad || '') : 'Boş yer';
      });
    }
    ['input', 'kb-sira'].forEach(function(o){ L.addEventListener(o, ciz); });
    new MutationObserver(ciz).observe(L, { childList:true });
    ciz();
  });

  /* ---------------- basit bildirim düğmesi ----------------
     <button data-bildir-hemen="Canlı girişi yayımlandı">: onay gerektirmeyen işlem; kısa bildirim çıkar. */
  document.addEventListener('click', function(e){
    var b = e.target.closest && e.target.closest('[data-bildir-hemen]'); if(!b || b.disabled) return;
    e.preventDefault(); window.kbBildir(b.getAttribute('data-bildir-hemen'));
  });
  /* ---------------- marka şablonu önizlemesi ----------------
     <div class="kb-marka-oniz" id="mo1" data-marka-oniz data-gorsel="url" data-kategori="Savunma" [data-renk="#…" kategori rengi = veri]
          [data-baslik="…"] [data-logo="sag-ust"] [data-serit="alt"] [data-oran="16:9"] [data-logo-boyut="14"] [data-baslik-bandi] [data-karart]></div>
     Ayar alanları canlı bağlanır: herhangi bir input/select'e data-mo="logo|serit|oran|logo-boyut|baslik-bandi|karart" [data-mo-hedef="#mo1"].
     Radyo ve seçim değeri, anahtar (checkbox) açık/kapalı, sayı (yüzde) yazılır. Oran düğmeleri önizlemenin altında kendiliğinden. */
  var MO_ORAN = ['16:9', '1:1', '4:5', '1.91:1', '9:16'];
  window.kbKurucu('[data-marka-oniz]', function(O){
    O.classList.add('kb-marka-oniz');
    O.innerHTML = '<div class="kmo-kutu" role="img"><span class="kmo-karart"></span><span class="kmo-serit"></span><span class="kmo-baslik"></span><span class="kmo-logo"><span class="kb-logo"></span></span></div>'
      + '<div class="chips kmo-oranlar" role="group" aria-label="Önizleme oranı">' + MO_ORAN.map(function(o){ return '<button type="button" class="chip" data-mo-oran-sec="' + o + '">' + o + '</button>'; }).join('') + '</div>';
    var K = O.querySelector('.kmo-kutu');
    function ciz(){
      var d = O.dataset, oran = d.oran || '16:9', p = oran.split(':');
      K.style.backgroundImage = d.gorsel ? 'url(' + d.gorsel + ')' : '';
      K.style.setProperty('--oran', p[0] + '/' + p[1]);
      if(d.renk) O.style.setProperty('--kat-renk', d.renk);
      O.style.setProperty('--logo-boyut', (+(d.logoBoyut || 14)) + '%');
      K.querySelector('.kmo-serit').textContent = d.kategori || '';
      K.querySelector('.kmo-baslik').textContent = d.baslik || '';
      K.setAttribute('aria-label', 'Marka şablonu önizlemesi · ' + oran + ' · logo ' + (d.logo || 'sag-ust') + ' · şerit ' + (d.serit || 'alt'));
      O.querySelectorAll('[data-mo-oran-sec]').forEach(function(b){ var on = b.dataset.moOranSec === oran; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', on); });
    }
    O.addEventListener('click', function(e){ var b = e.target.closest('[data-mo-oran-sec]'); if(b){ O.dataset.oran = b.dataset.moOranSec; ciz(); } });
    O._kbMoCiz = ciz; ciz();
  });
  function moUygula(el){
    var k = el.getAttribute('data-mo'); if(!k) return;
    var hedef = el.dataset.moHedef ? document.querySelectorAll(el.dataset.moHedef) : document.querySelectorAll('[data-marka-oniz]');
    var ad = k.replace(/-([a-z])/g, function(m, c){ return c.toUpperCase(); });
    hedef.forEach(function(O){
      if(el.type === 'checkbox'){ if(el.checked) O.dataset[ad] = ''; else delete O.dataset[ad]; }
      else if(el.type === 'radio'){ if(el.checked) O.dataset[ad] = el.value; }
      else O.dataset[ad] = el.value;
      if(O._kbMoCiz) O._kbMoCiz();
    });
  }
  ['input', 'change'].forEach(function(o){ document.addEventListener(o, function(e){ if(e.target.matches && e.target.matches('[data-mo]')) moUygula(e.target); }); });
  setTimeout(function(){ document.querySelectorAll('[data-mo]').forEach(function(el){ if(el.type !== 'radio' || el.checked) moUygula(el); }); }, 0);
})();
