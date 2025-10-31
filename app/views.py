from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import *


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class GeralView(View):
    def get(self, request, *args, **kwargs):
        jogos = Jogo.objects.all()
        membros = MembroEquipe.objects.all()
        tarefas = Tarefa.objects.all()
        return render(request, 'geral.html', {'jogos': jogos,'membros': membros,'tarefas': tarefas})


# Jogo e Relacionados

class JogosView(View):
    def get(self, request, *args, **kwargs):
        jogos = Jogo.objects.all()
        return render(request, 'jogos.html', {'jogos': jogos})


class DeleteJogoView(View):
    def get(self, request, id, *args, **kwargs):
        jogo = get_object_or_404(Jogo, id=id)
        jogo.delete()
        messages.success(request, "Jogo excluído com sucesso!")
        return redirect('jogos')


class EditarJogoView(View):
    def get(self, request, id, *args, **kwargs):
        jogo = get_object_or_404(Jogo, id=id)
        return render(request, 'editar_jogo.html', {'jogo': jogo})


class PlataformasView(View):
    def get(self, request, *args, **kwargs):
        plataformas = PlataformaJogo.objects.all()
        return render(request, 'plataformas.html', {'plataformas': plataformas})


class JogoPlataformaView(View):
    def get(self, request, *args, **kwargs):
        relacoes = Jogo_Plataforma.objects.all()
        return render(request, 'jogo_plataformas.html', {'relacoes': relacoes})


# Estúdio, Cidades e Equipe

class EstudioView(View):
    def get(self, request, *args, **kwargs):
        estudios = EstudioDesenvolvimento.objects.all()
        return render(request, 'estudios.html', {'estudios': estudios})


class CidadesView(View):
    def get(self, request, *args, **kwargs):
        cidades = Cidade.objects.all()
        return render(request, 'cidades.html', {'cidades': cidades})


class MembrosView(View):
    def get(self, request, *args, **kwargs):
        membros = MembroEquipe.objects.all()
        return render(request, 'membros.html', {'membros': membros})


class FuncoesView(View):
    def get(self, request, *args, **kwargs):
        funcoes = Funcao.objects.all()
        return render(request, 'funcoes.html', {'funcoes': funcoes})


# Alocação e Desenvolvimento

class AlocacoesView(View):
    def get(self, request, *args, **kwargs):
        alocacoes = Alocacao.objects.all()
        return render(request, 'alocacoes.html', {'alocacoes': alocacoes})


class EtapasView(View):
    def get(self, request, *args, **kwargs):
        etapas = EtapaDesenvolvimento.objects.all()
        return render(request, 'etapas.html', {'etapas': etapas})


class TarefasView(View):
    def get(self, request, *args, **kwargs):
        tarefas = Tarefa.objects.all()
        return render(request, 'tarefas.html', {'tarefas': tarefas})


class TarefaDetalheView(View):
    def get(self, request, *args, **kwargs):
        detalhes = TarefaDetalhe.objects.all()
        return render(request, 'detalhes_tarefas.html', {'detalhes': detalhes})


class ComponentesView(View):
    def get(self, request, *args, **kwargs):
        componentes = ComponenteProjetoJogo.objects.all()
        return render(request, 'componentes.html', {'componentes': componentes})


class TurnosView(View):
    def get(self, request, *args, **kwargs):
        turnos = TurnoTrabalho.objects.all()
        return render(request, 'turnos.html', {'turnos': turnos})


# Cenários e Assets

class CenariosView(View):
    def get(self, request, *args, **kwargs):
        cenarios = Cenario.objects.all()
        return render(request, 'cenarios.html', {'cenarios': cenarios})


class AssetsView(View):
    def get(self, request, *args, **kwargs):
        assets = AssetDigital.objects.all()
        return render(request, 'assets.html', {'assets': assets})


class CenarioAssetView(View):
    def get(self, request, *args, **kwargs):
        relacoes = Cenario_Asset.objects.all()
        return render(request, 'cenarios_assets.html', {'relacoes': relacoes})


# Análises e Ocorrências

class TiposAnaliseView(View):
    def get(self, request, *args, **kwargs):
        tipos = TipoAnalise.objects.all()
        return render(request, 'tipos_analise.html', {'tipos': tipos})


class FormulariosView(View):
    def get(self, request, *args, **kwargs):
        AnaliseProcessos = AnaliseProcesso.objects.all()
        return render(request, 'AnaliseProcessos.html', {'AnaliseProcessos': AnaliseProcessos})


class OcorrenciasView(View):
    def get(self, request, *args, **kwargs):
        ocorrencias = Ocorrencia.objects.all()
        return render(request, 'ocorrencias.html', {'ocorrencias': ocorrencias})


# Sistema

class UsuariosSistemaView(View):
    def get(self, request, *args, **kwargs):
        usuarios = UsuarioSistema.objects.all()
        return render(request, 'usuarios.html', {'usuarios': usuarios})


class ConfiguracoesSistemaView(View):
    def get(self, request, *args, **kwargs):
        configuracoes = ConfiguracaoSistema.objects.all()
        return render(request, 'configuracoes.html', {'configuracoes': configuracoes})

class JogosView(View):
    def get(self, request):
        busca = request.GET.get('q')
        if busca:
            jogos = Jogo.objects.filter(titulo__icontains=busca)
        else:
            jogos = Jogo.objects.all()
        return render(request, 'jogos.html', {'jogos': jogos})