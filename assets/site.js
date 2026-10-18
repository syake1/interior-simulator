(() => {
  const config = window.SITE_CONFIG;

  const experienceToggle = document.querySelector('.experience-toggle');
  if (experienceToggle) {
    experienceToggle.addEventListener('click', () => {
      const paused = experienceToggle.getAttribute('aria-pressed') !== 'true';
      experienceToggle.setAttribute('aria-pressed', String(paused));
      experienceToggle.textContent = paused ? '再生する' : '一時停止';
      document.querySelector('.experience-strip').classList.toggle('is-paused', paused);
    });
  }
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
    el.textContent = cities.length ? cities.join('・') : '県内の施工場所・工事内容をLINEでお知らせください。';
  });
  document.querySelectorAll('[data-compare]').forEach(el => {
    const slider = el.querySelector('input');
    slider.addEventListener('input', () => el.style.setProperty('--compare', `${slider.value}%`));
  });
})();
