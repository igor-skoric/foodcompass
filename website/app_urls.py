from django.urls import path
from django.views.generic import RedirectView
from . import app_views

urlpatterns = [
    path('', app_views.app_home, name='app_home'),
    path('poruke/', app_views.app_messages, name='app_messages'),
    path('poruke/<int:pk>/', app_views.app_message_detail, name='app_message_detail'),
    path('aktuelnosti/', app_views.app_news, name='app_news'),
    path('aktuelnosti/nova/', app_views.app_news_create, name='app_news_create'),
    path('aktuelnosti/<int:pk>/', app_views.app_news_detail, name='app_news_detail'),
    path('aktuelnosti/<int:pk>/izmena/', app_views.app_news_edit, name='app_news_edit'),
    path('saradnja/', app_views.app_partners, name='app_partners'),
    path('saradnja/novi/', app_views.app_partner_create, name='app_partner_create'),
    path('saradnja/<int:pk>/', app_views.app_partner_detail, name='app_partner_detail'),
    path('saradnja/<int:pk>/izmena/', app_views.app_partner_edit, name='app_partner_edit'),
    path('saradnici/', RedirectView.as_view(pattern_name='app_partners', permanent=False)),
    path('saradnici/novi/', RedirectView.as_view(pattern_name='app_partner_create', permanent=False)),
    path('saradnici/<int:pk>/', app_views.app_partner_detail_redirect),
    path('saradnici/<int:pk>/izmena/', app_views.app_partner_edit_redirect),
]
