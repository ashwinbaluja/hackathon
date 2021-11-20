from django.urls import path
from . import views

urlpatterns = [
    path('initialize/', views.create_self),
    path('create/', views.send_create),
]
