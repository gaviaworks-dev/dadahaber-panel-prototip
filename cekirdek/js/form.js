/* =====================================================================
   ÇEKİRDEK · FORM BİLEŞENLERİ DAVRANIŞI (düzenleme ekranlarının hepsinde aynı)
   - kb-tarih: tarih-saat seçici (tarayıcının tarih alanı asla kullanılmaz)
   - kb-cip-girdi: havuzdan aranan, yoksa aynı yerden eklenen çip girişi
   - [data-form]: kaydedilmemiş değişiklik, zorunlu alan doğrulaması, kaydedildi durumu
   - kb-zengin: zengin metin araç çubuğu (geçici; editör seçimi sorulacak)
   - [data-segment]: önizleme anahtarı · [data-ac]: seçime göre alan aç/kapat
   - kb-sosyal: platform sekmeleri, sayaçlar, oran, canlı kart
   ===================================================================== */
(function(){
  /* ---------------- yeni kayıt hali (?yeni=1): aynı ekran boş açılır ---------------- */
  if(new URLSearchParams(location.search).get('yeni') === '1'){
    document.querySelectorAll('[data-yeni-metin]').forEach(function(el){ el.textContent = el.getAttribute('data-yeni-metin'); });
    document.querySelectorAll('[data-yeni-gizle]').forEach(function(el){ el.hidden = true; });
    document.querySelectorAll('[data-yeni-goster]').forEach(function(el){ el.hidden = false; });
    document.querySelectorAll('[data-yeni-durum]').forEach(function(el){ el.setAttribute('data-state', el.getAttribute('data-yeni-durum')); });
    document.querySelectorAll('[data-yeni-bildir]').forEach(function(el){ el.setAttribute('data-bildir', el.getAttribute('data-yeni-bildir')); el.setAttribute('data-kaydet-metin', 'Yayımlandı'); });
    document.querySelectorAll('[data-form] .finput,[data-form] .ftext,[data-form] .km-satir input').forEach(function(el){ el.value = ''; });
    document.querySelectorAll('[data-form] .kz-alan').forEach(function(el){ el.innerHTML = '<p></p>'; });
    document.querySelectorAll('[data-form] .kb-cip').forEach(function(el){ el.remove(); });
    document.querySelectorAll('[data-form] [data-alan]:not(input):not(textarea):not(.kb-secim)').forEach(function(el){ el.textContent = ''; });
    document.querySelectorAll('.kb-secim[data-zorunlu]').forEach(function(sc){ sc.dataset.deger = ''; sc.classList.remove('is-dolu'); var l = sc.querySelector('.ks-deger'); if(l) l.textContent = sc.dataset.bos || ''; sc.querySelectorAll('.is-sec').forEach(function(x){ x.classList.remove('is-sec'); }); });
    var dur = document.querySelector('.side-card .kb-secim'); if(dur){ dur.dataset.deger = 'taslak'; var dl = dur.querySelector('.ks-deger'); if(dl) dl.textContent = 'Taslak'; }
    document.querySelectorAll('.kb-tarih-sec[data-yeni-bos]').forEach(function(k){ k.dataset.deger = ''; });
    document.querySelectorAll('.kb-kaydet .kk-durum i').forEach(function(i){ i.className = 'fa-solid fa-circle-dot'; });
    document.title = 'Yeni haber · ' + document.title.split(' · ').slice(1).join(' · ');
  }
  var tr = function(s){ return (s || '').toLocaleLowerCase('tr'); };
  var AYLAR = ['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık'];
  var iki = function(n){ return (n < 10 ? '0' : '') + n; };

  /* ---------------- tarih-saat seçici ---------------- */
  document.querySelectorAll('.kb-tarih-sec').forEach(function(kt){
    var btn = kt.querySelector('.kb-tarih-btn'), menu = kt.querySelector('.kb-tarih-menu'), yazi = kt.querySelector('.kt-deger');
    if(!btn || !menu || !yazi) return;
    var d = (kt.dataset.deger || '').match(/(\d{4})-(\d{2})-(\d{2})\s+(\d{2})\.(\d{2})/);
    var sec = d ? { y:+d[1], a:+d[2] - 1, g:+d[3], s:d[4] + '.' + d[5] } : null;
    var bugun = { y:2026, a:10, g:23 };
    var gor = sec ? { y:sec.y, a:sec.a } : { y:bugun.y, a:bugun.a };
    var enAz = kt.dataset.enaz === 'bugun';
    function yaz(){
      if(!sec){ yazi.innerHTML = '<span class="kt-bos">' + (kt.dataset.bos || 'Tarih ve saat seçin') + '</span>'; return; }
      yazi.textContent = iki(sec.g) + '.' + iki(sec.a + 1) + '.' + sec.y + ' ' + sec.s;
    }
    function ciz(){
      var ilk = new Date(gor.y, gor.a, 1), bas = (ilk.getDay() + 6) % 7, gun = new Date(gor.y, gor.a + 1, 0).getDate();
      var h = '<div class="kt-ay"><button type="button" data-kt="geri" aria-label="Önceki ay"><i class="fa-solid fa-chevron-left" aria-hidden="true"></i></button><b>' + AYLAR[gor.a] + ' ' + gor.y + '</b><button type="button" data-kt="ileri" aria-label="Sonraki ay"><i class="fa-solid fa-chevron-right" aria-hidden="true"></i></button></div><div class="kt-gunler">';
      ['Pt','Sa','Ça','Pe','Cu','Ct','Pz'].forEach(function(x){ h += '<span class="kt-bas">' + x + '</span>'; });
      for(var i = 0; i < bas; i++) h += '<span></span>';
      for(var g = 1; g <= gun; g++){
        var ge = enAz && (gor.y < bugun.y || (gor.y === bugun.y && (gor.a < bugun.a || (gor.a === bugun.a && g < bugun.g))));
        var c = (gor.y === bugun.y && gor.a === bugun.a && g === bugun.g ? ' is-bugun' : '') + (sec && sec.y === gor.y && sec.a === gor.a && sec.g === g ? ' is-sec' : '');
        h += '<button type="button" class="' + c.trim() + '" data-gun="' + g + '"' + (ge ? ' disabled' : '') + '>' + g + '</button>';
      }
      h += '</div><div class="kt-saat"><label for="' + kt.id + 'S">Saat</label><input id="' + kt.id + 'S" inputmode="numeric" maxlength="5" value="' + (sec ? sec.s : '16.05') + '" aria-label="Saat (ss.dd)">'
        + '<div class="kt-hizli"><button type="button" data-hizli="simdi">Şimdi</button><button type="button" data-hizli="1s">+1 sa</button></div></div>'
        + '<div class="kt-alt">' + (kt.dataset.temizlenir ? '<button type="button" class="btn btn-ghost btn-sm" data-kt="temizle">Temizle</button>' : '') + '<button type="button" class="btn btn-acc btn-sm" data-kt="tamam">Uygula</button></div>';
      menu.innerHTML = h;
    }
    btn.addEventListener('click', function(){ setTimeout(function(){ if(menu.classList.contains('open')) ciz(); }, 0); });
    menu.addEventListener('click', function(e){
      e.stopPropagation();
      var b = e.target.closest('button'); if(!b) return;
      var saat = menu.querySelector('.kt-saat input');
      if(b.dataset.kt === 'geri'){ gor.a--; if(gor.a < 0){ gor.a = 11; gor.y--; } ciz(); }
      else if(b.dataset.kt === 'ileri'){ gor.a++; if(gor.a > 11){ gor.a = 0; gor.y++; } ciz(); }
      else if(b.dataset.gun){ var s = saat.value; sec = { y:gor.y, a:gor.a, g:+b.dataset.gun, s:s }; ciz(); }
      else if(b.dataset.hizli){ sec = { y:2026, a:10, g:23, s:b.dataset.hizli === 'simdi' ? '16.05' : '17.05' }; gor = { y:2026, a:10 }; ciz(); }
      else if(b.dataset.kt === 'temizle'){ sec = null; yaz(); btn.click(); kt.dispatchEvent(new Event('input', {bubbles:true})); }
      else if(b.dataset.kt === 'tamam'){
        var v = saat.value.replace(':', '.'); var m = v.match(/^([01]?\d|2[0-3])\.([0-5]\d)$/);
        if(!m){ saat.focus(); saat.style.borderColor = 'var(--danger)'; return; }
        if(!sec) sec = { y:bugun.y, a:bugun.a, g:bugun.g, s:'' };
        sec.s = iki(+m[1]) + '.' + m[2]; yaz(); btn.click(); kt.dispatchEvent(new Event('input', {bubbles:true}));
      }
    });
    yaz();
  });

  /* ---------------- çip girişi ---------------- */
  document.querySelectorAll('.kb-cip-girdi').forEach(function(cg){
    var inp = cg.querySelector('input'), oneri = cg.querySelector('.kb-cip-oneri');
    var havuz = []; try{ havuz = JSON.parse(cg.dataset.havuz || '[]'); }catch(e){}
    function mevcut(){ return Array.prototype.map.call(cg.querySelectorAll('.kb-cip'), function(c){ return c.dataset.deger; }); }
    function ekle(v){
      v = v.trim(); if(!v || mevcut().indexOf(v) > -1) return;
      var c = document.createElement('span'); c.className = 'kb-cip'; c.dataset.deger = v;
      c.innerHTML = '<span></span><button type="button" aria-label="Kaldır"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button>';
      c.firstChild.textContent = v; cg.insertBefore(c, inp); inp.value = ''; goster(); cg.dispatchEvent(new Event('input', {bubbles:true}));
    }
    function goster(){
      var v = inp.value.trim(); if(!oneri) return;
      if(!v){ oneri.classList.remove('open'); return; }
      var var_ = mevcut(), h = '';
      havuz.filter(function(x){ return var_.indexOf(x) === -1 && tr(x).indexOf(tr(v)) > -1; }).slice(0, 6).forEach(function(x){ h += '<button type="button" data-ekle="' + x.replace(/"/g, '&quot;') + '"><i class="fa-solid fa-tag" aria-hidden="true"></i>' + x.replace(/</g, '&lt;') + '</button>'; });
      if(havuz.map(tr).indexOf(tr(v)) === -1) h += '<button type="button" class="kb-ekle" data-ekle="' + v.replace(/"/g, '&quot;') + '"><i class="fa-solid fa-plus" aria-hidden="true"></i>Havuza ekle: “' + v.replace(/</g, '&lt;') + '”</button>';
      oneri.innerHTML = h; oneri.classList.add('open');
    }
    cg.addEventListener('click', function(e){
      var x = e.target.closest('.kb-cip button'); if(x){ x.closest('.kb-cip').remove(); cg.dispatchEvent(new Event('input', {bubbles:true})); return; }
      var o = e.target.closest('[data-ekle]'); if(o){ e.stopPropagation(); ekle(o.dataset.ekle); inp.focus(); return; }
      inp.focus();
    });
    inp.addEventListener('input', function(e){ e.stopPropagation(); goster(); });
    inp.addEventListener('keydown', function(e){
      if(e.key === 'Enter' || e.key === ','){ e.preventDefault(); var ilk = oneri && oneri.querySelector('[data-ekle]'); ekle(ilk && !ilk.classList.contains('kb-ekle') ? ilk.dataset.ekle : inp.value); }
      if(e.key === 'Backspace' && !inp.value){ var s = cg.querySelectorAll('.kb-cip'); if(s.length) s[s.length - 1].remove(); }
      if(e.key === 'Escape' && oneri) oneri.classList.remove('open');
    });
    inp.addEventListener('blur', function(){ setTimeout(function(){ if(oneri) oneri.classList.remove('open'); }, 150); });
  });

  /* ---------------- form: değişiklik, doğrulama, kaydet ---------------- */
  document.querySelectorAll('[data-form]').forEach(function(F){
    var cubuk = document.querySelector('.kb-kaydet[data-form-icin="' + F.id + '"]');
    var durum = cubuk && cubuk.querySelector('.kk-durum span');
    var kirli = false;
    function kirlet(){ if(kirli) return; kirli = true; if(cubuk){ cubuk.classList.add('is-kirli'); cubuk.querySelector('.kk-durum i').className = 'fa-solid fa-circle-dot'; } if(durum) durum.textContent = 'Kaydedilmemiş değişiklikler var'; }
    F.addEventListener('input', function(e){ if(e.isTrusted || e.target.closest('.kb-tarih-sec,.kb-cip-girdi')) kirlet(); });
    F.addEventListener('kb-secim', kirlet);
    window.addEventListener('beforeunload', function(e){ if(kirli){ e.preventDefault(); e.returnValue = ''; } });
    function dogrula(){
      var hata = 0;
      F.querySelectorAll('.sa-form-tab').forEach(function(s){ s.classList.remove('has-error'); });
      F.querySelectorAll('[data-zorunlu]').forEach(function(el){
        var row = el.closest('.frow'), bos = el.matches('input,textarea') ? !el.value.trim() : el.matches('.kb-secim') ? !el.dataset.deger : !el.textContent.trim();
        if(row) row.classList.toggle('has-error', bos);
        if(bos){ hata++; var p = el.closest('.sa-form-panel'); if(p){ var s = F.querySelector('.sa-form-tab[data-panel="' + p.id + '"]'); if(s) s.classList.add('has-error'); } }
      });
      return hata;
    }
    if(cubuk) cubuk.querySelectorAll('[data-kaydet]').forEach(function(b){
      b.addEventListener('click', function(){
        var h = dogrula();
        if(h){ window.kbBildir(h + ' zorunlu alan boş; işaretli sekmelere bakın'); var ilk = F.querySelector('.frow.has-error'); var p = ilk && ilk.closest('.sa-form-panel'); if(p && p.hidden){ var s = F.querySelector('.sa-form-tab[data-panel="' + p.id + '"]'); if(s) s.click(); } if(ilk) ilk.scrollIntoView({block:'center', behavior:'smooth'}); return; }
        kirli = false; cubuk.classList.remove('is-kirli'); cubuk.querySelector('.kk-durum i').className = 'fa-solid fa-circle-check';
        if(durum) durum.textContent = (b.dataset.kaydetMetin || 'Kaydedildi') + ' · 23.11.2026 16.05 · ' + (document.getElementById('pmName') ? document.getElementById('pmName').textContent : '');
        window.kbBildir(b.dataset.bildir || 'Değişiklikler kaydedildi; önceki hal sürüm geçmişinde');
      });
    });
    F.addEventListener('input', function(e){ var r = e.target.closest && e.target.closest('.frow.has-error'); if(r) r.classList.remove('has-error'); });
  });

  /* ---------------- zengin metin araç çubuğu (geçici) ---------------- */
  document.querySelectorAll('.kb-zengin').forEach(function(z){
    var alan = z.querySelector('.kz-alan'), say = z.querySelector('[data-kz-say]');
    function sayac(){ if(!say) return; var k = (alan.innerText.trim().match(/\S+/g) || []).length; say.textContent = k + ' kelime · yaklaşık ' + Math.max(1, Math.round(k / 200)) + ' dk okuma'; }
    z.querySelectorAll('[data-kz]').forEach(function(b){
      b.addEventListener('mousedown', function(e){ e.preventDefault(); });
      b.addEventListener('click', function(){
        var k = b.dataset.kz; alan.focus();
        if(k === 'h2' || k === 'p' || k === 'blockquote') document.execCommand('formatBlock', false, k);
        else if(k === 'link'){ var u = 'https://'; document.execCommand('createLink', false, u); }
        else document.execCommand(k, false, null);
        sayac(); z.dispatchEvent(new Event('input', {bubbles:true}));
      });
    });
    alan.addEventListener('input', sayac); sayac();
  });

  /* ---------------- önizleme anahtarı ve seçime bağlı alanlar ---------------- */
  document.querySelectorAll('[data-segment]').forEach(function(sg){
    sg.addEventListener('click', function(e){
      var b = e.target.closest('button[data-hedef]'); if(!b) return;
      sg.querySelectorAll('button[data-hedef]').forEach(function(x){ x.classList.toggle('is-on', x === b); x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); var h = document.getElementById(x.dataset.hedef); if(h) h.hidden = x !== b; });
    });
  });
  window.kbAcKapat = acKapat;
  function acKapat(){ document.querySelectorAll('input[data-ac]').forEach(function(i){ var h = document.getElementById(i.dataset.ac); if(h) h.hidden = !i.checked; }); }
  document.addEventListener('change', function(e){ if(e.target.matches && e.target.matches('input[type=radio],input[type=checkbox]')) acKapat(); });
  acKapat();
  if(window.kbSayaclar) window.kbSayaclar();

  /* ---------------- medya seçici ve görsel yükleme ----------------
     Kap: [data-gorsel-alan]; hedef: [data-gorsel-hedef="web|mobil|…"] (background-image);
     [data-gorsel-kapsam="mobil"] düğmesi yalnızca o hedefi değiştirir; [data-gorsel-bilgi] metni güncellenir;
     [data-gorsel-bos]/[data-gorsel-dolu] boş ve dolu hali değişir. */
  var P = window.PANEL || {}, M = P.medya || {};
  var kokUrl = (function(){ var s = document.querySelector('script[src*="kayit.js"]'); return s ? new URL('../../', s.src).href : ''; })();
  function uygula(btn, url, kucuk, bilgi){
    var alan = btn.closest('[data-gorsel-alan]') || btn.closest('.kb-kap-govde') || document;
    var kap = btn.getAttribute('data-gorsel-kapsam');
    alan.querySelectorAll(kap ? '[data-gorsel-hedef="' + kap + '"]' : '[data-gorsel-hedef]').forEach(function(h){
      h.style.backgroundImage = 'url("' + (h.hasAttribute('data-gorsel-kucuk') && kucuk ? kucuk : url) + '")';
    });
    alan.querySelectorAll('[data-gorsel-bilgi]').forEach(function(b){ b.textContent = bilgi; });
    alan.querySelectorAll('[data-gorsel-bos]').forEach(function(x){ x.hidden = true; });
    alan.querySelectorAll('[data-gorsel-dolu]').forEach(function(x){ x.hidden = false; });
    var oto = alan.querySelector('.kg-oto');
    if(oto) oto.innerHTML = kap === 'mobil' ? '<i class="fa-solid fa-image" aria-hidden="true"></i> Ayrı görsel' : '<i class="fa-solid fa-wand-magic-sparkles" aria-hidden="true"></i> Webden kırpıldı';
    btn.dispatchEvent(new Event('input', {bubbles:true}));
  }
  var gizliDosya = document.createElement('input'); gizliDosya.type = 'file'; gizliDosya.accept = 'image/jpeg,image/png,image/webp'; gizliDosya.hidden = true;
  document.body.appendChild(gizliDosya);
  var yukleBtn = null;
  gizliDosya.addEventListener('change', function(){
    var f = gizliDosya.files && gizliDosya.files[0]; if(!f || !yukleBtn) return;
    var r = new FileReader();
    r.onload = function(){
      var img = new Image();
      img.onload = function(){
        var kb = Math.round(f.size / 1024);
        uygula(yukleBtn, r.result, null, 'Yüklendi: ' + f.name + ' · ' + img.naturalWidth + '×' + img.naturalHeight + ' · ' + kb + ' KB');
        window.kbBildir(img.naturalWidth < 1280 ? 'Görsel yüklendi; önerilen 1280 px genişliğin altında' : 'Görsel yüklendi');
        medyaKapat();
      };
      img.src = r.result;
    };
    r.readAsDataURL(f); gizliDosya.value = '';
  });
  var mOv = null, mBtn = null, mSec = null;
  function medyaKur(){
    mOv = document.createElement('div'); mOv.className = 'kb-medya-ov';
    var liste = (M.gorseller || []).map(function(g){
      return '<button type="button" class="kb-medya-oge" data-dosya="' + g.dosya + '" data-ad="' + g.ad + '"><span class="km-resim" style="background-image:url(' + kokUrl + M.kucuk + g.dosya + ')"></span><b>' + g.ad + '</b><small>' + g.olcu + ' · ' + g.kaynak + '</small></button>';
    }).join('');
    mOv.innerHTML = '<div class="kb-medya" role="dialog" aria-modal="true" aria-labelledby="kbMedyaBas"><div class="kb-kap-bas"><div><h2 id="kbMedyaBas">Medya havuzu</h2><div class="kb-kap-alt">' + (M.gorseller || []).length + ' görsel · Stok havuzu</div></div><button type="button" class="kb-kapat" data-medya-kapat aria-label="Kapat"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button></div>'
      + '<div class="kb-medya-arac"><div class="fb-search"><i class="fa-solid fa-magnifying-glass" aria-hidden="true"></i><input type="search" placeholder="Görsel ara" aria-label="Görsel ara"></div><button type="button" class="btn btn-ghost btn-sm" data-medya-dosya><i class="fa-solid fa-upload" aria-hidden="true"></i>Bilgisayardan yükle</button></div>'
      + '<div class="kb-medya-izgara">' + liste + '</div>'
      + '<div class="kb-kap-alt-cubuk"><span class="kb-sol kb-medya-secili">Bir görsel seçin</span><button type="button" class="btn btn-acc btn-sm" data-medya-tamam disabled><i class="fa-solid fa-check" aria-hidden="true"></i>Seç</button></div></div>';
    document.body.appendChild(mOv);
    mOv.addEventListener('click', function(e){
      if(e.target === mOv || e.target.closest('[data-medya-kapat]')){ medyaKapat(); return; }
      if(e.target.closest('[data-medya-dosya]')){ yukleBtn = mBtn; gizliDosya.click(); return; }
      var o = e.target.closest('.kb-medya-oge');
      if(o){ mSec = o; mOv.querySelectorAll('.kb-medya-oge').forEach(function(x){ x.classList.toggle('is-sec', x === o); }); mOv.querySelector('[data-medya-tamam]').disabled = false; mOv.querySelector('.kb-medya-secili').textContent = o.dataset.ad + ' seçildi'; return; }
      if(e.target.closest('[data-medya-tamam]') && mSec){
        uygula(mBtn, kokUrl + M.kok + mSec.dataset.dosya, kokUrl + M.kucuk + mSec.dataset.dosya, 'Havuzdan: ' + mSec.dataset.ad + ' · 1200×800 · Unsplash lisanslı');
        window.kbBildir('Görsel değiştirildi'); medyaKapat();
      }
    });
    mOv.querySelector('input[type=search]').addEventListener('input', function(e){ var v = tr(e.target.value); mOv.querySelectorAll('.kb-medya-oge').forEach(function(x){ x.hidden = v && tr(x.dataset.ad).indexOf(v) === -1; }); });
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && mOv.classList.contains('open')){ e.stopImmediatePropagation(); medyaKapat(); } }, true);
  }
  function medyaKapat(){ if(mOv){ mOv.classList.remove('open'); if(mBtn && mBtn.focus) mBtn.focus(); } }
  document.addEventListener('click', function(e){
    var b = e.target.closest('[data-medya-sec]');
    if(b){ e.preventDefault(); if(!mOv) medyaKur(); mBtn = b; mSec = null; mOv.querySelectorAll('.is-sec').forEach(function(x){ x.classList.remove('is-sec'); }); mOv.querySelector('[data-medya-tamam]').disabled = true; mOv.querySelector('.kb-medya-secili').textContent = 'Bir görsel seçin'; mOv.classList.add('open'); var s = mOv.querySelector('input[type=search]'); s.value = ''; s.dispatchEvent(new Event('input')); s.focus(); return; }
    var y = e.target.closest('[data-gorsel-yukle]');
    if(y){ e.preventDefault(); yukleBtn = y; gizliDosya.click(); }
  });

  /* ---------------- henüz kurulmayan pencereler: dürüst bildirim ---------------- */
  var NOT = { kirp:'Kırpma penceresi (odak noktası, oranlar, canlı önizleme) sıradaki adımda', medya:'Medya seçici sıradaki adımda', surum:'Sürüm geçmişi ve düzeltmeler penceresi sıradaki adımda' };
  document.addEventListener('click', function(e){
    var b = e.target.closest('[data-bildir-kirp],[data-bildir-medya],[data-bildir-surum]'); if(!b || b.hasAttribute('data-medya-sec') || b.hasAttribute('data-gorsel-yukle')) return;
    window.kbBildir(NOT[b.hasAttribute('data-bildir-kirp') ? 'kirp' : b.hasAttribute('data-bildir-medya') ? 'medya' : 'surum']);
  });
  /* SEO: başlıktan yeniden üret */
  document.querySelectorAll('[data-seo-uret]').forEach(function(b){
    b.addEventListener('click', function(){
      var F = b.closest('[data-form]') || document, bas = F.querySelector('[data-alan="baslik"]'), spot = F.querySelector('[data-alan="spot"]');
      var sb = F.querySelector('#sBaslik'), sa = F.querySelector('#sAciklama'), sl = F.querySelector('#sSlug');
      if(bas && sb){ var x = bas.value; sb.value = (x.length > 46 ? x.slice(0, 46).replace(/\s+\S*$/, '') : x) + ' | Dada Haber'; sb.dispatchEvent(new Event('input', {bubbles:true})); }
      if(spot && sa){ var s = spot.value; sa.value = s.length > 155 ? s.slice(0, 152).replace(/\s+\S*$/, '') + '…' : s; sa.dispatchEvent(new Event('input', {bubbles:true})); }
      if(bas && sl && window.kbSlug){ sl.value = window.kbSlug(bas.value); sl.dispatchEvent(new Event('input', {bubbles:true})); }
      window.kbBildir('SEO alanları başlık ve spottan yeniden üretildi');
    });
  });

  /* ---------------- sosyal medya sekmesi ---------------- */
  document.querySelectorAll('.kb-sosyal').forEach(function(S){
    var metin = S.querySelector('[data-sosyal-metin]'), kart = S.querySelector('.kb-sosyal-kart');
    var kartMetin = S.querySelector('.ksk-metin'), oranKap = S.querySelector('.kb-oranlar'), kirp = S.querySelector('.kk-cerceve'), kGor = S.querySelector('.ksk-gorsel');
    var sayaclar = S.querySelector('.kb-sayaclar'), hesap = S.querySelector('[data-sosyal-hesap]');
    var veri = {}, aktif = null;
    S.querySelectorAll('.kb-platform').forEach(function(p){ veri[p.dataset.platform] = { metin: p.dataset.metin || '' }; });
    function oran(o){
      var a = o === 'serbest' ? 'auto' : o.replace(':', '/');
      if(kirp) kirp.style.aspectRatio = o === 'serbest' ? '3/2' : a;
      if(kGor) kGor.style.aspectRatio = o === 'serbest' ? '3/2' : a;
    }
    function yaz(){
      var v = metin.value, link = (v.match(/https?:\/\/\S+/g) || []).length, et = (v.match(/#[\wçğıöşüÇĞİÖŞÜ]+/g) || []).length;
      var emoji = (v.match(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/gu) || []).length;
      var p = S.querySelector('.kb-platform.is-on'), sinir = +(p.dataset.sinir || 0), linkUz = +(p.dataset.linkUzunluk || 0);
      var n = v.replace(/https?:\/\/\S+/g, function(u){ return linkUz ? new Array(linkUz + 1).join('x') : u; }).length;
      var cm = S.querySelector('.kb-sosyal-say'); if(cm){ cm.querySelector('b').textContent = n + ' / ' + sinir; cm.classList.toggle('over', n > sinir); }
      var cb = S.querySelector('.kb-cubuk'); if(cb){ cb.querySelector('span').style.width = Math.min(100, n / sinir * 100) + '%'; cb.classList.toggle('warn', n > sinir * .9 && n <= sinir); cb.classList.toggle('over', n > sinir); }
      if(sayaclar) sayaclar.innerHTML = '<span>Bağlantı <b>' + link + '</b>' + (linkUz ? ' (' + linkUz + ' karakter sayılır)' : '') + '</span><span>Etiket <b>' + et + '</b></span><span>Emoji <b>' + emoji + '</b></span><span>Kalan <b>' + (sinir - n) + '</b></span>';
      if(kartMetin){ var guv = v.replace(/&/g, '&amp;').replace(/</g, '&lt;'); kartMetin.innerHTML = guv.replace(/(https?:\/\/\S+)/g, '<span class="ksk-link">$1</span>').replace(/(#[\wçğıöşüÇĞİÖŞÜ]+)/g, '<span class="ksk-link">$1</span>'); }
      if(aktif) veri[aktif].metin = v;
    }
    function sec(p){
      aktif = p.dataset.platform;
      S.querySelectorAll('.kb-platform').forEach(function(x){ x.classList.toggle('is-on', x === p); x.setAttribute('aria-selected', x === p ? 'true' : 'false'); });
      metin.value = veri[aktif].metin;
      kart.className = 'kb-sosyal-kart p-' + aktif;
      S.querySelectorAll('[data-sosyal-ad]').forEach(function(el){ el.textContent = p.dataset.ad; });
      S.querySelectorAll('[data-sosyal-tutamac]').forEach(function(el){ el.textContent = p.dataset.tutamac; });
      if(hesap){ var d = p.dataset.hesapDurum; hesap.className = 'pstat ' + (d === 'hata' ? 'warm' : 'ok'); hesap.textContent = d === 'hata' ? 'Bağlantı süresi doldu' : 'Bağlı'; }
      var uy = S.querySelector('[data-sosyal-uyari]'); if(uy) uy.hidden = p.dataset.hesapDurum !== 'hata';
      var oranlar = (p.dataset.oranlar || '').split(','), h = '';
      oranlar.forEach(function(o, i){ var px = o.split('='); h += '<button type="button" class="kb-oran' + (i === 0 ? ' is-on' : '') + '" data-oran="' + px[0] + '">' + (px[0] === 'serbest' ? 'Serbest' : px[0]) + '<small>' + (px[1] || 'kendi ölçüsü') + '</small></button>'; });
      oranKap.innerHTML = h; oran(oranlar[0].split('=')[0]);
      var ol = S.querySelector('[data-oran-not]'); if(ol) ol.textContent = (oranlar[0].split('=')[1] || '') + ' önerilir';
      yaz();
    }
    S.addEventListener('click', function(e){
      var p = e.target.closest('.kb-platform'); if(p){ sec(p); return; }
      var o = e.target.closest('.kb-oran'); if(o){ oranKap.querySelectorAll('.kb-oran').forEach(function(x){ x.classList.toggle('is-on', x === o); }); oran(o.dataset.oran); var ol = S.querySelector('[data-oran-not]'); if(ol) ol.textContent = o.querySelector('small').textContent + ' önerilir'; }
      var u = e.target.closest('[data-sosyal-uret]'); if(u){ metin.value = S.querySelector('.kb-platform.is-on').dataset.metin; yaz(); window.kbBildir('Metin yeniden üretildi (AI · prototip)'); }
    });
    metin.addEventListener('input', yaz);
    sec(S.querySelector('.kb-platform.is-on') || S.querySelector('.kb-platform'));
  });
})();
