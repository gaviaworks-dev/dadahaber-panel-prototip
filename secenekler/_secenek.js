/* Seçenek sayfaları: önizleme çerçevelerini kart genişliğine ölçekler. Ürüne girmez. */
(function(){
  function olcekle(){
    document.querySelectorAll('.sc-kap').forEach(function(k){
      var f = k.querySelector('iframe'); if(f) f.style.transform = 'scale(' + (k.clientWidth / 1440) + ')';
    });
  }
  window.addEventListener('resize', olcekle); olcekle();
})();
