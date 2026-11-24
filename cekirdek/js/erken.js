/* ÇEKİRDEK · erken betik — <head>'de, sayfa çizilmeden önce çalışır.
   Menünün dar/açık halini ve daraltma biçimini ilk çizimde uygular; menü açılıp kapanarak sıçramaz. */
(function(){
  var d = document.documentElement, P = window.PANEL || {}, q = new URLSearchParams(location.search);
  d.classList.add('kb-yukleniyor');
  var bicim = q.get('daraltma') || (P.menu || {}).daraltma || 'yok';
  if(['ikon','gizle','yok'].indexOf(bicim) === -1) bicim = 'yok';
  d.dataset.daraltma = bicim;
  var dar = false;
  if(bicim !== 'yok'){
    if(q.get('dar') === '1') dar = true;
    else { try{ dar = localStorage.getItem('dh_menu_dar') === '1'; }catch(e){} }
  }
  d.classList.toggle('kb-dar', dar);
})();
