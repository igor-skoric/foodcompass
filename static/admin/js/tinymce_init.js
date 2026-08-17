document.addEventListener('DOMContentLoaded', function () {
  if (!window.tinymce) return;

  function csrfToken() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : '';
  }

  tinymce.init({
    selector: '#id_body',
    height: 560,
    menubar: false,
    branding: false,
    plugins: 'lists link image table autolink',
    toolbar:
      'undo redo | blocks | bold italic underline | bullist numlist | link image | removeformat',
    automatic_uploads: true,
    convert_urls: false,
    relative_urls: false,
    images_upload_handler: function (blobInfo) {
      return new Promise(function (resolve, reject) {
        const form = new FormData();
        form.append('file', blobInfo.blob(), blobInfo.filename());
        fetch('/media-upload/', {
          method: 'POST',
          headers: { 'X-CSRFToken': csrfToken() },
          body: form,
          credentials: 'same-origin',
        })
          .then(function (res) {
            if (!res.ok) throw new Error('Upload nije uspeo.');
            return res.json();
          })
          .then(function (json) {
            if (!json.location) throw new Error('Nedostaje URL slike.');
            resolve(json.location);
          })
          .catch(function (err) {
            reject(err.message || err);
          });
      });
    },
    content_style: 'body{font-family:Georgia,serif;font-size:16px;line-height:1.65}',
  });
});
