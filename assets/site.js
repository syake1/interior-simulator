(() => {
  const config = window.SITE_CONFIG;
  const email = config.email;
  const experienceToggle = document.querySelector('.experience-toggle');
  if (experienceToggle) {
    experienceToggle.addEventListener('click', () => {
      const paused = experienceToggle.getAttribute('aria-pressed') !== 'true';
      experienceToggle.setAttribute('aria-pressed', String(paused));
      experienceToggle.textContent = paused ? '再生する' : '一時停止';
      document.querySelector('.experience-strip').classList.toggle('is-paused', paused);
    });
  }
  document.querySelectorAll('[data-email]').forEach(link => {
    link.href = `mailto:${email}?subject=${encodeURIComponent('内装工事のご相談')}`;
    if (link.hasAttribute('data-email-address')) link.textContent = email;
  });
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#main-nav');
  const closeMenu = () => { menu.setAttribute('aria-expanded', 'false'); nav.classList.remove('is-open'); };
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
  });
  nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
  document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });
  document.addEventListener('click', event => { if (!event.target.closest('.site-header')) closeMenu(); });
  document.querySelectorAll('[data-area]').forEach(el => {
    const cities = config.areas[el.dataset.area] || [];
    el.textContent = cities.length ? cities.join('・') : '県内の施工場所・工事内容をメールでお知らせください。';
  });
  document.querySelectorAll('[data-compare]').forEach(el => {
    const slider = el.querySelector('input');
    slider.addEventListener('input', () => el.style.setProperty('--compare', `${slider.value}%`));
  });
  const form = document.querySelector('#contact-form');
  if (form) {
    const preview = document.querySelector('#mail-preview');
    const status = document.querySelector('#form-status');
    form.addEventListener('submit', event => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const data = new FormData(form);
      const body = `ネットインテリア月島 ご担当者様\n\n内装工事について相談します。\n\nお名前：${data.get('name')}\nメールアドレス：${data.get('email')}\n施工希望地域：${data.get('region')}\n工事内容：${data.getAll('service').join('、') || '未定・相談したい'}\n\nお問い合わせ内容：\n${data.get('message')}\n\n`;
      preview.value = body;
      preview.closest('.mail-draft').hidden = false;
      const link = document.querySelector('#prepared-email');
      link.href = `mailto:${email}?subject=${encodeURIComponent('内装工事のご相談：' + data.get('name'))}&body=${encodeURIComponent(body)}`;
      status.textContent = 'メール文面を作成しました。下のボタンからメールアプリを開き、内容をご確認のうえ送信してください。まだお問い合わせは送信されていません。';
      link.focus();
    });
    document.querySelector('#copy-email').addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(preview.value);
        status.textContent = '文面をコピーしました。メールに貼り付けて送信してください。';
      } catch {
        preview.focus(); preview.select();
        status.textContent = '文面を選択しました。コピーしてメールに貼り付けてください。';
      }
    });
  }
})();
