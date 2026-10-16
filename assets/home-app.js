(() => {
  const standalone = () => matchMedia('(display-mode: standalone)').matches || navigator.standalone === true;
  const android = /Android/i.test(navigator.userAgent);
  const embedded = /Line\/|; wv\)|\bwv\b|GSA\/|FBAN|FBAV|Instagram/i.test(navigator.userAgent);
  let installPrompt = null, installed = false, busy = false, accepted = false;
  const entry = document.createElement('button');
  entry.type = 'button'; entry.className = 'home-app-menu'; entry.textContent = 'ホーム画面に追加';
  const nav = document.querySelector('#main-nav');
  const toggle = document.querySelector('.menu-toggle');
  const share = document.createElement('a');
  share.className = 'home-app-share'; share.textContent = 'LINEで紹介';
  const shareUrl = new URL('./', document.baseURI);
  shareUrl.searchParams.set('openExternalBrowser', '1');
  share.href = 'https://line.me/R/share?text=' + encodeURIComponent('ネットインテリア月島\n' + shareUrl.href);
  if (nav) nav.insertBefore(share, nav.querySelector('a.button'));
  if (nav) nav.insertBefore(entry, nav.querySelector('a.button'));
  else document.body.prepend(entry);
  const dialog = document.createElement('dialog');
  dialog.className = 'home-app-dialog'; dialog.setAttribute('aria-labelledby', 'home-app-title');
  dialog.innerHTML = '<h2 id="home-app-title"></h2><p class="home-app-steps" aria-live="polite"></p><div class="home-app-actions"><button type="button" class="button home-app-install" hidden>インストールする</button><a class="button home-app-chrome" hidden>Chromeで開く</a><a class="home-app-external" hidden>外部ブラウザで開く</a></div><form method="dialog"><button class="button" autofocus>閉じる</button></form>';
  document.body.appendChild(dialog);
  const title = dialog.querySelector('h2'), steps = dialog.querySelector('.home-app-steps');
  const installButton = dialog.querySelector('.home-app-install');
  const chromeLink = dialog.querySelector('.home-app-chrome'), externalLink = dialog.querySelector('.home-app-external');
  const target = new URL('index.html', document.baseURI);
  target.searchParams.set('install', '1'); target.searchParams.set('openExternalBrowser', '1');
  chromeLink.href = 'intent://' + target.host + target.pathname + target.search + '#Intent;scheme=https;package=com.android.chrome;S.browser_fallback_url=' + encodeURIComponent(target.href) + ';end';
  externalLink.href = target.href;
  function render() {
    installButton.hidden = true; chromeLink.hidden = true; externalLink.hidden = true;
    if (installed || standalone()) {
      title.textContent = 'ホーム画面のアイコンを確認';
      steps.textContent = 'アプリ一覧で「月島HP」または「ネットインテリア月島」を探し、アイコンを長押ししてホーム画面へ移動してください。';
    } else if (accepted) {
      title.textContent = '追加処理を受け付けました';
      steps.textContent = 'ブラウザでインストール処理中です。完了後、アプリ一覧で「月島HP」を確認してください。';
    } else if (installPrompt) {
      title.textContent = 'ホーム画面に追加';
      steps.textContent = '下の「インストールする」を押し、続いてAndroidの確認画面で追加を確定してください。';
      installButton.hidden = false;
    } else if (android) {
      title.textContent = embedded ? 'Chromeで開いて追加' : 'ホーム画面への追加';
      steps.textContent = embedded
        ? '現在は別のアプリ内で開いているため、この画面ではホーム画面への追加ができません。「Chromeで開く」を押し、移動先で三本線のメニューから「ホーム画面に追加」を押してください。'
        : 'この画面ではまだ追加されていません。インストール画面を表示できる状態になると、ここに「インストールする」ボタンが出ます。表示されない場合はChromeのメニューにある「インストールしてショートカットを作成」または「ホーム画面に追加」を選んでください。';
      chromeLink.hidden = false;
      externalLink.hidden = !embedded;
    } else {
      title.textContent = 'ホーム画面に追加する方法';
      steps.textContent = 'iPhoneはSafariでこのHPを開き、「共有」→「ホーム画面に追加」→「追加」の順に押してください。';
    }
  }
  async function install() {
    if (busy) return;
    const prompt = installPrompt;
    if (!prompt) { render(); if (!dialog.open) dialog.showModal(); return; }
    busy = true; installPrompt = null;
    try {
      await prompt.prompt();
      const choice = await prompt.userChoice;
      accepted = choice.outcome === 'accepted';
    } catch (_) { accepted = false; }
    finally { busy = false; render(); if (!dialog.open) dialog.showModal(); }
  }
  window.addEventListener('beforeinstallprompt', event => {
    event.preventDefault(); installPrompt = event; accepted = false; render();
  });
  entry.addEventListener('click', () => {
    toggle?.setAttribute('aria-expanded', 'false'); nav?.classList.remove('is-open');
    install();
  });
  installButton.addEventListener('click', install);
  window.addEventListener('appinstalled', () => { installed = true; installPrompt = null; render(); });
  dialog.addEventListener('close', () => { if (toggle && getComputedStyle(toggle).display !== 'none') toggle.focus(); });
  render();
  if (new URL(location.href).searchParams.get('install') === '1') { render(); dialog.showModal(); }
})();
