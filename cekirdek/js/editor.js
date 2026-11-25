/* =====================================================================
   ÇEKİRDEK · ZENGİN METİN EDİTÖRÜ (TipTap 2, assets/vendor/tiptap-2.27.3)
   Uzun metin alanı olan her yerde aynı editör (Tutarlılık): haber gövdesi, açıklamalar,
   yasal metinler, sayfalar. Beyar seçimi: 24.11.2026.

   Kullanım:
     <div class="kb-editor" data-editor-ad="Haber Metni" [data-editor-kisa] [data-editor-medya]>
       <div class="kz-alan ke-alan" data-zorunlu> …başlangıç HTML… </div>
     </div>
   - data-editor-kisa : kısa alan (açıklama); başlık ve medya düğmeleri yok.
   - data-editor-medya: görsel, video ve gömülü içerik düğmeleri (Multimedya modülüyle bağlanır).
   - Alt çubukta kelime, karakter ve okuma süresi.
   - Bağlantı ekleme satır içi kutudan (tarayıcının açılır kutusu kullanılmaz).
   ===================================================================== */
(function(){
  'use strict';
  var T = window.TipTap; if(!T) return;
  function dugme(k, ikon, ad, ek){ return '<button type="button" data-ke="' + k + '" title="' + ad + '" aria-label="' + ad + '"' + (ek || '') + '><i class="fa-solid ' + ikon + '" aria-hidden="true"></i></button>'; }
  var AYIR = '<span class="kz-ayir"></span>';

  document.querySelectorAll('.kb-editor').forEach(function(K){
    var alan = K.querySelector('.ke-alan'); if(!alan || alan._kbEditor) return;
    var kisa = K.hasAttribute('data-editor-kisa'), medya = K.hasAttribute('data-editor-medya'), ad = K.getAttribute('data-editor-ad') || 'Metin';
    var ilk = alan.innerHTML.trim(); alan.innerHTML = '';

    var arac = document.createElement('div'); arac.className = 'ke-arac'; arac.setAttribute('role', 'toolbar'); arac.setAttribute('aria-label', ad + ' biçimi');
    arac.innerHTML = (kisa ? '' : '<div class="ke-blok" role="group" aria-label="Paragraf türü"><button type="button" data-ke="p" aria-pressed="false">Paragraf</button><button type="button" data-ke="h2" aria-pressed="false">Ara başlık</button><button type="button" data-ke="h3" aria-pressed="false">Alt başlık</button></div>' + AYIR)
      + dugme('bold', 'fa-bold', 'Kalın (⌘B)') + dugme('italic', 'fa-italic', 'İtalik (⌘I)') + dugme('underline', 'fa-underline', 'Altı çizili (⌘U)') + (kisa ? '' : dugme('strike', 'fa-strikethrough', 'Üstü çizili'))
      + dugme('link', 'fa-link', 'Bağlantı (⌘K)') + AYIR
      + dugme('bulletList', 'fa-list-ul', 'Madde listesi') + dugme('orderedList', 'fa-list-ol', 'Numaralı liste') + (kisa ? '' : dugme('blockquote', 'fa-quote-right', 'Alıntı') + dugme('hr', 'fa-minus', 'Ayırıcı çizgi'))
      + (medya ? AYIR + dugme('gorsel', 'fa-image', 'Görsel ekle') + dugme('video', 'fa-video', 'Video ekle') + dugme('gomulu', 'fa-code', 'Gömülü içerik (X, Instagram, YouTube)') : '')
      + AYIR + dugme('temizle', 'fa-text-slash', 'Biçimi temizle') + dugme('undo', 'fa-rotate-left', 'Geri al (⌘Z)') + dugme('redo', 'fa-rotate-right', 'Yinele (⇧⌘Z)');
    var link = document.createElement('div'); link.className = 'ke-link'; link.hidden = true;
    link.innerHTML = '<i class="fa-solid fa-link" aria-hidden="true"></i><input type="url" placeholder="https://… ya da dadahaber.com/…" aria-label="Bağlantı adresi"><button type="button" class="btn btn-acc btn-sm" data-ke-link="uygula">Uygula</button><button type="button" class="btn btn-ghost btn-sm" data-ke-link="kaldir">Kaldır</button><button type="button" class="kb-bag" data-ke-link="vazgec">Vazgeç</button>';
    var alt = document.createElement('div'); alt.className = 'ke-alt';
    K.insertBefore(arac, alan); K.insertBefore(link, alan); K.appendChild(alt);

    var ed = new T.Editor({
      element: alan,
      extensions: [
        T.StarterKit.configure({ heading: { levels: [2, 3] }, codeBlock: false, code: false }),
        T.Underline,
        T.Link.configure({ openOnClick: false, autolink: true, HTMLAttributes: { rel: 'noopener', target: null } }),
        T.Placeholder.configure({ placeholder: K.getAttribute('data-editor-yer') || (ad + ' yazın…') }),
        T.CharacterCount
      ],
      content: ilk || '<p></p>',
      editorProps: { attributes: { 'aria-label': ad, role: 'textbox', 'aria-multiline': 'true', class: 'ke-icerik' } },
      onUpdate: function(){ durum(); K.dispatchEvent(new Event('input', { bubbles:true })); },
      onSelectionUpdate: durum, onFocus: function(){ K.classList.add('is-odak'); }, onBlur: function(){ K.classList.remove('is-odak'); }
    });
    alan._kbEditor = ed;

    function durum(){
      arac.querySelectorAll('[data-ke]').forEach(function(b){
        var k = b.dataset.ke, on = false;
        if(k === 'p') on = ed.isActive('paragraph'); else if(k === 'h2') on = ed.isActive('heading', { level:2 }); else if(k === 'h3') on = ed.isActive('heading', { level:3 });
        else if(/^(bold|italic|underline|strike|link|bulletList|orderedList|blockquote)$/.test(k)) on = ed.isActive(k);
        b.classList.toggle('is-on', on); if(b.hasAttribute('aria-pressed') || on) b.setAttribute('aria-pressed', on);
        if(k === 'undo') b.disabled = !ed.can().undo(); if(k === 'redo') b.disabled = !ed.can().redo();
      });
      var kel = ed.storage.characterCount.words(), kar = ed.storage.characterCount.characters();
      alt.innerHTML = '<span><b>' + kel.toLocaleString('tr') + '</b> kelime</span><span><b>' + kar.toLocaleString('tr') + '</b> karakter</span><span>Okuma <b>' + Math.max(1, Math.round(kel / 200)) + ' dk</b></span>';
    }
    function linkAc(){
      link.hidden = false; var i = link.querySelector('input'); i.value = ed.getAttributes('link').href || ''; i.focus(); i.select();
    }
    function linkKapat(){ link.hidden = true; ed.commands.focus(); }
    arac.addEventListener('mousedown', function(e){ if(e.target.closest('button')) e.preventDefault(); });
    arac.addEventListener('click', function(e){
      var b = e.target.closest('[data-ke]'); if(!b) return;
      var k = b.dataset.ke, c = ed.chain().focus();
      if(k === 'p') c.setParagraph().run(); else if(k === 'h2') c.toggleHeading({ level:2 }).run(); else if(k === 'h3') c.toggleHeading({ level:3 }).run();
      else if(k === 'bold') c.toggleBold().run(); else if(k === 'italic') c.toggleItalic().run(); else if(k === 'underline') c.toggleUnderline().run(); else if(k === 'strike') c.toggleStrike().run();
      else if(k === 'bulletList') c.toggleBulletList().run(); else if(k === 'orderedList') c.toggleOrderedList().run(); else if(k === 'blockquote') c.toggleBlockquote().run();
      else if(k === 'hr') c.setHorizontalRule().run(); else if(k === 'temizle') c.unsetAllMarks().clearNodes().run();
      else if(k === 'undo') c.undo().run(); else if(k === 'redo') c.redo().run();
      else if(k === 'link') linkAc();
      else if(k === 'gorsel' || k === 'video' || k === 'gomulu') window.kbBildir({ gorsel:'Metne görsel ekleme medya havuzundan açılacak (Multimedya modülüyle)', video:'Metne video ekleme Multimedya modülüyle gelecek', gomulu:'Gömülü içerik (X, Instagram, YouTube) Multimedya modülüyle gelecek' }[k]);
      durum();
    });
    link.addEventListener('click', function(e){
      var b = e.target.closest('[data-ke-link]'); if(!b) return;
      var v = link.querySelector('input').value.trim();
      if(b.dataset.keLink === 'uygula'){ if(v){ if(!/^https?:\/\//.test(v)) v = 'https://' + v.replace(/^\/+/, ''); ed.chain().focus().extendMarkRange('link').setLink({ href: v }).run(); } else ed.chain().focus().extendMarkRange('link').unsetLink().run(); }
      if(b.dataset.keLink === 'kaldir') ed.chain().focus().extendMarkRange('link').unsetLink().run();
      linkKapat(); durum();
    });
    link.querySelector('input').addEventListener('keydown', function(e){ if(e.key === 'Enter'){ e.preventDefault(); link.querySelector('[data-ke-link="uygula"]').click(); } if(e.key === 'Escape'){ e.stopPropagation(); linkKapat(); } });
    K.addEventListener('keydown', function(e){ if((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k'){ e.preventDefault(); linkAc(); } });
    durum();
  });
  /* AI adımı ve "yeni kayıt" için: alanın içeriğini editör üzerinden yaz */
  window.kbEditorYaz = function(alan, html){ if(alan && alan._kbEditor) alan._kbEditor.commands.setContent(html || '<p></p>', true); else if(alan) alan.innerHTML = html; };
})();
