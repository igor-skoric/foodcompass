from django.urls import path
from django.views.generic import RedirectView
from . import app_views


def _auth_redirect(name):
    return app_views.owner_required(RedirectView.as_view(pattern_name=name, permanent=False))


urlpatterns = [
    path('', app_views.app_home, name='app_home'),
    path('poruke/', app_views.app_messages, name='app_messages'),
    path('poruke/<int:pk>/', app_views.app_message_detail, name='app_message_detail'),
    path('aktuelnosti/', app_views.app_news, name='app_news'),
    path('aktuelnosti/nova/', app_views.app_news_create, name='app_news_create'),
    path('aktuelnosti/prevod/', app_views.app_news_translate, name='app_news_translate'),
    path('aktuelnosti/<int:pk>/', app_views.app_news_detail, name='app_news_detail'),
    path('aktuelnosti/<int:pk>/izmena/', app_views.app_news_edit, name='app_news_edit'),
    path('klijenti/', app_views.app_partners, name='app_partners'),
    path('klijenti/novi/', app_views.app_partner_create, name='app_partner_create'),
    path('klijenti/<int:pk>/', app_views.app_partner_detail, name='app_partner_detail'),
    path('klijenti/<int:pk>/izmena/', app_views.app_partner_edit, name='app_partner_edit'),
    path('saradnja/', _auth_redirect('app_partners')),
    path('saradnja/novi/', _auth_redirect('app_partner_create')),
    path('saradnja/<int:pk>/', _auth_redirect('app_partner_detail')),
    path('saradnja/<int:pk>/izmena/', _auth_redirect('app_partner_edit')),
    path('saradnici/', _auth_redirect('app_partners')),
    path('saradnici/novi/', _auth_redirect('app_partner_create')),
    path('saradnici/<int:pk>/', _auth_redirect('app_partner_detail')),
    path('saradnici/<int:pk>/izmena/', _auth_redirect('app_partner_edit')),
]
