from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static

from website import views

admin.site.site_header = 'Food Compass administracija'
admin.site.site_title = 'Food Compass'
admin.site.index_title = 'Upravljanje sajtom'

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('media-upload/', views.upload_image, name='upload_image'),
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('', include('website.urls')),
    prefix_default_language=False,
)

if settings.DEBUG or settings.SERVE_MEDIA:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
