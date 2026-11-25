/* =====================================================================
   ÇEKİRDEK · FORM BİLEŞENLERİ DAVRANIŞI (düzenleme ekranlarının hepsinde aynı)
   - kb-tarih: tarih-saat seçici (tarayıcının tarih alanı asla kullanılmaz)
   - kb-cip-girdi: havuzdan aranan, yoksa aynı yerden eklenen çip girişi
   - [data-form]: kaydedilmemiş değişiklik, zorunlu alan doğrulaması, kaydedildi durumu
   - zengin metin editörü: cekirdek/js/editor.js (TipTap)
   - [data-segment]: önizleme anahtarı · [data-ac]: seçime göre alan aç/kapat
   - kb-sosyal: platform sekmeleri, sayaçlar, oran, canlı kart
   ===================================================================== */
(function(){
  /* ---------------- sayfa durumu (?durum=…) ----------------
     Bir sayfanın halleri (ör. giris.html?durum=dustu, sifremi-unuttum.html?durum=gonderildi): [data-durum-goster="x"] yalnız
     ?durum=x ile görünür, [data-durum-gizle="x"] o durumda gizlenir. Listelerin içindekiler ([data-liste]) kendi ?durum='unu kullanır. */
  (function(){
    var d = new URLSearchParams(location.search).get('durum');
    document.querySelectorAll('[data-durum-goster],[data-durum-gizle]').forEach(function(el){
      if(el.closest('[data-liste]')) return;
      if(el.hasAttribute('data-durum-goster')) el.hidden = el.getAttribute('data-durum-goster').split(' ').indexOf(d) === -1;
      if(el.hasAttribute('data-durum-gizle') && el.getAttribute('data-durum-gizle').split(' ').indexOf(d) > -1) el.hidden = true;
    });
    if(d) document.documentElement.dataset.durum = d;
  })();

  /* ---------------- kayda göre değişen bloklar (?id=…) ----------------
     Tek düzenleme sayfası birden fazla kaydı gösterir: [data-kayit-icin~="yardim"] öğeleri yalnız ?id=yardim ile görünür;
     id yoksa [data-kayit-varsayilan] taşıyan kaydın id'si kullanılır. Başlık, alt satır, SEO gibi metinler de aynı nitelikle değişir. */
  (function(){
    var id = new URLSearchParams(location.search).get('id');
    var hepsi = document.querySelectorAll('[data-kayit-icin]'); if(!hepsi.length) return;
    if(!id){ var v = document.querySelector('[data-kayit-varsayilan]'); id = v ? v.getAttribute('data-kayit-varsayilan') : ''; }
    hepsi.forEach(function(el){ el.hidden = (' ' + el.getAttribute('data-kayit-icin') + ' ').indexOf(' ' + id + ' ') === -1; });
    document.documentElement.dataset.kayit = id;
  })();

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
    document.querySelectorAll('.kb-secim[data-oturum-yazar]').forEach(function(sc){
      var P0 = window.PANEL || {}, per = (P0.personalar || {})[document.documentElement.dataset.rol || 'super'] || {}, adx = per.ad || 'Oturumdaki Kullanıcı';
      var liste = sc.querySelector('.kb-secim-liste'), o = sc.querySelector('button[data-deger="' + adx + '"]');
      if(!o && liste){ o = document.createElement('button'); o.type = 'button'; o.dataset.deger = adx; o.dataset.ad = adx; o.innerHTML = adx + '<span class="ks-alt">siz</span>'; liste.insertBefore(o, liste.firstChild); }
      sc.dataset.deger = adx; sc.classList.add('is-dolu'); var l = sc.querySelector('.ks-deger'); if(l) l.textContent = adx;
    });
    document.querySelectorAll('.kb-secim[data-yeni-deger]').forEach(function(sc){ var v = sc.getAttribute('data-yeni-deger'), o = sc.querySelector('button[data-deger="' + v + '"]'); sc.dataset.deger = v; var dl = sc.querySelector('.ks-deger'); if(dl && o) dl.textContent = o.getAttribute('data-ad') || o.textContent; });
    document.querySelectorAll('.kb-tarih-sec[data-yeni-bos]').forEach(function(k){ k.dataset.deger = ''; });
    document.querySelectorAll('.kb-kaydet .kk-durum i').forEach(function(i){ i.className = 'fa-solid fa-circle-dot'; });
    document.title = (document.body.getAttribute('data-yeni-baslik') || 'Yeni Kayıt') + ' · ' + document.title.split(' · ').slice(1).join(' · ');
  }
  var tr = function(s){ return (s || '').toLocaleLowerCase('tr'); };
  var AYLAR = ['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık'];
  var iki = function(n){ return (n < 10 ? '0' : '') + n; };

  /* ---------------- tarih-saat seçici ---------------- */
  var GUNLER = ['Pazar','Pazartesi','Salı','Çarşamba','Perşembe','Cuma','Cumartesi'];
  window.kbKurucu('.kb-tarih-sec', function(kt){
    var btn = kt.querySelector('.kb-tarih-btn'), menu = kt.querySelector('.kb-tarih-menu'), yazi = kt.querySelector('.kt-deger');
    if(!btn || !menu || !yazi) return;
    document.body.appendChild(menu);  /* kökte açılır: hiçbir kapsayıcı konumunu ya da kırpmasını bozmaz */
    var saatsiz = kt.hasAttribute('data-saatsiz');
    var d = (kt.dataset.deger || '').match(/(\d{4})-(\d{2})-(\d{2})(?:\s+(\d{2})\.(\d{2}))?/);
    var sec = d ? { y:+d[1], a:+d[2] - 1, g:+d[3], h:+(d[4] || 0), m:+(d[5] || 0) } : null;
    var bugun = { y:2026, a:10, g:23, h:16, m:5 };
    var tas = null, gor = null;
    var enAz = kt.dataset.enaz === 'bugun';
    function metin(s){ return iki(s.g) + '.' + iki(s.a + 1) + '.' + s.y + (saatsiz ? '' : ' ' + iki(s.h) + '.' + iki(s.m)); }
    function ozet(s){ var gn = GUNLER[new Date(s.y, s.a, s.g).getDay()]; return gn + ', ' + s.g + ' ' + AYLAR[s.a] + ' ' + s.y + (saatsiz ? '' : ' · ' + iki(s.h) + '.' + iki(s.m)); }
    /* dışarıdan değer verme (tarih aralığı hazır seçimleri): kt.kbAyarla({y,a,g,h,m}) */
    kt.kbAyarla = function(s){ sec = s; yaz(); kt.dataset.secili = s ? s.y + '-' + iki(s.a + 1) + '-' + iki(s.g) : ''; };
    function yaz(){ if(!sec){ yazi.innerHTML = '<span class="kt-bos">' + (kt.dataset.bos || 'Tarih ve saat seçin') + '</span>'; return; } yazi.textContent = metin(sec); }
    function gecmis(y, a, g){ return enAz && (y < bugun.y || (y === bugun.y && (a < bugun.a || (a === bugun.a && g < bugun.g)))); }
    function ciz(){
      var ilk = new Date(gor.y, gor.a, 1), bas = (ilk.getDay() + 6) % 7, gun = new Date(gor.y, gor.a + 1, 0).getDate();
      var h = saatsiz ? '' : '<div class="kt-hizli-ust" role="group" aria-label="Hızlı seçim"><button type="button" data-hizli="0,16,5">Şimdi</button><button type="button" data-hizli="0,19,0">Bu Akşam 19.00</button><button type="button" data-hizli="1,8,0">Yarın 08.00</button><button type="button" data-hizli="1,12,0">Yarın 12.00</button></div>';
      h += '<div class="kt-govde"><div class="kt-ay"><button type="button" data-kt="geri" aria-label="Önceki ay"><i class="fa-solid fa-chevron-left" aria-hidden="true"></i></button><b>' + AYLAR[gor.a] + ' ' + gor.y + '</b><button type="button" data-kt="ileri" aria-label="Sonraki ay"><i class="fa-solid fa-chevron-right" aria-hidden="true"></i></button></div><div class="kt-gunler">';
      ['Pt','Sa','Ça','Pe','Cu','Ct','Pz'].forEach(function(x){ h += '<span class="kt-bas">' + x + '</span>'; });
      for(var i = 0; i < bas; i++) h += '<span></span>';
      for(var g = 1; g <= gun; g++){
        var c = (gor.y === bugun.y && gor.a === bugun.a && g === bugun.g ? ' is-bugun' : '') + (tas && tas.y === gor.y && tas.a === gor.a && tas.g === g ? ' is-sec' : '');
        h += '<button type="button" class="' + c.trim() + '" data-gun="' + g + '"' + (gecmis(gor.y, gor.a, g) ? ' disabled' : '') + ' aria-label="' + g + ' ' + AYLAR[gor.a] + '">' + g + '</button>';
      }
      h += '</div></div>' + (saatsiz ? '' : '<div class="kt-saat"><span>Saat</span>'
        + '<div class="kt-adim"><button type="button" data-adim="h,-1" aria-label="Saati azalt"><i class="fa-solid fa-minus" aria-hidden="true"></i></button><input inputmode="numeric" maxlength="2" data-kt-alan="h" aria-label="Saat" value="' + iki(tas.h) + '"><button type="button" data-adim="h,1" aria-label="Saati artır"><i class="fa-solid fa-plus" aria-hidden="true"></i></button></div>'
        + '<span class="kt-iki-nokta">.</span>'
        + '<div class="kt-adim"><button type="button" data-adim="m,-5" aria-label="Dakikayı azalt"><i class="fa-solid fa-minus" aria-hidden="true"></i></button><input inputmode="numeric" maxlength="2" data-kt-alan="m" aria-label="Dakika" value="' + iki(tas.m) + '"><button type="button" data-adim="m,5" aria-label="Dakikayı artır"><i class="fa-solid fa-plus" aria-hidden="true"></i></button></div></div>')
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
      var b0 = btn.getBoundingClientRect();
      menu.style.position = 'fixed'; menu.style.top = (b0.bottom + 8) + 'px'; menu.style.left = b0.left + 'px'; menu.style.bottom = 'auto'; menu.style.right = 'auto';
      menu._kbTetik = btn; if(window.kbAcilirSigdir) window.kbAcilirSigdir(menu, btn); /* ortak kural: görünür alanda, üst bar ve kaydet çubuğuna binmez, sağa sığmazsa sola */
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
      else if(b.dataset.kt === 'tamam'){ sec = tas; yaz(); kapat(); kt.dataset.secili = sec.y + '-' + iki(sec.a + 1) + '-' + iki(sec.g); kt.dispatchEvent(new Event('input', {bubbles:true})); kt.dispatchEvent(new CustomEvent('kb-tarih', { bubbles:true })); }
    });
    yaz();
  });

  /* ---------------- çip girişi ----------------
     .kb-cip-girdi[data-havuz]       : havuzdan aranır, yoksa "Havuza ekle" ile yerinde eklenir.
     .kb-cip-girdi[data-havuz-yonet] : havuz yerinde yönetilir; öneride her değerin ⋯ menüsü (adını düzelt, sil, kullanım sayısı).
     .kb-cip-girdi[data-serbest]     : havuz yok; Enter ya da virgülle çip olur, × ile kalkar (SEO anahtar kelimeleri, B2).
     .kb-cip-girdi[data-havuz-kapali]: yalnız havuzdakiler seçilir (havuz başka ekrandan yönetilir: alt konular → Kategoriler).
     .kb-cip-girdi[data-birincil]    : ilk çip "Ana"dır; bir çipin adına tıklamak onu ana yapar (alt konular).
     .kb-cip-girdi[data-ana-kaynak="#secim"][data-alt-harita]: seçimdeki değere göre havuz değişir (ana kategori → alt konular). */
  var kullanim = function(s){ var n = 0; for(var i = 0; i < s.length; i++) n = (n * 31 + s.charCodeAt(i)) % 997; return 3 + n % 58; };
  var h_ = function(s){ return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); };
  window.kbKurucu('.kb-cip-girdi', function(cg){
    var inp = cg.querySelector('input'), oneri = cg.querySelector('.kb-cip-oneri');
    var serbest = cg.hasAttribute('data-serbest'), yonet = cg.hasAttribute('data-havuz-yonet'), kapali = cg.hasAttribute('data-havuz-kapali'), birincil = cg.hasAttribute('data-birincil'), birim = cg.getAttribute('data-kullanim-birim') || 'haberde';
    var havuz = []; try{ havuz = JSON.parse(cg.dataset.havuz || '[]'); }catch(e){}
    var acikYonet = null;
    function mevcut(){ return Array.prototype.map.call(cg.querySelectorAll('.kb-cip'), function(c){ return c.dataset.deger; }); }
    function ekle(v){
      v = v.trim().replace(/,$/, ''); if(!v || mevcut().indexOf(v) > -1) return;
      var c = document.createElement('span'); c.className = 'kb-cip'; c.dataset.deger = v;
      c.innerHTML = '<span></span><button type="button" aria-label="Kaldır"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button>';
      c.firstChild.textContent = v; cg.insertBefore(c, inp); inp.value = ''; goster(); cg.dispatchEvent(new Event('input', {bubbles:true}));
    }
    function goster(){
      if(serbest || !oneri) return;
      var v = inp.value.trim();
      if(!v && !yonet){ oneri.classList.remove('open'); return; }
      var var_ = mevcut(), h = '';
      havuz.filter(function(x){ return var_.indexOf(x) === -1 && (!v || tr(x).indexOf(tr(v)) > -1); }).slice(0, yonet ? 8 : 6).forEach(function(x){
        if(yonet && acikYonet === x){
          h += '<div class="kco-yonet" data-yonet-kap="' + h_(x) + '"><div class="kco-yonet-bas"><b>' + h_(x) + '</b><span>' + kullanim(x) + ' ' + birim + ' kullanılıyor</span></div>'
            + '<div class="kco-duzelt"><input value="' + h_(x) + '" aria-label="Yeni ad"><button type="button" class="btn btn-ghost btn-sm" data-yeniden-adlandir="' + h_(x) + '"><i class="fa-solid fa-pen" aria-hidden="true"></i>Adını düzelt</button></div>'
            + '<div class="kco-alt"><button type="button" class="btn btn-ghost btn-sm danger" data-havuzdan-sil="' + h_(x) + '"><i class="fa-solid fa-trash" aria-hidden="true"></i>Havuzdan sil</button><button type="button" class="kb-bag" data-yonet-kapat>Vazgeç</button></div></div>';
          return;
        }
        h += '<div class="kco-satir"><button type="button" data-ekle="' + h_(x) + '"><i class="fa-solid fa-tag" aria-hidden="true"></i>' + h_(x) + '</button>'
          + (yonet ? '<button type="button" class="kco-diger" data-yonet="' + h_(x) + '" aria-label="' + h_(x) + ': düzelt ya da sil" title="Adını düzelt, sil"><i class="fa-solid fa-ellipsis" aria-hidden="true"></i></button>' : '') + '</div>';
      });
      if(v && !kapali && havuz.map(tr).indexOf(tr(v)) === -1) h += '<button type="button" class="kb-ekle" data-ekle="' + h_(v) + '" data-havuza="1"><i class="fa-solid fa-plus" aria-hidden="true"></i>Havuza ekle: “' + h_(v) + '”</button>';
      if(yonet) h += '<div class="kco-not">⋯ ile adını düzeltin ya da havuzdan silin; değişiklik bütün haberlerde geçerli olur</div>';
      if(kapali && v && !h) h = '<div class="kco-not">Bu adla seçenek yok. ' + (cg.dataset.havuzKapaliNot || 'Yeni alt konu Kategoriler\'den eklenir.') + '</div>';
      oneri.innerHTML = h; oneri.classList.toggle('open', !!h);
    }
    if(oneri) oneri.addEventListener('mousedown', function(e){ if(!e.target.closest('input')) e.preventDefault(); });
    var anaK = cg.dataset.anaKaynak && document.querySelector(cg.dataset.anaKaynak), harita = {};
    try{ harita = JSON.parse(cg.dataset.altHarita || '{}'); }catch(e){}
    if(anaK) anaK.addEventListener('kb-secim', function(){
      var yeni = harita[anaK.dataset.deger] || [], silinen = [];
      havuz = yeni.slice();
      cg.querySelectorAll('.kb-cip').forEach(function(c){ if(havuz.indexOf(c.dataset.deger) === -1){ silinen.push(c.dataset.deger); c.remove(); } });
      if(silinen.length) window.kbBildir(silinen.length + ' alt konu kaldırıldı (' + silinen.join(', ') + '); yeni kategoriden alt konu seçin');
      cg.dispatchEvent(new Event('input', {bubbles:true}));
    });
    cg.addEventListener('click', function(e){
      var x = e.target.closest('.kb-cip button'); if(x){ var c = x.closest('.kb-cip'), sonra = c.nextSibling, v = c.dataset.deger; c.remove(); cg.dispatchEvent(new Event('input', {bubbles:true})); window.kbBildir('“' + v + '” kaldırıldı', function(){ cg.insertBefore(c, sonra); cg.dispatchEvent(new Event('input', {bubbles:true})); }); return; }
      var bc = birincil && e.target.closest('.kb-cip'); if(bc && !e.target.closest('button')){ var ilkc = cg.querySelector('.kb-cip'); if(bc !== ilkc){ cg.insertBefore(bc, ilkc); cg.dispatchEvent(new Event('input', {bubbles:true})); window.kbBildir('“' + bc.dataset.deger + '” ana alt konu yapıldı; adres ve SEO buna göre'); } return; }
      var y = e.target.closest('[data-yonet]'); if(y){ e.stopPropagation(); acikYonet = y.dataset.yonet; goster(); return; }
      if(e.target.closest('[data-yonet-kapat]')){ e.stopPropagation(); acikYonet = null; goster(); inp.focus(); return; }
      var rn = e.target.closest('[data-yeniden-adlandir]');
      if(rn){ e.stopPropagation(); var eski = rn.dataset.yenidenAdlandir, yeni = rn.parentNode.querySelector('input').value.trim();
        if(!yeni || yeni === eski){ acikYonet = null; goster(); return; }
        havuz[havuz.indexOf(eski)] = yeni; cg.querySelectorAll('.kb-cip').forEach(function(c){ if(c.dataset.deger === eski){ c.dataset.deger = yeni; c.firstChild.textContent = yeni; } });
        acikYonet = null; goster(); window.kbBildir('“' + eski + '” → “' + yeni + '”; ' + kullanim(eski) + ' ' + birim + ' güncellendi', function(){ havuz[havuz.indexOf(yeni)] = eski; cg.querySelectorAll('.kb-cip').forEach(function(c){ if(c.dataset.deger === yeni){ c.dataset.deger = eski; c.firstChild.textContent = eski; } }); }); return; }
      var hs = e.target.closest('[data-havuzdan-sil]');
      if(hs){ e.stopPropagation(); var d = hs.dataset.havuzdanSil, n = kullanim(d);
        window.kbOnay({ tehlike:true, baslik:'“' + d + '” havuzdan silinsin mi?', metin: n + ' ' + birim + ' kullanılıyor; silinince o içeriklerden de kalkar. Çöpe gider, oradan geri alınabilir; işlem denetim izine yazılır.', evet:'Havuzdan sil',
          evetIs: function(){ var i = havuz.indexOf(d); havuz.splice(i, 1); cg.querySelectorAll('.kb-cip').forEach(function(c){ if(c.dataset.deger === d) c.remove(); }); acikYonet = null; goster(); window.kbBildir('“' + d + '” havuzdan silindi', function(){ havuz.splice(i, 0, d); goster(); }); } });
        return; }
      var o = e.target.closest('[data-ekle]'); if(o){ e.stopPropagation(); if(o.dataset.havuza) havuz.push(o.dataset.ekle); ekle(o.dataset.ekle); inp.focus(); return; }
      if(!e.target.closest('.kb-cip-oneri')) inp.focus();
    });
    inp.addEventListener('input', function(e){ e.stopPropagation(); acikYonet = null; goster(); });
    inp.addEventListener('focus', function(){ if(yonet) goster(); });
    inp.addEventListener('keydown', function(e){
      if(e.key === 'Enter' || e.key === ','){ e.preventDefault(); if(serbest){ ekle(inp.value); return; } var ilk = oneri && oneri.querySelector('[data-ekle]'); if(ilk && ilk.dataset.havuza) havuz.push(ilk.dataset.ekle); if(ilk) ekle(ilk.dataset.ekle); else if(!kapali) ekle(inp.value); }
      if(e.key === 'Backspace' && !inp.value){ var s = cg.querySelectorAll('.kb-cip'); if(s.length) s[s.length - 1].remove(); }
      if(e.key === 'Escape' && oneri) oneri.classList.remove('open');
    });
    inp.addEventListener('blur', function(){ setTimeout(function(){ if(oneri && !oneri.contains(document.activeElement)){ oneri.classList.remove('open'); acikYonet = null; } }, 150); });
  });

  /* ---------------- kaydedilmemiş değişiklikle geçiş: panelin onay penceresi ---------------- */
  var KIRLI = [];
  window.kbKirliVar = function(){ return KIRLI.some(function(x){ return x.kirli(); }); };
  function git(h){ window.kbGecisOnayli = true; location.href = h; }
  function kirliPencere(sonra, cikis){
    var tas = KIRLI.some(function(x){ return x.kirli() && x.taslakVar(); });
    window.kbOnay({ ikon: 'fa-circle-exclamation', baslik: 'Kaydedilmemiş değişiklikler var', metin: cikis ? 'Oturum kapanmadan önce değişikliklerinizi taslak olarak kaydedebilirsiniz.' : 'Sayfadan ayrılmadan önce değişikliklerinizi taslak olarak kaydedebilirsiniz.',
      evet: tas ? 'Taslak Kaydet ve Çık' : 'Kaydet ve Çık', vazgec: 'Sayfada Kal',
      evetIs: function(){ var ok = true; KIRLI.forEach(function(x){ if(x.kirli()) ok = x.taslak() && ok; }); if(ok) setTimeout(sonra, 600); },
      ikinci: { ad: 'Kaydetmeden Çık', tehlike: true, is: function(){ KIRLI.forEach(function(x){ x.temizle(); }); sonra(); } } });
  }
  window.kbGecisOnayla = kirliPencere;
  document.addEventListener('click', function(e){
    if(e.defaultPrevented || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest('a[href]'); if(!a) return;
    var h = a.getAttribute('href') || '', cikis = a.hasAttribute('data-cikis');
    if(a.target === '_blank' || a.hasAttribute('download') || /^(#|javascript:|mailto:|tel:)/.test(h)) return;
    var u = new URL(a.href, location.href); if(u.pathname === location.pathname && u.search === location.search && u.hash) return;
    if(!window.kbKirliVar()){
      if(cikis){ e.preventDefault(); window.kbOnay({ ikon: 'fa-right-from-bracket', baslik: 'Oturum kapatılsın mı?', metin: 'Bu cihazda oturumunuz kapanır; yeniden girişte e-posta ve şifreniz sorulur.', evet: 'Çıkış Yap', evetIs: function(){ git(a.href); } }); }
      return;
    }
    e.preventDefault(); e.stopPropagation();
    kirliPencere(function(){ git(a.href); }, cikis);
  }, true);
  /* tarayıcının kendi doğrulama balonu çıkmaz: zorunlu alan ve biçim hatası panelin bileşeniyle gösterilir (ferr) */
  document.querySelectorAll('form').forEach(function(f){ f.noValidate = true; });
  document.addEventListener('invalid', function(e){ e.preventDefault(); }, true);

  /* ---------------- form: değişiklik, doğrulama, kaydet ---------------- */
  document.querySelectorAll('[data-form]').forEach(function(F){
    var cubuk = document.querySelector('.kb-kaydet[data-form-icin="' + F.id + '"]');
    var durum = cubuk && cubuk.querySelector('.kk-durum span');
    var kirli = false;
    function kirlet(){ if(kirli) return; kirli = true; if(cubuk){ cubuk.classList.add('is-kirli'); cubuk.querySelector('.kk-durum i').className = 'fa-solid fa-circle-dot'; } if(durum) durum.textContent = 'Kaydedilmemiş değişiklikler var'; }
    F.addEventListener('input', function(e){ if(e.isTrusted || e.target.closest('.kb-tarih-sec,.kb-cip-girdi,.kb-editor')) kirlet(); });
    F.addEventListener('kb-secim', kirlet);
    /* KURAL · tarayıcı kutusu yok: panel içindeki her geçiş (menü, bağlantı, "…'e dön", çıkış) panelin kendi onay penceresiyle sorulur
       (aşağıda kbGecisOnayla). Tarayıcının kendi kutusu YALNIZ kaçınılmaz durumda kalır: sekmeyi kapatma, sayfayı yenileme, adres
       çubuğundan başka yere gitme — bunlar sayfanın dışında olduğu için panel penceresi açılamaz. Panel penceresinden onaylanan geçişte
       (window.kbGecisOnayli) sorulmaz. */
    window.addEventListener('beforeunload', function(e){ if(kirli && !window.kbGecisOnayli){ e.preventDefault(); e.returnValue = ''; } });
    KIRLI.push({ F: F, kirli: function(){ return kirli; }, temizle: function(){ kirli = false; }, taslak: function(){ var tb = document.querySelector('.kb-kaydet[data-form-icin="' + F.id + '"] [data-kaydet][data-kaydet-tur="taslak"]') || (cubuk && cubuk.querySelector('[data-kaydet]')); if(!tb) return true; tb.click(); return !kirli; }, taslakVar: function(){ return !!document.querySelector('.kb-kaydet[data-form-icin="' + F.id + '"] [data-kaydet][data-kaydet-tur="taslak"]'); } });
    function dogrula(tur){
      var hata = 0;
      F.querySelectorAll('.sa-form-tab').forEach(function(s){ s.classList.remove('has-error'); });
      F.querySelectorAll(tur === 'taslak' ? '[data-zorunlu-taslak]' : '[data-zorunlu]').forEach(function(el){
        var gz = el.closest('[hidden]'); if(gz && !gz.classList.contains('sa-form-panel')) return;  /* gizli kayıt bloğu ve kapalı alan sayılmaz */
        var row = el.closest('.frow'), bos = window.kbAlanBos ? window.kbAlanBos(el) : (el.matches('input,textarea') ? !el.value.trim() : !el.textContent.trim());
        if(row) row.classList.toggle('has-error', bos);
        if(bos){ hata++; var p = el.closest('.sa-form-panel'); if(p){ var s = F.querySelector('.sa-form-tab[data-panel="' + p.id + '"]'); if(s) s.classList.add('has-error'); } }
      });
      return hata;
    }
    if(cubuk) cubuk.querySelectorAll('[data-kaydet]').forEach(function(b){
      b.addEventListener('click', function(){
        var h = dogrula(b.dataset.kaydetTur);
        if(h){ window.kbBildir(h + ' zorunlu alan boş; işaretli sekmelere bakın', null, 'uyari'); var ilk = F.querySelector('.frow.has-error'); var p = ilk && ilk.closest('.sa-form-panel'); if(p && p.hidden){ var s = F.querySelector('.sa-form-tab[data-panel="' + p.id + '"]'); if(s) s.click(); } if(ilk) ilk.scrollIntoView({block:'center', behavior:'smooth'}); return; }
        function kaydet(){
          kirli = false; cubuk.classList.remove('is-kirli'); cubuk.querySelector('.kk-durum i').className = 'fa-solid fa-circle-check';
          if(durum) durum.textContent = (b.dataset.kaydetMetin || 'Kaydedildi') + ' · 23.11.2026 16.05 · ' + (document.getElementById('pmName') ? document.getElementById('pmName').textContent : '');
          window.kbBildir(b.dataset.bildir || 'Değişiklikler kaydedildi; önceki hal sürüm geçmişinde');
        }
        /* hassas kayıt (K15: rol, izin grubu, güvenlik politikası, otomatik yayın ayarı): data-kod → önce e-posta kodu */
        if(b.hasAttribute('data-kod') && window.kbKod) window.kbKod({ baslik: b.dataset.kodBaslik || 'Kaydetmeyi e-posta koduyla doğrulayın', evet: 'Doğrula ve kaydet', evetIs: kaydet });
        else kaydet();
      });
    });
    F.addEventListener('input', function(e){ var r = e.target.closest && e.target.closest('.frow.has-error'); if(r) r.classList.remove('has-error'); });
  });

  /* ---------------- önizleme anahtarı ve seçime bağlı alanlar ---------------- */
  window.kbKurucu('[data-segment]', function(sg){
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
    var don = alan.querySelector('[data-gorsel-webe-don]'); if(don) don.hidden = kap !== 'mobil';
    var oto = alan.querySelector('.kg-oto');
    if(oto) oto.innerHTML = kap === 'mobil' ? '<i class="fa-solid fa-image" aria-hidden="true"></i> Ayrı görsel' : '<i class="fa-solid fa-wand-magic-sparkles" aria-hidden="true"></i> Webden kırpıldı';
    btn.dispatchEvent(new Event('input', {bubbles:true}));
    /* kırpma: görsel değişince kırpma penceresi açılır (alan [data-kirp-sonra] taşıyorsa) */
    btn.dispatchEvent(new CustomEvent('kb-gorsel', { bubbles:true, detail:{ kapsam: kap } }));
  }
  var EH = M.etiket_havuzu || { kategoriler:[], kisiler:[], etiketler:[] };
  var gUrl = function(g, kucuk){ return g.url || (kokUrl + (kucuk ? M.kucuk : M.kok) + g.dosya); };
  var esc = function(s){ return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); };
  var kisiBul = function(ad){ return (EH.kisiler || []).filter(function(k){ return k.ad === ad; })[0] || { ad: ad, kisaltma: '' }; };

  /* ---------------- yükleme → etiketleme (M3) → kırpma ----------------
     Yükleme biter bitmez etiketleme penceresi açılır. Dada Haber'e ait görsel kategori ve en az bir kişi/kurum ya da
     etiketle havuza girer (M1–M3); dış kaynaklı görsel havuza girmez, yalnızca bu içerikte kalır.
     Pencerenin alanları (telif, kategori, kişi ve kurum, etiketler) Yasin Bey'e soruluyor (Beyar, 24.11.2026); değiştirme. */
  /* görsel kaldır (B7): alan boş haline döner, geri alınabilir · mobil görseli webden kırpılana döndür */
  document.addEventListener('click', function(e){
    var k = e.target.closest('[data-gorsel-kaldir]');
    if(k){ e.preventDefault(); var alan = k.closest('[data-gorsel-alan]'); if(!alan) return;
      var hedefler = Array.prototype.map.call(alan.querySelectorAll('[data-gorsel-hedef]'), function(h){ return [h, h.getAttribute('style') || '']; });
      var bos = alan.querySelectorAll('[data-gorsel-bos]'), dolu = alan.querySelectorAll('[data-gorsel-dolu]');
      hedefler.forEach(function(x){ x[0].style.backgroundImage = 'none'; });
      if(bos.length){ bos.forEach(function(x){ x.hidden = false; }); dolu.forEach(function(x){ x.hidden = true; }); }
      alan.dispatchEvent(new Event('input', { bubbles:true }));
      window.kbBildir('Görsel kaldırıldı', function(){ hedefler.forEach(function(x){ x[0].setAttribute('style', x[1]); }); bos.forEach(function(x){ x.hidden = true; }); dolu.forEach(function(x){ x.hidden = false; }); });
      return; }
    var d = e.target.closest('[data-gorsel-webe-don]');
    if(d){ e.preventDefault(); var al = d.closest('[data-gorsel-alan]'), web = al.querySelector('[data-gorsel-hedef="web"]'), mob = al.querySelector('[data-gorsel-hedef="mobil"]');
      if(web && mob){ mob.style.backgroundImage = web.style.backgroundImage; mob.style.backgroundSize = ''; mob.style.backgroundPosition = web.style.backgroundPosition; }
      var oto = al.querySelector('.kg-oto'); if(oto) oto.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles" aria-hidden="true"></i> Webden kırpıldı';
      d.hidden = true; window.kbBildir('Mobil görsel yeniden webden kırpılıyor'); }
  });

  var gizliDosya = document.createElement('input'); gizliDosya.type = 'file'; gizliDosya.accept = 'image/jpeg,image/png,image/webp'; gizliDosya.hidden = true;
  document.body.appendChild(gizliDosya);
  var yukleBtn = null;
  gizliDosya.addEventListener('change', function(){
    var f = gizliDosya.files && gizliDosya.files[0]; if(!f || !yukleBtn) return;
    var btn = yukleBtn, r = new FileReader();
    r.onload = function(){
      var img = new Image();
      img.onload = function(){
        var kb = Math.round(f.size / 1024), olcu = img.naturalWidth + '×' + img.naturalHeight;
        medyaKapat();
        /* kişisel görsel (profil fotoğrafı): etiketleme ve medya havuzu yok, doğrudan kırpmaya gider */
        if(btn.closest('[data-etiketsiz]')){ uygula(btn, r.result, null, 'Yüklendi: ' + f.name + ' · ' + olcu + ' · ' + kb + ' KB'); window.kbBildir('Görsel yüklendi'); return; }
        etiketle({ url: r.result, ad: f.name.replace(/\.[^.]+$/, '').replace(/[-_]+/g, ' '), olcu: olcu, kb: kb, kucukMu: img.naturalWidth < 1280 }, function(s){
          if(s.havuza) (M.gorseller = M.gorseller || []).unshift({ url: r.result, ad: s.ad, olcu: olcu, kaynak: 'Dada Haber · yeni yüklendi', etiket: s.etiket });
          uygula(btn, r.result, null, 'Yüklendi: ' + f.name + ' · ' + olcu + ' · ' + kb + ' KB · ' + (s.havuza ? 'medya havuzuna eklendi' : 'dış kaynak, yalnızca bu içerikte'));
          window.kbBildir(s.havuza ? 'Görsel etiketlendi ve medya havuzuna eklendi' : 'Görsel yalnızca bu içerikte kullanılacak; havuza eklenmedi');
        });
      };
      img.src = r.result;
    };
    r.readAsDataURL(f); gizliDosya.value = '';
  });

  var eOv = null, eIs = null;
  function etiketle(g, tamam){
    if(!eOv){
      eOv = document.createElement('div'); eOv.className = 'kb-medya-ov kb-etiketle-ov';
      eOv.innerHTML = '<div class="kb-medya kb-etiketle" role="dialog" aria-modal="true" aria-labelledby="kbEtBas">'
        + '<div class="kb-kap-bas"><div><h2 id="kbEtBas">Görseli etiketleyin</h2><div class="kb-kap-alt">Yükleme tamam · etiketsiz görsel medya havuzuna girmez · sonra kırpma</div></div><button type="button" class="kb-kapat" data-et-kapat aria-label="Kapat"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button></div>'
        + '<div class="ket-govde"><div class="ket-sol"><div class="ket-resim" data-et-resim></div><div class="ket-bilgi" data-et-bilgi></div></div>'
        + '<div class="ket-sag">'
        + '<div class="frow"><span class="flabel">Telif</span><div class="kb-secenek-grup ket-telif">'
        + '<label class="kb-secenek"><input type="radio" name="ketTelif" value="biz" checked><span><b>Dada Haber\'e ait</b><small>Medya havuzuna girer; etiket zorunlu</small></span></label>'
        + '<label class="kb-secenek"><input type="radio" name="ketTelif" value="dis"><span><b>Dış kaynak</b><small>Ajans, kurum, sosyal medya: yalnızca bu içerikte kalır, havuza girmez</small></span></label></div></div>'
        + '<div class="ket-etiketler" data-et-alanlar>'
        + '<div class="frow"><label for="ketAd">Görsel adı</label><input class="finput" id="ketAd" data-et-ad></div>'
        + '<div class="frow"><span class="flabel">Kategori <span class="zorunlu">*</span></span><div class="ket-kategori" role="radiogroup" aria-label="Kategori" data-et-kategori data-zorunlu data-zorunlu-metin="Kategori seçin"></div><div class="ferr"><i class="fa-solid fa-circle-exclamation" aria-hidden="true"></i>Kategori seçin</div></div>'
        + '<div class="frow ket-en-az"><div class="ket-en-az-ic" data-et-enaz data-zorunlu-cip data-zorunlu-metin="En az bir kişi/kurum ya da etiket ekleyin">'
        + '<div class="frow"><label for="ketKisi">Kişi ve kurum</label><div class="ket-cip" data-et-cip="kisiler"><input id="ketKisi" placeholder="Ad ya da kısaltma: RTE, MGK…" autocomplete="off"><div class="pnl-menu ket-oneri"></div></div></div>'
        + '<div class="frow"><label for="ketEt">Etiketler</label><div class="ket-cip" data-et-cip="etiketler"><input id="ketEt" placeholder="Etiket ara ya da yaz" autocomplete="off"><div class="pnl-menu ket-oneri"></div></div><span class="fhint">Medya havuzunun etiketleri; haberin etiketlerinden ayrıdır.</span></div>'
        + '</div><div class="ferr"><i class="fa-solid fa-circle-exclamation" aria-hidden="true"></i>En az bir kişi/kurum ya da etiket ekleyin</div></div>'
        + '</div></div></div>'
        + '<div class="kb-kap-alt-cubuk"><span class="kb-sol fhint" data-et-neden></span><button type="button" class="btn btn-acc btn-sm" data-et-tamam data-dogrula=".kb-etiketle"><i class="fa-solid fa-crop-simple" aria-hidden="true"></i>Devam: kırp</button></div></div>';
      document.body.appendChild(eOv);
      if(window.kbKapDuzenle) kbKapDuzenle(eOv);
      eOv.querySelector('[data-et-kategori]').innerHTML = (EH.kategoriler || []).map(function(k){ return '<label class="ket-kat"><input type="radio" name="ketKat" value="' + esc(k) + '"><span>' + esc(k) + '</span></label>'; }).join('');
      if(window.kbSecenekDuzenle) kbSecenekDuzenle(eOv);
      eOv.querySelectorAll('[data-et-cip]').forEach(function(C){
        var tur = C.getAttribute('data-et-cip'), inp = C.querySelector('input'), on = C.querySelector('.ket-oneri');
        function secili(){ return Array.prototype.map.call(C.querySelectorAll('.kb-cip'), function(c){ return c.dataset.deger; }); }
        function ekle(v){ if(!v || secili().indexOf(v) > -1) return; var c = document.createElement('span'); c.className = 'kb-cip'; c.dataset.deger = v; c.innerHTML = esc(v) + (tur === 'kisiler' && kisiBul(v).kisaltma ? ' <small>' + esc(kisiBul(v).kisaltma) + '</small>' : '') + '<button type="button" aria-label="' + esc(v) + ' kaldır"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button>'; C.insertBefore(c, inp); inp.value = ''; on.classList.remove('open'); kontrol(); }
        function ciz(){
          var q = tr(inp.value.trim()), s = secili(), h = '';
          var liste = tur === 'kisiler' ? (EH.kisiler || []).filter(function(k){ return !q || tr(k.ad).indexOf(q) > -1 || tr(k.kisaltma).indexOf(q) === 0; }).map(function(k){ return { v:k.ad, h: esc(k.ad) + ' <small>' + esc(k.kisaltma) + ' · ' + esc(k.tur) + '</small>' }; })
            : (EH.etiketler || []).filter(function(k){ return !q || tr(k).indexOf(q) > -1; }).map(function(k){ return { v:k, h: esc(k) }; });
          liste = liste.filter(function(x){ return s.indexOf(x.v) === -1; }).slice(0, 7);
          liste.forEach(function(x){ h += '<button type="button" data-v="' + esc(x.v) + '">' + x.h + '</button>'; });
          var var_ = (tur === 'kisiler' ? (EH.kisiler || []).map(function(k){ return tr(k.ad); }) : (EH.etiketler || []).map(tr)).indexOf(q) > -1;
          if(q && !var_) h += '<button type="button" class="kb-ekle" data-yeni="' + esc(inp.value.trim()) + '"><i class="fa-solid fa-plus" aria-hidden="true"></i>Medya havuzuna ekle: “' + esc(inp.value.trim()) + '”</button>';
          on.innerHTML = h; on.classList.toggle('open', !!h && document.activeElement === inp);
        }
        /* havuzda olmayan kişi/kurum: alanın altında küçük satır — ad, kısaltma (isteğe bağlı), tür. Pencerenin diğer alanları değişmez. */
        function yeniKisi(v){
          on.classList.remove('open'); var es = C.parentNode.querySelector('.ket-yeni-kisi'); if(es) es.remove();
          var r = document.createElement('div'); r.className = 'ket-yeni-kisi'; r.setAttribute('role', 'group'); r.setAttribute('aria-label', 'Havuza yeni kişi ya da kurum');
          r.innerHTML = '<div class="kyk-alanlar"><label class="kyk-ad"><span>Ad</span><input class="finput" data-kyk-ad value="' + esc(v) + '"></label>'
            + '<label class="kyk-kisa"><span>Kısaltma <small>isteğe bağlı</small></span><input class="finput" data-kyk-kisa placeholder="ör. MGK" maxlength="12" autocapitalize="characters"></label>'
            + '<div class="kyk-tur"><span>Tür</span><div class="kb-secenek-grup" role="radiogroup" aria-label="Tür"><label class="kb-secenek"><input type="radio" name="kykTur" value="Kişi" checked>Kişi</label><label class="kb-secenek"><input type="radio" name="kykTur" value="Kurum">Kurum</label></div></div></div>'
            + '<div class="kyk-dug"><button type="button" class="btn btn-ghost btn-sm" data-kyk-vazgec>Vazgeç</button><button type="button" class="btn btn-acc btn-sm" data-kyk-ekle><i class="fa-solid fa-plus" aria-hidden="true"></i>Havuza Ekle</button></div>';
          C.parentNode.insertBefore(r, C.nextSibling);
          if(window.kbSecenekDuzenle) window.kbSecenekDuzenle(r);
          r.querySelector('[data-kyk-kisa]').focus();
          r.addEventListener('click', function(e){
            if(e.target.closest('[data-kyk-vazgec]')){ r.remove(); inp.focus(); return; }
            if(!e.target.closest('[data-kyk-ekle]')) return;
            var ad = r.querySelector('[data-kyk-ad]').value.trim(), ks = r.querySelector('[data-kyk-kisa]').value.trim().toLocaleUpperCase('tr'), tr_ = (r.querySelector('input[name=kykTur]:checked') || {}).value || 'Kişi';
            if(!ad){ r.querySelector('[data-kyk-ad]').focus(); return; }
            var k = { ad: ad, kisaltma: ks, tur: tr_ }; EH.kisiler.push(k); r.remove(); ekle(ad);
            window.kbBildir('“' + ad + '”' + (ks ? ' (' + ks + ')' : '') + ' medya havuzuna ' + tr_.toLocaleLowerCase('tr') + ' olarak eklendi', function(){ var i = EH.kisiler.indexOf(k); if(i > -1) EH.kisiler.splice(i, 1); var c = C.querySelector('.kb-cip[data-deger="' + ad.replace(/"/g, '\\"') + '"]'); if(c){ c.remove(); kontrol(); } });
          });
          r.addEventListener('keydown', function(e){ if(e.key === 'Enter' && e.target.matches('input.finput')){ e.preventDefault(); r.querySelector('[data-kyk-ekle]').click(); } if(e.key === 'Escape'){ e.stopPropagation(); r.remove(); inp.focus(); } });
        }
        inp.addEventListener('input', ciz); inp.addEventListener('focus', ciz);
        inp.addEventListener('keydown', function(e){ if(e.key === 'Enter'){ e.preventDefault(); var b = on.querySelector('button'); if(b) b.dispatchEvent(new MouseEvent('mousedown', { bubbles:true })); } if(e.key === 'Backspace' && !inp.value){ var c = C.querySelectorAll('.kb-cip'); if(c.length){ c[c.length - 1].remove(); kontrol(); } } });
        inp.addEventListener('blur', function(){ setTimeout(function(){ on.classList.remove('open'); }, 120); });
        on.addEventListener('mousedown', function(e){
          var b = e.target.closest('button'); if(!b) return; e.preventDefault();
          if(b.dataset.yeni){ var v = b.dataset.yeni;
            if(tur === 'kisiler'){ yeniKisi(v); return; } /* kişi/kurum: kısaltma ve tür sorulur (küçük ekleme satırı) */
            EH.etiketler.push(v); window.kbBildir('“' + v + '” medya havuzunun etiketlerine eklendi'); ekle(v); }
          else ekle(b.dataset.v);
        });
        C.addEventListener('click', function(e){ var x = e.target.closest('.kb-cip button'); if(x){ x.closest('.kb-cip').remove(); kontrol(); } else inp.focus(); });
      });
      eOv.addEventListener('change', kontrol);
      eOv.addEventListener('click', function(e){
        if(e.target.closest('[data-et-kapat]')){ eOv.classList.remove('open'); window.kbBildir('Yükleme iptal edildi; görsel eklenmedi', null, 'bilgi'); return; }
        if(e.target.closest('[data-et-tamam]')){
          var biz = eOv.querySelector('input[name=ketTelif]:checked').value === 'biz', kat = eOv.querySelector('input[name=ketKat]:checked');
          if(biz && (!kat || !eOv.querySelector('[data-et-cip] .kb-cip'))) return;
          var al = function(t){ return Array.prototype.map.call(eOv.querySelectorAll('[data-et-cip="' + t + '"] .kb-cip'), function(c){ return c.dataset.deger; }); };
          eOv.classList.remove('open');
          if(eIs) eIs({ havuza: biz, ad: eOv.querySelector('[data-et-ad]').value.trim() || 'Adsız görsel', etiket: { kategori: kat ? kat.value : '', kisiler: al('kisiler'), etiketler: al('etiketler') } });
        }
      });
      document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && eOv.classList.contains('open')){ e.stopImmediatePropagation(); eOv.classList.remove('open'); } }, true);
    }
    function kontrol(){
      var biz = eOv.querySelector('input[name=ketTelif]:checked').value === 'biz', kat = !!eOv.querySelector('input[name=ketKat]:checked'), n = eOv.querySelectorAll('[data-et-cip] .kb-cip').length;
      /* dış kaynakta alanlar zorunlu değildir (havuza girmez) */
      var kz = eOv.querySelector('[data-et-kategori]'), ez = eOv.querySelector('[data-et-enaz]');
      [kz, ez].forEach(function(el){ if(biz) el.setAttribute('data-zorunlu', ''); else { el.removeAttribute('data-zorunlu'); var r = el.closest('.frow'); if(r) r.classList.remove('has-error'); } });
      if(kat) kz.closest('.frow').classList.remove('has-error'); if(n) ez.closest('.frow').classList.remove('has-error');
      eOv.querySelector('[data-et-alanlar]').classList.toggle('is-pasif', !biz);
      eOv.querySelector('[data-et-neden]').textContent = !biz ? 'Dış kaynak: havuza girmez, etiket gerekmez' : (kat && n) ? 'Havuza etiketleriyle girer' : '';
      if(window.kbPasifGuncelle) window.kbPasifGuncelle();
    }
    eIs = tamam;
    eOv.querySelector('[data-et-resim]').style.backgroundImage = 'url("' + g.url + '")';
    eOv.querySelector('[data-et-bilgi]').innerHTML = '<b>' + esc(g.olcu) + '</b> · ' + g.kb + ' KB' + (g.kucukMu ? '<span class="ket-uyari"><i class="fa-solid fa-triangle-exclamation" aria-hidden="true"></i>Önerilen 1280 px genişliğin altında</span>' : '');
    eOv.querySelector('[data-et-ad]').value = g.ad;
    eOv.querySelector('input[name=ketTelif][value=biz]').checked = true;
    eOv.querySelectorAll('.kb-etiketle .frow.has-error').forEach(function(r){ r.classList.remove('has-error'); });
    eOv.querySelectorAll('input[name=ketKat]').forEach(function(i){ i.checked = false; });
    eOv.querySelectorAll('[data-et-cip] .kb-cip').forEach(function(c){ c.remove(); });
    kontrol(); eOv.classList.add('open');
    setTimeout(function(){ eOv.querySelector('[data-et-ad]').focus(); }, 60);
  }
  window.kbEtiketle = etiketle;

  /* ---------------- medya seçici (M4): etiketle arama, kategori ve kişi/kurum ile gezme ---------------- */
  var mOv = null, mBtn = null, mSec = null, mSuz = { kategori:'', kisi:'' };
  function eslesir(g, q){
    if(!q) return true;
    var e = g.etiket || {}, alanlar = [g.ad, e.kategori].concat(e.etiketler || []);
    (e.kisiler || []).forEach(function(k){ alanlar.push(k); alanlar.push(kisiBul(k).kisaltma); });
    return tr(q).split(/\s+/).every(function(p){ return alanlar.some(function(a){ return a && tr(a).indexOf(p) > -1; }); });
  }
  function medyaCiz(){
    var q = mOv.querySelector('input[type=search]').value.trim(), gl = M.gorseller || [];
    var sonuc = gl.filter(function(g){ var e = g.etiket || {}; return (!mSuz.kategori || e.kategori === mSuz.kategori) && (!mSuz.kisi || (e.kisiler || []).indexOf(mSuz.kisi) > -1) && eslesir(g, q); });
    mOv.querySelector('.kb-medya-izgara').innerHTML = sonuc.map(function(g, i){
      var e = g.etiket || {}, et = [e.kategori].concat((e.kisiler || []).map(function(k){ return kisiBul(k).kisaltma || k; })).filter(Boolean).join(' · ');
      return '<button type="button" class="kb-medya-oge" data-i="' + gl.indexOf(g) + '" data-ad="' + esc(g.ad) + '"><span class="km-resim" style="background-image:url(' + gUrl(g, true) + ')"></span><b>' + esc(g.ad) + '</b><small>' + esc(et) + '</small></button>';
    }).join('') || '<div class="pnl-empty kb-medya-bos"><div class="pe-ico"><i class="fa-solid fa-image" aria-hidden="true"></i></div><h2>Bu aramayla görsel yok</h2><p>Kişi, kurum, kısaltma ya da etiketle arayın; süzgeçleri kaldırmayı deneyin.</p></div>';
    var k = (EH.kisiler || []).filter(function(x){ return q && tr(x.kisaltma) === tr(q); })[0];
    mOv.querySelector('[data-medya-ipucu]').innerHTML = k ? '<i class="fa-solid fa-circle-info" aria-hidden="true"></i>“' + esc(q) + '” → ' + esc(k.ad) : '';
    mOv.querySelector('[data-medya-say]').textContent = sonuc.length + ' görsel';
    mOv.querySelectorAll('[data-gez]').forEach(function(b){ var tur = b.dataset.gez, v = b.dataset.v || ''; b.classList.toggle('is-on', (tur === 'hepsi' && !mSuz.kategori && !mSuz.kisi) || (tur !== 'hepsi' && mSuz[tur] === v)); });
    var cip = []; if(mSuz.kategori) cip.push(['kategori', mSuz.kategori]); if(mSuz.kisi) cip.push(['kisi', mSuz.kisi]);
    mOv.querySelector('[data-medya-suz]').innerHTML = cip.map(function(c){ return '<span class="kb-cip">' + esc(c[1]) + '<button type="button" data-suz-kaldir="' + c[0] + '" aria-label="' + esc(c[1]) + ' süzgecini kaldır"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button></span>'; }).join('');
    if(mSec && !sonuc.some(function(g){ return gl.indexOf(g) === +mSec; })){ mSec = null; }
    mOv.querySelectorAll('.kb-medya-oge').forEach(function(x){ x.classList.toggle('is-sec', x.dataset.i === mSec); });
    var mt = mOv.querySelector('[data-medya-tamam]'); mt.disabled = false; mt.classList.toggle('is-pasif', mSec === null); mt.setAttribute('aria-disabled', mSec === null);
    mOv.querySelector('.kb-medya-secili').textContent = mSec !== null ? gl[+mSec].ad + ' seçildi' : 'Bir görsel seçin';
  }
  function gezCiz(){
    var gl = M.gorseller || [], say = function(f){ return gl.filter(f).length; };
    var kat = (EH.kategoriler || []).map(function(k){ var n = say(function(g){ return (g.etiket || {}).kategori === k; }); return n ? '<button type="button" data-gez="kategori" data-v="' + esc(k) + '">' + esc(k) + '<span>' + n + '</span></button>' : ''; }).join('');
    var kis = (EH.kisiler || []).map(function(k){ var n = say(function(g){ return ((g.etiket || {}).kisiler || []).indexOf(k.ad) > -1; }); return n ? '<button type="button" data-gez="kisi" data-v="' + esc(k.ad) + '" title="' + esc(k.ad) + '">' + esc(k.kisaltma || k.ad) + '<small>' + esc(k.kisaltma ? k.ad : '') + '</small><span>' + n + '</span></button>' : ''; }).join('');
    return '<button type="button" data-gez="hepsi">Bütün görseller<span>' + gl.length + '</span></button><div class="kmg-tt">Kategori</div>' + kat + '<div class="kmg-tt">Kişi ve kurum</div>' + kis;
  }
  function medyaKur(){
    mOv = document.createElement('div'); mOv.className = 'kb-medya-ov';
    mOv.innerHTML = '<div class="kb-medya" role="dialog" aria-modal="true" aria-labelledby="kbMedyaBas"><div class="kb-kap-bas"><div><h2 id="kbMedyaBas">Medya havuzu</h2><div class="kb-kap-alt">Yalnızca Dada Haber\'e ait görseller · etiketle aranır</div></div><button type="button" class="kb-kapat" data-medya-kapat aria-label="Kapat"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button></div>'
      + '<div class="kb-medya-arac"><div class="fb-search"><i class="fa-solid fa-magnifying-glass" aria-hidden="true"></i><input type="search" placeholder="Kişi, kurum, kısaltma (RTE) ya da etiket ara" aria-label="Medya Havuzunda Ara"></div><button type="button" class="btn btn-ghost btn-sm" data-medya-dosya><i class="fa-solid fa-upload" aria-hidden="true"></i>Bilgisayardan Yükle</button></div>'
      + '<div class="kb-medya-durum"><span data-medya-say></span><span class="kb-medya-suz" data-medya-suz></span><span class="kb-medya-ipucu" data-medya-ipucu></span></div>'
      + '<div class="kb-medya-gov"><nav class="kb-medya-gez" aria-label="Havuzu gez"></nav>'
      + '<div class="kb-medya-izgara"></div></div>'
      + '<div class="kb-kap-alt-cubuk"><span class="kb-sol kb-medya-secili">Bir görsel seçin</span><button type="button" class="btn btn-acc btn-sm" data-medya-tamam disabled><i class="fa-solid fa-check" aria-hidden="true"></i>Seç</button></div></div>';
    document.body.appendChild(mOv);
    if(window.kbKapDuzenle) kbKapDuzenle(mOv);
    mOv.addEventListener('click', function(e){
      if(e.target === mOv || e.target.closest('[data-medya-kapat]')){ medyaKapat(); return; }
      if(e.target.closest('[data-medya-dosya]')){ yukleBtn = mBtn; gizliDosya.click(); return; }
      var gz = e.target.closest('[data-gez]');
      if(gz){ if(gz.dataset.gez === 'hepsi'){ mSuz = { kategori:'', kisi:'' }; } else { mSuz[gz.dataset.gez] = mSuz[gz.dataset.gez] === gz.dataset.v ? '' : gz.dataset.v; } medyaCiz(); return; }
      var sk = e.target.closest('[data-suz-kaldir]'); if(sk){ mSuz[sk.dataset.suzKaldir] = ''; medyaCiz(); return; }
      var o = e.target.closest('.kb-medya-oge');
      if(o){ mSec = o.dataset.i; medyaCiz(); return; }
      if(e.target.closest('[data-medya-tamam]') && mSec === null){ var iz = mOv.querySelector('.kb-medya-izgara'); iz.classList.add('is-uyari'); setTimeout(function(){ iz.classList.remove('is-uyari'); }, 1200); mOv.querySelector('.kb-medya-secili').textContent = 'Önce bir görsel seçin'; return; }
      if(e.target.closest('[data-medya-tamam]') && mSec !== null){
        var g = (M.gorseller || [])[+mSec], et = g.etiket || {};
        uygula(mBtn, gUrl(g), gUrl(g, true), 'Havuzdan: ' + g.ad + ' · ' + (g.olcu || '') + ' · ' + [et.kategori].concat(et.kisiler || []).filter(Boolean).join(', '));
        window.kbBildir('Görsel değiştirildi'); medyaKapat();
      }
    });
    mOv.querySelector('input[type=search]').addEventListener('input', medyaCiz);
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && mOv.classList.contains('open')){ e.stopImmediatePropagation(); medyaKapat(); } }, true);
  }
  function medyaKapat(){ if(mOv && mOv.classList.contains('open')){ mOv.classList.remove('open'); if(mBtn && mBtn.focus) mBtn.focus(); } }
  document.addEventListener('click', function(e){
    var b = e.target.closest('[data-medya-sec]');
    if(b){ e.preventDefault(); if(!mOv) medyaKur(); mBtn = b; mSec = null; mSuz = { kategori:'', kisi:'' }; var s = mOv.querySelector('input[type=search]'); s.value = b.dataset.medyaAra || ''; /* data-medya-ara: hazır arama (görsel eksik haberde öneri, YS1) */ mOv.querySelector('.kb-medya-gez').innerHTML = gezCiz(); medyaCiz(); mOv.classList.add('open'); s.focus(); return; }
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
      /* görünen kayıttan çalışır (?id= ile tek sayfada birden fazla kayıt olabilir) */
      var F = b.closest('[data-form]') || document;
      var gor = function(sec){ return Array.prototype.filter.call(F.querySelectorAll(sec), function(el){ var g = el.closest('[hidden]'); return !g || g.classList.contains('sa-form-panel'); })[0] || null; };
      var bas = gor('[data-alan="baslik"]'), spot = gor('[data-alan="spot"]');
      var sb = gor('input[data-alan="seo-baslik"]') || F.querySelector('#sBaslik'), sa = gor('textarea[data-alan="seo-aciklama"],input[data-alan="seo-aciklama"]') || F.querySelector('#sAciklama'), sl = gor('input[data-alan="slug"]') || F.querySelector('#sSlug');
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
      if(k === 'b-u' || k === 'i-u'){ if(!secili){ window.kbBildir('Önce metinden bir bölüm seçin', null, 'bilgi'); return; } ekle(unicodeYap(secili, k.charAt(0)), true); }
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

  /* ---------------- sosyal medya sekmesi ----------------
     KURAL · platform düğmesi durumu (Beyar): renk tek başına anlam taşımaz; her durumun ikonu ve ipucu var.
       bağlı ve paylaşılacak: işaret yok · sorunlu (bağlantı süresi doldu, hata): köşede kırmızı uyarı ikonu + neden ·
       "Bu Platformda Paylaşma": düğme soluk, platform ikonu üstü çizili · metin sınırı aşıldı ya da metin boş: küçük kehribar ünlem.
     KURAL · önizleme: her platform kendi gönderi düzeninde, ayrı şablon (X, Facebook, LinkedIn, Instagram, Telegram). Ortak: yuvarlak
       profil resmi (tema logosu), hesap adı, platforma özgü ikinci satır; ikonlar kitteki ikon setinden; platform logosu/marka varlığı
       kopyalanmaz, yalnız düzen benzer. Yazılan metin, oran, konum ve etiketler canlı güncellenir. */
  var PLAT_AD = { x: ['fa-brands fa-x-twitter', 'X gönderisi'], facebook: ['fa-brands fa-facebook', 'Facebook gönderisi'], linkedin: ['fa-brands fa-linkedin', 'LinkedIn gönderisi'], instagram: ['fa-brands fa-instagram', 'Instagram gönderisi'], telegram: ['fa-brands fa-telegram', 'Telegram mesajı'] };
  function esS(s){ return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  /* önizleme şablonu (dışarıdan da çağrılır: UI kit) — o: { pid, ad, tut, mt (biçimli metin), kes, gor (görsel html), orS, oranAkt, alan, lb, konum } */
  function sosyalSablon(o){
    var pid = o.pid, ad = o.ad, tut = o.tut, mt = o.mt, kes = o.kes, gor = o.gor, orS = o.orS, oranAkt = o.oranAkt, alan = o.alan, lb = o.lb, konum = o.konum;
      var ava = '<span class="ksp-ava kb-logo-isaret" aria-hidden="true"></span>', h = '';
    if(pid === 'x') h = '<div class="ksp ksp-x">' + ava + '<div class="ksp-ic"><div class="ksp-x-bas"><b>' + ad + '</b><i class="fa-solid fa-circle-check ksp-tik" aria-hidden="true"></i><span class="ksp-mut">' + tut + ' · 1 dk</span><i class="fa-solid fa-ellipsis ksp-mut ksp-sag" aria-hidden="true"></i></div>'
      + '<div class="ksp-metin">' + mt + (kes ? '<span class="ksp-devam">… daha fazla</span>' : '') + '</div>'
      + '<div class="ksp-x-kart">' + gor + '<span class="ksp-alan">' + alan + '</span></div>'
      + '<div class="ksp-eylem ksp-x-eylem"><span><i class="fa-regular fa-comment" aria-hidden="true"></i>12</span><span><i class="fa-solid fa-retweet" aria-hidden="true"></i>34</span><span><i class="fa-regular fa-heart" aria-hidden="true"></i>210</span><span><i class="fa-solid fa-chart-simple" aria-hidden="true"></i>8,4 B</span><span class="ksp-sag"><i class="fa-regular fa-bookmark" aria-hidden="true"></i><i class="fa-solid fa-arrow-up-from-bracket" aria-hidden="true"></i></span></div></div></div>';
    else if(pid === 'facebook') h = '<div class="ksp ksp-fb"><div class="ksp-bas">' + ava + '<div class="ksp-kim"><b>' + ad + '</b><span class="ksp-mut">1 dk · <i class="fa-solid fa-earth-americas" aria-hidden="true" title="Herkese açık"></i></span></div><i class="fa-solid fa-ellipsis ksp-mut ksp-sag" aria-hidden="true"></i></div>'
      + '<div class="ksp-metin ksp-pad">' + mt + (kes ? '<span class="ksp-devam">… Devamını gör</span>' : '') + '</div>' + gor
      + '<div class="ksp-serit"><small>' + alan.toUpperCase() + '</small><b>' + lb + '</b></div>'
      + '<div class="ksp-say ksp-pad"><span><i class="fa-solid fa-thumbs-up ksp-tepki" aria-hidden="true"></i>128</span><span>14 yorum · 9 paylaşım</span></div>'
      + '<div class="ksp-dug"><span><i class="fa-regular fa-thumbs-up" aria-hidden="true"></i>Beğen</span><span><i class="fa-regular fa-comment" aria-hidden="true"></i>Yorum Yap</span><span><i class="fa-solid fa-share" aria-hidden="true"></i>Paylaş</span></div></div>';
    else if(pid === 'linkedin') h = '<div class="ksp ksp-li"><div class="ksp-bas"><span class="ksp-ava ksp-kare kb-logo-isaret" aria-hidden="true"></span><div class="ksp-kim"><b>' + ad + '</b><span class="ksp-mut">' + tut + '</span><span class="ksp-mut">1 dk · <i class="fa-solid fa-earth-americas" aria-hidden="true"></i></span></div><i class="fa-solid fa-ellipsis ksp-mut ksp-sag" aria-hidden="true"></i></div>'
      + '<div class="ksp-metin ksp-pad">' + mt + (kes ? '<span class="ksp-devam">…daha fazla</span>' : '') + '</div>' + gor
      + '<div class="ksp-serit"><b>' + lb + '</b><small>' + alan + '</small></div>'
      + '<div class="ksp-say ksp-pad"><span><i class="fa-solid fa-thumbs-up ksp-tepki" aria-hidden="true"></i>86</span><span>7 yorum · 4 yeniden yayın</span></div>'
      + '<div class="ksp-dug"><span><i class="fa-regular fa-thumbs-up" aria-hidden="true"></i>Beğen</span><span><i class="fa-regular fa-comment" aria-hidden="true"></i>Yorum Yap</span><span><i class="fa-solid fa-retweet" aria-hidden="true"></i>Yeniden Yayınla</span><span><i class="fa-solid fa-paper-plane" aria-hidden="true"></i>Gönder</span></div></div>';
    else if(pid === 'instagram') h = '<div class="ksp ksp-ig"><div class="ksp-bas"><span class="ksp-halka">' + ava + '</span><div class="ksp-kim"><b>' + ad + '</b>' + (konum ? '<span class="ksp-mut">' + konum + '</span>' : '') + '</div><i class="fa-solid fa-ellipsis ksp-sag" aria-hidden="true"></i></div>'
      + gor.replace('aspect-ratio:' + orS, 'aspect-ratio:' + (oranAkt === '4:5' ? '4/5' : '1/1'))
      + '<div class="ksp-eylem ksp-ig-eylem"><i class="fa-regular fa-heart" aria-hidden="true"></i><i class="fa-regular fa-comment" aria-hidden="true"></i><i class="fa-regular fa-paper-plane" aria-hidden="true"></i><i class="fa-regular fa-bookmark ksp-sag" aria-hidden="true"></i></div>'
      + '<div class="ksp-pad ksp-ig-alt"><b class="ksp-begeni">1.284 beğenme</b><div class="ksp-metin"><b>' + ad + '</b> ' + mt + (kes ? '<span class="ksp-devam">… devamı</span>' : '') + '</div><span class="ksp-mut">12 yorumun tümünü gör</span><span class="ksp-mut ksp-kucuk">1 dakika önce</span></div></div>';
    else if(pid === 'telegram') h = '<div class="ksp ksp-tg"><div class="ksp-balon">' + gor + '<div class="ksp-pad"><b class="ksp-kanal">' + ad + '</b><div class="ksp-metin">' + mt + '</div>'
      + '<div class="ksp-tg-link"><b>Dada Haber</b><span>' + lb + '</span></div><span class="ksp-tg-alt"><i class="fa-solid fa-eye" aria-hidden="true"></i>2,1 B · 16.05</span></div></div></div>';
    return h;
  }
  window.kbSosyalOnizle = function(kap, o){ /* UI kit ve başka sayfalar: tek önizleme çiz */
    var orS = (o.oran || '16:9') === 'serbest' ? '3/2' : (o.oran || '16:9').replace(':', '/');
    var gor = '<div class="ksp-gorsel" style="background-image:url(' + esS(o.gorsel) + ');aspect-ratio:' + orS + '"></div>';
    var mt = esS(o.metin).replace(/(https?:\/\/\S+)/g, '<span class="ksp-link">$1</span>').replace(/(#[\wçğıöşüÇĞİÖŞÜ]+)/g, '<span class="ksp-link">$1</span>');
    kap.className = 'kb-sosyal-kart p-' + o.platform;
    kap.innerHTML = sosyalSablon({ pid: o.platform, ad: esS(o.ad || 'Dada Haber'), tut: esS(o.tutamac || ''), mt: mt, kes: !!o.kes, gor: gor, orS: orS, oranAkt: o.oran || '16:9', alan: 'dadahaber.com', lb: esS(o.baslik || ''), konum: esS(o.konum || '') });
  };
  document.querySelectorAll('.kb-sosyal').forEach(function(S){
    var metin = S.querySelector('[data-sosyal-metin]'), kart = document.querySelector('[data-sosyal-onizle]') || S.querySelector('.kb-sosyal-kart');
    var oranKap = S.querySelector('.kb-oranlar'), kirp = S.querySelector('.kk-cerceve');
    var sayaclar = S.querySelector('.kb-sayaclar'), hesap = S.querySelector('[data-sosyal-hesap]');
    var veri = {}, aktif = null, oranAkt = '16:9';
    /* görsel ve bağlantı bilgisi: sayfadaki ilk önizlemeden okunur (kırpma bileşeni sonradan [data-kirp-izle] öğesini günceller) */
    var g0 = kart && kart.querySelector('.ksk-gorsel, .ksp-gorsel'), gorsel = { img: g0 ? g0.style.backgroundImage : '', pos: g0 ? g0.style.backgroundPosition : '' };
    var alt0 = kart && kart.querySelector('.ksk-kart-alt'), linkBaslik = alt0 ? alt0.textContent.split(' · ').slice(1).join(' · ').trim() : '';
    S.querySelectorAll('.kb-platform').forEach(function(p){
      veri[p.dataset.platform] = { metin: p.dataset.metin || '' };
      var d = p.querySelector('.kp-durum'); if(d) d.remove();
      if(!p.querySelector('.kp-isaret')){ var s = document.createElement('span'); s.className = 'kp-isaret'; p.appendChild(s); }
      var ik = p.querySelector('i'); if(ik) ik.classList.add('kp-ikon');
    });
    /* "Bu Platformda Paylaşma" seçimi: sayfada yoksa çekirdek ekler (her platform için ayrı) */
    var paylas = S.querySelector('[data-sosyal-paylas]');
    if(!paylas){
      var tr_ = document.createElement('div'); tr_.className = 'toggle-row kb-sosyal-paylas';
      tr_.innerHTML = '<span>Bu Platformda Paylaş<small>Kapalıysa gönderi bu platforma gitmez; metin ve kırpım saklanır</small></span><label class="toggle"><input type="checkbox" data-sosyal-paylas checked aria-label="Bu platformda paylaş"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>';
      var pl = S.querySelector('.kb-platformlar'); pl.parentNode.insertBefore(tr_, pl.nextSibling); paylas = tr_.querySelector('input');
    }
    function oran(o){
      oranAkt = o;
      var a = o === 'serbest' ? 'auto' : o.replace(':', '/');
      S.querySelectorAll('[data-kirp-ac^="sosyal."]').forEach(function(b){ b.setAttribute('data-kirp-ac', 'sosyal.' + o); });
      if(kirp){ kirp.setAttribute('data-kirp-izle', 'sosyal.' + o); kirp.style.aspectRatio = o === 'serbest' ? '3/2' : a; }
      onizle();
    }
    var PL = {}; ((window.PANEL || {}).sosyal_platformlar || []).forEach(function(x){ PL[x.id] = x; });
    var arac = S.querySelector('[data-sosyal-arac]'), notEl = S.querySelector('[data-sosyal-not]'), ek = S.querySelector('[data-sosyal-ek]');
    function telegram(s){
      return s.replace(/\[([^\]]+)\]\((https?:[^)]+)\)/g, '<span class="ksp-link">$1</span>')
        .replace(/\|\|([^|]+)\|\|/g, '<span class="ksk-spoiler">$1</span>').replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/__([^_]+)__/g, '<u>$1</u>').replace(/\*([^*\n]+)\*/g, '<b>$1</b>').replace(/(^|[\s(])_([^_\n]+)_/g, '$1<i>$2</i>').replace(/~([^~\n]+)~/g, '<s>$1</s>')
        .replace(/(^|\n)&gt; ?([^\n]*)/g, '$1<span class="ksk-alinti">$2</span>');
    }
    function edit(pid){ var p = S.querySelector('.kb-platform[data-platform="' + pid + '"]'); return { p: p, ed: (PL[pid] || {}).editor || {}, sinir: +(((PL[pid] || {}).editor || {}).sinir || (p && p.dataset.sinir) || 0) }; }
    function uzunluk(v, ed){ var lu = +(ed.link_uzunluk || 0); return v.replace(/https?:\/\/\S+/g, function(u){ return lu ? new Array(lu + 1).join('x') : u; }).length; }
    /* düğme durumları */
    function durumlar(){
      S.querySelectorAll('.kb-platform').forEach(function(p){
        var pid = p.dataset.platform, e = edit(pid), v = (veri[pid] || {}).metin || '', n = uzunluk(v, e.ed), et = (v.match(/#[\wçğıöşüÇĞİÖŞÜ]+/g) || []).length;
        var sorun = p.dataset.hesapDurum === 'hata', paylasma = p.dataset.paylasma === '1';
        var eksik = !paylasma && (n === 0 ? 'Metin boş' : (e.sinir && n > e.sinir) ? 'Metin sınırı aşıldı (' + n + ' / ' + e.sinir + ')' : (e.ed.etiket_siniri && et > e.ed.etiket_siniri) ? 'Etiket sınırı aşıldı (' + et + ' / ' + e.ed.etiket_siniri + ')' : '');
        p.classList.toggle('is-sorun', sorun); p.classList.toggle('is-paylasma', paylasma); p.classList.toggle('is-eksik', !!eksik && !sorun);
        var s = p.querySelector('.kp-isaret'), ip = sorun ? (p.dataset.hesapNeden || 'Bağlantı süresi doldu; hesabı yeniden bağlayın') : paylasma ? 'Bu platformda paylaşılmayacak' : eksik;
        s.innerHTML = sorun ? '<i class="fa-solid fa-triangle-exclamation" aria-hidden="true"></i>' : (eksik ? '<i class="fa-solid fa-exclamation" aria-hidden="true"></i>' : '');
        s.hidden = !(sorun || eksik);
        p.title = p.textContent.trim() + (ip ? ' · ' + ip : ' · bağlı, paylaşılacak');
        p.setAttribute('aria-label', p.title);
      });
    }
    /* önizleme şablonları */
    function bicimle(s, pid, ed){ s = pid === 'telegram' ? telegram(s) : s; return s.replace(/(^|[^"(])(https?:\/\/\S+)/g, '$1<span class="ksp-link">$2</span>').replace(/(#[\wçğıöşüÇĞİÖŞÜ]+)/g, '<span class="ksp-link">$1</span>').replace(/(^|\s)(@[\w.]+)/g, '$1<span class="ksp-link">$2</span>'); }
    function onizle(){
      if(!kart || !aktif) return;
      var p = S.querySelector('.kb-platform.is-on'), pid = aktif, ed = (PL[pid] || {}).editor || {}, v = metin.value;
      var eskiG = kart.querySelector('.ksp-gorsel, .ksk-gorsel'); if(eskiG && eskiG.style.backgroundImage){ gorsel.img = eskiG.style.backgroundImage; gorsel.pos = eskiG.style.backgroundPosition; gorsel.size = eskiG.style.backgroundSize; }
      var ad = esS(p.dataset.ad || 'Dada Haber'), tut = esS(p.dataset.tutamac || ''), metinH = esS(v), konumEl = S.querySelector('[data-oneri="konum"]'), konum = esS((konumEl && konumEl.value) || (pid === 'instagram' ? p.dataset.tutamac : '') || '');
      var kes = ed.kesim && v.length > ed.kesim, kesik = metinH;
      if(kes){ kesik = metinH.slice(0, ed.kesim); var bo = kesik.search(/\s\S*$/); if(bo > ed.kesim * .6) kesik = kesik.slice(0, bo); kesik = kesik.replace(/\s+$/, ''); } /* kelime sınırında kes */
      var mt = bicimle(kesik, pid, ed);
      var orS = oranAkt === 'serbest' ? '3/2' : oranAkt.replace(':', '/');
      var gor = '<div class="ksp-gorsel" data-kirp-izle="sosyal.' + oranAkt + '" style="background-image:' + esS(gorsel.img) + ';background-position:' + esS(gorsel.pos || '50% 50%') + ';' + (gorsel.size ? 'background-size:' + esS(gorsel.size) + ';' : '') + 'aspect-ratio:' + orS + '"></div>';
      var alan = 'dadahaber.com', lb = esS(linkBaslik || (document.querySelector('[data-alan="baslik"]') || {}).value || '');
      var h = sosyalSablon({ pid: pid, ad: ad, tut: tut, mt: mt, kes: kes, gor: gor, orS: orS, oranAkt: oranAkt, alan: alan, lb: lb, konum: konum });
      kart.className = 'kb-sosyal-kart p-' + pid + (p.classList.contains('is-paylasma') ? ' is-paylasma' : '');
      kart.innerHTML = h + (p.classList.contains('is-paylasma') ? '<div class="ksp-perde"><i class="fa-solid fa-ban" aria-hidden="true"></i>Bu platformda paylaşılmayacak</div>' : '');
      document.querySelectorAll('[data-sosyal-ad-platform]').forEach(function(el){ var a = PLAT_AD[pid] || ['fa-solid fa-share-nodes', p.textContent.trim()]; el.innerHTML = '<i class="' + a[0] + '" aria-hidden="true"></i>' + a[1]; el.classList.add('kb-sosyal-plat-ad'); });
    }
    function yaz(){
      var v = metin.value, link = (v.match(/https?:\/\/\S+/g) || []).length, et = (v.match(/#[\wçğıöşüÇĞİÖŞÜ]+/g) || []).length;
      var emoji = (v.match(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/gu) || []).length;
      var p = S.querySelector('.kb-platform.is-on'), e = edit(p.dataset.platform), ed = e.ed, sinir = e.sinir, linkUz = +(ed.link_uzunluk || p.dataset.linkUzunluk || 0);
      var n = uzunluk(v, ed);
      var cm = S.querySelector('.kb-sosyal-say'); if(cm){ cm.querySelector(':scope > b').textContent = n + ' / ' + sinir; cm.classList.toggle('over', n > sinir); }
      var cb = S.querySelector('.kb-cubuk'); if(cb){ cb.querySelector('span').style.width = Math.min(100, n / sinir * 100) + '%'; cb.classList.toggle('warn', n > sinir * .9 && n <= sinir); cb.classList.toggle('over', n > sinir); }
      var etAsim = ed.etiket_siniri && et > ed.etiket_siniri;
      if(sayaclar) sayaclar.innerHTML = (ed.link_yok ? '' : '<span>Bağlantı <b>' + link + '</b>' + (linkUz ? ' (' + linkUz + ' karakter sayılır)' : '') + '</span>') + '<span' + (etAsim ? ' class="over"' : '') + '>Etiket <b>' + et + (ed.etiket_siniri ? ' / ' + ed.etiket_siniri : '') + '</b></span><span>Emoji <b>' + emoji + '</b></span>' + (ed.kesim ? '<span>Görünen <b>' + Math.min(n, ed.kesim) + ' / ' + ed.kesim + '</b></span>' : '') + '<span>Kalan <b>' + (sinir - n) + '</b></span>';
      if(aktif) veri[aktif].metin = v;
      durumlar(); onizle();
    }
    function sec(p){
      aktif = p.dataset.platform;
      S.querySelectorAll('.kb-platform').forEach(function(x){ x.classList.toggle('is-on', x === p); x.setAttribute('aria-selected', x === p ? 'true' : 'false'); });
      metin.value = veri[aktif].metin;
      var plk = PL[aktif] || { ad: p.textContent.trim(), editor: {} }, edk = plk.editor || {};
      if(arac) window.kbSosyalArac(arac, metin, plk);
      if(notEl) notEl.innerHTML = '<i class="fa-solid fa-circle-info" aria-hidden="true"></i>' + (edk.not || '');
      metin.dataset.oneriYok = (edk.araclar || []).indexOf('kisi') === -1 ? '@' : '';
      if(ek){ var ekler = (edk.araclar || []).filter(function(x){ return x === 'konum' || x === 'gorselde-etiket'; }); ek.hidden = !ekler.length; ek.querySelectorAll('[data-sosyal-ek-alan]').forEach(function(f){ f.hidden = ekler.indexOf(f.getAttribute('data-sosyal-ek-alan')) === -1; }); }
      document.querySelectorAll('[data-sosyal-ad]').forEach(function(el){ el.textContent = p.dataset.ad; });
      document.querySelectorAll('[data-sosyal-tutamac]').forEach(function(el){ el.textContent = p.dataset.tutamac; });
      if(hesap){ var d = p.dataset.hesapDurum; hesap.className = 'pstat ' + (d === 'hata' ? 'warm' : 'ok'); hesap.textContent = d === 'hata' ? 'Bağlantı süresi doldu' : 'Bağlı'; }
      var uy = S.querySelector('[data-sosyal-uyari]'); if(uy) uy.hidden = p.dataset.hesapDurum !== 'hata';
      if(paylas) paylas.checked = p.dataset.paylasma !== '1';
      var oranlar = (p.dataset.oranlar || '').split(','), h = '';
      oranlar.forEach(function(o, i){ var px = o.split('='); h += '<button type="button" class="kb-oran' + (i === 0 ? ' is-on' : '') + '" data-oran="' + px[0] + '">' + (px[0] === 'serbest' ? 'Serbest' : px[0]) + '<small>' + (px[1] || 'kendi ölçüsü') + '</small></button>'; });
      oranKap.innerHTML = h;
      var ol = S.querySelector('[data-oran-not]'); if(ol) ol.textContent = (oranlar[0].split('=')[1] || '') + ' önerilir';
      oranAkt = oranlar[0].split('=')[0];
      yaz(); oran(oranAkt);
    }
    S.addEventListener('click', function(e){
      var p = e.target.closest('.kb-platform'); if(p){ sec(p); return; }
      var o = e.target.closest('.kb-oran'); if(o){ oranKap.querySelectorAll('.kb-oran').forEach(function(x){ x.classList.toggle('is-on', x === o); }); oran(o.dataset.oran); var ol = S.querySelector('[data-oran-not]'); if(ol) ol.textContent = o.querySelector('small').textContent + ' önerilir'; }
      var u = e.target.closest('[data-sosyal-uret]'); if(u){ metin.value = S.querySelector('.kb-platform.is-on').dataset.metin; yaz(); window.kbBildir('Metin yeniden üretildi (AI · prototip)'); }
    });
    if(paylas) paylas.addEventListener('change', function(){ var p = S.querySelector('.kb-platform.is-on'); if(!p) return; if(paylas.checked) delete p.dataset.paylasma; else p.dataset.paylasma = '1';
      durumlar(); onizle(); window.kbBildir(p.textContent.trim() + (paylas.checked ? ': paylaşılacak' : ': bu platformda paylaşılmayacak'), function(){ paylas.checked = !paylas.checked; paylas.dispatchEvent(new Event('change', { bubbles: true })); }); });
    metin.addEventListener('input', yaz);
    S.addEventListener('input', function(e){ if(e.target.matches && e.target.matches('[data-oneri="konum"]')) onizle(); });
    sec(S.querySelector('.kb-platform.is-on') || S.querySelector('.kb-platform'));
  });
})();
