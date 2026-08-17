from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('o-nama/', views.about, name='about'),
    path('o-meni/', views.about_me, name='about_me'),
    path('usluge/', views.services, name='services'),
    path('usluge/<slug:slug>/', views.service_detail, name='service_detail'),
    path('od-ideje-do-police/', views.journey, name='journey'),
    path('strucna-podrska/', views.support, name='support'),
    path('haccp-nadzor/', views.support, name='support_legacy'),
    path('aktuelnosti/', views.news_list, name='news'),
    path('aktuelnosti/<slug:slug>/', views.news_detail, name='news_detail'),
    path('kontakt/', views.contact, name='contact'),
]
