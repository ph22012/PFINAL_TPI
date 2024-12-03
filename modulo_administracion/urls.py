from django.urls import path
from . import views
urlpatterns = [
    path('', views.GeneralView, name='GeneralView'),
]