/* Çekmece ve pencere ölçümü — araclar/duyarli.html ve araclar/denetim.html ortak kullanır (KURAL · kap başlığı).
   Sayfadaki her çekmece/pencere şablonu (<template data-baslik>) çekirdeğin kbAc'ı ile açılır ve ölçülür:
   kapat düğmesi tamamen görünür ve üstünde başka öğe yok · alt çubuk düğmeleri görünür alanda · içerik yatay taşmıyor ·
   alt satır tek satır ("…") · başlık yüksekliği (sayfalar arası karşılaştırma araclar/duyarli.py'de).
   Sonuç: { olculen, hata:[…], bas:[{ad, h}] } */
(function(g){
  g.kbPencereTara = function(d, win){
    var W = d.documentElement.clientWidth, H = win.innerHeight, sonuc = { olculen: 0, hata: [], bas: [], notlu: [] };
    if(!win.kbAc) return sonuc;
    function icinde(r, k){ return r.left >= Math.max(0, k.left) - 1 && r.right <= Math.min(W, k.right) + 1 && r.top >= Math.max(0, k.top) - 1 && r.bottom <= Math.min(H, k.bottom) + 1; }
    function gor(e){ return e && e.getClientRects().length && !e.closest('[hidden]') && win.getComputedStyle(e).visibility !== 'hidden'; }
    var sab = Array.prototype.filter.call(d.querySelectorAll('template[data-baslik][id]'), function(t){ return !t.closest('.kb-cekmece, .kb-pencere'); });
    sab.slice(0, 40).forEach(function(t){
      var id = t.id, tur = d.querySelector('[data-pencere="' + id + '"]') ? 'pencere' : 'cekmece', ad = (t.dataset.baslik || id).slice(0, 28);
      try{ win.kbAc(id, tur); }catch(x){ sonuc.hata.push('"' + ad + '": açılamadı (' + x.message + ')'); return; }
      var k = Array.prototype.filter.call(d.querySelectorAll('.kb-cekmece, .kb-pencere'), function(x){ return !x.hidden; }).pop();
      if(!k){ return; }
      k.classList.add('open'); sonuc.olculen++;
      var kr = k.getBoundingClientRect(), on = (tur === 'pencere' ? 'pencere' : 'çekmece') + ' "' + ad + '"';
      if(kr.left < -1 || kr.right > W + 1) sonuc.hata.push(on + ': kap ekrana sığmıyor (' + Math.round(kr.left) + '…' + Math.round(kr.right) + ')');
      var kp = k.querySelector('.kb-kap-bas .kb-kapat');
      if(!kp || !gor(kp)) sonuc.hata.push(on + ': kapat düğmesi yok ya da görünmüyor');
      else {
        var pr = kp.getBoundingClientRect();
        if(!icinde(pr, kr) || pr.width < 30) sonuc.hata.push(on + ': kapat düğmesi görünür alanın dışında (' + Math.round(pr.left) + '…' + Math.round(pr.right) + ' / ' + Math.round(Math.min(W, kr.right)) + ')');
        else { var ust = d.elementFromPoint(pr.left + pr.width / 2, pr.top + pr.height / 2); if(ust && ust !== kp && !kp.contains(ust)) sonuc.hata.push(on + ': kapat düğmesinin üstünde başka öğe var'); }
      }
      Array.prototype.forEach.call(k.querySelectorAll('.kb-kap-alt-cubuk .btn, .kb-kap-alt-cubuk button'), function(b){
        if(!gor(b)) return; var br = b.getBoundingClientRect();
        if(!icinde(br, kr)) sonuc.hata.push(on + ': alt çubuk düğmesi "' + b.textContent.trim().slice(0, 16) + '" görünür alanın dışında');
      });
      var gv = k.querySelector('.kb-kap-govde');
      if(k.scrollWidth > k.clientWidth + 1) sonuc.hata.push(on + ': kap yatay taşıyor (' + k.scrollWidth + ' > ' + k.clientWidth + ')');
      if(gv){
        var gr = gv.getBoundingClientRect(), tasan = null;
        Array.prototype.some.call(gv.querySelectorAll('*'), function(e){
          if(!gor(e) || e.closest('.pnl-menu:not(.open), .kb-secim-menu:not(.open), [class*="oniz"] *, .ptable-wrap *, .chips *') || /^(fixed|absolute)$/.test(win.getComputedStyle(e).position)) return false;
          var er = e.getBoundingClientRect(); if(er.width && er.right > gr.right + 1){ tasan = (e.className && typeof e.className === 'string' ? e.className.split(' ')[0] : e.tagName.toLowerCase()) + ' +' + Math.round(er.right - gr.right) + 'px'; return true; }
          return false;
        });
        if(gv.scrollWidth > gv.clientWidth + 1 || tasan) sonuc.hata.push(on + ': içerik yatay taşıyor' + (tasan ? ' (' + tasan + ')' : ''));
      }
      var alt = k.querySelector('.kb-kap-bas .kb-kap-alt');
      if(alt && alt.scrollWidth > alt.clientWidth + 1 && win.getComputedStyle(alt).textOverflow !== 'ellipsis') sonuc.hata.push(on + ': alt satır kesilmeden taşıyor');
      if(k.querySelector('.kb-kap-govde > .kb-kap-not')) sonuc.notlu.push(id);
      var hb = k.querySelector('.kb-kap-bas'); if(hb) sonuc.bas.push({ ad: on, h: Math.round(hb.getBoundingClientRect().height) });
      if(win.kbKapat) win.kbKapat();
      k.classList.remove('open'); k.hidden = true;
    });
    return sonuc;
  };
})(window);
