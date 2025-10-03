# views.py
from django.views.generic import TemplateView
from django.shortcuts import render
from django.views import View

# View para a página inicial
class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

# View para a página geral
class GeralView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'geral.html')

# Views para os novos templates
class AdminView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'admin.html')

class ArtigoView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'artigo.html')

class ArtigosView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'artigos.html')

class DesastreView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'desastre.html')

class DesastresView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'desastres.html')

class GeneralizadoView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'generalizado.html')

class Index1View(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index1.html')

class JogoView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'jogo.html')

class Jogo1View(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'jogo1.html')

class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

class UsuarioView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'usuario.html')