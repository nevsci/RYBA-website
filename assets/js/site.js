'use strict';

// The HTML remains usable without JavaScript. Enhance only the interactive parts.
document.documentElement.classList.add('js');

const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('.site-nav');
function closeMenu() {
  menuButton.setAttribute('aria-expanded', 'false');
  navigation.classList.remove('is-open');
}
menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('is-open', open);
});
navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    menuButton.focus();
  }
});

document.querySelectorAll('.mascot-stage').forEach(logo => {
  logo.addEventListener('click', () => {
    const flipped = !logo.classList.contains('is-flipped');
    logo.classList.toggle('is-flipped', flipped);
    logo.setAttribute('aria-pressed', String(flipped));
  });
});

const tabs = [...document.querySelectorAll('.preview-tab')];
const panels = [...document.querySelectorAll('.preview-panel')];
const tablist = document.querySelector('.preview-tabs');
tablist.setAttribute('role', 'tablist');
tablist.setAttribute('aria-label', 'Explore RYBA workspaces');
function selectTab(tab, moveFocus = false) {
  tabs.forEach(item => {
    const selected = item === tab;
    item.setAttribute('aria-selected', String(selected));
    item.tabIndex = selected ? 0 : -1;
  });
  panels.forEach(panel => { panel.hidden = panel.id !== tab.getAttribute('aria-controls'); });
  if (moveFocus) tab.focus();
}
tabs.forEach((tab, index) => {
  tab.setAttribute('role', 'tab');
  tab.addEventListener('click', () => selectTab(tab));
  tab.addEventListener('keydown', event => {
    let next;
    if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
    if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = tabs.length - 1;
    if (next !== undefined) { event.preventDefault(); selectTab(tabs[next], true); }
  });
});
panels.forEach(panel => { panel.setAttribute('role', 'tabpanel'); panel.tabIndex = 0; });
selectTab(tabs[0]);

if ('IntersectionObserver' in window) {
  const links = [...navigation.querySelectorAll('.nav-link[href^="#"]')];
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      links.forEach(link => {
        if (link.hash === '#' + entry.target.id) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    });
  }, { rootMargin: '-20% 0px -55% 0px', threshold: 0 });
  links.forEach(link => { const section = document.querySelector(link.hash); if (section) observer.observe(section); });
}

// Canonical source: the main website's download page. Never mirror installers here.
// Keep the verified HTML fallback links in sync whenever editing the website.
const DOWNLOADS_PAGE = 'https://nevesely.science/downloads/';
function formatFor(url) {
  if (/\/Windows\/RYBA_[^/]+_x64-setup\.exe$/i.test(url.pathname)) return 'windows-setup';
  if (/\/Windows\/RYBA_[^/]+_windows-x86_64_portable\.exe$/i.test(url.pathname)) return 'windows-portable';
  if (/\/Linux\/RYBA_[^/]+\.deb$/i.test(url.pathname)) return 'deb';
  if (/\/Linux\/RYBA_[^/]+\.AppImage$/i.test(url.pathname)) return 'appimage';
  if (/\/MacOS\/RYBA_[^/]+\.app\.zip$/i.test(url.pathname)) return 'macos';
  return null;
}
async function refreshDownloads() {
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 8000);
    let response;
    try { response = await fetch(DOWNLOADS_PAGE, { signal: controller.signal, credentials: 'omit', cache: 'no-cache' }); }
    finally { clearTimeout(timeout); }
    if (!response.ok) return;
    const page = new DOMParser().parseFromString(await response.text(), 'text/html');
    const found = new Map();
    page.querySelectorAll('a[href]').forEach(sourceLink => {
      const url = new URL(sourceLink.getAttribute('href'), DOWNLOADS_PAGE);
      if (url.origin !== 'https://nevesely.science' || !url.pathname.startsWith('/assets/projects/RYBA/')) return;
      const format = formatFor(url);
      if (format && !found.has(format)) found.set(format, { url, sourceLink });
    });
    // Refresh as a complete set, so an incomplete response cannot mix releases.
    if (!['windows-setup', 'windows-portable', 'deb', 'appimage', 'macos'].every(format => found.has(format))) return;
    for (const [format, { url, sourceLink }] of found) {
      const target = document.querySelector('[data-download="' + format + '"]');
      if (!target) continue;
      const filename = decodeURIComponent(url.pathname.split('/').pop());
      target.href = url.href;
      target.querySelector('.file-name').textContent = filename;
      for (const attribute of ['data-goatcounter-click', 'data-goatcounter-title', 'data-goatcounter-no-session']) {
        const value = sourceLink.getAttribute(attribute);
        if (value !== null) target.setAttribute(attribute, value);
        else target.removeAttribute(attribute);
      }
      const version = filename.match(/^RYBA_(\d+(?:\.\d+)+)/);
      document.querySelectorAll('[data-release-for="' + format + '"]').forEach(label => {
        label.textContent = version ? 'Version ' + version[1] : 'Latest build';
      });
    }
  } catch (_) {
    // A network failure leaves the verified, working HTML links in place.
  }
}
refreshDownloads();


// Enhance image links with a full-size view; links still work without JavaScript.
const overviewLightbox = document.querySelector('#overview-lightbox');
if (overviewLightbox && typeof overviewLightbox.showModal === 'function') {
  const lightboxImage = overviewLightbox.querySelector('#overview-lightbox-image');
  const lightboxTitle = overviewLightbox.querySelector('#overview-lightbox-title');
  const originalLink = overviewLightbox.querySelector('#overview-original-link');
  let previousImageLink;
  document.querySelectorAll('a[data-overview-image]').forEach(link => {
    link.addEventListener('click', event => {
      if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      previousImageLink = link;
      lightboxImage.src = link.href;
      lightboxImage.alt = link.dataset.imageAlt;
      lightboxTitle.textContent = link.dataset.imageTitle;
      originalLink.href = link.href;
      overviewLightbox.showModal();
    });
  });
  overviewLightbox.querySelector('.overview-lightbox-close').addEventListener('click', () => overviewLightbox.close());
  overviewLightbox.addEventListener('click', event => {
    if (event.target !== overviewLightbox) return;
    const bounds = overviewLightbox.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right ||
        event.clientY < bounds.top || event.clientY > bounds.bottom) overviewLightbox.close();
  });
  overviewLightbox.addEventListener('close', () => previousImageLink?.focus());
}
