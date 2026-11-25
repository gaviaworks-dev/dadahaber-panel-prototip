/* Blok boşluğu ölçümü — araclar/denetim.html ve araclar/duyarli.html ortak kullanır (KURAL · boşluk: "ait olduğuna yakın, komşusuna uzak").
   Gerçek tarayıcıda, alt alta duran komşu iki bloğun GÖRÜNEN kenarları arasındaki mesafe ölçülür.
   Blok türleri: kutu (zemini ya da çerçevesi olan: kart, bilgi bandı, AI kutusu…) · çizgi (ayırıcı kenar) · grup (alan grubu, form bölümü)
     · tablo · düğme sırası · başlık. Form denetimleri (giriş, seçenek, çip, düğme) tek başına blok sayılmaz; bulundukları sıra sayılır.
   Alt sınır: kitin en küçük blok aralığı (--b-3 = 12 px). Başlıktan kendi içeriğine: --b-2 (8 px; başlık altındakine aittir).
   Sonuç: { yapisik:[…], binme:[…] } — binme = sıfırın altı (üst üste). Sayılmayan: kenardan kenara bitişik bölümler (kart başlığı + tablo),
     aynı sınıftan bitişik liste öğeleri, önizleme/editör/takvim/grafik içi (sitenin ya da cihazın taklidi). */
(function(g){
  var ATLA = '.kb-fark, [class*="oniz"], svg, canvas, table, .pnl-menu, .pnl-top, .row-acts, [class*="onizleme"], .kb-tel, .kb-sosyal-kart, .kb-kirp, .kb-kirp-alan, .kb-takvim, .rte-govde, .ql-editor, [contenteditable], .kb-grafik, .kb-arac, .sa-form-tabs, .chips, .kb-kaydet, .sr-only, .kb-marka-onizleme, .kb-eposta-onizleme';
  var KONTROL = '.kb-cip, input, textarea, select, button, .btn, .ia-btn, .chip, .finput, .ftext, .fsel, .kb-tarih-btn, .kb-secenek, .kb-oran, .pstat, .kb-rozet, .ch-cnt, .avatar, .kb-avatar, label, a.btn';
  var BASLIK = 'h1, h2, h3, h4, h5, legend, .form-sec-tt, .pc-title, .kb-baslik, .ph-title';
  function px(win, ad, yedek){ var v = parseFloat(win.getComputedStyle(win.document.documentElement).getPropertyValue(ad)); return isNaN(v) ? yedek : v; }
  g.kbBoslukOlc = function(kok, win, et){
    var d = win.document, BLOK = px(win, '--b-3', 12), BAS = px(win, '--b-2', 8), sonuc = { yapisik: [], binme: [] }, gor = {};
    function seffaf(c){ return !c || c === 'transparent' || c === 'rgba(0, 0, 0, 0)'; }
    function gorunur(e){ return e && e.getClientRects().length && !e.closest('[hidden], template') && win.getComputedStyle(e).visibility !== 'hidden'; }
    function cs(e){ return win.getComputedStyle(e); }
    function zeminli(e){ var c = cs(e).backgroundColor; if(seffaf(c)) return false; var p = e.parentElement; while(p && seffaf(cs(p).backgroundColor)) p = p.parentElement; return !p || cs(p).backgroundColor !== c; }
    function kenar(e, y){ return parseFloat(cs(e)['border' + y + 'Width']) > 0 && cs(e)['border' + y + 'Style'] !== 'none'; }
    function cerceveli(e){ return kenar(e, 'Top') && kenar(e, 'Bottom') && kenar(e, 'Left') && kenar(e, 'Right'); }
    function blokMu(e){ var ds = cs(e).display; return ds !== 'inline' && ds !== 'contents' && ds !== 'none' && e.getBoundingClientRect().height > 4; }
    function tur(e){
      if(e.matches(BASLIK)) return 'baslik';
      if(e.matches(KONTROL)) return null;
      if(e.matches('.ptable-wrap')) return 'tablo';
      var r = e.getBoundingClientRect();
      if((zeminli(e) || cerceveli(e)) && r.width >= 120 && r.height >= 24) return 'kutu';
      if(e.matches('.form-sec, .frow, .form-grid, .toggle-row, fieldset, .kb-alan-grup')) return 'grup';
      if(kenar(e, 'Top') || kenar(e, 'Bottom')) return 'cizgi';
      var c = Array.prototype.filter.call(e.children, gorunur);
      if(c.length && c.every(function(x){ return x.matches('.btn, .ia-btn, a.btn, .kb-oran, .kb-secenek, .chip'); })) return 'dugme';
      return null;
    }
    /* görünen alt/üst kenarı veren öğe: kendisi blok değilse kenara yaslı çocuğuna iner */
    function inis(e, alt){
      var r0 = e.getBoundingClientRect()[alt ? 'bottom' : 'top'];
      for(var k = 0; k < 8 && e; k++){
        if(e.closest(ATLA) && k) return null;
        var t = tur(e); if(t) return { e: e, t: t };
        var c = alt ? e.lastElementChild : e.firstElementChild;
        while(c && !(gorunur(c) && blokMu(c) && cs(c).position !== 'absolute' && cs(c).position !== 'fixed')) c = alt ? c.previousElementSibling : c.nextElementSibling;
        if(!c || Math.abs(c.getBoundingClientRect()[alt ? 'bottom' : 'top'] - r0) > 1.5) return null;
        e = c;
      }
      return null;
    }
    function altKenar(x){ var r = x.e.getBoundingClientRect(); return (zeminli(x.e) || kenar(x.e, 'Bottom')) ? r.bottom : r.bottom - parseFloat(cs(x.e).paddingBottom || 0); }
    function ustKenar(x){ var r = x.e.getBoundingClientRect(); return (zeminli(x.e) || kenar(x.e, 'Top')) ? r.top : r.top + parseFloat(cs(x.e).paddingTop || 0); }
    function ad(e){ var c = (e.className && e.className.baseVal === undefined ? e.className : '').split(' ').filter(function(s){ return s && !/^is-/.test(s); })[0]; return c || (e.tagName.toLowerCase() + (e.parentElement ? '<' + ad(e.parentElement) : '')); }
    Array.prototype.forEach.call(kok.querySelectorAll('*'), function(e){
      if(!gorunur(e) || !blokMu(e) || e.closest(ATLA) || /^(absolute|fixed)$/.test(cs(e).position)) return;
      var p = e.previousElementSibling; while(p && !(gorunur(p) && blokMu(p) && !/^(absolute|fixed)$/.test(cs(p).position))) p = p.previousElementSibling;
      if(!p || p.closest(ATLA)) return;
      var pr = p.getBoundingClientRect(), er = e.getBoundingClientRect();
      if(er.top < pr.bottom - 2 && er.top < pr.top + pr.height / 2) return; /* yan yana (aynı satır) */
      if(er.left >= pr.right - 1 || er.right <= pr.left + 1) return;
      var A = inis(p, true), B = inis(e, false); if(!A || !B) return;
      if(A.t === 'grup' && B.t === 'grup' && !zeminli(A.e) && !zeminli(B.e) && !kenar(A.e, 'Bottom') && !kenar(B.e, 'Top')) { /* iki düz alan grubu: aralığı ızgara verir, yine ölçülür */ }
      var ar = A.e.getBoundingClientRect(), br = B.e.getBoundingClientRect();
      var tamBoy = Math.abs(ar.left - br.left) <= 2 && Math.abs(ar.right - br.right) <= 2;
      var cizgiyle = kenar(A.e, 'Bottom') || kenar(B.e, 'Top') || zeminli(A.e) || zeminli(B.e);
      if(tamBoy && cizgiyle && (A.t === 'cizgi' || B.t === 'cizgi' || A.t === 'tablo' || B.t === 'tablo')) return; /* kenardan kenara bitişik bölüm */
      var aralik = ustKenar(B) - altKenar(A);
      if(ad(A.e) === ad(B.e) && Math.abs(aralik) <= 1.5 && (kenar(A.e, 'Bottom') || kenar(B.e, 'Top'))) return; /* bitişik liste öğeleri */
      /* aynı türden tekrar eden kutular bir listedir: liste aralığı --b-2; alan grupları ve başlık dışı her şey blok aralığı */
      var ayni = ad(A.e) === ad(B.e) && A.t !== 'grup';
      var en = (A.t === 'baslik' || ayni) ? BAS : BLOK;
      var yer = (et || '') + ad(A.e) + ' → ' + ad(B.e) + ' (' + Math.round(aralik) + 'px) ⊂ ' + ad(e.parentElement);
      if(gor[yer]) return; gor[yer] = 1;
      if(aralik < -0.5) sonuc.binme.push(yer); else if(aralik < en - 0.5) sonuc.yapisik.push(yer);
    });
    return sonuc;
  };
  /* sayfa + her sekme + açılan her pencere/çekmece (en çok 10) */
  g.kbBoslukTara = function(d, win, ek){ /* ek(kok, win, et): her durumda çalışan ek ölçüm (yerlesim-olc.js kbDurumOlc) */
    var main = d.querySelector('.pnl-main') || d.body, top = { yapisik: [], binme: [], durum: 0, ek: [] };
    function ekle(s){ top.durum++; top.yapisik = top.yapisik.concat(s.yapisik); top.binme = top.binme.concat(s.binme); }
    function sekmeli(kok, on){
      ekle(g.kbBoslukOlc(kok, win, on)); if(ek) top.ek = top.ek.concat(ek(kok, win, on));
      var sk = Array.prototype.filter.call(kok.querySelectorAll('.sa-form-tab[data-panel]'), function(t){ return t.getClientRects().length && !t.closest('[hidden]'); });
      for(var z = 1; z < sk.length && z < 9; z++){ sk[z].click(); var on2 = on + 'sekme "' + sk[z].textContent.trim().replace(/\s+\d+$/, '').slice(0, 18) + '": '; ekle(g.kbBoslukOlc(kok, win, on2)); if(ek) top.ek = top.ek.concat(ek(kok, win, on2)); }
      if(sk.length > 1) sk[0].click();
    }
    sekmeli(main, '');
    var acilan = {}, tik = 0;
    Array.prototype.some.call(main.querySelectorAll('[data-tanim], [data-pencere], [data-sablon-ac]'), function(t){
      if(tik >= 10) return true; if(!t.getClientRects().length || t.closest('[hidden]') || t.disabled) return false;
      var anahtar = (t.getAttribute('data-tanim') || t.getAttribute('data-pencere') || t.getAttribute('data-sablon-ac') || '').replace(/-[^-]*$/, '');
      if(acilan[anahtar]) return false; acilan[anahtar] = 1; tik++;
      function aciklar(){ return Array.prototype.filter.call(d.querySelectorAll('.kb-cekmece, .kb-pencere, .sa-modal-ov, [class$="-ov"]'), function(x){ return !x.hidden && (x.matches('.kb-cekmece, .kb-pencere') || x.classList.contains('open')); }); }
      var once = aciklar();
      try{ t.click(); }catch(x){ return false; }
      var k = aciklar().filter(function(x){ return once.indexOf(x) < 0; }).pop();
      if(k){ k.classList.add('open'); var b = k.querySelector('h2, h3, .kc-baslik, .pc-title'); sekmeli(k, 'pencere "' + (b ? b.textContent.trim().slice(0, 18) : anahtar) + '": '); }
      if(win.kbKapat) try{ win.kbKapat(); }catch(x){}
      d.dispatchEvent(new win.KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
      Array.prototype.forEach.call(d.querySelectorAll('.kb-cekmece, .kb-pencere, .sa-modal-ov'), function(x){ x.classList.remove('open'); if(!x.classList.contains('sa-modal-ov')) x.hidden = true; }); /* kapanış gecikmesini bekleme: aynı kap yeniden açılınca yeni sayılsın */
      return false;
    });
    return top;
  };
})(window);
