from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_game, name='create_game'),
    path('join/', views.join_game, name='join_game'),
    path('game/<str:code>/', views.multiplayer_game, name='multiplayer_game'),
    path('single/', views.play, name='play'),
] 