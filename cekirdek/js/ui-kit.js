/* UI kit sayfasının yalnız gösterim düğmeleri (bileşenleri çağırır; yeni davranış eklemez) */
(function(){
  document.querySelectorAll('[data-renk-deger]').forEach(function(el){ el.textContent = getComputedStyle(document.documentElement).getPropertyValue(el.dataset.renkDeger).trim(); });
  document.addEventListener('click', function(e){
    var a = e.target.closest('[data-kit-ac]'); if(a){ window.kbAc(a.dataset.kitAc === 'cekmece' ? 'kitCekmece' : 'kitPencere', a.dataset.kitAc); return; }
    if(e.target.closest('[data-kit-onay]')){ window.kbOnay({ tehlike:true, baslik:'Kayıt çöpe taşınsın mı?', metin:'Çöp sekmesine gider, oradan geri alınabilir. 12 haberde kullanılıyor; oradan da çıkar. İşlem denetim izine yazılır.', evet:'Çöpe Taşı', evetIs: function(){ window.kbBildir('Çöpe taşındı', function(){ window.kbBildir('Geri alındı'); }); } }); return; }
    if(e.target.closest('[data-kit-uclu]')){ window.kbOnay({ ikon:'fa-circle-exclamation', baslik:'Kaydedilmemiş değişiklikler var', metin:'Sayfadan ayrılmadan önce değişikliklerinizi taslak olarak kaydedebilirsiniz.', evet:'Taslak Kaydet ve Çık', vazgec:'Sayfada Kal', evetIs: function(){ window.kbBildir('Taslak kaydedildi; sonraki sayfaya geçiliyor'); }, ikinci:{ ad:'Kaydetmeden Çık', tehlike:true, is: function(){ window.kbBildir('Değişiklikler kaydedilmeden çıkıldı', null, 'uyari'); } } }); return; }
    if(e.target.closest('[data-kit-cikis]')){ window.kbOnay({ ikon:'fa-right-from-bracket', baslik:'Oturum kapatılsın mı?', metin:'Bu cihazda oturumunuz kapanır; yeniden girişte e-posta ve şifreniz sorulur.', evet:'Çıkış Yap', evetIs: function(){ window.kbBildir('Oturum kapatıldı (örnek)'); } }); return; }
    if(e.target.closest('[data-kit-kod]')){ window.kbKod({ baslik:'E-posta koduyla doğrulayın', metin:'Bakım modunu açıyorsunuz.', evetIs: function(){ window.kbBildir('Doğrulandı'); } }); return; }
    if(e.target.closest('[data-kit-tasi]')){ window.kbTasiSil({ ad:'Spor › Basketbol', haber:128, alt:0, hedefler:['Spor › Futbol','Spor › Voleybol','Spor › Diğer Branşlar'], evetIs: function(h){ window.kbBildir('128 haber “' + h + '” konusuna taşındı; Basketbol çöpe gitti', function(){}); } }); return; }
    var tb = e.target.closest('[data-kit-tur]'); if(tb){ window.kbBildir({ basari:'Haber kaydedildi', bilgi:'Prototipte yalnızca ilk sayfa gösteriliyor', uyari:'3 zorunlu alan eksik; işaretli alanları doldurun', hata:'Kaydedilemedi: sunucuya ulaşılamadı' }[tb.dataset.kitTur], tb.dataset.kitTur === 'basari' ? function(){} : null, tb.dataset.kitTur); return; }
    if(e.target.closest('[data-kit-bildir]')){ window.kbBildir('Haber çöpe taşındı', function(){ window.kbBildir('Geri alındı'); }); }
  });
})();
