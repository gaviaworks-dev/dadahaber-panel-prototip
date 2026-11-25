"""K ve L · dikey öğeli iki iskelet (DADAHABER-13 kalıp alternatifleri) — t-kalip4.

_uret.py bu modülden iki şey alır:
  ISKELETLER_KL      ALT listesindeki K ve L kaydının yerine geçer (aynı alanlar + pasif).
  kl_parca(tip, al, saat)
                     tuval()'de kp-blok'tan ÖNCE çağrılır; her tuvale (hangi iskelet seçili olursa olsun) L'nin
                     dev dikey kelimesini yazar. Yalnız .kp-l altında görünür (kl.css); başka iskelette display:none.
                     al: tuval()'in kategori yardımcısı (beş kategoriyi data-k ile yazar ya da akış kartında tek)
                     saat: _uret.saat (Son Dakika'da saat dikey yazıya girer)
Çizim kalip/kl.css'te (kalip.css'ten SONRA yüklenir; seçiciler #kpSahne .kp-k / #kpSahne .kp-l).
K, tuvalde zaten olan parçaları kullanır: kp-sekil (bant), kp-sekil2 (bayrak), kp-etiket-dikey (bantta dikey etiket).
"""
import html

e = lambda s: html.escape(str(s), quote=True)

# Gilroy ExtraBold büyük harf ve rakam genişliği (em; tarayıcıda ölçüldü, 25.11.2026) — dev kelimenin boyunu sığdırmak için
_EM = {"A": .68, "B": .60, "C": .72, "Ç": .72, "D": .71, "E": .53, "F": .52, "G": .78, "Ğ": .78, "H": .66, "I": .28, "İ": .28, "J": .57,
       "K": .63, "L": .48, "M": .82, "N": .67, "O": .79, "Ö": .79, "P": .59, "Q": .79, "R": .62, "S": .59, "Ş": .59, "T": .54, "U": .65,
       "Ü": .65, "V": .66, "W": 1.0, "X": .62, "Y": .63, "Z": .54, " ": .25, "·": .28, ".": .28, ":": .28, "%": .78,
       "0": .63, "1": .40, "2": .53, "3": .55, "4": .58, "5": .55, "6": .56, "7": .49, "8": .57, "9": .56}


def buyuk(s):
    """Türkçe büyük harf (i → İ, ı → I)"""
    return s.replace("i", "İ").replace("ı", "I").upper()


def em(s, olcek=1.0):
    return sum(_EM.get(c, .66) for c in s) * olcek


def kl_parca(tip, al, saat=None):
    """L · Sırt: dev dikey kelime (kategori adı; Son Dakika'da "SON DAKİKA") + yanında küçük bölge (Son Dakika'da saat)."""
    def yaz(d):
        kelime = "SON DAKİKA" if tip == "sd" else buyuk(d["ad"])
        ek = f'{d["ad"]} · {saat(d["b"])}' if tip == "sd" and saat else d.get("r", "Türkiye")
        n = em(kelime) * 1.04 + em(buyuk(ek), .17) + len(ek) * .17 * .12 + .3   # dev kelime + aralık + küçük yazı (0,17 em, harf aralığı .12)
        return f'<span class="kl-ic" data-olc-parca="kl-kelime" style="--n:{n:.2f}"><b>{e(kelime)}</b><small>{e(ek)}</small></span>'
    return f'<span class="kl-dev" aria-hidden="true">{al(yaz)}</span>'


ISKELETLER_KL = [
    dict(id="k", harf="K", ad="Bant", aile="Dikey öğe: kenarda bant",
         fikir="Sol alttan kategori renginde ince bir bant yükselir; ucundaki bayrakta logo, bantta dikey “Kategori · Bölge”; başlık bandın yanına, dibine hizalanır.",
         kaynak="Dikey etiket fikri BPT Haber'in ince şeridinden (yalnız çıkış noktası, biçimi alınmadı); logodan türeyip içeriğe uzanan çerçeve NowThis'ten; tek geometrik şekille kurulan sistem DW'den; kategoriye göre renk kodu Sky Sports'tan.",
         oz="Akışta bant ve bayrak her karede aynı yerde durduğu için çok tanınır; fotoğrafın üst yarısı tamamen serbest kalır. Bayrak logoyu tuvalin ortasına yakın taşır; logonun köşede olmasını isteyen için alışılmadık.",
         guc="guclu",
         orn=dict(logo="duz", etiket="duz", oge="yok", bvurgu="renkli", islem="gecis", kose="keskin"),
         yz=dict(_="koyu"), lz=dict(_="kat"),
         pasif=dict(etiket=dict(dikey="Bu iskelette etiket zaten bantta dikey yazılır."))),
    dict(id="l", harf="L", ad="Sırt", aile="Dikey öğe: dev dikey kelime",
         fikir="Kategori adı sağ kenarda kitap sırtı gibi dev ve dikey yazılır; başlık yanında, logo sol üstte. Son Dakika'da dev yazı “SON DAKİKA” olur.",
         kaynak="Fotoğraf üstünde tek kalın kelime Sky Sports'tan; sabit adla tekrar eden seri başlığı The Guardian'dan; dikey yazı fikri BPT Haber'den (yalnız çıkış noktası, biçimi alınmadı).",
         oz="Akışta en çok göze çarpan kalıp; kategori uzaktan okunur. Dev kelime başlığa yer bıraktığı için başlık sütunu daralır; uzun başlık bir adım küçülür.",
         guc="guclu",
         orn=dict(logo="duz", etiket="duz", oge="kalin", bvurgu="renkli", islem="gecis", kose="keskin"),
         yz=dict(_="koyu"), lz=dict(_="koyu"),
         pasif=dict(etiket=dict(dikey="Bu iskelette kategori zaten dev dikey kelimedir."))),
]
