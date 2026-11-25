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

/* kit · sosyal medya önizlemeleri: açık mecraların hepsi, kayıttaki sırayla, kendi şablonuyla (yazı mecraları yatay görsel, video mecraları dikey 9:16) */
(function(){
  var K = document.querySelector('[data-kit-sosyal]'); if(!K || !window.kbSosyalOnizle) return;
  var pl = (window.PANEL || {}).sosyal_platformlar || [], h = '';
  pl.forEach(function(p){ h += '<div class="kit-sosyal-oge"><span class="kit-etk">' + p.ad + '</span><div class="kb-sosyal-kart" data-kit-sosyal-p="' + p.id + '"></div></div>'; });
  K.innerHTML = h;
  pl.forEach(function(p){ var el = K.querySelector('[data-kit-sosyal-p="' + p.id + '"]'); var vid = p.tur === 'video';
    window.kbSosyalOnizle(el, { platform: p.id, ad: 'Dada Haber', tutamac: p.id === 'bluesky' ? '@dadahaber.bsky.social' : '@dadahaber', metin: "Asgari ücret görüşmelerinde ilk toplantı 4 Aralık'ta. Komisyon taraflarla ilk kez masaya oturuyor. #AsgariÜcret", gorsel: 'veri/gorsel/p195.jpg', oran: vid ? '9:16' : ((p.oranlar || ['16:9'])[0] === 'serbest' ? '16:9' : (p.oranlar || ['16:9'])[0]), baslik: "Asgari ücrette ilk toplantı 4 Aralık'ta" }); });
})();
