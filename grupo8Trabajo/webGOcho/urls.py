from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro'),
    path('administracion/', views.administracion, name='administracion'),

    path('alta_producto/', views.alta_producto, name='alta_producto'),
    path('eliminar_menu/<int:id_obj>', views.eliminar,name='eliminar'),
    path('editar_producto/<int:id_menu>', views.editar_producto, name='editar_producto'),

    path('eliminar_cliente/<int:id_obj>', views.eliminar_cliente, name='eliminar_cliente'),


    path("accounts/login/", auth_views.LoginView.as_view(template_name="webGOcho/registration/login.html"), name="login"),
    path("accounts/logout/", views.user_logout, name="logout"),
    path("accounts/password_reset/", auth_views.PasswordResetView.as_view(template_name="webApp/registration/password_reset.html"), name="password_reset")
]