/* Yerleşim ölçümleri — araclar/denetim.html ve araclar/duyarli.html ortak kullanır. Her biri gerçek tarayıcıda ölçer.
   kbDurumOlc(kok, win, et): her durumda (sayfa, sekme, açık pencere) çalışır → [ 'kural: mesaj', … ]
     · secenek-yalniz  — seçenek grubunda son satırda tek kutu kalmış (KURAL · seçenek grubu)
     · secenek-satir   — çok seçimli grup iki satırı aşmış, açılır listeye dönmemiş
   kbSayfaOlc(d, win): sayfa başına bir kez → [ … ]
     · sayfalama       — listede çekirdek sayfalaması yok, çok satırlı değil, ya da "sonraki" çalışmıyor (KURAL · sayfalama)
     · yapiskan        — sağ sütun yapışkanken üst bar ya da kaydet çubuğunun altına giriyor; sütun içinde kart kartın altından akıyor */
(function(g){
  function gor(e, win){ return e && e.getClientRects().length && !e.closest('[hidden], template') && win.getComputedStyle(e).visibility !== 'hidden'; }
  g.kbDurumOlc = function(kok, win, et){
    var out = [], on = et || '';
    Array.prototype.forEach.call(kok.querySelectorAll('.kb-secenek-grup, .ket-kategori, [data-secenek-grup]'), function(G){
      if(!gor(G, win) || G.classList.contains('is-acilir') || G.closest('.kb-arac, .kb-arac-filtre-pen, [data-secenek-serbest], [class*="oniz"]')) return;
      var og = Array.prototype.filter.call(G.children, function(c){ return c.tagName === 'LABEL' && gor(c, win); }); if(og.length < 2) return;
      var sat = {}; og.forEach(function(o){ var t = Math.round(o.getBoundingClientRect().top); sat[t] = (sat[t] || 0) + 1; });
      var k = Object.keys(sat).map(Number).sort(function(a, b){ return a - b; });
      if(k.length > 1 && sat[k[k.length - 1]] === 1 && og.length > 2 && !G.classList.contains('is-alt-alta')) out.push('secenek-yalniz: ' + on + '"' + (og[og.length - 1].textContent || '').trim().replace(/\s+/g, ' ').slice(0, 24) + '" son satırda yalnız (' + og.length + ' seçenek, ' + k.length + ' satır)');
      var cok = og[0].querySelector('input[type=checkbox]');
      if(cok && k.length > 2 && !G.classList.contains('is-alt-alta')) out.push('secenek-satir: ' + on + og.length + ' seçenek ' + k.length + ' satıra yayılmış, açılır listeye dönmemiş');
    });
    /* kesik: taşmayı gizleyen kutu (overflow hidden/clip) içeriğini kesiyor — bilerek kısaltma (… , satır sınırı) ve kaydırma kapları hariç.
       Örnek: şifre güç çubuğu 6 px'lik liste satırıydı, satır simgesi içinde kesik görünüyordu (eski ölçüm yalnız metin sınıflarına bakıyordu). */
    var KES_ATLA = '[class*="oniz"], .kb-kirp, .kb-kirp-alan, .ptable-wrap, .kb-editor, .ql-editor, [contenteditable], .kb-takvim, .pnl-menu, .chips, .kb-arac, svg, canvas, .kb-grafik, .sr-only, .kb-tel, .kb-sosyal-kart, .kmo-kutu, .kg-resim, .kb-medya, .kb-avatar, .avatar';
    Array.prototype.forEach.call(kok.querySelectorAll('*'), function(e){
      if(!gor(e, win) || e.closest(KES_ATLA)) return;
      var cs = win.getComputedStyle(e); if(!/hidden|clip/.test(cs.overflowY + cs.overflowX)) return;
      if(cs.textOverflow === 'ellipsis' || cs.webkitLineClamp !== 'none' && cs.webkitLineClamp || /auto|scroll/.test(cs.overflowY + cs.overflowX)) return;
      if(e.matches('img, video, iframe, input, textarea, select, progress, [style*="background-image"]') || cs.backgroundImage !== 'none' && !e.children.length) return;
      if(!e.childNodes.length && !win.getComputedStyle(e, '::before').content.replace(/none|normal|""/g, '') && !win.getComputedStyle(e, '::after').content.replace(/none|normal|""/g, '')) return;
      var r = e.getBoundingClientRect(); if(r.height < 2 || r.width < 2) return;
      /* yalnız akıştaki içerik sayılır: bilerek kırpılan süs (mutlak konumlu çocuk ya da ::after dairesi) taşma değildir */
      var akis = Array.prototype.filter.call(e.children, function(x){ var s = win.getComputedStyle(x); return gor(x, win) && !/absolute|fixed/.test(s.position); });
      var tasar = false, ust = r.top + parseFloat(cs.borderTopWidth), alt = r.bottom - parseFloat(cs.borderBottomWidth);
      if(akis.length) tasar = akis.some(function(x){ var q = x.getBoundingClientRect(); return q.bottom > alt + 1.5 || q.top < ust - 1.5; });
      else { var pb = win.getComputedStyle(e, '::before'), pa = win.getComputedStyle(e, '::after'); var sahte = (pb.content !== 'none' && pb.position === 'absolute') || (pa.content !== 'none' && pa.position === 'absolute');
        tasar = !sahte && e.scrollHeight > e.clientHeight + 2; }
      if(tasar && parseFloat(cs.maxHeight) !== e.clientHeight){
        var ps = win.getComputedStyle(e, '::before').content; var tx = (e.textContent || '').trim().slice(0, 22) || (ps && ps !== 'none' ? 'simge (::before)' : e.className.split(' ')[0]);
        out.push('kesik: ' + on + (e.className && typeof e.className === 'string' ? e.className.split(' ')[0] : e.tagName.toLowerCase()) + ' içeriği kesiliyor (' + e.scrollHeight + ' > ' + e.clientHeight + 'px) "' + tx + '"');
      }
    });
    /* binme: akıştaki kardeş öğeler üst üste (negatif boşluk, sabit yükseklikli kutuya sığmayan satır) */
    Array.prototype.forEach.call(kok.querySelectorAll('*'), function(P){
      if(!gor(P, win) || P.closest(KES_ATLA) || P.children.length < 2) return;
      var ds = win.getComputedStyle(P).display; if(/inline|table|grid|contents/.test(ds) && ds !== 'block') { if(!/^flex$/.test(ds)) return; if(win.getComputedStyle(P).flexDirection.indexOf('column') < 0) return; }
      var c = Array.prototype.filter.call(P.children, function(x){ var s = win.getComputedStyle(x); return gor(x, win) && !/absolute|fixed|sticky/.test(s.position) && s.float === 'none' && !x.matches('input, code, kbd') && x.getBoundingClientRect().height > 2; });
      for(var i = 1; i < c.length; i++){
        var a = c[i - 1].getBoundingClientRect(), b = c[i].getBoundingClientRect();
        if(b.left >= a.right - 1 || b.right <= a.left + 1) continue;
        if(b.top < a.bottom - 2 && b.top > a.top + 2){ out.push('binme: ' + on + (c[i - 1].className && typeof c[i - 1].className === 'string' ? c[i - 1].className.split(' ')[0] : c[i - 1].tagName.toLowerCase()) + ' ile sonraki öğe ' + Math.round(a.bottom - b.top) + 'px üst üste'); break; }
      }
    });
    /* HİZA (Beyar): (a) tekrarlayan satırlarda aynı görevdeki öğenin sol kenarı ve dikey konumu satırlar arasında aynı;
       (c) yan yana form alanlarında etiket ve kutu üst kenarı aynı; (d) kart başlığı ile kart içeriği aynı sol çizgide. Tolerans 1 px. */
    function ad(e){ return (e.className && typeof e.className === 'string' ? e.className.split(' ').filter(function(s){ return s && !/^is-|^has-/.test(s); })[0] : '') || e.tagName.toLowerCase(); }
    var HIZA_ATLA = KES_ATLA + ', .kb-cip-girdi, .kit-satir, .kit-satirlar, .kit-iki, table, .chips, .kb-secenek-grup, .ket-kategori, .is-bolmeli, .is-kutu, .pager, .kb-arac, .row-acts, .ph-actions, .kb-takvim, .kb-kanallar';
    Array.prototype.forEach.call(kok.querySelectorAll('*'), function(P){
      if(!gor(P, win) || P.closest(HIZA_ATLA) || P.children.length < 3) return;
      var ds = win.getComputedStyle(P).display; if(ds === 'grid' && win.getComputedStyle(P).gridTemplateColumns.split(' ').length > 1) return; /* çok sütunlu ızgara: kartlar yan yana */
      var R = Array.prototype.filter.call(P.children, function(x){ return gor(x, win) && !/absolute|fixed/.test(win.getComputedStyle(x).position); });
      if(R.length < 3) return; var rk = ad(R[0]); R = R.filter(function(x){ return ad(x) === rk; }); if(R.length < 3) return;
      var L0 = R[0].getBoundingClientRect().left; if(R.some(function(x){ return Math.abs(x.getBoundingClientRect().left - L0) > 1; })) return; /* satırlar alt alta değil */
      if(R.some(function(x){ var s = win.getComputedStyle(x); if(/flex/.test(s.display)) return s.flexDirection.indexOf('column') > -1; if(/grid/.test(s.display)) return s.gridTemplateColumns.split(' ').length < 2; return true; })) return; /* yalnız yatay satır (flex satır ya da çok sütunlu ızgara) */
      var sol = {}, dik = {};
      R.forEach(function(x){
        var xr = x.getBoundingClientRect(), say = {}, ai = win.getComputedStyle(x).alignItems;
        Array.prototype.forEach.call(x.children, function(c){ if(!gor(c, win) || /absolute|fixed/.test(win.getComputedStyle(c).position)) return; var k = ad(c); say[k] = (say[k] || 0) + 1; });
        Array.prototype.forEach.call(x.children, function(c){ if(!gor(c, win) || /absolute|fixed/.test(win.getComputedStyle(c).position)) return; var k = ad(c); if(say[k] !== 1) return; var cr = c.getBoundingClientRect();
          var esnek = parseFloat(win.getComputedStyle(c).flexGrow) > 0 || /grid/.test(win.getComputedStyle(x).display) && win.getComputedStyle(c).justifySelf !== 'end';
          var v3 = [cr.left - xr.left, xr.right - cr.right, (cr.left + cr.right) / 2 - (xr.left + xr.right) / 2]; v3.esnek = parseFloat(win.getComputedStyle(c).flexGrow) > 0; (sol[k] = sol[k] || []).push(v3);
          if(cr.height < xr.height - 2) (dik[k] = dik[k] || []).push(ai === 'center' ? (cr.top + cr.height / 2) - (xr.top + xr.height / 2) : cr.top - xr.top); });
      });
      Object.keys(sol).forEach(function(k){ var v = sol[k]; if(v.length < 3) return; /* sola, sağa ya da ortaya yaslı: üçünden biri tutarlıysa hizalı */
        /* büyüyen (flex-grow) öğede sağ/orta hizası kendiliğinden tutar: yalnız sol kenar sayılır */
        var s = Math.min.apply(null, (v.some(function(x){ return x.esnek; }) ? [0] : [0, 1, 2]).map(function(j){ var a = v.map(function(x){ return x[j]; }); return Math.max.apply(null, a) - Math.min.apply(null, a); }));
        if(s > 1.5) out.push('hiza: ' + on + rk + ' satırlarında .' + k + ' kenarı ' + Math.round(s) + 'px sapıyor'); });
      Object.keys(dik).forEach(function(k){ var v = dik[k]; if(v.length < 3) return; var s = Math.max.apply(null, v) - Math.min.apply(null, v); if(s > 1.5) out.push('hiza: ' + on + rk + ' satırlarında .' + k + ' dikey konumu ' + Math.round(s) + 'px sapıyor'); });
    });
    /* (c) yan yana form alanları */
    Array.prototype.forEach.call(kok.querySelectorAll('.form-grid, .frow.two, .kb-iki, .sc-stack'), function(G){
      if(!gor(G, win) || G.closest(KES_ATLA)) return;
      var F = Array.prototype.filter.call(G.children, function(x){ return gor(x, win) && x.classList.contains('frow'); }), sat = {};
      /* aynı görsel satır: üst kenarları birbirine 16 px'ten yakın ve yan yana (yatayda örtüşmeyen) alanlar */
      var satL = []; F.forEach(function(x){ var r = x.getBoundingClientRect(), s = satL.filter(function(g){ var q = g[0].getBoundingClientRect(); return Math.abs(q.top - r.top) < 16 && (r.left >= q.right - 1 || r.right <= q.left + 1); })[0]; if(s) s.push(x); else satL.push([x]); });
      satL.forEach(function(g, i){ sat[i] = g; });
      Object.keys(sat).forEach(function(k){ var s = sat[k]; if(s.length < 2) return;
        var et = s.map(function(x){ var l = x.querySelector(':scope > label, :scope > .flabel'); return l ? l.getBoundingClientRect().top : null; }).filter(function(v){ return v !== null; });
        var ku = s.map(function(x){ var c = x.querySelector(':scope > input, :scope > textarea, :scope > select, :scope > .kb-secim, :scope > .kb-tarih-sec, :scope > .kb-cip-girdi, :scope > .kb-sifre, :scope > .kb-tel, :scope > div > .finput'); return c ? c.getBoundingClientRect().top : null; }).filter(function(v){ return v !== null; });
        if(et.length > 1 && Math.max.apply(null, et) - Math.min.apply(null, et) > 1.5) out.push('hiza: ' + on + 'yan yana alanlarda etiket üst kenarı ' + Math.round(Math.max.apply(null, et) - Math.min.apply(null, et)) + 'px farklı (' + s.map(function(x){ var l = x.querySelector(':scope > label, :scope > .flabel'); return l ? l.textContent.trim().slice(0, 14) : '?'; }).join(' / ') + ')');
        if(ku.length > 1 && Math.max.apply(null, ku) - Math.min.apply(null, ku) > 1.5) out.push('hiza: ' + on + 'yan yana alanlarda kutu üst kenarı ' + Math.round(Math.max.apply(null, ku) - Math.min.apply(null, ku)) + 'px farklı');
      });
    });
    /* (d) kart başlığı ile içerik aynı sol çizgide */
    Array.prototype.forEach.call(kok.querySelectorAll('.pnl-card'), function(C){
      if(!gor(C, win) || C.closest(KES_ATLA)) return;
      var h = C.querySelector(':scope > .pc-head .pc-title'), b = C.querySelector(':scope > .pc-body'); if(!h || !b || !gor(b, win)) return;
      var bs = win.getComputedStyle(b), icSol = b.getBoundingClientRect().left + parseFloat(bs.paddingLeft) + parseFloat(bs.borderLeftWidth);
      var hs = h.getBoundingClientRect().left;
      if(Math.abs(hs - icSol) > 1.5 && parseFloat(bs.paddingLeft) > 0) out.push('hiza: ' + on + 'kart "' + h.textContent.trim().slice(0, 18) + '" başlığı ile içeriği ' + Math.round(hs - icSol) + 'px farklı sol çizgide');
    });
    /* YAZIM (Beyar): etiket, bölüm/kart başlığı, sekme, düğme, menü öğesi, pencere başlığı, seçenek adı → Her Kelimenin Baş Harfi Büyük.
       Bağlaç ve edatlar küçük (ve, ya da, ile, için, veya…). Açıklama, ipucu, bildirim, tablo içeriği cümle düzeninde (ölçülmez).
       Yalnız öğenin kendi metni okunur (içindeki <small>, sayaç, açıklama hariç). 7 kelimeden uzun etiket cümle sayılır (kararsız, ayrı listelenir). */
    var BAGLAC = ['ve', 'ya', 'da', 'de', 'ile', 'için', 'veya', 'ki', 'mi', 'mı', 'mu', 'mü', 'gibi', 'kadar', 'göre', 'ama', 'yoksa']; /* bağlaç ve edat */
    var YZ = 'label:not(.kb-secenek):not(.toggle):not(.kb-onay):not(.ket-kat), .flabel, .form-sec-tt, .pc-title, .pnl-main h1, .kb-kap-bas h2, .sa-modal h2, .sa-form-tab, .btn, .pnl-menu a, .pnl-menu button, .kb-secenek, .chip[data-sekme], .kb-platform, .toggle-row > span';
    function kendiMetin(e){ var s = ''; Array.prototype.forEach.call(e.childNodes, function(n){ if(n.nodeType === 3) s += n.textContent; else if(n.nodeType === 1 && /^(B|STRONG|EM)$/.test(n.tagName) && !n.matches('.ch-cnt, .ks-say, .sd-say, small, .kb-sag, .fdil, .zorunlu, .kp-isaret, .sr-only, .kb-rozet, .pstat, [class*="say"]') && !n.children.length) s += n.textContent; }); return s.replace(/\s+/g, ' ').trim(); }
    Array.prototype.forEach.call(kok.querySelectorAll(YZ), function(e){
      if(!gor(e, win) || e.closest('[class*="oniz"], .kb-sosyal-kart, .ksp, .kb-telefon, .kb-editor, .kb-takvim, .kit-kod, code, .kb-log, .pager, .ptable td, .kb-dosya, .kb-yukle')) return; /* sürükle-bırak alanındaki yönerge cümledir */
      var m = kendiMetin(e); if(!m || m.length < 2) return;
      var k = m.split(' ').filter(Boolean); if(k.length > 7) return; /* cümle */
      if(k.length > 4 && e.matches('.kb-secenek, .chip, .pnl-menu a, .pnl-menu button')) return; /* seçenek olarak duran içerik (haber başlığı, kayıt adı) veridir */
      var kotu = k.filter(function(w, i){
        var c = w.replace(/^[("“'«]+/, ''); if(!c) return false; var h = c.charAt(0);
        if(!/[a-zçğıöşü]/.test(h)) return false; /* büyük, rakam, simge */
        if(/[A-ZÇĞİÖŞÜ]/.test(c.slice(1))) return false; /* iOS gibi özel yazım */
        if(/^(https?:|@|#|www\.)/.test(c) || /[a-z]\.[a-z]/i.test(c)) return false; /* adres, alan adı, tutamaç */
        if(i > 0 && BAGLAC.indexOf(c.replace(/[),.:;!?"”']+$/, '').toLocaleLowerCase('tr')) > -1) return false;
        if(i > 0 && /^[·•\-–—|/]$/.test(k[i - 1])) return false; /* "· ölçü" gibi ek bilgi */
        return true; });
      if(kotu.length){ out.push('yazim: ' + on + '"' + m.slice(0, 40) + '" (' + kotu.slice(0, 3).join(', ') + ')'); (g.kbYazimTam = g.kbYazimTam || []).push(m); }
    });
    return out;
  };
  /* AÇILAN KUTULAR (Beyar): sayfadaki bütün açılır kutular gerçekten açılır ve ölçülür — açılır liste, tarih ve tarih aralığı, Filtreler,
     ⋯ menüsü, renk seçici. Kural: kutu görünür alanın içinde; üst barın ve kaydet çubuğunun üstüne binmez; içindekiler kesilmez. */
  g.kbAcilirOlc = function(d, win, sinir){
    var out = [], W = d.documentElement.clientWidth, H = win.innerHeight, n = 0;
    var ust = d.querySelector('.pnl-top'), ub = ust ? ust.getBoundingClientRect().bottom : 0;
    var tet = Array.prototype.filter.call(d.querySelectorAll('.pnl-main [data-acilir], .pnl-main [data-diger], .pnl-main [data-renk-ac]'), function(b){ return gor(b, win) && !b.disabled; });
    var gorulen = {};
    tet.slice(0, sinir || 40).forEach(function(b){
      var anahtar = b.getAttribute('data-acilir') || (b.hasAttribute('data-diger') ? 'diger' : 'renk'); if(gorulen[anahtar]) return; gorulen[anahtar] = 1;
      d.documentElement.style.scrollBehavior = 'auto';
      win.scrollTo(0, Math.max(0, b.getBoundingClientRect().top + win.scrollY - H * 0.62)); /* tetik ekranın alt kısmında: en zor durum */
      try{ b.click(); }catch(x){ return; }
      var m = b.getAttribute('data-acilir') ? d.getElementById(b.getAttribute('data-acilir')) : (b.hasAttribute('data-diger') ? d.querySelector('.kb-diger-menu.open') : d.querySelector('.kb-renk-pop.open'));
      if(!m || !m.classList.contains('open')){ d.body.click(); return; }
      m.style.transition = 'none'; m.style.opacity = '1'; m.style.transform = 'none';
      if(win.kbAcilirSigdir) win.kbAcilirSigdir(m, b); n++;
      var r = m.getBoundingClientRect(), ad = '"' + ((b.getAttribute('aria-label') || b.textContent || anahtar).trim().replace(/\s+/g, ' ').slice(0, 20)) + '"';
      if(r.width && (r.left < -1 || r.right > W + 1)) out.push('acilir: ' + ad + ' kutusu ekrandan yatay taşıyor (' + Math.round(r.left) + '…' + Math.round(r.right) + ' / ' + W + ')');
      var kk = Array.prototype.filter.call(d.querySelectorAll('.kb-kaydet'), function(k){ var q = k.getBoundingClientRect(); return q.height && q.top < H && win.getComputedStyle(k).position === 'sticky'; })[0];
      var alt = kk ? kk.getBoundingClientRect().top : H;
      if(!b.closest('.pnl-top') && r.height && r.top < ub - 1) out.push('acilir: ' + ad + ' kutusu üst barın altına giriyor');
      if(r.height && r.bottom > alt + 1 && !b.closest('.kb-kaydet')) out.push('acilir: ' + ad + ' kutusu ' + (kk ? 'kaydet çubuğunun' : 'ekranın') + ' altına giriyor (' + Math.round(r.bottom - alt) + 'px)');
      /* içerik kesilmesi: kutunun içindeki bir öğe kutunun sağından taşıyor ya da kutu yatayda kırpıyor */
      var tas = Array.prototype.filter.call(m.querySelectorAll('*'), function(e){ var q = e.getBoundingClientRect(); return gor(e, win) && q.width && q.right > r.right + 1 && !/fixed/.test(win.getComputedStyle(e).position); })[0];
      if(tas) out.push('acilir: ' + ad + ' kutusunda "' + (tas.textContent || tas.className).trim().slice(0, 18) + '" kesiliyor');
      d.dispatchEvent(new win.KeyboardEvent('keydown', { key: 'Escape', bubbles: true })); d.body.click(); m.classList.remove('open'); m.style.transition = m.style.opacity = m.style.transform = '';
    });
    win.scrollTo(0, 0);
    out.n = n; return out;
  };
  g.kbSayfaOlc = function(d, win){
    var out = [];
    var h1 = d.querySelector('.pnl-main .pnl-page-head h1'), k1 = Array.prototype.filter.call(d.querySelectorAll('.pnl-main .pnl-card, .pnl-main .kb-bant, .pnl-main .form-layout'), function(x){ return gor(x, win) && !x.parentElement.closest('.pnl-card'); })[0];
    if(h1 && k1 && gor(h1, win) && Math.abs(h1.getBoundingClientRect().left - k1.getBoundingClientRect().left) > 1.5) out.push('hiza: sayfa başlığı ile içerik ' + Math.round(h1.getBoundingClientRect().left - k1.getBoundingClientRect().left) + 'px farklı sol çizgide');
    /* YENİ KAYIT BOŞ AÇILIR (Beyar): ?yeni=1 ekranında formda örnek veri kalmaz — dolu metin alanı, seçili çip, örnek satır.
       Sistemin doldurduğu değer (oturumdaki yazar, varsayılan) [data-yeni-kalir] ile işaretlenir; anahtar ve seçenekler sayılmaz. */
    if(/[?&]yeni=1/.test(win.location.search)){
      var F = d.querySelector('[data-form]') || d.querySelector('.pnl-main'), dolu = [];
      Array.prototype.forEach.call(F.querySelectorAll('input.finput, textarea.ftext, .kz-alan'), function(e){
        if(!gor(e, win) || e.closest('[data-yeni-kalir], [hidden], .kb-kap-govde, [data-ai-grup].is-ai') || e.hasAttribute('data-yeni-kalir') || e.readOnly) return;
        var v = (e.value != null ? e.value : e.textContent).trim(); if(v) dolu.push((e.getAttribute('aria-label') || e.id || 'alan') + ': "' + v.slice(0, 24) + '"'); });
      Array.prototype.forEach.call(F.querySelectorAll('.kb-cip-girdi .kb-cip, [data-sirali-havuz] .km-satir, [data-satir-liste] > .km-satir'), function(e){ if(gor(e, win) && !e.closest('[data-yeni-kalir]')) dolu.push('örnek ' + (e.classList.contains('kb-cip') ? 'çip' : 'satır') + ' "' + (e.textContent || '').trim().slice(0, 20) + '"'); });
      if(dolu.length) out.push('yeni-dolu: yeni kayıt ekranında örnek veri: ' + dolu.slice(0, 3).join(' · ') + (dolu.length > 3 ? ' (+' + (dolu.length - 3) + ')' : ''));
    }
    /* sayfalama */
    Array.prototype.forEach.call(d.querySelectorAll('[data-liste], [data-kart-liste]'), function(L){
      if(!gor(L, win) || L.dataset.gorunum === 'takvim') return;
      var ad = '"' + (L.dataset.listeAd || L.id || 'liste') + '"', P = L.querySelector('.kb-sayfala');
      if(!P){ out.push('sayfalama: ' + ad + ' listesinde çekirdek sayfalaması yok'); return; }
      var pr = P.getBoundingClientRect(); if(pr.height > 76) out.push('sayfalama: ' + ad + ' sayfalama satırı tek satır değil (' + Math.round(pr.height) + 'px)');
      if(P.classList.contains('is-tek')) return;
      var bilgi = P.querySelector('.pi-uzun').textContent, ilk = Array.prototype.filter.call(L.querySelectorAll('tr[data-satir], [data-kart]'), function(r){ return !r.hidden; })[0];
      var s = P.querySelector('[data-pg="sonraki"]'); if(!s || s.disabled){ out.push('sayfalama: ' + ad + ' çok sayfa var ama "sonraki" pasif'); return; }
      s.click();
      var ilk2 = Array.prototype.filter.call(L.querySelectorAll('tr[data-satir], [data-kart]'), function(r){ return !r.hidden; })[0];
      if(P.querySelector('.pi-uzun').textContent === bilgi || ilk2 === ilk) out.push('sayfalama: ' + ad + ' "sonraki" sayfayı değiştirmiyor');
      var i0 = P.querySelector('[data-pg="ilk"]'); if(i0 && !i0.disabled) i0.click();
    });
    /* yapışkan sağ sütun: birkaç kaydırma konumunda */
    var sc = Array.prototype.filter.call(d.querySelectorAll('.side-card'), function(s){ return gor(s, win); })[0];
    if(sc){
      var ust = d.querySelector('.pnl-top'), ub = ust ? ust.getBoundingClientRect().bottom : 64, kk = Array.prototype.filter.call(d.querySelectorAll('.kb-kaydet'), function(k){ return gor(k, win) && win.getComputedStyle(k).position === 'sticky'; })[0];
      var eskiY = win.scrollY, H = d.documentElement.scrollHeight - win.innerHeight;
      d.documentElement.style.scrollBehavior = 'auto';
      [0.25, 0.5, 0.75, 1].forEach(function(f){
        win.scrollTo(0, Math.round(H * f));
        var r = sc.getBoundingClientRect(), yap = win.getComputedStyle(sc).position === 'sticky';
        if(yap && r.top >= ub - 1){ var kt = kk ? kk.getBoundingClientRect().top : win.innerHeight; if(r.bottom > kt + 1 && r.top < kt) out.push('yapiskan: sağ sütun kaydet çubuğunun altına giriyor (' + Math.round(r.bottom - kt) + 'px, kaydırma %' + Math.round(f * 100) + ')'); }
        var c = Array.prototype.filter.call(sc.children, function(x){ return gor(x, win); });
        for(var i = 1; i < c.length; i++){ var a = c[i - 1].getBoundingClientRect(), b = c[i].getBoundingClientRect(); if(b.top < a.bottom - 1 && b.bottom > a.top + 1){ out.push('yapiskan: sağ sütunda kart kartın altından akıyor (kaydırma %' + Math.round(f * 100) + ')'); break; } }
      });
      win.scrollTo(0, eskiY);
    }
    return out.filter(function(x, i){ return out.indexOf(x) === i; });
  };
})(window);
