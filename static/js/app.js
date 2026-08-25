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

(function () {
  const root = document.querySelector('[data-payment-formset]');
  if (!root) return;

  const holder = root.querySelector('[data-payment-forms]');
  const template = root.querySelector('[data-payment-empty]');
  const addBtn = root.querySelector('[data-payment-add]');
  const totalInput = root.querySelector('input[name$="-TOTAL_FORMS"]');

  function bindDelete(row) {
    const checkbox = row.querySelector('input[type="checkbox"][name$="-DELETE"]');
    if (!checkbox) return;
    checkbox.addEventListener('change', function () {
      row.classList.toggle('is-removed', checkbox.checked);
    });
    if (checkbox.checked) row.classList.add('is-removed');
  }

  if (holder) {
    holder.querySelectorAll('[data-payment-form]').forEach(bindDelete);
  }

  if (addBtn && template && totalInput && holder) {
    addBtn.addEventListener('click', function () {
      const index = totalInput.value;
      const wrap = document.createElement('div');
      wrap.innerHTML = template.innerHTML.replace(/__prefix__/g, index).trim();
      const row = wrap.firstElementChild;
      if (!row) return;
      holder.appendChild(row);
      bindDelete(row);
      totalInput.value = Number(index) + 1;
      const amount = row.querySelector('input[name$="-amount"]');
      if (amount) amount.focus();
    });
  }
})();
