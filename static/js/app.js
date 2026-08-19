(function () {
  const TOAST_COPY = {
    created: 'Unos je dodat.',
    saved: 'Unos je sačuvan.',
  };

  function hideToast(el) {
    if (!el) return;
    el.classList.remove('is-visible');
    window.setTimeout(function () {
      el.remove();
    }, 280);
  }

  function showToast(text) {
    if (!text) return;
    document.querySelectorAll('.app-toast').forEach(function (node) {
      node.remove();
    });
    const el = document.createElement('div');
    el.className = 'app-toast';
    el.setAttribute('role', 'status');
    el.textContent = text;
    document.body.appendChild(el);
    window.requestAnimationFrame(function () {
      el.classList.add('is-visible');
    });
    const timer = window.setTimeout(function () {
      hideToast(el);
    }, 3400);
    el.addEventListener('click', function () {
      window.clearTimeout(timer);
      hideToast(el);
    });
  }

  window.appToast = showToast;

  const params = new URLSearchParams(window.location.search);
  const toastKey = params.get('toast');
  if (toastKey && TOAST_COPY[toastKey]) {
    showToast(TOAST_COPY[toastKey]);
    params.delete('toast');
    const next = params.toString();
    const clean = window.location.pathname + (next ? '?' + next : '') + window.location.hash;
    window.history.replaceState({}, '', clean);
  }
})();

(function () {
  const toolbar = document.querySelector('[data-filter]');
  const toggle = document.querySelector('[data-filter-toggle]');
  if (!toolbar || !toggle) return;

  function setOpen(open) {
    toolbar.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.textContent = open ? 'Zatvori filter' : 'Filter';
  }

  toggle.addEventListener('click', function () {
    setOpen(!toolbar.classList.contains('is-open'));
  });
})();

(function () {
  const app = document.querySelector('[data-app]');
  const burger = document.querySelector('[data-app-burger]');
  const backdrop = document.querySelector('[data-app-backdrop]');
  const sidebar = document.querySelector('[data-app-sidebar]');
  if (!app || !burger) return;

  function setOpen(open) {
    app.classList.toggle('is-nav-open', open);
    burger.classList.toggle('is-active', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.setAttribute('aria-label', open ? 'Zatvori meni' : 'Otvori meni');
    document.documentElement.classList.toggle('app-nav-open', open);
    if (backdrop) {
      backdrop.hidden = !open;
    }
  }

  burger.addEventListener('click', function () {
    setOpen(!app.classList.contains('is-nav-open'));
  });

  if (backdrop) {
    backdrop.addEventListener('click', function () {
      setOpen(false);
    });
  }

  if (sidebar) {
    sidebar.addEventListener('click', function (event) {
      const link = event.target.closest('a, button');
      if (link && window.matchMedia('(max-width: 860px)').matches) {
        setOpen(false);
      }
    });
  }

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') setOpen(false);
  });
})();
