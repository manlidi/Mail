from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('inscription/', views.inscription, name='inscription'),
    path('login/', views.connexion, name='login'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('confirmation/', views.confirmation_page, name='confirmation'),
    path('confirm/<str:confirmation_token>/', views.confirmation_view, name='confirm'),
]
