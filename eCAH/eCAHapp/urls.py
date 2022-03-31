
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('salas/', views.lobby, name='lobby'),
    path('salas/nuevasala/', views.new_room, name='newroom'),
    path('salas/verificanick/', views.nickcheck, name='nickCheck'),
    path('salas/<str:room_name>/', views.created_room, name='room'),
    path('acerca_del_juego', views.about, name='about'),
    path('contacto', views.contact, name='contact'),
]