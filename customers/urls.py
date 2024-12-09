from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.registro, name='signup'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('principal/', views.principal, name='principal'),
    path('logout/', views.custom_logout, name='logout'),
]