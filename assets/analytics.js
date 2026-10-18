(() => {
  'use strict';
  const tag = document.currentScript;
  const id = tag?.dataset.measurementId || '';
  // Keep local previews and setup checks out of the business reports.
  if (location.hostname !== 'syake1.github.io' || !location.pathname.startsWith('/interior-simulator/') || !/^G-[A-Z0-9]+$/.test(id)) return;
  if (window.__tsukishimaAnalyticsLoaded) return;
  window.__tsukishimaAnalyticsLoaded = true;
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  const page = new URL(location.href);
  page.search = ''; page.hash = '';
  let referrer = '';
  try { const ref = new URL(document.referrer); ref.search = ''; ref.hash = ''; referrer = ref.href; } catch (_) {}
  window.gtag('js', new Date());
  const settings = {
    page_location: page.href,
    page_referrer: referrer,
    allow_google_signals: false,
    allow_ad_personalization_signals: false
  };
  // Label the owner's public social-profile links without forwarding arbitrary URL parameters.
  const source = new URL(location.href).searchParams.get('utm_source')?.toLowerCase();
  if (['line', 'instagram', 'facebook', 'x'].includes(source)) {
    settings.campaign_source = source;
    settings.campaign_medium = 'social';
    settings.campaign_name = 'profile';
  }
  window.gtag('config', id, settings);
  const script = document.createElement('script');
  script.async = true;
  script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
  document.head.appendChild(script);
  document.addEventListener('click', event => {
    const link = event.target.closest('a[data-line]');
    if (!link) return;
    const area = link.closest('.site-header') ? 'header' : link.closest('.mobile-cta') ? 'mobile_bar' : link.closest('.footer') ? 'footer' : 'content';
    window.gtag('event', 'line_contact_click', { link_area: area });
  });
})();
