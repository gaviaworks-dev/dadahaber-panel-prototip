#!/usr/bin/env python3
"""Raporlar modülü · dışa aktarım pencerelerinin ortak parçası: Biçim seçimi (PDF · XLSX · CSV, PDF varsayılan) ve
yalnız PDF seçiliyken görünen "PDF Görünümü" (tema logolu kapak). site.html (_uret_site.py) ile index.html ve
disa-aktarim.html'deki Dışa Aktar pencereleri aynı işaretlemeyi buradan alır (Tutarlılık).
Kapak çekirdek bileşeni: .kb-belge-onizleme (UI kit "PDF Kapağı")."""

BICIM_ALT = 'PDF, XLSX ya da CSV · 7 gün indirilebilir'
BICIMLER = [('pdf', 'PDF', 'Dada Haber logolu, kapak ve grafiklerle · paylaşmaya hazır'),
            ('xlsx', 'XLSX', 'Biçimli Excel · her bölüm ayrı sayfada'),
            ('csv', 'CSV', 'UTF-8, virgülle ayrılmış · Excel ve Sheets açar')]

def bicim(ad, onek, rapor, aralik, bolumler, sayfa):
    """ad: radio grubu adı · onek: kimlik öneki · rapor/aralik: kapak metni · bolumler: kapaktaki bölüm adları · sayfa: tahmini sayfa"""
    secenek = ''.join(
        f'<label class="kb-secenek kb-secenek-kart"><input type="radio" name="{ad}" value="{v}"'
        + (f' data-ac="{onek}Pdf" checked' if v == 'pdf' else '') + f'><span><b>{b}</b><small>{s}</small></span></label>'
        for v, b, s in BICIMLER)
    kapak = ''.join(f'<li>{x}</li>' for x in bolumler)
    return (f'<div class="frow"><span class="flabel">Biçim</span>'
            f'<div class="kb-kart-sec" data-alan-id="bicim" data-zorunlu-metin="PDF, XLSX ya da CSV seçin">{secenek}</div></div>'
            f'<div class="frow" id="{onek}Pdf"><span class="flabel">PDF Görünümü</span>'
            f'<div class="kb-belge-onizleme"><div class="kbo-sayfa"><span class="kbo-logo kb-logo kb-logo-acik" role="img" aria-label="Tema logosu"></span>'
            f'<b class="kbo-baslik">{rapor}</b><span class="kbo-tarih">{aralik}</span><ol class="kbo-bolumler">{kapak}</ol>'
            f'<span class="kbo-alt"><span>Dada Haber</span><span>{sayfa} sayfa · PDF</span></span></div></div>'
            f'<span class="fhint">Her sayfanın üstünde tema logosu, altında rapor adı ve sayfa numarası bulunur.</span></div>')
