from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro'),
    path('administracion/', views.administracion, name='administracion'),
    path('alta_producto/', views.alta_producto, name='alta_producto')
]