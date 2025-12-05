from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import LoginForm, RegistroForm
from .models import (
    Usuario, Jogo, CaracteristicaJogo, RequisitoJogo, 
    AtualizacaoJogo, FAQJogo, ImagemJogo, Avaliacao, 
    PerguntaUsuario, Desastre, Artigo, Acontecimento,
    Risco, Pagina, Pergunta, TopicoArtigo, TopicoDesastre, TipoDesastre,
    PrevencaoDesastre, RecursoDesastre, EventoHistorico, ImagemDesastre
)
from django.db.models import Avg, Count, Q
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator

# View para a página inicial
class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

# Views para os novos templates
# Continuando a view AdminView no views.py

class AdminView(View):
    def get(self, request, *args, **kwargs):
        # Verificar se o usuário está logado
        if 'usuario_id' not in request.session:
            messages.error(request, 'Você precisa fazer login para acessar esta página.')
            return redirect('login')
        
        usuario_id = request.session.get('usuario_id')
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            if not usuario.is_admin:
                messages.error(request, 'Acesso restrito a administradores.')
                return redirect('index')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
            return redirect('index')
        
        # Obter seção ativa
        active_section = request.GET.get('section', 'dashboard')
        
        # Dados comuns para todas as seções
        base_context = {
            'user_info': {
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email,
                'tipo': usuario.tipo,
                'is_admin': usuario.is_admin,
                'is_authenticated': True
            },
            'active_section': active_section,
        }
        
        # Dados específicos por seção
        if active_section == 'dashboard':
            context = self.get_dashboard_context()
            context.update(base_context)
            return render(request, 'admin.html', context)
            
        elif active_section == 'users':
            context = self.get_users_context()
            context.update(base_context)
            return render(request, 'admin.html', context)
            
        elif active_section == 'articles':
            context = self.get_articles_context()
            context.update(base_context)
            return render(request, 'admin.html', context)
            
        elif active_section == 'disasters':
            context = self.get_disasters_context()
            context.update(base_context)
            return render(request, 'admin.html', context)
            
        elif active_section == 'games':
            context = self.get_games_context()
            context.update(base_context)
            return render(request, 'admin.html', context)
            
        elif active_section == 'questions':
            context = self.get_questions_context()
            context.update(base_context)
            return render(request, 'admin.html', context)
            
        elif active_section == 'ratings':
            context = self.get_ratings_context()
            context.update(base_context)
            return render(request, 'admin.html', context)
            
        elif active_section == 'settings':
            context = self.get_settings_context()
            context.update(base_context)
            return render(request, 'admin.html', context)
            
        elif active_section == 'logs':
            context = self.get_logs_context()
            context.update(base_context)
            return render(request, 'admin.html', context)
            
        else:
            context = self.get_dashboard_context()
            context.update(base_context)
            return render(request, 'admin.html', context)
    
    def get_dashboard_context(self):
        """Contexto para a seção Dashboard"""
        total_usuarios = Usuario.objects.count()
        total_artigos = Artigo.objects.count()
        total_desastres = Desastre.objects.count()
        total_jogos = Jogo.objects.filter(ativo=True).count()
        
        # Estatísticas recentes
        usuarios_recentes = Usuario.objects.filter(
            data__gte=timezone.now().date() - timedelta(days=30)
        ).count()
        
        # Perguntas pendentes
        perguntas_pendentes = PerguntaUsuario.objects.filter(status='pendente').count()
        
        # Avaliações recentes
        avaliacoes_recentes = Avaliacao.objects.filter(
            horario__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        # Top jogos por avaliação
        top_jogos = Jogo.objects.filter(ativo=True).annotate(
            avg_rating=Avg('avaliacao__nota')
        ).order_by('-avaliacao_media')[:5]
        
        # Últimas atividades
        ultimas_perguntas = PerguntaUsuario.objects.all().order_by('-data_envio')[:10]
        ultimos_usuarios = Usuario.objects.all().order_by('-data')[:10]
        ultimas_avaliacoes = Avaliacao.objects.all().order_by('-horario')[:10]
        
        # Dados para gráficos
        usuarios_por_tipo = Usuario.objects.values('tipo').annotate(
            total=Count('id')
        ).order_by('-total')
        
        return {
            'total_usuarios': total_usuarios,
            'total_artigos': total_artigos,
            'total_desastres': total_desastres,
            'total_jogos': total_jogos,
            'usuarios_recentes': usuarios_recentes,
            'perguntas_pendentes': perguntas_pendentes,
            'avaliacoes_recentes': avaliacoes_recentes,
            'top_jogos': top_jogos,
            'ultimas_perguntas': ultimas_perguntas,
            'ultimos_usuarios': ultimos_usuarios,
            'ultimas_avaliacoes': ultimas_avaliacoes,
            'usuarios_por_tipo': list(usuarios_por_tipo),
        }
    
    def get_users_context(self):
        """Contexto para a seção Usuários"""
        usuarios = Usuario.objects.all().order_by('-data')
        
        return {
            'usuarios': usuarios,
            'total_usuarios': usuarios.count(),
        }
    
    def get_articles_context(self):
        """Contexto para a seção Artigos"""
        artigos = Artigo.objects.all().order_by('-dataPublicacao')
        
        return {
            'artigos': artigos,
            'total_artigos': artigos.count(),
        }
    
    def get_disasters_context(self):
        """Contexto para a seção Desastres"""
        desastres = Desastre.objects.all().order_by('titulo')
        
        return {
            'desastres': desastres,
            'total_desastres': desastres.count(),
        }
    
    def get_games_context(self):
        """Contexto para a seção Jogos"""
        jogos = Jogo.objects.all().order_by('-data_lancamento')
        
        return {
            'jogos': jogos,
            'total_jogos': jogos.count(),
        }
    
    def get_questions_context(self):
        """Contexto para a seção Perguntas"""
        perguntas = PerguntaUsuario.objects.all().order_by('-data_envio')
        jogos = Jogo.objects.filter(ativo=True)
        
        return {
            'perguntas': perguntas,
            'jogos': jogos,
            'perguntas_pendentes': perguntas.filter(status='pendente').count(),
        }
    
    def get_ratings_context(self):
        """Contexto para a seção Avaliações"""
        avaliacoes = Avaliacao.objects.all().order_by('-horario')
        jogos = Jogo.objects.filter(ativo=True)
        
        return {
            'avaliacoes': avaliacoes,
            'jogos': jogos,
            'avaliacoes_recentes': avaliacoes.filter(
                horario__gte=timezone.now() - timedelta(days=7)
            ).count(),
        }
    
    def get_settings_context(self):
        """Contexto para a seção Configurações"""
        return {}
    
    def get_logs_context(self):
        """Contexto para a seção Logs"""
        return {}

class ArtigoView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'artigo.html')

class ArtigosView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'artigos.html')

# Adicione uma nova view para desastre detalhado
class DesastreView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'desastre.html')

class DesastreDetailView(View):
    def get(self, request, desastre_id, *args, **kwargs):
        try:
            # Buscar o desastre
            desastre = Desastre.objects.get(id=desastre_id)
            
            # Buscar detalhes
            detalhes = getattr(desastre, 'detalhes', None)
            
            # Buscar tipos
            tipos = TipoDesastre.objects.filter(desastre=desastre)
            
            # Buscar prevenções
            prevencoes = PrevencaoDesastre.objects.filter(desastre=desastre).order_by('ordem')
            
            # Buscar recursos
            recursos = RecursoDesastre.objects.filter(desastre=desastre).order_by('ordem')
            
            # Buscar eventos históricos
            eventos_historicos = EventoHistorico.objects.filter(desastre=desastre).order_by('-data')[:5]
            
            # Buscar imagens
            imagens = ImagemDesastre.objects.filter(desastre=desastre).order_by('ordem')[:4]
            
            # Dados padrão se não houver detalhes
            if not detalhes:
                # Criar dados padrão baseados no tipo de desastre
                dados_padrao = self.get_dados_padrao(desastre)
                context = {**dados_padrao, 'desastre': desastre}
            else:
                context = {
                    'desastre': desastre,
                    'detalhes': detalhes,
                    'tipos': tipos,
                    'prevencoes': prevencoes,
                    'recursos': recursos,
                    'eventos_historicos': eventos_historicos,
                    'imagens': imagens,
                }
            
            return render(request, 'desastre_detalhe.html', context)
            
        except Desastre.DoesNotExist:
            messages.error(request, 'Desastre não encontrado.')
            return redirect('desastres')
    
    def get_dados_padrao(self, desastre):
        """Retorna dados padrão para desastres sem detalhes cadastrados"""
        dados = {
            'detalhes': {
                'visao_geral_completa': f"Informações detalhadas sobre {desastre.titulo.lower()}. Este desastre natural pode causar sérios danos à infraestrutura e risco à vida humana.",
                'causas': "Movimento das placas tectônicas\nAtividade vulcânica\nDeslizamentos de terra subterrâneos",
                'medidas_prevencao': "Construções resistentes\nPlano familiar de emergência\nKit de emergência sempre à mão",
                'durante_desastre': "Mantenha a calma e procure abrigo\nAfaste-se de janelas e objetos pesados\nSiga as instruções das autoridades",
                'frequencia_global': "Varia conforme o tipo e região",
                'areas_risco': "Regiões próximas a falhas geológicas\nÁreas costeiras\nRegiões com atividade vulcânica",
            },
            'tipos': [],
            'prevencoes': [
                {'titulo': 'Construções resistentes', 'descricao': 'Edifícios devem seguir códigos de construção apropriados.', 'ordem': 1, 'icone': 'fas fa-building'},
                {'titulo': 'Plano familiar', 'descricao': 'Estabeleça pontos de encontro e comunicação para a família.', 'ordem': 2, 'icone': 'fas fa-users'},
                {'titulo': 'Kit de emergência', 'descricao': 'Mantenha água, comida e remédios acessíveis.', 'ordem': 3, 'icone': 'fas fa-first-aid'},
            ],
            'recursos': [
                {'titulo': 'Guia de Sobrevivência', 'tipo': 'guia', 'descricao': 'PDF com instruções detalhadas', 'url': '#', 'icone': 'fas fa-book'},
                {'titulo': 'Mapa de Risco', 'tipo': 'mapa', 'descricao': 'Mapa interativo de áreas de risco', 'url': '#', 'icone': 'fas fa-map'},
                {'titulo': 'Vídeo Educativo', 'tipo': 'video', 'descricao': 'Vídeo sobre prevenção', 'url': '#', 'icone': 'fas fa-video'},
            ],
            'eventos_historicos': [
                {'titulo': 'Evento Histórico 1', 'descricao': 'Descrição do evento histórico', 'data': '2020-01-01', 'localizacao': 'Localização', 'magnitude': '8.0'},
                {'titulo': 'Evento Histórico 2', 'descricao': 'Descrição do evento histórico', 'data': '2010-01-01', 'localizacao': 'Localização', 'magnitude': '7.5'},
            ],
            'imagens': [],
        }
        return dados


# Atualize a view DesastresView para listar todos os desastres
class DesastresView(View):
    def get(self, request, *args, **kwargs):
        # Buscar todos os desastres
        desastres = Desastre.objects.all()
        
        # Buscar desastres por categoria
        categorias = {
            'geologico': Desastre.objects.filter(tipos__categoria='geologico').distinct(),
            'meteorologico': Desastre.objects.filter(tipos__categoria='meteorologico').distinct(),
            'hidrologico': Desastre.objects.filter(tipos__categoria='hidrologico').distinct(),
            'climatico': Desastre.objects.filter(tipos__categoria='climatico').distinct(),
        }
        
        # Estatísticas
        total_desastres = desastres.count()
        desastres_recentes = Desastre.objects.filter(detalhes__isnull=False).count()
        
        context = {
            'desastres': desastres,
            'categorias': categorias,
            'total_desastres': total_desastres,
            'desastres_recentes': desastres_recentes,
        }
        
        return render(request, 'desastres.html', context)



class GeneralizadoView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'generalizado.html')

class JogoView(View):
    def get(self, request, *args, **kwargs):
        try:
            # Buscar o jogo principal
            jogo = Jogo.objects.filter(ativo=True).first()
            
            if not jogo:
                messages.error(request, 'Nenhum jogo disponível no momento.')
                return redirect('index')
            
            # Buscar FAQs visíveis
            faqs = FAQJogo.objects.filter(
                jogo=jogo, 
                ativo=True, 
                visivel=True
            ).order_by('ordem', 'categoria')
            
            # Agrupar FAQs por categoria
            faqs_por_categoria = {}
            for faq in faqs:
                categoria = faq.get_categoria_display()
                if categoria not in faqs_por_categoria:
                    faqs_por_categoria[categoria] = []
                faqs_por_categoria[categoria].append(faq)
            
            # Buscar dados relacionados
            caracteristicas = CaracteristicaJogo.objects.filter(jogo=jogo).order_by('ordem')
            requisitos_minimos = RequisitoJogo.objects.filter(jogo=jogo, tipo='minimo')
            requisitos_recomendados = RequisitoJogo.objects.filter(jogo=jogo, tipo='recomendado')
            atualizacoes = AtualizacaoJogo.objects.filter(jogo=jogo).order_by('-data')[:5]
            imagens = ImagemJogo.objects.filter(jogo=jogo).order_by('ordem')
            
            # Buscar avaliações de especialistas
            avaliacoes_especialistas = Avaliacao.objects.filter(
                jogo=jogo,
                usuario__tipo__in=['especialista', 'admin', 'editor']
            ).select_related('usuario').order_by('-nota')[:3]
            
            # Calcular média das avaliações
            media_avaliacoes = Avaliacao.objects.filter(jogo=jogo).aggregate(
                media=Avg('nota'),
                total=Count('id')
            )
            
            context = {
                'jogo': jogo,
                'caracteristicas': caracteristicas,
                'requisitos_minimos': requisitos_minimos,
                'requisitos_recomendados': requisitos_recomendados,
                'atualizacoes': atualizacoes,
                'faqs_por_categoria': faqs_por_categoria,
                'faqs': faqs,
                'imagens': imagens[:4],
                'avaliacoes_especialistas': avaliacoes_especialistas,
                'media_avaliacoes': media_avaliacoes['media'] or 4.8,
                'total_avaliacoes': media_avaliacoes['total'] or 50,
            }
            
            return render(request, 'jogo.html', context)
            
        except Exception as e:
            messages.error(request, f'Erro ao carregar informações do jogo: {str(e)}')
            return redirect('index')
    
    def post(self, request, *args, **kwargs):
        # Para o formulário de pergunta do usuário
        action = request.POST.get('action', 'enviar_pergunta')
        
        if action == 'enviar_pergunta':
            try:
                jogo = Jogo.objects.filter(ativo=True).first()
                
                if not jogo:
                    messages.error(request, 'Jogo não encontrado.')
                    return redirect('jogo')
                
                pergunta_texto = request.POST.get('pergunta', '').strip()
                email = request.POST.get('email', '').strip()
                
                if not pergunta_texto:
                    messages.error(request, 'Por favor, digite sua pergunta.')
                    return redirect('jogo')
                
                if not email:
                    messages.error(request, 'Por favor, forneça seu email para resposta.')
                    return redirect('jogo')
                
                # Verificar se o usuário está logado
                usuario = None
                if 'usuario_id' in request.session:
                    try:
                        usuario = Usuario.objects.get(id=request.session['usuario_id'])
                    except Usuario.DoesNotExist:
                        pass
                
                # Criar a pergunta do usuário
                PerguntaUsuario.objects.create(
                    usuario=usuario,
                    jogo=jogo,
                    pergunta=pergunta_texto,
                    email=email,
                    status='pendente'
                )
                
                messages.success(request, 'Pergunta enviada com sucesso! Responderemos em breve por email.')
                
            except Exception as e:
                messages.error(request, f'Erro ao enviar pergunta: {str(e)}')
        
        return redirect('jogo')

# View para login
class LoginView(View):
    def get(self, request, *args, **kwargs):
        # Se já estiver logado, redirecionar para index
        if 'usuario_id' in request.session:
            return redirect('index')
        
        form = LoginForm()
        registro_form = RegistroForm()
        tab = request.GET.get('tab', 'login')
        
        # Passar informações do usuário para o contexto
        user_info = None
        if 'usuario_id' in request.session:
            try:
                usuario = Usuario.objects.get(id=request.session['usuario_id'])
                user_info = {
                    'id': usuario.id,
                    'nome': usuario.nome,
                    'email': usuario.email,
                    'tipo': usuario.tipo,
                    'is_admin': usuario.is_admin,
                    'is_authenticated': True
                }
            except Usuario.DoesNotExist:
                pass
        
        return render(request, 'login.html', {
            'form': form,
            'registro_form': registro_form,
            'active_tab': tab,
            'user_info': user_info
        })

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get('email')
            senha = form.cleaned_data.get('senha')
            
            try:
                usuario = Usuario.objects.get(email=email)
                if usuario.verificar_senha(senha):
                    # Armazenar informações do usuário na sessão
                    request.session['usuario_id'] = usuario.id
                    request.session['usuario_nome'] = usuario.nome
                    request.session['usuario_email'] = usuario.email
                    request.session['usuario_tipo'] = usuario.tipo
                    
                    messages.success(request, f'Bem-vindo(a), {usuario.nome}!')
                    return redirect('index')
                else:
                    messages.error(request, 'Senha incorreta.')
            except Usuario.DoesNotExist:
                messages.error(request, 'Nenhum usuário encontrado com este email.')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
        
        registro_form = RegistroForm()
        
        # Passar informações do usuário para o contexto
        user_info = None
        if 'usuario_id' in request.session:
            try:
                usuario = Usuario.objects.get(id=request.session['usuario_id'])
                user_info = {
                    'id': usuario.id,
                    'nome': usuario.nome,
                    'email': usuario.email,
                    'tipo': usuario.tipo,
                    'is_admin': usuario.is_admin,
                    'is_authenticated': True
                }
            except Usuario.DoesNotExist:
                pass
        
        return render(request, 'login.html', {
            'form': form,
            'registro_form': registro_form,
            'active_tab': 'login',
            'user_info': user_info
        })

class RegistroView(View):
    def post(self, request, *args, **kwargs):
        registro_form = RegistroForm(request.POST)
        
        if registro_form.is_valid():
            try:
                usuario = registro_form.save()
                
                # Login automático após registro
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nome'] = usuario.nome
                request.session['usuario_email'] = usuario.email
                request.session['usuario_tipo'] = usuario.tipo
                
                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect('index')
            except Exception as e:
                messages.error(request, f'Erro ao criar usuário: {str(e)}')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
        
        # Se houver erros, mostrar formulário de login com erros de registro
        form = LoginForm()
        
        # Passar informações do usuário para o contexto
        user_info = None
        if 'usuario_id' in request.session:
            try:
                usuario = Usuario.objects.get(id=request.session['usuario_id'])
                user_info = {
                    'id': usuario.id,
                    'nome': usuario.nome,
                    'email': usuario.email,
                    'tipo': usuario.tipo,
                    'is_admin': usuario.is_admin,
                    'is_authenticated': True
                }
            except Usuario.DoesNotExist:
                pass
        
        return render(request, 'login.html', {
            'form': form,
            'registro_form': registro_form,
            'active_tab': 'register',
            'user_info': user_info
        })

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        # Limpar a sessão
        if 'usuario_id' in request.session:
            del request.session['usuario_id']
        if 'usuario_nome' in request.session:
            del request.session['usuario_nome']
        if 'usuario_email' in request.session:
            del request.session['usuario_email']
        if 'usuario_tipo' in request.session:
            del request.session['usuario_tipo']
        
        messages.success(request, 'Logout realizado com sucesso!')
        return redirect('index')

class UsuarioView(View):
    def get(self, request, *args, **kwargs):
        # Verificar se o usuário está logado
        if 'usuario_id' not in request.session:
            messages.error(request, 'Você precisa fazer login para acessar esta página.')
            return redirect('login')
        
        # Obter informações do usuário
        usuario_id = request.session.get('usuario_id')
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            
            # Preparar informações do usuário para o contexto
            user_info = {
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email,
                'tipo': usuario.tipo,
                'is_admin': usuario.is_admin,
                'is_authenticated': True
            }
            
            return render(request, 'usuario.html', {
                'usuario': usuario,
                'user_info': user_info
            })
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
            return redirect('index')
    
    def post(self, request, *args, **kwargs):
        # Verificar se o usuário está logado
        if 'usuario_id' not in request.session:
            messages.error(request, 'Você precisa fazer login para executar esta ação.')
            return redirect('login')
        
        usuario_id = request.session.get('usuario_id')
        action = request.POST.get('action')
        
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            
            if action == 'update_profile':
                # Atualizar informações do perfil
                usuario.nome = request.POST.get('nome')
                usuario.email = request.POST.get('email')
                usuario.tipo = request.POST.get('tipo', 'usuario')
                usuario.save()
                
                # Atualizar sessão
                request.session['usuario_nome'] = usuario.nome
                request.session['usuario_email'] = usuario.email
                request.session['usuario_tipo'] = usuario.tipo
                
                messages.success(request, 'Perfil atualizado com sucesso!')
                
            elif action == 'change_password':
                current_password = request.POST.get('current_password')
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')
                
                # Verificar senha atual
                if usuario.senha != current_password:
                    messages.error(request, 'Senha atual incorreta.')
                elif new_password != confirm_password:
                    messages.error(request, 'As senhas não coincidem.')
                else:
                    usuario.senha = new_password
                    usuario.save()
                    messages.success(request, 'Senha alterada com sucesso!')
            
            elif action == 'request_access':
                access_type = request.POST.get('access_type')
                message = request.POST.get('message', '')
                messages.info(request, f'Solicitação de acesso {access_type} enviada. Entraremos em contato em breve.')
            
            elif action == 'save_preferences':
                messages.success(request, 'Preferências salvas com sucesso!')
            
            return redirect('usuario')
            
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
            return redirect('index')

# API para o painel administrativo
@csrf_exempt
@require_POST
def admin_api(request, endpoint):
    """Endpoint de API para operações administrativas"""
    if 'usuario_id' not in request.session:
        return JsonResponse({'error': 'Não autorizado'}, status=401)
    
    try:
        usuario = Usuario.objects.get(id=request.session['usuario_id'])
        if not usuario.is_admin:
            return JsonResponse({'error': 'Permissão negada'}, status=403)
    except Usuario.DoesNotExist:
        return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    
    # Endpoints disponíveis
    if endpoint == 'update_user':
        user_id = data.get('id')
        
        try:
            user = Usuario.objects.get(id=user_id)
            if 'nome' in data:
                user.nome = data['nome']
            if 'email' in data:
                user.email = data['email']
            if 'tipo' in data:
                user.tipo = data['tipo']
            if 'ativo' in data:
                user.ativo = data['ativo']
            user.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Usuário atualizado com sucesso',
                'user': {
                    'id': user.id,
                    'nome': user.nome,
                    'email': user.email,
                    'tipo': user.tipo,
                    'ativo': user.ativo
                }
            })
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
    
    elif endpoint == 'delete_user':
        user_id = data.get('id')
        
        try:
            user = Usuario.objects.get(id=user_id)
            # Não permitir deletar a si mesmo
            if user.id == usuario.id:
                return JsonResponse({'error': 'Não pode deletar sua própria conta'}, status=400)
            
            user.delete()
            return JsonResponse({'success': True, 'message': 'Usuário deletado com sucesso'})
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
    
    elif endpoint == 'update_question_status':
        question_id = data.get('id')
        status = data.get('status')
        resposta = data.get('resposta', '')
        
        try:
            pergunta = PerguntaUsuario.objects.get(id=question_id)
            pergunta.status = status
            pergunta.resposta_admin = resposta
            pergunta.data_resposta = timezone.now()
            pergunta.admin_respondeu = usuario
            pergunta.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Status atualizado com sucesso',
                'pergunta': {
                    'id': pergunta.id,
                    'status': pergunta.status,
                    'data_resposta': pergunta.data_resposta.strftime('%d/%m/%Y %H:%M')
                }
            })
        except PerguntaUsuario.DoesNotExist:
            return JsonResponse({'error': 'Pergunta não encontrada'}, status=404)
    
    elif endpoint == 'get_users':
        # Obter usuários com filtros
        tipo = data.get('tipo')
        status = data.get('status')
        search = data.get('search')
        
        usuarios = Usuario.objects.all()
        
        if tipo and tipo != 'all':
            usuarios = usuarios.filter(tipo=tipo)
        
        if status and status != 'all':
            if status == 'active':
                usuarios = usuarios.filter(ativo=True)
            elif status == 'inactive':
                usuarios = usuarios.filter(ativo=False)
        
        if search:
            usuarios = usuarios.filter(
                Q(nome__icontains=search) |
                Q(email__icontains=search)
            )
        
        # Paginação
        page = data.get('page', 1)
        per_page = data.get('per_page', 10)
        paginator = Paginator(usuarios, per_page)
        
        try:
            page_obj = paginator.page(page)
            users_data = []
            for user in page_obj:
                users_data.append({
                    'id': user.id,
                    'nome': user.nome,
                    'email': user.email,
                    'tipo': user.tipo,
                    'ativo': user.ativo,
                    'data': user.data.strftime('%d/%m/%Y'),
                    'imagem': user.imagem
                })
            
            return JsonResponse({
                'success': True,
                'users': users_data,
                'total': paginator.count,
                'pages': paginator.num_pages,
                'current_page': page
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif endpoint == 'get_questions':
        # Obter perguntas com filtros
        status = data.get('status')
        jogo_id = data.get('jogo_id')
        search = data.get('search')
        
        perguntas = PerguntaUsuario.objects.all().select_related('usuario', 'jogo')
        
        if status and status != 'all':
            perguntas = perguntas.filter(status=status)
        
        if jogo_id and jogo_id != 'all':
            perguntas = perguntas.filter(jogo_id=jogo_id)
        
        if search:
            perguntas = perguntas.filter(
                Q(pergunta__icontains=search) |
                Q(email__icontains=search) |
                Q(usuario__nome__icontains=search)
            )
        
        # Paginação
        page = data.get('page', 1)
        per_page = data.get('per_page', 10)
        paginator = Paginator(perguntas.order_by('-data_envio'), per_page)
        
        try:
            page_obj = paginator.page(page)
            questions_data = []
            for question in page_obj:
                questions_data.append({
                    'id': question.id,
                    'usuario': question.usuario.nome if question.usuario else None,
                    'email': question.email,
                    'pergunta': question.pergunta,
                    'jogo': question.jogo.titulo,
                    'data_envio': question.data_envio.strftime('%d/%m/%Y %H:%M'),
                    'status': question.status,
                    'status_display': question.get_status_display(),
                    'tempo_decorrido': question.tempo_decorrido
                })
            
            return JsonResponse({
                'success': True,
                'questions': questions_data,
                'total': paginator.count,
                'pages': paginator.num_pages,
                'current_page': page
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif endpoint == 'export_data':
        # Exportar dados (exemplo: usuários)
        data_type = data.get('type', 'users')
        
        if data_type == 'users':
            usuarios = Usuario.objects.all().values('nome', 'email', 'tipo', 'ativo', 'data')
            data_list = list(usuarios)
            
            return JsonResponse({
                'success': True,
                'data': data_list,
                'type': 'users',
                'filename': f'usuarios_{timezone.now().strftime("%Y%m%d_%H%M%S")}.json'
            })
        
        elif data_type == 'questions':
            perguntas = PerguntaUsuario.objects.all().values(
                'pergunta', 'email', 'status', 'data_envio'
            )
            data_list = list(perguntas)
            
            return JsonResponse({
                'success': True,
                'data': data_list,
                'type': 'questions',
                'filename': f'perguntas_{timezone.now().strftime("%Y%m%d_%H%M%S")}.json'
            })
        
        return JsonResponse({'error': 'Tipo de exportação não suportado'}, status=400)
    
    return JsonResponse({'error': 'Endpoint não encontrado'}, status=404)