(function () {
  const button = document.getElementById('news-translate');
  const status = document.getElementById('news-translate-status');
  const overlay = document.getElementById('news-translate-overlay');
  if (!button) return;

  const url = button.getAttribute('data-translate-url');
  const hint = status ? status.textContent : '';

  function csrfToken() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : '';
  }

  function editor(id) {
    return window.tinymce && tinymce.get(id);
  }

  function fieldValue(id) {
    const tinymceEditor = editor(id);
    if (tinymceEditor) return tinymceEditor.getContent();
    const el = document.getElementById(id);
    return el ? el.value : '';
  }

  function setField(id, value) {
    const el = document.getElementById(id);
    if (el) el.value = value || '';
    const tinymceEditor = editor(id);
    if (tinymceEditor) tinymceEditor.setContent(value || '');
  }

  function hasTranslation() {
    return ['id_title_en', 'id_excerpt_en', 'id_body_en', 'id_title_ru', 'id_excerpt_ru', 'id_body_ru']
      .some(function (id) {
        return fieldValue(id).replace(/<[^>]*>/g, '').trim();
      });
  }

  function setStatus(text, kind) {
    if (!status) return;
    status.textContent = text || hint;
    status.classList.toggle('is-error', kind === 'error');
    status.classList.toggle('is-ok', kind === 'ok');
  }

  function notify(text, kind) {
    if (window.appShowToast) window.appShowToast(text, kind);
  }

  function setLoading(on) {
    button.disabled = on;
    document.documentElement.classList.toggle('app-translating', on);
    if (overlay) overlay.hidden = !on;
    if (on) setStatus('Tekst se prevodi…');
  }

  button.addEventListener('click', function () {
    if (window.tinymce) tinymce.triggerSave();
    const title = fieldValue('id_title');
    const excerpt = fieldValue('id_excerpt');
    const body = fieldValue('id_body');
    if (![title, excerpt, body].some(function (value) { return value.replace(/<[^>]*>/g, '').trim(); })) {
      setStatus('Prvo unesite srpski tekst.', 'error');
      notify('Prvo unesite srpski tekst.', 'error');
      return;
    }
    if (hasTranslation() && !window.confirm('Prepisati postojeći prevod na engleski i ruski?')) {
      return;
    }

    setLoading(true);

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken(),
      },
      credentials: 'same-origin',
      body: JSON.stringify({ title: title, excerpt: excerpt, body: body }),
    })
      .then(function (res) {
        return res.json().then(function (data) {
          if (!res.ok) throw new Error(data.error || 'Prevod nije uspeo.');
          return data;
        });
      })
      .then(function (data) {
        setField('id_title_en', data.title_en);
        setField('id_excerpt_en', data.excerpt_en);
        setField('id_body_en', data.body_en);
        setField('id_title_ru', data.title_ru);
        setField('id_excerpt_ru', data.excerpt_ru);
        setField('id_body_ru', data.body_ru);
        setStatus('Prevod je uspešan. Pregledajte ga i sačuvajte vest.', 'ok');
        notify('Tekst je uspešno preveden na engleski i ruski.', 'ok');
      })
      .catch(function (err) {
        const message = err.message || 'Prevod nije uspeo.';
        setStatus(message, 'error');
        notify(message, 'error');
      })
      .finally(function () {
        setLoading(false);
      });
  });
})();
