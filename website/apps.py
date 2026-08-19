from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'
    verbose_name = 'Sajt'

    def ready(self):
        import mimetypes
        mimetypes.add_type('application/manifest+json', '.webmanifest')
