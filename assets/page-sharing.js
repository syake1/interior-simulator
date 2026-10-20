(() => {
  'use strict';
  const area = document.querySelector('.page-sharing');
  if (!area) return;
  const canonical = document.querySelector('link[rel="canonical"]')?.href;
  if (!canonical) return;
  const target = new URL(canonical);
  if (target.origin !== 'https://syake1.github.io' || !target.pathname.startsWith('/interior-simulator/')) return;
  target.search = ''; target.hash = '';
  const url = target.href;
  const status = area.querySelector('.sharing-status');
  const fallback = area.querySelector('.sharing-fallback');
  const field = fallback.querySelector('input');
  const track = (method) => {
    // Sharing is a user action; a handoff does not prove an SNS post was published.
    if (location.hostname === 'syake1.github.io' && typeof window.gtag === 'function') {
      window.gtag('event', 'page_share_action', { share_method: method });
    }
  };
  const copy = async () => {
    try {
      if (!navigator.clipboard?.writeText) throw new Error('clipboard unavailable');
      await navigator.clipboard.writeText(url);
      status.textContent = 'URLをコピーしました。LINEやメッセージに貼り付けて共有できます。';
      fallback.hidden = true;
      track('copy');
    } catch (_) {
      fallback.hidden = false;
      field.value = url; field.focus(); field.select();
      status.textContent = '下のURLを選択してコピーしてください。';
    }
  };
  area.querySelector('[data-copy-page]').addEventListener('click', copy);
  area.querySelector('[data-share-page]').addEventListener('click', async () => {
    if (!navigator.share) { await copy(); return; }
    try {
      await navigator.share({ title: document.title, url });
      status.textContent = '共有先への受け渡しが完了しました。';
      track('native_handoff');
    } catch (error) {
      if (error.name === 'AbortError') return;
      await copy();
    }
  });
})();
