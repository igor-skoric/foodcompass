(function () {
  const TOAST_COPY = {
    created: 'Unos je dodat.',
    saved: 'Unos je sačuvan.',
    deleted: 'Unos je obrisan.',
    translated: 'Vest je sačuvana. Prevod na engleski i ruski je popunjen.',
  };

  function hideToast(el) {
    if (!el) return;
    el.classList.remove('is-visible');
    window.setTimeout(function () {
      el.remove();
    }, 280);
  }

  function showToast(text, kind) {
    if (!text) return;
    document.querySelectorAll('.app-toast').forEach(function (node) {
      node.remove();
    });
    const el = document.createElement('div');
    el.className = 'app-toast' + (kind ? ' app-toast--' + kind : '');
    el.setAttribute('role', kind === 'error' ? 'alert' : 'status');
    el.textContent = text;
    document.body.appendChild(el);
    window.requestAnimationFrame(function () {
      el.classList.add('is-visible');
    });
    const timer = window.setTimeout(function () {
      hideToast(el);
    }, kind === 'error' ? 5200 : 3800);
    el.addEventListener('click', function () {
      window.clearTimeout(timer);
      hideToast(el);
    });
  }

  window.appShowToast = showToast;

  const params = new URLSearchParams(window.location.search);
  const toastKey = params.get('toast');
  if (toastKey && TOAST_COPY[toastKey]) {
    showToast(TOAST_COPY[toastKey]);
    params.delete('toast');
    const next = params.toString();
    const clean = window.location.pathname + (next ? '?' + next : '') + window.location.hash;
    window.history.replaceState({}, '', clean);
  }

  const serverErrors = [];
  document.querySelectorAll(
    '.app-form .errorlist li, .app-form .contact-form__error, .app-login__form .contact-form__error'
  ).forEach(function (node) {
    const field = node.closest('.field');
    const label = field && field.querySelector(':scope > span');
    const text = (node.textContent || '').replace(/\s+/g, ' ').trim();
    if (!text) return;
    serverErrors.push(label ? (label.textContent.trim() + ': ' + text) : text);
  });
  if (serverErrors.length) {
    showToast(serverErrors.filter(function (item, index) {
      return serverErrors.indexOf(item) === index;
    }).join(' '), 'error');
  }
})();

(function () {
  const dialog = document.querySelector('[data-confirm-dialog]');
  const titleEl = document.getElementById('app-confirm-title');
  const textEl = document.getElementById('app-confirm-text');
  const acceptBtn = dialog && dialog.querySelector('[data-confirm-accept]');
  const cancelBtn = dialog && dialog.querySelector('[data-confirm-cancel]');
  if (!dialog || !titleEl || !textEl || !acceptBtn || !cancelBtn) return;

  const app = document.querySelector('[data-app]');
  const dismissEls = dialog.querySelectorAll('[data-confirm-dismiss]');
  let pendingForm = null;
  let lastFocus = null;

  function setOpen(open) {
    dialog.hidden = !open;
    document.documentElement.classList.toggle('app-confirm-open', open);
    if (app) app.inert = open;
    if (open) {
      cancelBtn.focus();
    } else if (lastFocus && typeof lastFocus.focus === 'function') {
      lastFocus.focus();
    }
  }

  function close() {
    pendingForm = null;
    setOpen(false);
  }

  document.querySelectorAll('form[data-confirm]').forEach(function (form) {
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      pendingForm = form;
      lastFocus = document.activeElement;
      titleEl.textContent = form.getAttribute('data-confirm-title') || 'Obrisati unos?';
      textEl.textContent = form.getAttribute('data-confirm') || 'Ova radnja se ne može opozvati.';
      setOpen(true);
    });
  });

  acceptBtn.addEventListener('click', function () {
    const form = pendingForm;
    if (!form) {
      close();
      return;
    }
    pendingForm = null;
    setOpen(false);
    form.submit();
  });

  dismissEls.forEach(function (el) {
    el.addEventListener('click', close);
  });

  document.addEventListener('keydown', function (event) {
    if (dialog.hidden) return;
    if (event.key === 'Escape') {
      event.preventDefault();
      close();
      return;
    }
    if (event.key !== 'Tab') return;
    const focusable = Array.prototype.slice.call(
      dialog.querySelectorAll('button:not([disabled])')
    );
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });
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

  function localToday() {
    const now = new Date();
    return new Date(now.getTime() - now.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
  }

  function fillPaymentDate(row) {
    const paid = row.querySelector('input[type="date"][name$="-paid_on"]');
    if (paid && !paid.value) paid.value = localToday();
  }

  function bindDelete(row) {
    const checkbox = row.querySelector('input[type="checkbox"][name$="-DELETE"]');
    if (!checkbox) return;
    checkbox.addEventListener('change', function () {
      row.classList.toggle('is-removed', checkbox.checked);
    });
    if (checkbox.checked) row.classList.add('is-removed');
  }

  if (holder) {
    holder.querySelectorAll('[data-payment-form]').forEach(function (row) {
      bindDelete(row);
      fillPaymentDate(row);
    });
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
      fillPaymentDate(row);
      totalInput.value = Number(index) + 1;
      const amount = row.querySelector('input[name$="-amount"]');
      if (amount) amount.focus();
    });
  }
})();
