(() => {
  const standalone = () => window.matchMedia('(display-mode: standalone)').matches || navigator.standalone === true;
  let installPrompt = null;
  window.addEventListener('beforeinstallprompt', event => {
    event.preventDefault();
    installPrompt = event;
  });
  const section = document.createElement('section');
  section.className = 'home-app';
  section.setAttribute('aria-label', 'ホーム画面への追加');
  section.innerHTML = '<img src="assets/app-icon-192.png" width="48" height="48" alt=""><div><strong>月島のHPをホーム画面に</strong><p>ロゴをタップして、次回からすぐに開けます。</p><button type="button" class="button home-app-add">ホーム画面に追加</button></div>';
  const dialog = document.createElement('dialog');
  dialog.className = 'home-app-dialog';
  dialog.setAttribute('aria-labelledby', 'home-app-title');
  dialog.innerHTML = '<h2 id="home-app-title">ホーム画面に追加する方法</h2><p class="home-app-steps"></p><p>追加すると、月島のロゴからこのHPを開けます。</p><form method="dialog"><button class="button" autofocus>閉じる</button></form>';
  const apple = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  dialog.querySelector('.home-app-steps').textContent = apple
    ? 'SafariでこのHPを開き、メニューの「共有」→「ホーム画面に追加」→「追加」の順に押してください。「Webアプリとして開く」が表示される場合はオンにしてください。'
    : 'Chromeのメニュー（右上の「︙」）から「ホーム画面に追加」または「アプリをインストール」を選んでください。表示されない場合は、ChromeでこのHPを開き直してください。';
  section.hidden = standalone();
  (document.querySelector('.footer') || document.body).appendChild(section);
  document.body.appendChild(dialog);
  section.querySelector('button').addEventListener('click', async () => {
    const prompt = installPrompt;
    installPrompt = null;
    if (prompt) {
      try {
        await prompt.prompt();
        const choice = await prompt.userChoice;
        if (choice.outcome === 'accepted') section.hidden = true;
        return;
      } catch (_) { /* Browser instructions remain available when prompting fails. */ }
    }
    if (!dialog.open) dialog.showModal();
  });
  window.addEventListener('appinstalled', () => {
    installPrompt = null;
    section.hidden = true;
    if (dialog.open) dialog.close();
  });
  window.matchMedia('(display-mode: standalone)').addEventListener('change', () => { section.hidden = standalone(); });
})();
