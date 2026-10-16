(() => {
  const standalone = () => window.matchMedia('(display-mode: standalone)').matches || navigator.standalone === true;
  let installPrompt = null;
  window.addEventListener('beforeinstallprompt', event => {
    event.preventDefault();
    installPrompt = event;
  });
  const section = document.createElement('button');
  section.type = 'button';
  section.className = 'home-app-menu';
  section.textContent = 'ホーム画面に追加';
  const dialog = document.createElement('dialog');
  dialog.className = 'home-app-dialog';
  dialog.setAttribute('aria-labelledby', 'home-app-title');
  dialog.innerHTML = '<h2 id="home-app-title">ホーム画面に追加する方法</h2><p class="home-app-steps"></p><p>追加すると、月島のロゴからこのHPを開けます。</p><form method="dialog"><button class="button" autofocus>閉じる</button></form>';
  const apple = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  dialog.querySelector('.home-app-steps').textContent = apple
    ? 'SafariでこのHPを開き、メニューの「共有」→「ホーム画面に追加」→「追加」の順に押してください。「Webアプリとして開く」が表示される場合はオンにしてください。'
    : 'Chromeのメニュー（右上の「︙」）から「ホーム画面に追加」または「アプリをインストール」を選んでください。表示されない場合は、ChromeでこのHPを開き直してください。';
  const nav = document.querySelector('#main-nav');
  const toggle = document.querySelector('.menu-toggle');
  if (nav) nav.insertBefore(section, nav.querySelector('a.button'));
  else document.body.prepend(section);
  document.body.appendChild(dialog);
  const showInstalled = () => {
    dialog.querySelector('.home-app-steps').textContent = 'インストールしたアイコンが見つからない場合は、スマホのアプリ一覧で「月島HP」または「ネットインテリア月島」を探してください。アイコンを長押ししてホーム画面へ移動できます。';
  };
  dialog.addEventListener('close', () => { if (toggle && getComputedStyle(toggle).display !== 'none') toggle.focus(); });
  section.addEventListener('click', async () => {
    if (toggle) toggle.setAttribute('aria-expanded', 'false');
    nav?.classList.remove('is-open');
    if (standalone()) showInstalled();
    const prompt = installPrompt;
    installPrompt = null;
    if (prompt) {
      try {
        await prompt.prompt();
        const choice = await prompt.userChoice;
        if (choice.outcome === 'accepted') { showInstalled(); if (!dialog.open) dialog.showModal(); }
        return;
      } catch (_) { /* Browser instructions remain available when prompting fails. */ }
    }
    if (!dialog.open) dialog.showModal();
  });
  window.addEventListener('appinstalled', () => {
    installPrompt = null;
    showInstalled();
    if (!dialog.open) dialog.showModal();
  });

})();
