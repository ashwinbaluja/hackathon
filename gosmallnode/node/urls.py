
from django.urls import path
from . import views

urlpatterns = [
    path('newcompany/', views.receive_create),
    path('preparereceive/', views.trust_receive),
    path('products/', views.get_products),
    path('missing/', views.fix_missing),
]
