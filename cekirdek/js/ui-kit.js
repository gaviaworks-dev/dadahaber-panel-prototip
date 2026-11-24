/* UI kit sayfasının yalnız gösterim düğmeleri (bileşenleri çağırır; yeni davranış eklemez) */
(function(){
  document.querySelectorAll('[data-renk-deger]').forEach(function(el){ el.textContent = getComputedStyle(document.documentElement).getPropertyValue(el.dataset.renkDeger).trim(); });
  document.addEventListener('click', function(e){
    var a = e.target.closest('[data-kit-ac]'); if(a){ window.kbAc(a.dataset.kitAc === 'cekmece' ? 'kitCekmece' : 'kitPencere', a.dataset.kitAc); return; }
    if(e.target.closest('[data-kit-onay]')){ window.kbOnay({ tehlike:true, baslik:'Kayıt çöpe taşınsın mı?', metin:'Çöp sekmesine gider, oradan geri alınabilir. 12 haberde kullanılıyor; oradan da çıkar. İşlem denetim izine yazılır.', evet:'Çöpe taşı', evetIs: function(){ window.kbBildir('Çöpe taşındı', function(){ window.kbBildir('Geri alındı'); }); } }); return; }
    if(e.target.closest('[data-kit-kod]')){ window.kbKod({ baslik:'E-posta koduyla doğrulayın', metin:'Bakım modunu açıyorsunuz.', evetIs: function(){ window.kbBildir('Doğrulandı'); } }); return; }
    if(e.target.closest('[data-kit-tasi]')){ window.kbTasiSil({ ad:'Spor › Basketbol', haber:128, alt:0, hedefler:['Spor › Futbol','Spor › Voleybol','Spor › Diğer Branşlar'], evetIs: function(h){ window.kbBildir('128 haber “' + h + '” konusuna taşındı; Basketbol çöpe gitti', function(){}); } }); return; }
    if(e.target.closest('[data-kit-bildir]')){ window.kbBildir('Haber çöpe taşındı', function(){ window.kbBildir('Geri alındı'); }); }
  });
})();
