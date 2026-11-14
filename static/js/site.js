(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // mobile menu
  var burger = $('[data-burger]'), links = $('[data-links]');
  if (burger) burger.addEventListener('click', function () {
    var open = links.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
  });

  // dark / light toggle (remembered in this browser only)
  var tt = $('[data-theme-toggle]');
  if (tt) tt.addEventListener('click', function () {
    var root = document.documentElement;
    var dark = root.dataset.theme === 'dark' ||
      (!root.dataset.theme && matchMedia('(prefers-color-scheme: dark)').matches);
    root.dataset.theme = dark ? 'light' : 'dark';
    try { localStorage.setItem('theme', root.dataset.theme); } catch (e) {}
  });

  // project category filter
  var filters = $('[data-filters]');
  if (filters) filters.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    $$('button', filters).forEach(function (x) { x.classList.toggle('on', x === b); });
    $$('[data-grid] .project').forEach(function (c) {
      c.hidden = b.dataset.cat && c.dataset.cat !== b.dataset.cat;
    });
  });

  // click-to-load video embeds (no third-party request until the visitor presses play)
  $$('[data-embed]').forEach(function (el) {
    el.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = el.dataset.embed + (el.dataset.embed.indexOf('?') > -1 ? '&' : '?') + 'autoplay=1';
      f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      f.allowFullscreen = true; f.loading = 'lazy';
      el.innerHTML = ''; el.appendChild(f);
    }, { once: true });
  });
})();
