from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('geral/', GeralView.as_view(), name='geral'),

    # Novas URLs
    path('admin_personalizado/', AdminView.as_view(), name='admin_personalizado'),
    path('artigo/', ArtigoView.as_view(), name='artigo'),
    path('artigos/', ArtigosView.as_view(), name='artigos'),
    path('artigos1/', Artigos1View.as_view(), name='artigos1'),
    path('desastre/', DesastreView.as_view(), name='desastre'),
    path('desastres/', DesastresView.as_view(), name='desastres'),
    path('generalizado/', GeneralizadoView.as_view(), name='generalizado'),
    path('index1/', Index1View.as_view(), name='index1'),
    path('jogo/', JogoView.as_view(), name='jogo'),
    path('jogo1/', Jogo1View.as_view(), name='jogo1'),
    path('login/', LoginView.as_view(), name='login'),
    path('usuario/', UsuarioView.as_view(), name='usuario'),
]