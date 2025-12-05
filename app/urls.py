from django.urls import path
from .views import (
    IndexView, AdminView, ArtigoView, ArtigosView,
    DesastreView, DesastresView, GeneralizadoView,
    JogoView, LoginView, UsuarioView, RegistroView, 
    LogoutView, DesastreDetailView , admin_api
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin-personalizado/', AdminView.as_view(), name='admin_personalizado'),
    path('admin-api/<str:endpoint>/', admin_api, name='admin_api'),
    path('artigo/', ArtigoView.as_view(), name='artigo'),
    path('artigos/', ArtigosView.as_view(), name='artigos'),
    path('desastres/', DesastresView.as_view(), name='desastres'),
    path('desastre/<int:desastre_id>/', DesastreDetailView.as_view(), name='desastre_detalhe'),
    path('desastre/', DesastreView.as_view(), name='desastre'),  # Mantenha para compatibilidade
    path('generalizado/', GeneralizadoView.as_view(), name='generalizado'),
    path('jogo/', JogoView.as_view(), name='jogo'),
    path('login/', LoginView.as_view(), name='login'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('usuario/', UsuarioView.as_view(), name='usuario'),
]