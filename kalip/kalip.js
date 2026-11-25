/* =====================================================================
   SOSYAL MEDYA KALIP ALTERNATİFLERİ · yalnız bu sayfanın küçük betiği (ortak dosya değil)
   - Süsleme katmanı: #kpSusleme'deki seçimler etkin alternatifin kabına (.kp-orn[data-alt]) data-o-* olarak yazılır;
     aynı alternatifin "Hepsini Yan Yana Gör" kartı da güncellenir. Sekme değişince seçimler o alternatifin durumuna döner.
   - "Bunu Seç" ve özet satırı: seçilen alternatifler süslemeleriyle birlikte #kpOzet'e yazılır.
   Kategori, mecra ve düğme alanı çekirdeğin data-mo bağıyla çalışır (alan.js).
   ===================================================================== */
(function(){
  var sahne = document.getElementById('kpSahne'), sus = document.getElementById('kpSusleme'), ozet = document.querySelector('#kpOzet .kp-ozet-metin');
  if(!sahne || !sus) return;
  var GRUP = ['logo', 'etiket', 'oge', 'bvurgu', 'islem', 'kose'];
  var AD = {
    logo: { duz:'logo düz', plaka:'logo beyaz plakada', rozet:'logo yuvarlak rozette', renk:'logo kategori renginde' },
    etiket: { duz:'etiket düz yazı', dolu:'etiket dolu kutu', cerceve:'etiket çerçeveli kutu', nokta:'etiket nokta ve yazı', dikey:'etiket dikey yazı' },
    oge: { ince:'vurgu ince çizgi', kalin:'vurgu kalın kısa çizgi', kose:'vurgu köşe işareti', nokta:'vurgu nokta dizisi', yok:'vurgu öğesi yok' },
    bvurgu: { yok:'başlık vurgusu yok', renkli:'başlıkta kelime renkli', zeminli:'başlıkta kelime zeminli', alti:'başlıkta altı çizgili' },
    islem: { dogal:'görsel doğal', gecis:'görsel alttan geçişli', ton:'görsel kategori tonunda', sb:'görsel siyah-beyaz' },
    kose: { keskin:'köşe keskin', yuvarlak:'köşe yuvarlak' }
  };
  function panel(){ return sahne.querySelector('.sa-form-panel:not([hidden])'); }
  function kaplar(alt){ return sahne.querySelectorAll('.kp-orn[data-alt="' + alt + '"]'); }
  /* süsleme denetimlerini etkin alternatifin durumuna getir */
  function esitle(){
    var p = panel(), alt = p && p.dataset.alt;
    sus.classList.toggle('is-kapali', !alt);
    var ad = sus.querySelector('.kp-sus-ad'); if(ad) ad.textContent = alt ? p.dataset.ad : 'Hepsini Yan Yana Gör: her kalıp kendi seçimiyle';
    if(!alt) return;
    GRUP.forEach(function(g){
      var v = p.getAttribute('data-o-' + g), i = sus.querySelector('input[data-orn="' + g + '"][value="' + v + '"]');
      if(i && !i.checked){ i.checked = true; i._kpSessiz = true; i.dispatchEvent(new Event('change', { bubbles:true })); i._kpSessiz = false; }
    });
  }
  sus.addEventListener('change', function(e){
    var i = e.target; if(!i.matches('input[data-orn]') || i._kpSessiz || !i.checked) return;
    var p = panel(); if(!p || !p.dataset.alt) return;
    kaplar(p.dataset.alt).forEach(function(k){ k.setAttribute('data-o-' + i.dataset.orn, i.value); });
    yaz();
  });
  sus.addEventListener('click', function(e){
    if(!e.target.closest('[data-kp-varsayilan]')) return;
    var p = panel(); if(!p || !p.dataset.alt) return;
    kaplar(p.dataset.alt).forEach(function(k){ GRUP.forEach(function(g){ k.setAttribute('data-o-' + g, k.getAttribute('data-v-' + g)); }); });
    esitle(); yaz();
  });
  sahne.addEventListener('click', function(e){ if(e.target.closest('.sa-form-tab')) setTimeout(esitle, 0); });
  /* özet: seçilen iskelet + süsleme */
  function yaz(){
    if(!ozet) return;
    var secili = Array.prototype.filter.call(sahne.querySelectorAll('input.kp-sec'), function(c){ return c.checked; });
    if(!secili.length){ ozet.textContent = 'henüz seçilmedi; her alternatifin altındaki “Bunu Seç” ile işaretleyin.'; return; }
    ozet.textContent = secili.map(function(c){
      var p = sahne.querySelector('.sa-form-panel[data-alt="' + c.dataset.alt + '"]');
      var degisen = GRUP.filter(function(g){ return p.getAttribute('data-o-' + g) !== p.getAttribute('data-v-' + g); });
      var liste = (degisen.length ? degisen : GRUP).map(function(g){ return AD[g][p.getAttribute('data-o-' + g)]; });
      return p.dataset.ad + ' (' + (degisen.length ? '' : 'varsayılan: ') + liste.join(', ') + ')';
    }).join(' · ');
  }
  sahne.addEventListener('change', function(e){ if(e.target.matches('input.kp-sec')) yaz(); });
  /* başlığı sığdır: üç satıra sığmayan başlık en çok %30 küçülür (gerçek kalıpta da aynı kural: kesilmez, küçülür) */
  function sigdir(){
    sahne.querySelectorAll('.kp-baslik').forEach(function(b){
      if(!b.getClientRects().length) return;
      b.style.fontSize = ''; var ilk = parseFloat(getComputedStyle(b).fontSize), f = ilk;
      while(b.scrollHeight > b.clientHeight + 1 && f > ilk * .7){ f *= .95; b.style.fontSize = f + 'px'; }
    });
  }
  document.addEventListener('change', function(){ sigdir(); });
  sahne.addEventListener('click', function(e){ if(e.target.closest('.sa-form-tab')) setTimeout(sigdir, 0); });
  window.addEventListener('resize', function(){ clearTimeout(sigdir._z); sigdir._z = setTimeout(sigdir, 120); });
  if(document.fonts && document.fonts.ready) document.fonts.ready.then(sigdir);
  window.kpSigdir = sigdir;
  esitle(); yaz(); sigdir();
})();
