from django.urls import path
from . import views
from django.urls import path, reverse_lazy

app_name = 'usuarios'

urlpatterns = [
    path('cadastro', views.cadastro_usuario, name='cadastro'),
    path('login', views.login_usuario, name='login'),
    path('logout', views.logout_usuario, name='logout'),
    path('menu', views.user_menu, name='user_menu'),
    path('index', views.return_index, name='index'),
    path('listar_usuarios', views.listar_usuarios, name='listar_usuarios'),
    path('deletar_usuario/<int:user_id>/', views.deletar_usuario, name='deletar_usuario'),

]
