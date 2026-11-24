/* =====================================================================
   ÇEKİRDEK · ALAN VE ONAY BİLEŞENLERİ (bütün modüllerde aynı)
   - kb-kanallar     : yayın kanalları seçimi (Web · Uygulama · Sosyal Medya; Yasin Bey Y1)
   - kb-okuma-onay   : içerik sonuna kadar okununca etkinleşen onay düğmesi (Y2/Y3)
   - kbKod           : e-posta koduyla doğrulama penceresi (K15; hassas işlemler)
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
  document.querySelectorAll('.kb-kanallar').forEach(function(K){
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
  document.querySelectorAll('.kb-okuma-onay').forEach(function(O){
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
    function ciz(){
      if(!gecerli()){
        btn.disabled = false; O.classList.remove('is-bekliyor', 'is-okundu');
        neden.innerHTML = '';
        return;
      }
      var o = oran(); if(o >= .99) okundu = true;
      btn.disabled = !okundu;
      O.classList.toggle('is-bekliyor', !okundu); O.classList.toggle('is-okundu', okundu);
      O.style.setProperty('--ko', (okundu ? 100 : Math.round(o * 100)) + '%');
      neden.innerHTML = okundu
        ? '<i class="fa-solid fa-circle-check" aria-hidden="true"></i>İçerik sonuna kadar okundu'
        : '<i class="fa-solid fa-book-open-reader" aria-hidden="true"></i>Onaylamak için içeriği sonuna kadar okuyun <b>%' + Math.round(o * 100) + '</b>';
    }
    btn.setAttribute('aria-describedby', neden.id || (neden.id = 'ko' + Math.random().toString(36).slice(2, 7)));
    hedef.addEventListener('scroll', ciz, { passive:true });
    window.addEventListener('scroll', ciz, { passive:true });
    window.addEventListener('resize', ciz);
    document.addEventListener('kb-rol', function(){ okundu = false; ciz(); });
    ciz();
  });

  /* ---------------- e-posta kodu (K15) ---------------- */
  var kov = null, kodIs = null, kodOnce = null, sure = null;
  function kodKur(){
    kov = document.createElement('div'); kov.className = 'sa-modal-ov kb-kod-ov';
    kov.innerHTML = '<div class="sa-modal kb-kod" role="alertdialog" aria-modal="true" aria-labelledby="kbKodBas"><div class="sa-modal-ico"><i class="fa-solid fa-envelope-circle-check" aria-hidden="true"></i></div>'
      + '<h2 id="kbKodBas"></h2><p data-kod-metin></p>'
      + '<div class="kb-kod-kutular" role="group" aria-label="6 haneli kod">' + [0,1,2,3,4,5].map(function(i){ return '<input inputmode="numeric" maxlength="1" aria-label="' + (i + 1) + '. hane" autocomplete="one-time-code">'; }).join('') + '</div>'
      + '<div class="kb-kod-alt"><span data-kod-sure></span><button type="button" class="kb-bag" data-kod-yeniden disabled>Kodu yeniden gönder</button></div>'
      + '<div class="ferr kb-kod-hata" data-kod-hata><i class="fa-solid fa-circle-exclamation" aria-hidden="true"></i>Kod 6 rakam olmalı.</div>'
      + '<p class="fhint kb-kod-ipucu">Prototip: herhangi 6 rakam kabul edilir.</p>'
      + '<div class="sa-modal-acts"><button type="button" class="btn btn-ghost" data-kod-hayir>Vazgeç</button><button type="button" class="btn btn-acc" data-kod-evet>Doğrula</button></div></div>';
    document.body.appendChild(kov);
    var kutular = kov.querySelectorAll('.kb-kod-kutular input');
    kutular.forEach(function(k, i){
      k.addEventListener('input', function(){ k.value = k.value.replace(/\D/g, '').slice(-1); kov.querySelector('[data-kod-hata]').style.display = ''; if(k.value && kutular[i + 1]) kutular[i + 1].focus(); });
      k.addEventListener('keydown', function(e){ if(e.key === 'Backspace' && !k.value && kutular[i - 1]) kutular[i - 1].focus(); if(e.key === 'Enter') kov.querySelector('[data-kod-evet]').click(); });
      k.addEventListener('paste', function(e){ var v = (e.clipboardData.getData('text') || '').replace(/\D/g, '').slice(0, 6); if(!v) return; e.preventDefault(); v.split('').forEach(function(c, j){ if(kutular[j]) kutular[j].value = c; }); kutular[Math.min(5, v.length)].focus(); });
    });
    kov.addEventListener('click', function(e){
      if(e.target === kov || e.target.closest('[data-kod-hayir]')){ kodKapat(); return; }
      if(e.target.closest('[data-kod-yeniden]')){ sayac(); window.kbBildir('Yeni kod e-postanıza gönderildi'); return; }
      if(e.target.closest('[data-kod-evet]')){
        var v = Array.prototype.map.call(kutular, function(k){ return k.value; }).join('');
        if(v.length < 6){ kov.querySelector('[data-kod-hata]').style.display = 'flex'; return; }
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
    kov.querySelectorAll('.kb-kod-kutular input').forEach(function(k){ k.value = ''; });
    kodIs = o.evetIs; kodOnce = document.activeElement;
    kov.classList.add('open'); sayac();
    setTimeout(function(){ kov.querySelector('.kb-kod-kutular input').focus(); }, 60);
  };

  /* ---------------- AI ile üret adımı ----------------
     [data-ai-adim data-ai-kaynak="#a,#b"]: kaynak alanlar doluysa işaretli [data-ai-grup] bölümleri üretilir.
     Üretilen bölüm "AI önerisi" etiketi alır; etiket bölümde bir değişiklik yapılınca "gözden geçirildi"ye döner. */
  document.querySelectorAll('[data-ai-adim]').forEach(function(A){
    var kaynak = (A.getAttribute('data-ai-kaynak') || '').split(',').map(function(s){ return document.querySelector(s.trim()); }).filter(Boolean);
    var btn = A.querySelector('[data-ai-uret]'), neden = A.querySelector('[data-ai-neden]'), durumEl = A.querySelector('[data-ai-durum]');
    function hazir(){ return kaynak.every(function(k){ return k.value.trim().length > 0; }); }
    function bak(){ if(A.classList.contains('is-bitti')) return; var h = hazir(); btn.disabled = !h || !A.querySelector('.kaa-secim input:checked'); neden.textContent = h ? 'Başlık ve spot hazır' : 'Önce başlık ve spot'; }
    kaynak.forEach(function(k){ k.addEventListener('input', bak); });
    A.querySelector('.kaa-secim').addEventListener('change', bak); bak();
    function doldur(g){
      g.querySelectorAll('[data-ai-ornek]').forEach(function(el){
        if(el.classList.contains('kz-alan')) el.innerHTML = el.dataset.aiOrnek;
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

  /* ---------------- maskeli gizli değer ----------------
     Değer hiçbir zaman açık gösterilmez; "Yenile" e-posta koduyla yeni değer üretir ve yalnızca o an bir kez gösterir. */
  document.querySelectorAll('.kb-maske').forEach(function(M){
    M.addEventListener('click', function(e){
      var b = e.target.closest('[data-maske-yenile],[data-maske-kopyala],[data-maske-gizle]'); if(!b) return;
      if(b.hasAttribute('data-maske-kopyala')){
        var v = M.querySelector('.km-acik code').textContent;
        if(navigator.clipboard) navigator.clipboard.writeText(v).catch(function(){});
        window.kbBildir('Kopyalandı; bu değer bir daha gösterilmeyecek'); return;
      }
      if(b.hasAttribute('data-maske-gizle')){ M.classList.remove('is-acik'); M.querySelector('.km-acik').hidden = true; return; }
      window.kbOnay({ ikon:'fa-rotate', baslik: (M.dataset.ad || 'Değer') + ' yenilensin mi?', metin: M.dataset.yenileMetin || 'Eski değer hemen geçersiz olur; onu kullanan yerler yeni değerle güncellenmelidir. İşlem e-posta koduyla doğrulanır ve denetim izine yazılır.', evet:'Yenile',
        evetIs: function(){ window.kbKod({ baslik:'Yenilemeyi doğrulayın', evet:'Doğrula ve yenile', evetIs: function(){
          var harf = 'abcdefghjkmnpqrstuvwxyz23456789', v = (M.dataset.onEk || '');
          for(var i = 0; i < 24; i++) v += harf.charAt(Math.floor(Math.random() * harf.length));
          M.querySelector('.km-deger').textContent = '•'.repeat(16) + v.slice(-4);
          M.querySelector('.km-acik code').textContent = v;
          M.querySelector('.km-acik').hidden = false; M.classList.add('is-acik');
          var m = M.querySelector('.km-meta'); if(m) m.textContent = 'Yenilendi · 24.11.2026 16.05 · ' + ad();
          window.kbBildir((M.dataset.ad || 'Değer') + ' yenilendi; denetim izine yazıldı');
        } }); } });
    });
  });

  /* ---------------- telefon (ülke kodu + maske) ---------------- */
  var MASKE = { '90':'### ### ## ##', '49':'#### #######', '44':'#### ######', '1':'### ### ####', '994':'## ### ## ##' };
  document.querySelectorAll('.kb-tel').forEach(function(T){
    var giris = T.querySelector('input'), ulke = T.querySelector('.kb-secim'), row = T.closest('.frow');
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
  document.querySelectorAll('input[data-eposta]').forEach(function(i){
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
  document.querySelectorAll('[data-siralanir]').forEach(function(L){
    var tasinan = null;
    function bitti(){ L.dispatchEvent(new Event('input', { bubbles:true })); }
    L.querySelectorAll('[data-sira]').forEach(function(s){
      var t = s.querySelector('.kb-tutamac'); if(!t) return;
      t.addEventListener('pointerdown', function(){ s.draggable = true; });
      s.addEventListener('dragstart', function(e){ tasinan = s; s.classList.add('is-tasiniyor'); e.dataTransfer.effectAllowed = 'move'; try{ e.dataTransfer.setData('text/plain', ''); }catch(x){} });
      s.addEventListener('dragend', function(){ s.classList.remove('is-tasiniyor'); s.draggable = false; tasinan = null; bitti(); });
      t.addEventListener('keydown', function(e){
        if(e.key === 'ArrowUp' && s.previousElementSibling){ e.preventDefault(); L.insertBefore(s, s.previousElementSibling); t.focus(); bitti(); }
        if(e.key === 'ArrowDown' && s.nextElementSibling){ e.preventDefault(); L.insertBefore(s.nextElementSibling, s); t.focus(); bitti(); }
      });
    });
    L.addEventListener('dragover', function(e){
      if(!tasinan) return; e.preventDefault();
      var alt = Array.prototype.filter.call(L.querySelectorAll('[data-sira]'), function(x){ return x !== tasinan; })
        .filter(function(x){ var r = x.getBoundingClientRect(); return e.clientY < r.top + r.height / 2; })[0];
      if(alt) L.insertBefore(tasinan, alt); else L.appendChild(tasinan);
    });
  });

  /* ---------------- özellik anahtarı ----------------
     <label class="toggle"><input type="checkbox" data-anahtar="Yorumlar" data-anahtar-etki="haber detayı, canlı anlatım"></label>
     Değişiklik önce/sonra onayıyla uygulanır, hemen yayına yansır, geri alınabilir ve denetim izine yazılır. */
  document.querySelectorAll('input[data-anahtar]').forEach(function(i){
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
})();
