(() => {
  let dialog;
  const desktop = matchMedia('(min-width:901px) and (hover:hover)');
  document.addEventListener('click', event => {
    const button = event.target.closest('a[data-line]');
    if (!button || !desktop.matches || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button !== 0) return;
    event.preventDefault();
    if (!dialog) {
      dialog = document.createElement('dialog');
      dialog.className = 'line-contact-dialog';
      dialog.setAttribute('aria-labelledby', 'line-dialog-heading');
      dialog.innerHTML = '<button class="line-dialog-close" type="button" aria-label="LINEの案内を閉じる">閉じる ×</button><h2 id="line-dialog-heading">LINEでお問い合わせ</h2><p>スマホでQRコードを読み取り、友だち追加後にご相談内容をお送りください。</p><img class="line-dialog-qr" src="images/line-qr.png" width="200" height="200" alt="ネットインテリア月島のLINE友だち追加QRコード"><p class="note">施工箇所の写真も送れます。</p><div class="line-dialog-actions"><a class="button secondary" href="index.html">ホームに戻る</a><a class="line-dialog-external" href="https://page.line.me/793emvrc" target="_blank" rel="noopener noreferrer">LINEの友だち追加ページを開く ↗</a></div>';
      document.body.append(dialog);
      dialog.querySelector('button').addEventListener('click', () => dialog.close());
      dialog.addEventListener('click', e => { if (e.target === dialog) { const r = dialog.getBoundingClientRect(); if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dialog.close(); } });
    }
    dialog.showModal();
  });
})();
