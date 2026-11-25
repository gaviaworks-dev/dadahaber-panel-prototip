/* Dada Haber Yönetim Paneli — görsel kırpma penceresi (çekirdek bileşen)
   Kullanım:
     <button data-kirp-ac [data-kirp-oran="web.detay"]> — en yakın [data-gorsel-alan] kabının görseliyle açılır.
     window.kbKirp({ gorsel, odak:{x,y}, oranlar:[…], secili, tamam:function(sonuc){} })
   Model: bir odak noktası bütün oranları hizalar. Editör bir oranı elle düzeltirse o oran "düzeltildi" olur ve
   odak değişse de yerinde kalır. Her oran "kırpmadan kullan" ile bütün görseli (bulanık zeminle) gösterebilir.
   Sonuç: { odak:{x,y}, oranlar:{ id:{x,y,g,y2,kirpmasiz} } } — x,y sol üst köşe, g genişlik (görsele oranla 0–1).
   Ölçüler modül kaydından gelir (PANEL.gorsel_alanlari, PANEL.sosyal_oranlar). */
(function(){
  'use strict';
  var P = window.PANEL || {};
  function oranSayi(s){ if(s === 'serbest') return null; var m = String(s).split(':'); return +m[0] / +(m[1] || 1); }

  /* kayıttan varsayılan oran listesi: modülün görsel alanı + sosyal medya oranları */
  /* alan kendi oranlarını taşıyabilir: data-kirp-oranlar="id=Ad=16:10=400×250;…" */
  function alanOranlari(s){
    return s.split(';').map(function(x){ var p = x.split('='), px = (p[3] || '').split('×').map(Number); return { id: p[0], grup: 'Bu alan', ad: p[1], oran: p[2], px: px[1] ? px : null }; });
  }
  function varsayilanOranlar(alanAnahtar){
    var parca = (alanAnahtar || 'haberler.kapak').split('.'), alan = ((P.gorsel_alanlari || {})[parca[0]] || {})[parca[1]] || {};
    var liste = [];
    ['web', 'mobil'].forEach(function(grup){
      Object.keys(alan[grup] || {}).forEach(function(k){
        var o = alan[grup][k];
        liste.push({ id: grup + '.' + k, grup: grup === 'web' ? 'Web' : 'Mobil', ad: (grup === 'web' ? 'Web ' : 'Mobil ') + (k === 'detay' ? 'detay' : 'kart'), oran: o.oran, px: o.px });
      });
    });
    if(alan.bildirim) liste.push({ id: 'bildirim', grup: 'Bildirim', ad: 'Bildirim Görseli', oran: alan.bildirim.oran, px: alan.bildirim.px || [1024, 512] });
    (P.sosyal_oranlar || []).forEach(function(o){ liste.push({ id: 'sosyal.' + o.oran, grup: 'Sosyal Medya', ad: 'Sosyal ' + o.oran, oran: o.oran, px: o.px }); });
    if((P.sosyal_oranlar || []).length) liste.push({ id: 'sosyal.serbest', grup: 'Sosyal Medya', ad: 'Sosyal serbest', oran: 'serbest', px: null });
    return liste;
  }

  var ov, durum;
  function kur(){
    ov = document.createElement('div'); ov.className = 'kb-kirp-ov';
    ov.innerHTML = ''
      + '<div class="kb-kirp" role="dialog" aria-modal="true" aria-labelledby="kbKirpBas">'
      + '<div class="kb-kap-bas"><div><h2 id="kbKirpBas">Görseli kırp</h2><div class="kb-kap-alt" data-kp-bilgi></div></div><button type="button" class="kb-kapat" data-kp-kapat aria-label="Kapat"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button></div>'
      + '<div class="kp-govde">'
      + '  <div class="kp-sol">'
      + '    <div class="kp-arac">'
      + '      <div class="kp-kip" role="group" aria-label="Düzenleme biçimi"><button type="button" class="is-on" data-kp-kip="odak" aria-pressed="true"><i class="fa-solid fa-crosshairs" aria-hidden="true"></i>Odak noktası</button><button type="button" data-kp-kip="cerceve" aria-pressed="false"><i class="fa-solid fa-crop-simple" aria-hidden="true"></i>Bu oranı düzelt</button></div>'
      + '      <span class="kp-ipucu" data-kp-ipucu></span>'
      + '    </div>'
      + '    <div class="kp-sahne" data-kp-sahne><div class="kp-resim" data-kp-resim></div><div class="kp-cerceve" data-kp-cerceve><i></i><i></i><i></i><i></i><span class="kp-tutamac" data-kp-tutamac hidden></span><span class="kp-etk" data-kp-etk></span></div><span class="kp-odak" data-kp-odak></span></div>'
      + '    <div class="kp-alt-arac">'
      + '      <label class="kp-yakin"><i class="fa-solid fa-magnifying-glass-minus" aria-hidden="true"></i><input type="range" min="1" max="3" step="0.01" value="1" data-kp-yakin aria-label="Yakınlaştırma"><i class="fa-solid fa-magnifying-glass-plus" aria-hidden="true"></i><b data-kp-yakin-deger>%100</b></label>'
      + '      <label class="kp-kirpmasiz"><input type="checkbox" data-kp-kirpmasiz> Kırpmadan kullan<small>bütün görsel sığdırılır, kenarlar görselle dolar</small></label>'
      + '      <button type="button" class="btn btn-ghost btn-sm" data-kp-sifirla><i class="fa-solid fa-rotate-left" aria-hidden="true"></i>Bu oranı sıfırla</button>'
      + '    </div>'
      + '  </div>'
      + '  <div class="kp-sag">'
      + '    <div class="kp-bolum-tt">Oranlar<button type="button" class="kb-bag" data-kp-hepsi>Hepsini odağa hizala</button></div>'
      + '    <div class="kp-oranlar" data-kp-oranlar role="listbox" aria-label="Oranlar"></div>'
      + '    <div class="kp-bolum-tt" data-kp-onizle-tt>Canlı önizleme</div>'
      + '    <div class="kp-onizle">'
      + '      <figure class="kpo-site"><div class="kpo-gorsel" data-kp-onizle="web.kart"></div><figcaption><span class="kpo-kat">Gündem</span><b data-kp-baslik></b></figcaption><small>Sitede kart</small></figure>'
      + '      <figure class="kpo-mobil"><div class="kpo-tel"><div class="kpo-gorsel" data-kp-onizle="mobil.kart"></div><b data-kp-baslik></b><span></span><span></span></div><small>Mobil kart</small></figure>'
      + '      <figure class="kpo-sosyal"><div class="kpo-sos-bas"><span class="kpo-ava"></span><b>Dada Haber</b><i class="fa-brands fa-x-twitter" aria-hidden="true"></i></div><div class="kpo-gorsel" data-kp-onizle="sosyal"></div><small data-kp-sosyal-etk>Sosyal kart</small></figure>'
      + '    </div>'
      + '  </div>'
      + '</div>'
      + '<div class="kb-kap-alt-cubuk"><span class="kb-sol kp-ozet" data-kp-ozet></span><button type="button" class="btn btn-acc btn-sm" data-kp-tamam><i class="fa-solid fa-check" aria-hidden="true"></i>Uygula</button></div>'
      + '</div>';
    document.body.appendChild(ov);

    var sahne = ov.querySelector('[data-kp-sahne]'), cer = ov.querySelector('[data-kp-cerceve]'), odak = ov.querySelector('[data-kp-odak]');
    ov.addEventListener('click', function(e){
      if(e.target === ov || e.target.closest('[data-kp-kapat]')){ kapat(); return; }
      var k = e.target.closest('[data-kp-kip]'); if(k){ kipSec(k.dataset.kpKip); return; }
      if(e.target.closest('[data-kp-diger]')){ durum.digerAcik = !durum.digerAcik; if(!durum.digerAcik && !/^(web|mobil)\./.test(durum.aktif) && durum.oranlar[0]) durum.aktif = durum.oranlar.filter(function(x){ return x.grup === 'Web' || x.grup === 'Mobil' || x.grup === 'Bu alan'; }).concat(durum.oranlar)[0].id; ciz(); return; }
      var o = e.target.closest('[data-kp-oran]'); if(o){ durum.aktif = o.dataset.kpOran; ciz(); return; }
      if(e.target.closest('[data-kp-sifirla]')){ delete durum.duz[durum.aktif]; delete durum.kirpmasiz[durum.aktif]; ciz(); window.kbBildir('Oran odak noktasına göre yeniden hizalandı'); return; }
      if(e.target.closest('[data-kp-hepsi]')){ durum.duz = {}; ciz(); window.kbBildir('Bütün oranlar odak noktasına hizalandı'); return; }
      if(e.target.closest('[data-kp-tamam]')){ var s = sonuc(); kapat(); if(durum.tamam) durum.tamam(s); window.kbBildir('Kırpma uygulandı: ' + Object.keys(s.oranlar).length + ' oran'); }
    });
    ov.querySelector('[data-kp-yakin]').addEventListener('input', function(e){
      var c = kirpim(durum.aktif), o = aktifOran();
      durum.duz[durum.aktif] = { cx: c.x + c.g / 2, cy: c.y + c.y2 / 2, z: +e.target.value, r: o.r };
      ciz();
    });
    ov.querySelector('[data-kp-kirpmasiz]').addEventListener('change', function(e){ if(e.target.checked) durum.kirpmasiz[durum.aktif] = true; else delete durum.kirpmasiz[durum.aktif]; ciz(); });

    /* sürükleme: odak kipinde odak noktası, çerçeve kipinde çerçeve, tutamaçta serbest oran boyu */
    var surukle = null;
    sahne.addEventListener('pointerdown', function(e){
      if(!durum) return;
      var r = durum.yer, px = (e.clientX - sahne.getBoundingClientRect().left - r.ox) / r.g, py = (e.clientY - sahne.getBoundingClientRect().top - r.oy) / r.y;
      if(durum.kip === 'odak'){ surukle = { tur:'odak' }; odakYaz(px, py); }
      else if(e.target.closest('[data-kp-tutamac]')){ surukle = { tur:'boy', bx:e.clientX, by:e.clientY, c:kirpim(durum.aktif) }; }
      else if(e.target.closest('[data-kp-cerceve]')){ surukle = { tur:'tasi', bx:e.clientX, by:e.clientY, c:kirpim(durum.aktif) }; }
      else return;
      sahne.setPointerCapture(e.pointerId); e.preventDefault();
    });
    sahne.addEventListener('pointermove', function(e){
      if(!surukle) return;
      var r = durum.yer, rect = sahne.getBoundingClientRect();
      if(surukle.tur === 'odak'){ odakYaz((e.clientX - rect.left - r.ox) / r.g, (e.clientY - rect.top - r.oy) / r.y); return; }
      var dx = (e.clientX - surukle.bx) / r.g, dy = (e.clientY - surukle.by) / r.y, c = surukle.c, o = aktifOran();
      if(surukle.tur === 'tasi') durum.duz[durum.aktif] = { cx: c.x + c.g / 2 + dx, cy: c.y + c.y2 / 2 + dy, z: c.z, r: o.r };
      else { var g = Math.max(.12, Math.min(1 - c.x, c.g + dx)), h = Math.max(.12, Math.min(1 - c.y, c.y2 + dy)); durum.duz[durum.aktif] = { cx: c.x + g / 2, cy: c.y + h / 2, z: 1, r: (g * durum.W) / (h * durum.H), serbestG: g, serbestY: h }; }
      ciz();
    });
    sahne.addEventListener('pointerup', function(){ surukle = null; });
    sahne.addEventListener('wheel', function(e){
      if(durum.kip !== 'cerceve') return; e.preventDefault();
      var s = ov.querySelector('[data-kp-yakin]'); s.value = Math.max(1, Math.min(3, +s.value - e.deltaY / 400)); s.dispatchEvent(new Event('input'));
    }, { passive:false });
    sahne.addEventListener('keydown', function(e){
      var adim = e.shiftKey ? .05 : .01, m = { ArrowLeft:[-adim,0], ArrowRight:[adim,0], ArrowUp:[0,-adim], ArrowDown:[0,adim] }[e.key];
      if(!m) return; e.preventDefault(); odakYaz(durum.odak.x + m[0], durum.odak.y + m[1]);
    });
    sahne.tabIndex = 0; sahne.setAttribute('aria-label', 'Odak noktası: ok tuşlarıyla taşıyın');
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && ov.classList.contains('open')){ e.stopImmediatePropagation(); kapat(); } }, true);
    window.addEventListener('resize', function(){ if(ov.classList.contains('open')) ciz(); });
  }

  function kipSec(k){
    durum.kip = k;
    ov.querySelectorAll('[data-kp-kip]').forEach(function(b){ var on = b.dataset.kpKip === k; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', on); });
    ciz();
  }
  function odakYaz(x, y){
    durum.odak = { x: Math.max(0, Math.min(1, x)), y: Math.max(0, Math.min(1, y)) };
    ciz();
  }
  function aktifOran(){ return durum.oranlar.filter(function(o){ return o.id === durum.aktif; })[0]; }

  /* bir oranın kırpımı (görsele oranla): {x, y, g, y2, z} */
  function kirpim(id){
    var o = durum.oranlar.filter(function(x){ return x.id === id; })[0], d = durum.duz[id], W = durum.W, H = durum.H;
    var r = o.r || (d && d.r) || W / H, z = d ? d.z || 1 : 1;
    var cw = Math.min(W, H * r) / z, ch = cw / r;
    if(d && d.serbestG){ cw = d.serbestG * W; ch = d.serbestY * H; }
    var cx = d ? d.cx * W : durum.odak.x * W, cy = d ? d.cy * H : durum.odak.y * H;
    var x0 = Math.max(0, Math.min(W - cw, cx - cw / 2)), y0 = Math.max(0, Math.min(H - ch, cy - ch / 2));
    return { x: x0 / W, y: y0 / H, g: cw / W, y2: ch / H, z: z };
  }
  /* önizleme kutusuna kırpımı yaz (yüzdeyle; kutunun ölçüsünü bilmeye gerek yok) */
  function boya(el, id){
    var c = kirpim(id), url = 'url("' + durum.gorsel + '")', kirpmasiz = durum.kirpmasiz[id];
    el.classList.toggle('is-kirpmasiz', !!kirpmasiz);
    if(kirpmasiz){ el.style.backgroundImage = url + ',' + url; el.style.backgroundSize = 'contain,cover'; el.style.backgroundPosition = 'center,center'; el.style.backgroundRepeat = 'no-repeat'; return; }
    el.style.backgroundImage = url; el.style.backgroundRepeat = 'no-repeat';
    el.style.backgroundSize = (100 / c.g) + '% auto';
    el.style.backgroundPosition = (c.g >= .999 ? 50 : c.x / (1 - c.g) * 100) + '% ' + (c.y2 >= .999 ? 50 : c.y / (1 - c.y2) * 100) + '%';
  }
  window.kbKirpBoya = function(el, gorsel, kirp){
    /* sayfadaki görsel alanlarına sonucu yazar: kirp = {x,y,g,y2,kirpmasiz} */
    if(!kirp) return;
    var url = 'url("' + gorsel + '")';
    if(kirp.kirpmasiz){ el.style.backgroundImage = url + ',' + url; el.style.backgroundSize = 'contain,cover'; el.style.backgroundPosition = 'center,center'; el.style.backgroundRepeat = 'no-repeat'; el.classList.add('is-kirpmasiz'); return; }
    el.classList.remove('is-kirpmasiz'); el.style.backgroundImage = url; el.style.backgroundRepeat = 'no-repeat';
    el.style.backgroundSize = (100 / kirp.g) + '% auto';
    el.style.backgroundPosition = (kirp.g >= .999 ? 50 : kirp.x / (1 - kirp.g) * 100) + '% ' + (kirp.y2 >= .999 ? 50 : kirp.y / (1 - kirp.y2) * 100) + '%';
  };

  function ciz(){
    var sahne = ov.querySelector('[data-kp-sahne]'), SW = sahne.clientWidth, SH = sahne.clientHeight, W = durum.W, H = durum.H;
    var s = Math.min(SW / W, SH / H), gw = W * s, gh = H * s, ox = (SW - gw) / 2, oy = (SH - gh) / 2;
    durum.yer = { ox: ox, oy: oy, g: gw, y: gh };
    var res = ov.querySelector('[data-kp-resim]');
    res.style.cssText = 'left:' + ox + 'px;top:' + oy + 'px;width:' + gw + 'px;height:' + gh + 'px;background-image:url("' + durum.gorsel + '")';
    var c = kirpim(durum.aktif), o = aktifOran(), km = durum.kirpmasiz[durum.aktif];
    var cer = ov.querySelector('[data-kp-cerceve]');
    cer.style.cssText = km ? 'left:' + ox + 'px;top:' + oy + 'px;width:' + gw + 'px;height:' + gh + 'px' : 'left:' + (ox + c.x * gw) + 'px;top:' + (oy + c.y * gh) + 'px;width:' + (c.g * gw) + 'px;height:' + (c.y2 * gh) + 'px';
    cer.classList.toggle('is-tasinir', durum.kip === 'cerceve' && !km);
    ov.querySelector('[data-kp-tutamac]').hidden = !(durum.kip === 'cerceve' && !o.r && !km);
    ov.querySelector('[data-kp-etk]').textContent = o.ad + ' · ' + (o.oran === 'serbest' ? 'serbest' : o.oran) + (o.px ? ' · ' + o.px[0] + '×' + o.px[1] : '');
    var od = ov.querySelector('[data-kp-odak]'); od.style.left = (ox + durum.odak.x * gw) + 'px'; od.style.top = (oy + durum.odak.y * gh) + 'px';
    sahne.classList.toggle('kip-odak', durum.kip === 'odak');
    ov.querySelector('[data-kp-ipucu]').textContent = durum.kip === 'odak'
      ? 'Görselde önemli yere tıklayın ya da noktayı sürükleyin; düzeltilmemiş bütün oranlar ona göre hizalanır.'
      : (o.r ? 'Çerçeveyi sürükleyin, tekerlek ya da sürgüyle yakınlaştırın. Yalnızca bu oran değişir.' : 'Serbest oran: çerçeveyi taşıyın, sağ alt köşeden boyutlandırın.');
    var yk = ov.querySelector('[data-kp-yakin]'); yk.value = c.z; yk.disabled = !o.r || km;
    ov.querySelector('[data-kp-yakin-deger]').textContent = '%' + Math.round(c.z * 100);
    ov.querySelector('[data-kp-kirpmasiz]').checked = !!km;

    /* oran listesi (M5): o alan için gereken oranlar (web, mobil, alanın kendi oranları) açıkta;
       bildirim ve sosyal medya oranları "Diğer oranlar" altında kapalı, otomatik hizalandıkları tek satırla yazılır. */
    var ANA = { 'Web':1, 'Mobil':1, 'Bu alan':1 };
    function satir(x){
      var dz = durum.duz[x.id], kmz = durum.kirpmasiz[x.id];
      return '<button type="button" role="option" aria-selected="' + (x.id === durum.aktif) + '" class="kp-oran' + (x.id === durum.aktif ? ' is-on' : '') + '" data-kp-oran="' + x.id + '">'
        + '<span class="kp-mini" style="aspect-ratio:' + (x.r || W / H) + '" data-kp-mini="' + x.id + '"></span>'
        + '<span class="kp-oran-yazi"><b>' + x.ad + '</b><small>' + (x.oran === 'serbest' ? 'Serbest' : x.oran) + (x.px ? ' · ' + x.px[0] + '×' + x.px[1] : '') + '</small></span>'
        + '<span class="kp-durum ' + (kmz ? 'is-kirpmasiz' : dz ? 'is-duz' : '') + '">' + (kmz ? 'Kırpmasız' : dz ? 'Düzeltildi' : 'Otomatik') + '</span></button>';
    }
    var anaL = durum.oranlar.filter(function(x){ return ANA[x.grup]; }), digL = durum.oranlar.filter(function(x){ return !ANA[x.grup]; });
    if(!anaL.length){ anaL = digL; digL = []; }
    if(digL.some(function(x){ return x.id === durum.aktif; })) durum.digerAcik = true;
    var h = '', grup = '';
    anaL.forEach(function(x){ if(x.grup !== grup){ grup = x.grup; h += '<div class="kp-grup">' + grup + '</div>'; } h += satir(x); });
    if(digL.length){
      var dzS = digL.filter(function(x){ return durum.duz[x.id] || durum.kirpmasiz[x.id]; }).length;
      h += '<div class="kp-diger' + (durum.digerAcik ? ' is-acik' : '') + '"><button type="button" class="kp-diger-bas" data-kp-diger aria-expanded="' + !!durum.digerAcik + '"><i class="fa-solid fa-chevron-right" aria-hidden="true"></i><span><b>Diğer oranlar (' + digL.length + ')</b><small>Bildirim ve sosyal medya · ' + (dzS ? (digL.length - dzS) + ' otomatik, ' + dzS + ' düzeltildi' : 'odak noktasına göre otomatik hizalandı') + '</small></span></button>';
      if(durum.digerAcik){ grup = ''; digL.forEach(function(x){ if(x.grup !== grup){ grup = x.grup; h += '<div class="kp-grup">' + grup + '</div>'; } h += satir(x); }); }
      h += '</div>';
    }
    ov.querySelector('[data-kp-oranlar]').innerHTML = h;
    ov.querySelectorAll('[data-kp-mini]').forEach(function(el){ boya(el, el.dataset.kpMini); });

    /* canlı önizleme: site kartı, mobil kart, sosyal kart (aktif sosyal oran ya da ilk sosyal oran) */
    var sosyal = /^sosyal\./.test(durum.aktif) ? durum.aktif : (durum.oranlar.filter(function(x){ return /^sosyal\./.test(x.id); })[0] || {}).id;
    ov.querySelectorAll('[data-kp-onizle]').forEach(function(el){
      var id = el.dataset.kpOnizle === 'sosyal' ? sosyal : el.dataset.kpOnizle, x = durum.oranlar.filter(function(o){ return o.id === id; })[0];
      el.closest('figure').hidden = !x || (el.dataset.kpOnizle === 'sosyal' && !durum.digerAcik); if(el.closest('figure').hidden) return;
      el.style.aspectRatio = x.r || (kirpim(id).g * W) / (kirpim(id).y2 * H);
      boya(el, id);
      el.closest('figure').classList.toggle('is-aktif', id === durum.aktif);
    });
    var sx = durum.oranlar.filter(function(o){ return o.id === sosyal; })[0];
    ov.querySelector('[data-kp-sosyal-etk]').textContent = sx ? 'Sosyal kart · ' + (sx.oran === 'serbest' ? 'serbest' : sx.oran) : '';
    var onz = ov.querySelector('.kp-onizle'); onz.hidden = !onz.querySelector('figure:not([hidden])'); ov.querySelector('[data-kp-onizle-tt]').hidden = onz.hidden;
    var duzSay = Object.keys(durum.duz).length, kmSay = Object.keys(durum.kirpmasiz).length;
    ov.querySelector('[data-kp-ozet]').textContent = 'Odak %' + Math.round(durum.odak.x * 100) + ' · %' + Math.round(durum.odak.y * 100) + ' · ' + (durum.oranlar.length - duzSay - kmSay) + ' oran otomatik' + (duzSay ? ', ' + duzSay + ' düzeltildi' : '') + (kmSay ? ', ' + kmSay + ' kırpmasız' : '');
  }

  function sonuc(){
    var s = { odak: { x: durum.odak.x, y: durum.odak.y }, oranlar: {}, ham: { duz: JSON.parse(JSON.stringify(durum.duz)), kirpmasiz: JSON.parse(JSON.stringify(durum.kirpmasiz)) } };
    durum.oranlar.forEach(function(o){ var c = kirpim(o.id); s.oranlar[o.id] = { x: c.x, y: c.y, g: c.g, y2: c.y2, kirpmasiz: !!durum.kirpmasiz[o.id], duzeltildi: !!durum.duz[o.id] }; });
    return s;
  }
  var once = null;
  function kapat(){ ov.classList.remove('open'); document.body.style.overflow = ''; if(once && once.focus) once.focus(); }

  window.kbKirp = function(o){
    if(!ov) kur();
    var img = new Image();
    img.onload = function(){
      var oranlar = (o.oranlar || varsayilanOranlar(o.alan)).map(function(x){ return Object.assign({ r: oranSayi(x.oran) }, x); });
      durum = { gorsel: o.gorsel, W: img.naturalWidth, H: img.naturalHeight, odak: o.odak || { x: .5, y: .5 }, oranlar: oranlar,
        aktif: o.secili && oranlar.some(function(x){ return x.id === o.secili; }) ? o.secili : oranlar[0].id, duz: {}, kirpmasiz: {}, digerAcik: false, kip: o.secili ? 'cerceve' : 'odak', tamam: o.tamam };
      if(o.ham){ durum.duz = JSON.parse(JSON.stringify(o.ham.duz)); durum.kirpmasiz = JSON.parse(JSON.stringify(o.ham.kirpmasiz)); }
      ov.querySelector('[data-kp-bilgi]').textContent = (o.ad ? o.ad + ' · ' : '') + durum.W + '×' + durum.H + ' · ' + oranlar.length + ' oran';
      ov.querySelectorAll('[data-kp-baslik]').forEach(function(b){ b.textContent = o.baslik || 'Asgari ücret görüşmelerinde ilk toplantı 4 Aralık\'ta yapılacak'; });
      once = document.activeElement;
      ov.classList.add('open'); document.body.style.overflow = 'hidden';
      kipSec(durum.kip);
      requestAnimationFrame(function(){ ciz(); ov.querySelector('[data-kp-kapat]').focus(); });
    };
    img.src = o.gorsel;
  };

  /* görsel seçilince ya da yüklenince [data-kirp-sonra] taşıyan alanda kırpma kendiliğinden açılır */
  document.addEventListener('kb-gorsel', function(e){
    var alan = e.target.closest && e.target.closest('[data-kirp-sonra]'); if(!alan) return;
    var kap = e.detail && e.detail.kapsam, b = alan.querySelector(kap ? '[data-kirp-ac="' + kap + '.kart"]' : '[data-kirp-ac]');
    if(b) setTimeout(function(){ b.click(); }, 320);
  });

  /* sayfadaki görsel alanı: [data-kirp-ac] düğmesi, en yakın [data-gorsel-alan] kabındaki [data-kirp-oran] kutularını günceller */
  var sonKirp = new WeakMap();
  document.addEventListener('click', function(e){
    var b = e.target.closest('[data-kirp-ac]'); if(!b) return;
    e.preventDefault();
    var alan = (b.dataset.kirpAlan && document.querySelector(b.dataset.kirpAlan)) || b.closest('[data-gorsel-alan]') || document;
    var secili = b.getAttribute('data-kirp-ac') || null;
    var hedef = (secili && alan.querySelector('[data-kirp-oran="' + secili + '"]')) || alan.querySelector('[data-kirp-oran]') || alan.querySelector('[data-gorsel-hedef]');
    var m = hedef && (hedef.style.backgroundImage || '').match(/url\(["']?([^"')]+)/);
    if(!m){ window.kbBildir('Önce bir görsel yükleyin ya da havuzdan seçin', null, 'uyari'); return; }
    var odakEl = alan.querySelector('.kg-odak'), odak = odakEl ? { x: parseFloat(odakEl.style.left) / 100, y: parseFloat(odakEl.style.top) / 100 } : null;
    window.kbKirp({ gorsel: m[1], odak: odak, alan: alan.getAttribute('data-gorsel-alan') || 'haberler.kapak', secili: secili, oranlar: alan.getAttribute && alan.getAttribute('data-kirp-oranlar') ? alanOranlari(alan.getAttribute('data-kirp-oranlar')) : null, ham: sonKirp.get(alan),
      ad: alan.getAttribute('data-gorsel-ad'),
      tamam: function(s){
        sonKirp.set(alan, s.ham);
        /* yalnızca aynı görseli taşıyan kutular güncellenir (mobil için ayrı görsel yüklendiyse o ayrı kırpılır) */
        alan.querySelectorAll('[data-kirp-oran]').forEach(function(el){ if((el.style.backgroundImage || '').indexOf(m[1]) > -1) window.kbKirpBoya(el, m[1], s.oranlar[el.getAttribute('data-kirp-oran')]); });
        alan.querySelectorAll('.kg-odak').forEach(function(o){ o.style.left = s.odak.x * 100 + '%'; o.style.top = s.odak.y * 100 + '%'; });
        document.querySelectorAll('[data-kirp-izle]').forEach(function(el){ var k = s.oranlar[el.getAttribute('data-kirp-izle')]; if(k) window.kbKirpBoya(el, m[1], k); });
        alan.dispatchEvent(new Event('input', { bubbles:true }));
      } });
  });
})();
