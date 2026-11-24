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
    /* AI adımı: [data-ai-grup] içindeki örnek değerler saklanır; "Gerisini AI ile üret" bunları geri yazar */
    document.querySelectorAll('[data-ai-grup] .finput,[data-ai-grup] .ftext,[data-ai-grup] .km-satir input').forEach(function(el){ el.dataset.aiOrnek = el.value; });
    document.querySelectorAll('[data-ai-grup] .kz-alan').forEach(function(el){ el.dataset.aiOrnek = el.innerHTML; });
    document.querySelectorAll('[data-ai-grup] .kb-cip-girdi').forEach(function(el){ el.dataset.aiCip = Array.prototype.map.call(el.querySelectorAll('.kb-cip'), function(c){ return c.outerHTML; }).join(''); });
    document.querySelectorAll('[data-ai-grup] .kb-secim[data-zorunlu]').forEach(function(sc){ sc.dataset.aiOrnek = sc.dataset.deger || ''; });
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
  var GUNLER = ['Pazar','Pazartesi','Salı','Çarşamba','Perşembe','Cuma','Cumartesi'];
  document.querySelectorAll('.kb-tarih-sec').forEach(function(kt){
    var btn = kt.querySelector('.kb-tarih-btn'), menu = kt.querySelector('.kb-tarih-menu'), yazi = kt.querySelector('.kt-deger');
    if(!btn || !menu || !yazi) return;
    document.body.appendChild(menu);  /* kökte açılır: hiçbir kapsayıcı konumunu ya da kırpmasını bozmaz */
    var d = (kt.dataset.deger || '').match(/(\d{4})-(\d{2})-(\d{2})\s+(\d{2})\.(\d{2})/);
    var sec = d ? { y:+d[1], a:+d[2] - 1, g:+d[3], h:+d[4], m:+d[5] } : null;
    var bugun = { y:2026, a:10, g:23, h:16, m:5 };
    var tas = null, gor = null;
    var enAz = kt.dataset.enaz === 'bugun';
    function metin(s){ return iki(s.g) + '.' + iki(s.a + 1) + '.' + s.y + ' ' + iki(s.h) + '.' + iki(s.m); }
    function ozet(s){ var gn = GUNLER[new Date(s.y, s.a, s.g).getDay()]; return gn + ', ' + s.g + ' ' + AYLAR[s.a] + ' · ' + iki(s.h) + '.' + iki(s.m); }
    function yaz(){ if(!sec){ yazi.innerHTML = '<span class="kt-bos">' + (kt.dataset.bos || 'Tarih ve saat seçin') + '</span>'; return; } yazi.textContent = metin(sec); }
    function gecmis(y, a, g){ return enAz && (y < bugun.y || (y === bugun.y && (a < bugun.a || (a === bugun.a && g < bugun.g)))); }
    function ciz(){
      var ilk = new Date(gor.y, gor.a, 1), bas = (ilk.getDay() + 6) % 7, gun = new Date(gor.y, gor.a + 1, 0).getDate();
      var h = '<div class="kt-hizli-ust" role="group" aria-label="Hızlı seçim"><button type="button" data-hizli="0,16,5">Şimdi</button><button type="button" data-hizli="0,19,0">Bu akşam 19.00</button><button type="button" data-hizli="1,8,0">Yarın 08.00</button><button type="button" data-hizli="1,12,0">Yarın 12.00</button></div>';
      h += '<div class="kt-govde"><div class="kt-ay"><button type="button" data-kt="geri" aria-label="Önceki ay"><i class="fa-solid fa-chevron-left" aria-hidden="true"></i></button><b>' + AYLAR[gor.a] + ' ' + gor.y + '</b><button type="button" data-kt="ileri" aria-label="Sonraki ay"><i class="fa-solid fa-chevron-right" aria-hidden="true"></i></button></div><div class="kt-gunler">';
      ['Pt','Sa','Ça','Pe','Cu','Ct','Pz'].forEach(function(x){ h += '<span class="kt-bas">' + x + '</span>'; });
      for(var i = 0; i < bas; i++) h += '<span></span>';
      for(var g = 1; g <= gun; g++){
        var c = (gor.y === bugun.y && gor.a === bugun.a && g === bugun.g ? ' is-bugun' : '') + (tas && tas.y === gor.y && tas.a === gor.a && tas.g === g ? ' is-sec' : '');
        h += '<button type="button" class="' + c.trim() + '" data-gun="' + g + '"' + (gecmis(gor.y, gor.a, g) ? ' disabled' : '') + ' aria-label="' + g + ' ' + AYLAR[gor.a] + '">' + g + '</button>';
      }
      h += '</div></div><div class="kt-saat"><span>Saat</span>'
        + '<div class="kt-adim"><button type="button" data-adim="h,-1" aria-label="Saati azalt"><i class="fa-solid fa-minus" aria-hidden="true"></i></button><input inputmode="numeric" maxlength="2" data-kt-alan="h" aria-label="Saat" value="' + iki(tas.h) + '"><button type="button" data-adim="h,1" aria-label="Saati artır"><i class="fa-solid fa-plus" aria-hidden="true"></i></button></div>'
        + '<span class="kt-iki-nokta">.</span>'
        + '<div class="kt-adim"><button type="button" data-adim="m,-5" aria-label="Dakikayı azalt"><i class="fa-solid fa-minus" aria-hidden="true"></i></button><input inputmode="numeric" maxlength="2" data-kt-alan="m" aria-label="Dakika" value="' + iki(tas.m) + '"><button type="button" data-adim="m,5" aria-label="Dakikayı artır"><i class="fa-solid fa-plus" aria-hidden="true"></i></button></div></div>'
        + '<div class="kt-alt"><span class="kt-ozet">' + ozet(tas) + '<small>' + (kt.dataset.not || 'Türkiye saati') + '</small></span>'
        + (kt.dataset.temizlenir ? '<button type="button" class="btn btn-ghost btn-sm" data-kt="temizle">Temizle</button>' : '<button type="button" class="btn btn-ghost btn-sm" data-kt="vazgec">Vazgeç</button>')
        + '<button type="button" class="btn btn-acc btn-sm" data-kt="tamam">Uygula</button></div>';
      menu.innerHTML = h;
    }
    function ozetYaz(){ var o = menu.querySelector('.kt-ozet'); if(o) o.firstChild.nodeValue = ozet(tas); }
    function kapat(){ if(btn.getAttribute('aria-expanded') === 'true') btn.click(); }
    window.addEventListener('scroll', function(){ if(menu.classList.contains('open')) kapat(); }, true);
    btn.addEventListener('click', function(){ setTimeout(function(){
      if(!menu.classList.contains('open')) return;
      tas = sec ? { y:sec.y, a:sec.a, g:sec.g, h:sec.h, m:sec.m } : { y:bugun.y, a:bugun.a, g:bugun.g, h:bugun.h, m:bugun.m };
      gor = { y:tas.y, a:tas.a }; ciz();
      /* her zaman ekranın içinde: önce düğmenin altı, sığmazsa üstü, o da sığmazsa ekrana sığacak en yakın yer */
      var b0 = btn.getBoundingClientRect(), h = menu.offsetHeight, w = menu.offsetWidth, ust0 = 72, alt0 = window.innerHeight - 12;
      var y = b0.bottom + 8;
      if(y + h > alt0) y = (b0.top - 8 - h >= ust0) ? b0.top - 8 - h : Math.max(ust0, alt0 - h);
      var x = Math.min(b0.left, window.innerWidth - w - 12);
      menu.style.position = 'fixed'; menu.style.top = y + 'px'; menu.style.left = Math.max(12, x) + 'px'; menu.style.bottom = 'auto'; menu.style.right = 'auto';
    }, 0); });
    menu.addEventListener('input', function(e){
      var a = e.target.getAttribute('data-kt-alan'); if(!a) return; e.stopPropagation();
      var v = parseInt(e.target.value.replace(/\D/g, ''), 10); if(isNaN(v)) return;
      tas[a] = Math.max(0, Math.min(a === 'h' ? 23 : 59, v)); ozetYaz();
    });
    menu.addEventListener('click', function(e){
      e.stopPropagation();
      var b = e.target.closest('button'); if(!b) return;
      if(b.dataset.kt === 'geri'){ gor.a--; if(gor.a < 0){ gor.a = 11; gor.y--; } ciz(); }
      else if(b.dataset.kt === 'ileri'){ gor.a++; if(gor.a > 11){ gor.a = 0; gor.y++; } ciz(); }
      else if(b.dataset.gun){ tas.y = gor.y; tas.a = gor.a; tas.g = +b.dataset.gun; ciz(); }
      else if(b.dataset.adim){
        var p = b.dataset.adim.split(','), k = p[0], s = +p[1];
        if(k === 'h') tas.h = (tas.h + s + 24) % 24; else tas.m = (Math.round(tas.m / 5) * 5 + s + 60) % 60;
        var inp = menu.querySelector('[data-kt-alan="' + k + '"]'); if(inp) inp.value = iki(tas[k]); ozetYaz();
      }
      else if(b.dataset.hizli){
        var q = b.dataset.hizli.split(',').map(Number), dt = new Date(bugun.y, bugun.a, bugun.g + q[0]);
        tas = { y:dt.getFullYear(), a:dt.getMonth(), g:dt.getDate(), h:q[1], m:q[2] }; gor = { y:tas.y, a:tas.a }; ciz();
      }
      else if(b.dataset.kt === 'vazgec'){ kapat(); }
      else if(b.dataset.kt === 'temizle'){ sec = null; yaz(); kapat(); kt.dispatchEvent(new Event('input', {bubbles:true})); }
      else if(b.dataset.kt === 'tamam'){ sec = tas; yaz(); kapat(); kt.dispatchEvent(new Event('input', {bubbles:true})); }
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
      h.style.backgroundSize = ''; h.style.backgroundPosition = ''; h.classList.remove('is-kirpmasiz');
    });
    alan.querySelectorAll('[data-gorsel-bilgi]').forEach(function(b){ b.textContent = bilgi; });
    alan.querySelectorAll('[data-gorsel-bos]').forEach(function(x){ x.hidden = true; });
    alan.querySelectorAll('[data-gorsel-dolu]').forEach(function(x){ x.hidden = false; });
    var oto = alan.querySelector('.kg-oto');
    if(oto) oto.innerHTML = kap === 'mobil' ? '<i class="fa-solid fa-image" aria-hidden="true"></i> Ayrı görsel' : '<i class="fa-solid fa-wand-magic-sparkles" aria-hidden="true"></i> Webden kırpıldı';
    btn.dispatchEvent(new Event('input', {bubbles:true}));
    /* kırpma: görsel değişince kırpma penceresi açılır (alan [data-kirp-sonra] taşıyorsa) */
    btn.dispatchEvent(new CustomEvent('kb-gorsel', { bubbles:true, detail:{ kapsam: kap } }));
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
  var NOT = { kirp:'Bu görsel alanında kırpma yok', medya:'Medya seçici sıradaki adımda', surum:'Sürüm geçmişi ve düzeltmeler penceresi sıradaki adımda' };
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

  /* ---------------- profile göre metin (Bana etkisi) ---------------- */
  document.querySelectorAll('[data-profil-metin]').forEach(function(PM){
    function say(){
      var n = PM.querySelectorAll('[data-pm-kart]:not([hidden])').length, s = PM.querySelector('[data-pm-say]');
      if(s) s.textContent = n ? n + ' profil için ayrı metin' : 'Yalnızca genel metin';
    }
    function ac(id, odak){
      var k = PM.querySelector('[data-pm-kart="' + id + '"]'), c = PM.querySelector('[data-pm-cip="' + id + '"]'); if(!k || !c) return;
      k.hidden = false; c.classList.add('is-on'); c.setAttribute('aria-pressed', 'true');
      var d = c.querySelector('.kb-pm-durum'); if(d) d.className = 'fa-solid fa-check kb-pm-durum';
      if(odak){ var ta = k.querySelector('textarea'); ta.focus(); }
      say(); PM.dispatchEvent(new Event('input', {bubbles:true}));
    }
    function kapat(id){
      var k = PM.querySelector('[data-pm-kart="' + id + '"]'), c = PM.querySelector('[data-pm-cip="' + id + '"]'); if(!k || !c) return;
      k.hidden = true; c.classList.remove('is-on'); c.setAttribute('aria-pressed', 'false');
      var d = c.querySelector('.kb-pm-durum'); if(d) d.className = 'fa-solid fa-plus kb-pm-durum';
      say(); PM.dispatchEvent(new Event('input', {bubbles:true}));
    }
    PM.addEventListener('click', function(e){
      var c = e.target.closest('[data-pm-cip]');
      if(c){ var k = PM.querySelector('[data-pm-kart="' + c.dataset.pmCip + '"]'); if(k && k.hidden) ac(c.dataset.pmCip, true); else if(k) k.querySelector('textarea').focus(); return; }
      var x = e.target.closest('[data-pm-kaldir]');
      if(x){ var kk = x.closest('[data-pm-kart]'), id = kk.dataset.pmKart, eski = kk.querySelector('textarea').value; kapat(id); window.kbBildir(kk.querySelector('b').textContent + ' metni kaldırıldı', function(){ ac(id); kk.querySelector('textarea').value = eski; }); return; }
      if(e.target.closest('[data-pm-oner]')){
        var n = 0;
        PM.querySelectorAll('[data-pm-kart]').forEach(function(k){
          var ta = k.querySelector('textarea');
          if(!ta.value.trim() && k.dataset.oneri){ ta.value = k.dataset.oneri; ac(k.dataset.pmKart); if(window.kbSayaclar) window.kbSayaclar(k); n++; }
        });
        window.kbBildir(n ? n + ' profil için öneri eklendi (AI · prototip); kontrol edip düzeltin' : 'Bütün ilgili profillerin metni zaten dolu');
      }
    });
    say();
  });

  /* ---------------- sosyal gönderi metni araç çubuğu ----------------
     X, Instagram, Facebook ve LinkedIn gerçek kalın yazıyı desteklemez: kalın ve italik Unicode harfle yapılır
     (Türkçe özel harflerin karşılığı yoktur, olduğu gibi kalır). Telegram gerçek biçimi destekler. */
  function unicodeYap(s, tur){
    var tabanB = tur === 'b' ? 0x1D5D4 : 0x1D608, rakam = tur === 'b' ? 0x1D7EC : null;
    return Array.from(s).map(function(c){
      var k = c.codePointAt(0);
      if(k >= 65 && k <= 90) return String.fromCodePoint(tabanB + k - 65);
      if(k >= 97 && k <= 122) return String.fromCodePoint(tabanB + 26 + k - 97);
      if(rakam && k >= 48 && k <= 57) return String.fromCodePoint(rakam + k - 48);
      return c;
    }).join('');
  }
  /* araç tanımları: platform kayıttaki "editor.araclar" listesine göre bunlardan kendi çubuğunu kurar */
  var ARAC = {
    'b-u': { ikon:'fa-bold', ad:'Kalın (Unicode harf; ç ğ ı ö ş ü değişmez)' },
    'i-u': { ikon:'fa-italic', ad:'İtalik (Unicode harf)' },
    'b': { ikon:'fa-bold', ad:'Kalın', sar:['*','*'] },
    'i': { ikon:'fa-italic', ad:'İtalik', sar:['_','_'] },
    'u': { ikon:'fa-underline', ad:'Altı çizili', sar:['__','__'] },
    's': { ikon:'fa-strikethrough', ad:'Üstü çizili', sar:['~','~'] },
    'kod': { ikon:'fa-code', ad:'Kod', sar:['`','`'] },
    'spoiler': { ikon:'fa-eye-slash', ad:'Gizli metin (dokununca açılır)', sar:['||','||'] },
    'alinti': { ikon:'fa-quote-right', ad:'Alıntı', satir:'>' },
    'link-metin': { ikon:'fa-link', ad:'Metne bağlantı ver' },
    'emoji': { ikon:'fa-face-smile', ad:'Emoji', regular:true },
    'etiket': { ikon:'fa-hashtag', ad:'Etiket (#)' },
    'kisi': { ikon:'fa-at', ad:'Hesap etiketle (@)' },
    'link': { ikon:'fa-link', ad:'Haber bağlantısı' },
    'konum': { ikon:'fa-location-dot', ad:'Konum ekle' },
    'gorselde-etiket': { ikon:'fa-user-tag', ad:'Görselde kişi etiketle' }
  };
  var EMOJI = '📰 🔴 ⚡ 📌 📊 📈 📉 💰 🏛️ ⚽ 🏀 🛡️ 🌍 🎓 ❄️ 🚗 ✈️ ✅ ⚠️ 👉'.split(' ');
  var HABER_URL = 'https://dadahaber.com/gundem/asgari-ucret-ilk-toplanti';
  window.kbSosyalArac = function(ar, ta, pl){
    var ed = (pl && pl.editor) || {}, araclar = ed.araclar || ['b-u','i-u','emoji','etiket','kisi','link'], h = '', son = '';
    var grup = function(k){ return /^(b|i|u|s|kod|spoiler|alinti|b-u|i-u|link-metin)$/.test(k) ? 'bicim' : /^(konum|gorselde-etiket)$/.test(k) ? 'ek' : 'ekle'; };
    araclar.forEach(function(k){
      var d = ARAC[k]; if(!d) return;
      if(son && grup(k) !== son) h += '<span class="kz-ayir"></span>'; son = grup(k);
      h += '<button type="button" data-sa="' + k + '" title="' + d.ad + '" aria-label="' + d.ad + '"><i class="fa-' + (d.regular ? 'regular' : 'solid') + ' ' + d.ikon + '" aria-hidden="true"></i></button>';
    });
    if(ed.link_yok) h += '<span class="kz-ayir"></span><button type="button" data-sa="link-yok" class="is-pasif" title="Instagram açıklamasında bağlantı tıklanmaz; profildeki bağlantı kullanılır" aria-label="Bağlantı (bu platformda tıklanmaz)"><i class="fa-solid fa-link-slash" aria-hidden="true"></i></button>';
    h += '<span class="kb-sa-platform">' + (pl ? pl.ad + ' editörü' : '') + '</span>';
    h += '<div class="kb-emoji" hidden>' + EMOJI.map(function(x){ return '<button type="button" data-emoji="' + x + '" aria-label="' + x + '">' + x + '</button>'; }).join('') + '</div>';
    ar.innerHTML = h;
  };
  document.querySelectorAll('.kb-sosyal-arac').forEach(function(ar){
    var ta = ar.parentNode.querySelector('textarea'); if(!ta) return;
    function ekle(m, sec){
      var s = ta.selectionStart, e = ta.selectionEnd, v = ta.value;
      ta.value = v.slice(0, s) + m + v.slice(e); ta.focus();
      var son = s + m.length; ta.setSelectionRange(sec ? s : son, son);
      ta.dispatchEvent(new Event('input', {bubbles:true}));
    }
    ar.addEventListener('mousedown', function(e){ if(e.target.closest('button')) e.preventDefault(); });
    ar.addEventListener('click', function(e){
      var b = e.target.closest('button'); if(!b) return;
      var k = b.dataset.sa, s = ta.selectionStart, en = ta.selectionEnd, secili = ta.value.slice(s, en), d = ARAC[k] || {};
      if(k === 'b-u' || k === 'i-u'){ if(!secili){ window.kbBildir('Önce metinden bir bölüm seçin'); return; } ekle(unicodeYap(secili, k.charAt(0)), true); }
      else if(d.sar){ ekle(d.sar[0] + (secili || 'metin') + d.sar[1], true); }
      else if(d.satir){ var bas = ta.value.lastIndexOf('\n', s - 1) + 1; ta.setSelectionRange(bas, bas); ekle(d.satir + ' '); }
      else if(k === 'link-metin'){ ekle('[' + (secili || 'haberin tamamı') + '](' + HABER_URL + ')'); }
      else if(k === 'emoji'){ var m = ar.querySelector('.kb-emoji'); m.hidden = !m.hidden; }
      else if(b.dataset.emoji){ ekle(b.dataset.emoji); ar.querySelector('.kb-emoji').hidden = true; }
      else if(k === 'etiket'){ ekle(secili ? '#' + secili.replace(/\s+/g, '') : '#'); }
      else if(k === 'kisi'){ ekle(secili ? '@' + secili.replace(/\s+/g, '') : '@'); }
      else if(k === 'link'){ ekle(HABER_URL); }
      else if(k === 'konum' || k === 'gorselde-etiket'){ var f = document.querySelector(k === 'konum' ? '#soKonum' : '#soGorselEt'); if(f){ f.focus(); f.scrollIntoView({ block:'center', behavior:'smooth' }); } }
      else if(k === 'link-yok'){ window.kbBildir('Instagram açıklamasında bağlantı tıklanmaz; profildeki bağlantı kullanılır'); }
    });
  });

  /* ---------------- @ ve # önerileri (platform editörlerindeki gibi) ----------------
     [data-oneri] metin alanında @ yazınca hesap, # yazınca etiket önerilir; [data-oneri="konum"] konum önerir. ↑↓ Enter Esc. */
  var ONR = (window.PANEL || {}).sosyal_oneriler || {};
  var oKutu = document.createElement('div'); oKutu.className = 'pnl-menu kb-oneri'; oKutu.setAttribute('role', 'listbox'); document.body.appendChild(oKutu);
  var oAlan = null, oBas = 0, oSecili = 0;
  function imlecYeri(el, konum){
    if(el.tagName !== 'TEXTAREA'){ var r0 = el.getBoundingClientRect(); return { x: r0.left + 12, y: r0.bottom }; }
    var ay = document.createElement('div'), cs = getComputedStyle(el);
    ['fontFamily','fontSize','fontWeight','lineHeight','letterSpacing','paddingTop','paddingRight','paddingBottom','paddingLeft','borderTopWidth','borderLeftWidth','boxSizing','width','wordWrap','whiteSpace'].forEach(function(k){ ay.style[k] = cs[k]; });
    ay.style.position = 'absolute'; ay.style.visibility = 'hidden'; ay.style.whiteSpace = 'pre-wrap'; ay.style.wordWrap = 'break-word';
    ay.textContent = el.value.slice(0, konum); var sp = document.createElement('span'); sp.textContent = '​'; ay.appendChild(sp);
    document.body.appendChild(ay); var r = el.getBoundingClientRect(), x = r.left + sp.offsetLeft, y = r.top + sp.offsetTop - el.scrollTop + parseFloat(cs.lineHeight || 20);
    ay.remove(); return { x: x, y: y };
  }
  function oKapat(){ oKutu.classList.remove('open'); oAlan = null; }
  function oCiz(el, tur, sorgu){
    var q = tr(sorgu), liste;
    if(tur === '@') liste = (ONR.hesaplar || []).filter(function(h){ return !q || tr(h.ad).indexOf(q) > -1 || tr(h.tutamac).indexOf(q) > -1; }).slice(0, 6).map(function(h){
      return { yaz: '@' + h.tutamac + ' ', html: '<span class="ko-ava">' + h.ad.split(' ').map(function(x){ return x.charAt(0); }).join('').slice(0, 2) + '</span><span class="ko-yazi"><b>' + h.ad + (h.onayli ? ' <i class="fa-solid fa-circle-check ko-onay" aria-label="Onaylı hesap"></i>' : '') + '</b><small>@' + h.tutamac + ' · ' + h.tur + '</small></span>' }; });
    else if(tur === '#') liste = (ONR.etiketler || []).filter(function(h){ return !q || tr(h).indexOf(q) === 0; }).slice(0, 6).map(function(h){ return { yaz: '#' + h + ' ', html: '<span class="ko-ava ko-et">#</span><span class="ko-yazi"><b>#' + h + '</b><small>önerilen etiket</small></span>' }; });
    else liste = (ONR.konumlar || []).filter(function(h){ return !q || tr(h).indexOf(q) > -1; }).slice(0, 6).map(function(h){ return { yaz: h, html: '<span class="ko-ava ko-et"><i class="fa-solid fa-location-dot" aria-hidden="true"></i></span><span class="ko-yazi"><b>' + h + '</b><small>konum</small></span>' }; });
    if(!liste.length){ oKapat(); return; }
    oKutu.innerHTML = '<div class="ko-bas">' + (tur === '@' ? 'Hesap etiketle' : tur === '#' ? 'Etiketler' : 'Konum') + '<span>Prototip: örnek hesaplar</span></div>' + liste.map(function(x, i){ return '<button type="button" role="option" data-yaz="' + x.yaz.replace(/"/g, '&quot;') + '"' + (i === 0 ? ' class="is-sec"' : '') + '>' + x.html + '</button>'; }).join('');
    oSecili = 0; oAlan = el;
    var y = imlecYeri(el, el.selectionStart);
    oKutu.style.position = 'fixed'; oKutu.style.right = 'auto'; oKutu.style.left = Math.min(y.x, innerWidth - 320) + 'px'; oKutu.style.top = (y.y + 4) + 'px';
    oKutu.classList.add('open');
  }
  function oYaz(btn){
    var el = oAlan, v = el.value, s = el.selectionStart, yaz = btn.dataset.yaz;
    el.value = v.slice(0, oBas) + yaz + v.slice(s); var k = oBas + yaz.length; el.focus(); el.setSelectionRange(k, k);
    oKapat(); el.dispatchEvent(new Event('input', {bubbles:true}));
  }
  document.addEventListener('input', function(e){
    var el = e.target; if(!el.matches || !el.matches('[data-oneri]')) return;
    if(el.dataset.oneri === 'konum'){ oBas = 0; oCiz(el, 'konum', el.value); return; }
    var s = el.selectionStart, onu = el.value.slice(0, s), m = onu.match(/(^|\s)([@#])([\wçğıöşüÇĞİÖŞÜ_.]*)$/);
    if(!m){ oKapat(); return; }
    var sinir = el.dataset.oneriYok || ''; if(sinir.indexOf(m[2]) > -1){ oKapat(); return; }
    oBas = s - m[3].length - 1; oCiz(el, m[2], m[3]);
  });
  document.addEventListener('keydown', function(e){
    if(!oAlan || !oKutu.classList.contains('open') || e.target !== oAlan) return;
    var b = oKutu.querySelectorAll('button[data-yaz]');
    if(e.key === 'ArrowDown' || e.key === 'ArrowUp'){ e.preventDefault(); oSecili = (oSecili + (e.key === 'ArrowDown' ? 1 : -1) + b.length) % b.length; b.forEach(function(x, i){ x.classList.toggle('is-sec', i === oSecili); }); }
    else if(e.key === 'Enter' || e.key === 'Tab'){ e.preventDefault(); oYaz(b[oSecili]); }
    else if(e.key === 'Escape'){ e.stopPropagation(); oKapat(); }
  }, true);
  oKutu.addEventListener('mousedown', function(e){ var b = e.target.closest('button[data-yaz]'); if(b){ e.preventDefault(); oYaz(b); } });
  document.addEventListener('click', function(e){ if(oAlan && !oKutu.contains(e.target) && e.target !== oAlan) oKapat(); });
  window.addEventListener('scroll', function(){ if(oAlan) oKapat(); }, true);

  /* ---------------- sosyal medya sekmesi ---------------- */
  document.querySelectorAll('.kb-sosyal').forEach(function(S){
    var metin = S.querySelector('[data-sosyal-metin]'), kart = document.querySelector('[data-sosyal-onizle]') || S.querySelector('.kb-sosyal-kart');
    var kartMetin = kart.querySelector('.ksk-metin'), oranKap = S.querySelector('.kb-oranlar'), kirp = S.querySelector('.kk-cerceve'), kGor = kart.querySelector('.ksk-gorsel');
    var sayaclar = S.querySelector('.kb-sayaclar'), hesap = S.querySelector('[data-sosyal-hesap]');
    var veri = {}, aktif = null;
    S.querySelectorAll('.kb-platform').forEach(function(p){ veri[p.dataset.platform] = { metin: p.dataset.metin || '' }; });
    function oran(o){
      var a = o === 'serbest' ? 'auto' : o.replace(':', '/');
      S.querySelectorAll('[data-kirp-ac^="sosyal."]').forEach(function(b){ b.setAttribute('data-kirp-ac', 'sosyal.' + o); });
      if(kirp) kirp.setAttribute('data-kirp-izle', 'sosyal.' + o);
      if(kGor) kGor.setAttribute('data-kirp-izle', 'sosyal.' + o);
      if(kirp) kirp.style.aspectRatio = o === 'serbest' ? '3/2' : a;
      if(kGor) kGor.style.aspectRatio = o === 'serbest' ? '3/2' : a;
    }
    var PL = {}; ((window.PANEL || {}).sosyal_platformlar || []).forEach(function(x){ PL[x.id] = x; });
    var arac = S.querySelector('[data-sosyal-arac]'), notEl = S.querySelector('[data-sosyal-not]'), ek = S.querySelector('[data-sosyal-ek]');
    function kesimli(html, kesim, duz){
      if(!kesim || duz.length <= kesim) return html;
      return '<span class="ksk-kesim">' + html + '</span><span class="ksk-dahafazla">… daha fazla</span>';
    }
    function telegram(s){
      return s.replace(/\[([^\]]+)\]\((https?:[^)]+)\)/g, '<span class="ksk-link">$1</span>')
        .replace(/\|\|([^|]+)\|\|/g, '<span class="ksk-spoiler">$1</span>').replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/__([^_]+)__/g, '<u>$1</u>').replace(/\*([^*\n]+)\*/g, '<b>$1</b>').replace(/(^|[\s(])_([^_\n]+)_/g, '$1<i>$2</i>').replace(/~([^~\n]+)~/g, '<s>$1</s>')
        .replace(/(^|\n)&gt; ?([^\n]*)/g, '$1<span class="ksk-alinti">$2</span>');
    }
    function yaz(){
      var v = metin.value, link = (v.match(/https?:\/\/\S+/g) || []).length, et = (v.match(/#[\wçğıöşüÇĞİÖŞÜ]+/g) || []).length;
      var emoji = (v.match(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/gu) || []).length;
      var p = S.querySelector('.kb-platform.is-on'), ed = (PL[p.dataset.platform] || {}).editor || {}, sinir = +(ed.sinir || p.dataset.sinir || 0), linkUz = +(ed.link_uzunluk || p.dataset.linkUzunluk || 0);
      var n = v.replace(/https?:\/\/\S+/g, function(u){ return linkUz ? new Array(linkUz + 1).join('x') : u; }).length;
      var cm = S.querySelector('.kb-sosyal-say'); if(cm){ cm.querySelector(':scope > b').textContent = n + ' / ' + sinir; cm.classList.toggle('over', n > sinir); }
      var cb = S.querySelector('.kb-cubuk'); if(cb){ cb.querySelector('span').style.width = Math.min(100, n / sinir * 100) + '%'; cb.classList.toggle('warn', n > sinir * .9 && n <= sinir); cb.classList.toggle('over', n > sinir); }
      var etAsim = ed.etiket_siniri && et > ed.etiket_siniri;
      if(sayaclar) sayaclar.innerHTML = (ed.link_yok ? '' : '<span>Bağlantı <b>' + link + '</b>' + (linkUz ? ' (' + linkUz + ' karakter sayılır)' : '') + '</span>') + '<span' + (etAsim ? ' class="over"' : '') + '>Etiket <b>' + et + (ed.etiket_siniri ? ' / ' + ed.etiket_siniri : '') + '</b></span><span>Emoji <b>' + emoji + '</b></span>' + (ed.kesim ? '<span>Görünen <b>' + Math.min(n, ed.kesim) + ' / ' + ed.kesim + '</b></span>' : '') + '<span>Kalan <b>' + (sinir - n) + '</b></span>';
      if(kartMetin){
        var guv = v.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'), kes = ed.kesim ? guv.slice(0, ed.kesim) : guv;
        var bicimle = function(s){ s = p.dataset.platform === 'telegram' ? telegram(s) : s; return s.replace(/(^|[^"(])(https?:\/\/\S+)/g, '$1<span class="ksk-link' + (ed.link_yok ? ' is-tiksiz' : '') + '">$2</span>').replace(/(#[\wçğıöşüÇĞİÖŞÜ]+)/g, '<span class="ksk-link">$1</span>').replace(/(^|\s)(@[\w.]+)/g, '$1<span class="ksk-link">$2</span>'); };
        kartMetin.innerHTML = ed.kesim && v.length > ed.kesim ? bicimle(kes) + '<span class="ksk-dahafazla">… daha fazla</span>' : bicimle(guv);
      }
      if(aktif) veri[aktif].metin = v;
    }
    function sec(p){
      aktif = p.dataset.platform;
      S.querySelectorAll('.kb-platform').forEach(function(x){ x.classList.toggle('is-on', x === p); x.setAttribute('aria-selected', x === p ? 'true' : 'false'); });
      metin.value = veri[aktif].metin;
      kart.className = 'kb-sosyal-kart p-' + aktif;
      var plk = PL[aktif] || { ad: p.textContent.trim(), editor: {} }, edk = plk.editor || {};
      if(arac) window.kbSosyalArac(arac, metin, plk);
      if(notEl) notEl.innerHTML = '<i class="fa-solid fa-circle-info" aria-hidden="true"></i>' + (edk.not || '');
      metin.dataset.oneriYok = (edk.araclar || []).indexOf('kisi') === -1 ? '@' : '';
      if(ek){ var ekler = (edk.araclar || []).filter(function(x){ return x === 'konum' || x === 'gorselde-etiket'; }); ek.hidden = !ekler.length; ek.querySelectorAll('[data-sosyal-ek-alan]').forEach(function(f){ f.hidden = ekler.indexOf(f.getAttribute('data-sosyal-ek-alan')) === -1; }); }
      document.querySelectorAll('[data-sosyal-ad-platform]').forEach(function(el){ el.textContent = p.textContent.trim(); });
      document.querySelectorAll('[data-sosyal-ad]').forEach(function(el){ el.textContent = p.dataset.ad; });
      document.querySelectorAll('[data-sosyal-tutamac]').forEach(function(el){ el.textContent = p.dataset.tutamac; });
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
