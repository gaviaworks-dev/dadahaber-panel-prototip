// Taklit çerçeveleri: geniş görünümü kabın genişliğine sığdırır; dar ekranda (data-dogal-alt altında) sayfayı kendi duyarlı halinde açar.
(function () {
  'use strict';
  var cerceveler = [].slice.call(document.querySelectorAll('.cer'));
  var yukseklik = {}; // src -> { genislik: yükseklik }

  function dosya(src) { return src.split('/').pop(); }

  function kur(c) {
    var ic = c.querySelector('.cer-ic');
    var f = document.createElement('iframe');
    f.src = c.dataset.src;
    f.loading = 'lazy';
    f.title = c.querySelector('figcaption span').textContent;
    f.setAttribute('scrolling', 'no');
    ic.appendChild(f);
    c._f = f;
    c._ic = ic;
  }

  function olc(c) {
    var gen = +c.dataset.gen;
    var kap = c._ic.clientWidth || c.clientWidth;
    var dogalAlt = +(c.dataset.dogalAlt || 0);
    var dogal = dogalAlt && kap < dogalAlt;
    var w = dogal ? kap : gen;
    var k = dogal ? 1 : Math.min(1, kap / gen);
    var olcu = yukseklik[dosya(c.dataset.src)];
    var h = (olcu && olcu[w]) || +c.dataset.h;
    if (c._w !== w) { c._w = w; c._f.style.width = w + 'px'; }
    c._f.style.height = h + 'px';
    c._f.style.transform = k === 1 ? 'none' : 'scale(' + k + ')';
    c._ic.style.height = Math.ceil(h * k) + 'px';
  }

  cerceveler.forEach(kur);
  function hepsi() { cerceveler.forEach(olc); }
  hepsi();

  window.addEventListener('message', function (ev) {
    var d = ev.data;
    if (!d || !d.oneriCerceve || !d.h) return;
    var ad = d.oneriCerceve.split('?')[0];
    cerceveler.forEach(function (c) {
      if (dosya(c.dataset.src) !== ad || ev.source !== c._f.contentWindow) return;
      yukseklik[ad] = yukseklik[ad] || {};
      yukseklik[ad][c._w] = d.h;
      olc(c);
    });
  });

  var zaman;
  window.addEventListener('resize', function () { clearTimeout(zaman); zaman = setTimeout(hepsi, 120); });
})();
