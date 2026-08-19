# Food Compass

Django sajt — Food Compass.

## Pokretanje

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_news
python manage.py createsuperuser
python manage.py runserver
```

Sajt: http://127.0.0.1:8000/
Admin: http://127.0.0.1:8000/admin/

Lokalni rad ne zahteva `.env` fajl (`DEBUG` ostaje uključen).

## Deploy

1. Kopiraj `.env.example` u `.env` na serveru i popuni vrednosti, uključujući SMTP za kontakt formu (`EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `CONTACT_EMAIL`).
2. Generiši tajni ključ:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

3. Na Linux VPS-u (preporučeno):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
gunicorn config.wsgi:application --config gunicorn.conf.py
```

Ispred Gunicorna stavi Nginx ili Caddy sa HTTPS. Kada SSL radi, u `.env` uključi `DJANGO_SSL_REDIRECT=true`.

Folderi `media/` i `db.sqlite3` moraju da ostanu na disku (nisu u gitu). Ako koristiš Nginx za fajlove, isključi `DJANGO_SERVE_MEDIA`.

Za Railway / Render / slične PaaS servise dovoljni su `Procfile` i `runtime.txt`.

## Jezici

Pripremljena je trojezična struktura (SR / ENG / RU). Tekst je trenutno samo na srpskom — prevodi dolaze kasnije.

## Aktuelnosti

Administratori u Django adminu mogu da dodaju tekst, naslovnu sliku i dodatne slike. U editoru je moguće i ubacivanje slika u sam tekst.
