# app/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from app.models import (
    Usuario, Jogo, CaracteristicaJogo, RequisitoJogo, 
    AtualizacaoJogo, FAQJogo, ImagemJogo,
    Desastre, Acontecimento, Risco, Artigo, Pagina,
    Avaliacao, TopicoArtigo, TopicoDesastre, Pergunta,
    PerguntaUsuario
)
from datetime import date, datetime
import random

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de exemplo'
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando população do banco de dados...'))
        
        # Limpar dados existentes (opcional - comente se não quiser limpar)
        # self.limpar_dados()
        
        # Criar usuários
        self.criar_usuarios()
        
        # Criar desastres
        self.criar_desastres()
        
        # Criar jogos com todas as relações
        self.criar_jogos()
        
        # Criar artigos
        self.criar_artigos()
        
        # Criar acontecimentos
        self.criar_acontecimentos()
        
        # Criar riscos
        self.criar_riscos()
        
        # Criar páginas
        self.criar_paginas()
        
        # Criar avaliações
        self.criar_avaliacoes()
        
        # Criar perguntas
        self.criar_perguntas()
        
        self.stdout.write(self.style.SUCCESS('Banco de dados populado com sucesso!'))
    
    def limpar_dados(self):
        """Limpa todos os dados existentes (opcional)"""
        self.stdout.write('Limpando dados existentes...')
        
        # Remova o comentário abaixo se quiser limpar os dados
        # PerguntaUsuario.objects.all().delete()
        # Pergunta.objects.all().delete()
        # Avaliacao.objects.all().delete()
        # Pagina.objects.all().delete()
        # TopicoDesastre.objects.all().delete()
        # TopicoArtigo.objects.all().delete()
        # Risco.objects.all().delete()
        # Acontecimento.objects.all().delete()
        # Artigo.objects.all().delete()
        # ImagemJogo.objects.all().delete()
        # FAQJogo.objects.all().delete()
        # AtualizacaoJogo.objects.all().delete()
        # RequisitoJogo.objects.all().delete()
        # CaracteristicaJogo.objects.all().delete()
        # Jogo.objects.all().delete()
        # Desastre.objects.all().delete()
        # Usuario.objects.all().delete()
        
        self.stdout.write(self.style.WARNING('Dados limpos!'))
    
    def criar_usuarios(self):
        """Cria usuários de exemplo"""
        self.stdout.write('Criando usuários...')
        
        usuarios = [
            {
                'nome': 'Admin Master',
                'email': 'admin@acriseg.com',
                'senha': 'admin123',
                'tipo': 'admin',
                'imagem': 'https://ui-avatars.com/api/?name=Admin+Master&background=FF6B6B&color=fff&size=200'
            },
            {
                'nome': 'João Editor',
                'email': 'editor@acriseg.com',
                'senha': 'editor123',
                'tipo': 'editor',
                'imagem': 'https://s2.glbimg.com/Pk8F42ljoy9IYRk0E4eH0ikhho0=/640x424/top/i.glbimg.com/og/ig/infoglobo/f/original/2021/04/09/img_0857.jpg'
            },
            {
                'nome': 'Maria Usuária',
                'email': 'maria@exemplo.com',
                'senha': 'maria123',
                'tipo': 'usuario',
                'imagem': 'https://ui-avatars.com/api/?name=Maria+Usuario&background=45B7D1&color=fff&size=200'
            },
            {
                'nome': 'Carlos Especialista',
                'email': 'carlos@especialista.com',
                'senha': 'especialista123',
                'tipo': 'especialista',
                'imagem': 'https://ui-avatars.com/api/?name=Carlos+Especialista&background=96CEB4&color=fff&size=200'
            },
            {
                'nome': 'Ana Professora',
                'email': 'ana@escola.com',
                'senha': 'professora123',
                'tipo': 'usuario',
                'imagem': 'https://ui-avatars.com/api/?name=Ana+Professora&background=FECA57&color=fff&size=200'
            }
        ]
        
        for user_data in usuarios:
            # Verifica se o usuário já existe
            if not Usuario.objects.filter(email=user_data['email']).exists():
                usuario = Usuario.objects.create(
                    nome=user_data['nome'],
                    email=user_data['email'],
                    senha=make_password(user_data['senha']),  # Hash da senha
                    tipo=user_data['tipo'],
                    imagem=user_data.get('imagem'),
                    data=date.today()
                )
                self.stdout.write(f"  ✓ Usuário criado: {user_data['nome']} ({user_data['email']})")
            else:
                self.stdout.write(f"  ⏭ Usuário já existe: {user_data['email']}")
        
        self.stdout.write(self.style.SUCCESS(f'{len(usuarios)} usuários processados!'))
    
    def criar_desastres(self):
        """Cria desastres naturais"""
        self.stdout.write('Criando desastres...')
        
        desastres = [
            {
                'titulo': 'Enchentes',
                'descricao': 'Inundações causadas por chuvas intensas, transbordamento de rios ou marés altas',
                'icone': '🌊'
            },
            {
                'titulo': 'Queimadas',
                'descricao': 'Incêndios florestais e urbanos de grandes proporções',
                'icone': '🔥'
            },
            {
                'titulo': 'Terremotos',
                'descricao': 'Tremores de terra causados por movimentos tectônicos',
                'icone': '🌍'
            },
            {
                'titulo': 'Furacões',
                'descricao': 'Tempestades tropicais com ventos de alta velocidade',
                'icone': '🌀'
            },
            {
                'titulo': 'Secas',
                'descricao': 'Períodos prolongados de escassez de água',
                'icone': '☀️'
            },
            {
                'titulo': 'Deslizamentos',
                'descricao': 'Movimento de massa de terra e rochas em encostas',
                'icone': '⛰️'
            }
        ]
        
        for desastre_data in desastres:
            if not Desastre.objects.filter(titulo=desastre_data['titulo']).exists():
                Desastre.objects.create(**desastre_data)
                self.stdout.write(f"  ✓ Desastre criado: {desastre_data['titulo']}")
        
        self.stdout.write(self.style.SUCCESS(f'{len(desastres)} desastres criados!'))
    
    def criar_jogos(self):
        """Cria jogos com todas as relações"""
        self.stdout.write('Criando jogo principal...')
        
        # Verifica se o jogo já existe
        if Jogo.objects.filter(titulo="Survivor: Desafio da Natureza").exists():
            jogo = Jogo.objects.get(titulo="Survivor: Desafio da Natureza")
            self.stdout.write(f"  ⏭ Jogo já existe: {jogo.titulo}")
        else:
            # Criar jogo principal
            jogo = Jogo.objects.create(
                titulo="Survivor: Desafio da Natureza",
                subtitulo="Um jogo educativo imersivo que ensina sobre preparação e resposta a desastres naturais",
                descricao="Desenvolvido em parceria com especialistas em gestão de crises.",
                descricao_detalhada="Survivor: Desafio da Natureza é um jogo educativo que combina aprendizado com diversão. Através de simulações realistas, os jogadores aprendem a identificar riscos, tomar decisões críticas e implementar medidas de prevenção contra desastres naturais. O jogo foi desenvolvido em colaboração com geólogos, meteorologistas e especialistas em defesa civil.",
                desenvolvedor="A Crise G Studios",
                plataformas="Windows, Android, iOS",
                idade_recomendada="12+ anos",
                tamanho="850MB (PC) / 320MB (Mobile)",
                versao="1.3.2",
                download_windows="https://example.com/download/windows",
                download_android="https://example.com/download/android",
                download_ios="https://example.com/download/ios",
                imagem_capa="https://images.unsplash.com/photo-1593113630400-ea4288922497?q=80&w=1000",
                data_lancamento=date(2024, 1, 15),
                ativo=True,
                jogadores_ativos=50000,
                avaliacao_media=4.8,
                tempo_jogo_medio="12h",
                aprendizado_efetivo="95%"
            )
            self.stdout.write(f"  ✓ Jogo criado: {jogo.titulo}")
        
        # Características do jogo
        self.stdout.write('  Adicionando características...')
        caracteristicas = [
            ("fas fa-bolt", "Simulações realistas de 6 tipos de desastres naturais"),
            ("fas fa-brain", "Sistema de tomada de decisões com consequências"),
            ("fas fa-user-check", "Conteúdo validado por especialistas"),
            ("fas fa-clock", "Modo história com 12+ horas de gameplay"),
            ("fas fa-gamepad", "Desafios rápidos para aprendizagem objetiva"),
            ("fas fa-chart-line", "Estatísticas de desempenho detalhadas"),
            ("fas fa-users", "Modo multiplayer cooperativo"),
            ("fas fa-trophy", "Sistema de conquistas e recompensas"),
            ("fas fa-book", "Biblioteca de conhecimento integrada"),
            ("fas fa-mobile-alt", "Interface otimizada para dispositivos móveis"),
        ]
        
        for i, (icone, desc) in enumerate(caracteristicas):
            if not CaracteristicaJogo.objects.filter(jogo=jogo, descricao=desc).exists():
                CaracteristicaJogo.objects.create(
                    jogo=jogo,
                    icone=icone,
                    descricao=desc,
                    ordem=i
                )
        
        # Requisitos mínimos
        self.stdout.write('  Adicionando requisitos mínimos...')
        requisitos_min = [
            "Windows 10 64-bit",
            "Intel i3 ou equivalente AMD",
            "4GB RAM",
            "Placa de vídeo com 1GB VRAM (DirectX 11)",
            "2GB de espaço livre em disco",
            "Conexão internet para ativação",
            "Resolução mínima 1280x720"
        ]
        
        for req in requisitos_min:
            if not RequisitoJogo.objects.filter(jogo=jogo, tipo='minimo', descricao=req).exists():
                RequisitoJogo.objects.create(jogo=jogo, tipo='minimo', descricao=req)
        
        # Requisitos recomendados
        self.stdout.write('  Adicionando requisitos recomendados...')
        requisitos_rec = [
            "Windows 11 64-bit",
            "Intel i5 ou equivalente AMD Ryzen 5",
            "8GB RAM",
            "Placa de vídeo com 2GB VRAM (DirectX 12)",
            "4GB de espaço livre em SSD",
            "Conexão internet banda larga",
            "Resolução 1920x1080"
        ]
        
        for req in requisitos_rec:
            if not RequisitoJogo.objects.filter(jogo=jogo, tipo='recomendado', descricao=req).exists():
                RequisitoJogo.objects.create(jogo=jogo, tipo='recomendado', descricao=req)
        
        # Atualizações
        self.stdout.write('  Adicionando atualizações...')
        atualizacoes = [
            ("1.3", date(2025, 8, 25), "Novo cenário de seca extrema adicionado", "Inclui mecânicas de gestão de recursos hídricos e agrícolas"),
            ("1.2", date(2025, 7, 15), "Módulo de terremotos com novas mecânicas de sobrevivência", "Triângulo da vida, pontos seguros e kit de emergência"),
            ("1.1", date(2025, 6, 2), "Melhorias na interface do usuário e correção de bugs", "Otimização para dispositivos móveis"),
            ("1.0.5", date(2025, 5, 10), "Adicionado suporte a 5 novos idiomas", "Espanhol, Francês, Alemão, Italiano e Japonês"),
            ("1.0", date(2024, 1, 15), "Lançamento oficial do jogo", "Versão inicial com 4 cenários de desastres")
        ]
        
        for i, (versao, data, desc, detalhes) in enumerate(atualizacoes):
            if not AtualizacaoJogo.objects.filter(jogo=jogo, versao=versao).exists():
                AtualizacaoJogo.objects.create(
                    jogo=jogo,
                    versao=versao,
                    data=data,
                    descricao=desc,
                    detalhes=detalhes,
                    ordem=i
                )
        
        # FAQs
        self.stdout.write('  Adicionando FAQs...')
        faqs = [
            ("O jogo é gratuito?", "Sim, a versão básica do jogo é completamente gratuita com todos os recursos essenciais. Oferecemos uma versão premium com conteúdo adicional por R$ 29,90.", "geral"),
            ("Posso usar em sala de aula?", "Absolutamente! Temos material de apoio pedagógico disponível para professores. Entre em contato para obter licenças especiais para escolas.", "pedagogico"),
            ("Como o jogo ajuda em situações reais?", "O jogo simula situações reais com base em protocolos de emergência oficiais. Jogadores relatam aumento de 70% na capacidade de resposta a desastres após 10 horas de gameplay.", "pedagogico"),
            ("Precisa de internet para jogar?", "Não, após o download o jogo funciona totalmente offline. Apenas as atualizações e recursos online requerem conexão.", "tecnico"),
            ("Tem suporte para controle?", "Sim, o jogo tem suporte nativo para controles Xbox e PlayStation, além de teclado e mouse.", "tecnico"),
            ("Posso resetar meu progresso?", "Sim, na seção de configurações do jogo você pode resetar seu progresso a qualquer momento.", "jogabilidade"),
            ("O jogo tem legendas em português?", "Sim, o jogo tem áudio e legendas totalmente em português brasileiro.", "geral"),
            ("Posso jogar com amigos?", "Sim, temos um modo cooperativo onde até 4 jogadores podem enfrentar desafios juntos.", "jogabilidade"),
        ]
        
        for i, (pergunta, resposta, categoria) in enumerate(faqs):
            if not FAQJogo.objects.filter(jogo=jogo, pergunta=pergunta).exists():
                FAQJogo.objects.create(
                    jogo=jogo,
                    pergunta=pergunta,
                    resposta=resposta,
                    ordem=i,
                    ativo=True,
                    visivel=True,
                    categoria=categoria,
                    data_criacao=datetime.now()
                )
        
        # Imagens
        self.stdout.write('  Adicionando imagens...')
        imagens = [
            ("https://images.unsplash.com/photo-1593113630400-ea4288922497?q=80&w=1000", "Terremoto nível 7.2 - Escolhas críticas durante abalo sísmico"),
            ("https://images.unsplash.com/photo-1536514498073-50e69d39c6cf?q=80&w=1000", "Furacão categoria 4 - Evacuação estratégica em zona costeira"),
            ("https://images.unsplash.com/photo-1506905925346-21bda4d32df4?q=80&w=1000", "Planejamento de rotas de fuga e pontos de encontro"),
            ("https://images.unsplash.com/photo-1518837695005-2083093ee35b?q=80&w=1000", "Simulação de inundação urbana - Altura crítica da água"),
            ("https://images.unsplash.com/photo-1506905925346-21bda4d32df4?q=80&w=1000", "Interface do jogo mostrando mapa de riscos"),
            ("https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=1000", "Kit de emergência virtual - Itens essenciais"),
        ]
        
        for i, (url, legenda) in enumerate(imagens):
            if not ImagemJogo.objects.filter(jogo=jogo, url=url).exists():
                ImagemJogo.objects.create(
                    jogo=jogo,
                    url=url,
                    legenda=legenda,
                    ordem=i
                )
        
        self.stdout.write(self.style.SUCCESS('Jogo e todas as relações criadas com sucesso!'))
        return jogo
    
    def criar_artigos(self):
        """Cria artigos educativos"""
        self.stdout.write('Criando artigos...')
        
        usuarios = Usuario.objects.all()
        if not usuarios:
            self.stdout.write(self.style.WARNING('  ⚠ Nenhum usuário encontrado para criar artigos'))
            return
        
        artigos = [
            {
                'titulo': 'Como se Preparar para Enchentes',
                'resumo': 'Guia completo com dicas práticas para se preparar e responder a situações de enchentes urbanas.',
                'dataPublicacao': date(2024, 3, 10),
                'usuario': usuarios[1]  # Editor
            },
            {
                'titulo': 'Prevenção de Queimadas em Áreas Rurais',
                'resumo': 'Estratégias eficazes para prevenir incêndios florestais e proteger propriedades rurais.',
                'dataPublicacao': date(2024, 4, 15),
                'usuario': usuarios[2]  # Maria
            },
            {
                'titulo': 'Kit de Emergência para Terremotos',
                'resumo': 'Lista essencial de itens que devem compor seu kit de emergência para situações sísmicas.',
                'dataPublicacao': date(2024, 5, 20),
                'usuario': usuarios[3]  # Especialista
            },
            {
                'titulo': 'Educação Ambiental nas Escolas',
                'resumo': 'A importância de incluir a educação ambiental e prevenção de desastres no currículo escolar.',
                'dataPublicacao': date(2024, 6, 5),
                'usuario': usuarios[4]  # Professora
            }
        ]
        
        for artigo_data in artigos:
            if not Artigo.objects.filter(titulo=artigo_data['titulo']).exists():
                Artigo.objects.create(**artigo_data)
                self.stdout.write(f"  ✓ Artigo criado: {artigo_data['titulo']}")
        
        # Criar tópicos para os artigos
        for artigo in Artigo.objects.all():
            for i in range(1, 4):
                titulo_topico = f"Tópico {i} - {artigo.titulo[:30]}..."
                if not TopicoArtigo.objects.filter(artigo=artigo, titulo=titulo_topico).exists():
                    TopicoArtigo.objects.create(
                        artigo=artigo,
                        titulo=titulo_topico,
                        texto=f"Conteúdo detalhado do tópico {i} do artigo sobre {artigo.titulo}. Este é um texto de exemplo que seria substituído pelo conteúdo real do artigo."
                    )
        
        self.stdout.write(self.style.SUCCESS(f'{len(artigos)} artigos criados!'))
    
    def criar_acontecimentos(self):
        """Cria acontecimentos históricos"""
        self.stdout.write('Criando acontecimentos...')
        
        acontecimentos = [
            {
                'titulo': 'Enchente Histórica em São Paulo - 2023',
                'descricao': 'A maior enchente registrada na cidade de São Paulo, com níveis de água atingindo 2 metros em algumas regiões.',
                'dataAcontecimento': date(2023, 2, 10),
                'risco': 'Alto'
            },
            {
                'titulo': 'Queimadas na Amazônia - 2022',
                'descricao': 'Série de incêndios florestais que consumiram milhares de hectares na floresta amazônica.',
                'dataAcontecimento': date(2022, 8, 15),
                'risco': 'Crítico'
            },
            {
                'titulo': 'Terremoto no Chile - 2021',
                'descricao': 'Terremoto de magnitude 7.5 que afetou a região central do Chile, com alerta de tsunami.',
                'dataAcontecimento': date(2021, 9, 1),
                'risco': 'Médio'
            }
        ]
        
        for ac_data in acontecimentos:
            if not Acontecimento.objects.filter(titulo=ac_data['titulo']).exists():
                Acontecimento.objects.create(**ac_data)
                self.stdout.write(f"  ✓ Acontecimento criado: {ac_data['titulo']}")
        
        self.stdout.write(self.style.SUCCESS(f'{len(acontecimentos)} acontecimentos criados!'))
    
    def criar_riscos(self):
        """Cria riscos associados a desastres"""
        self.stdout.write('Criando riscos...')
        
        desastres = Desastre.objects.all()
        if not desastres:
            self.stdout.write(self.style.WARNING('  ⚠ Nenhum desastre encontrado para criar riscos'))
            return
        
        riscos = [
            {
                'nome': 'Risco de Inundação Zona Norte',
                'nivel': 'Alto',
                'descricao': 'Área com histórico de alagamentos durante períodos de chuva intensa.',
                'localizacao': 'Zona Norte - São Paulo',
                'desastre': desastres[0]  # Enchentes
            },
            {
                'nome': 'Risco de Incêndio Florestal',
                'nivel': 'Crítico',
                'descricao': 'Região com vegetação seca e condições climáticas favoráveis à propagação de fogo.',
                'localizacao': 'Chapada Diamantina - BA',
                'desastre': desastres[1]  # Queimadas
            },
            {
                'nome': 'Risco Sísmico Costa Oeste',
                'nivel': 'Médio',
                'descricao': 'Região com atividade tectônica constante e histórico de abalos sísmicos.',
                'localizacao': 'Costa Oeste - Chile',
                'desastre': desastres[2]  # Terremotos
            }
        ]
        
        for risco_data in riscos:
            if not Risco.objects.filter(nome=risco_data['nome']).exists():
                Risco.objects.create(**risco_data)
                self.stdout.write(f"  ✓ Risco criado: {risco_data['nome']}")
        
        self.stdout.write(self.style.SUCCESS(f'{len(riscos)} riscos criados!'))
    
    def criar_paginas(self):
        """Cria páginas do site"""
        self.stdout.write('Criando páginas...')
        
        # Busca objetos existentes
        artigos = Artigo.objects.all()
        desastres = Desastre.objects.all()
        jogos = Jogo.objects.all()
        acontecimentos = Acontecimento.objects.all()
        
        if not artigos or not desastres or not jogos or not acontecimentos:
            self.stdout.write(self.style.WARNING('  ⚠ Dados insuficientes para criar páginas'))
            return
        
        paginas = [
            {
                'titulo': 'Guia de Enchentes',
                'descricao': 'Página com informações completas sobre prevenção e resposta a enchentes.',
                'artigo': artigos[0] if len(artigos) > 0 else None,
                'desastre': desastres[0] if len(desastres) > 0 else None,
                'jogo': jogos[0] if len(jogos) > 0 else None,
                'acontecimento': acontecimentos[0] if len(acontecimentos) > 0 else None
            },
            {
                'titulo': 'Central de Emergências',
                'descricao': 'Recursos e informações para situações de emergência.',
                'artigo': artigos[1] if len(artigos) > 1 else None,
                'desastre': desastres[1] if len(desastres) > 1 else None,
                'jogo': None,
                'acontecimento': acontecimentos[1] if len(acontecimentos) > 1 else None
            }
        ]
        
        for pagina_data in paginas:
            if not Pagina.objects.filter(titulo=pagina_data['titulo']).exists():
                Pagina.objects.create(**pagina_data)
                self.stdout.write(f"  ✓ Página criada: {pagina_data['titulo']}")
        
        self.stdout.write(self.style.SUCCESS(f'{len(paginas)} páginas criadas!'))
    
    def criar_avaliacoes(self):
        """Cria avaliações para o jogo"""
        self.stdout.write('Criando avaliações...')
        
        usuarios = Usuario.objects.all()
        jogos = Jogo.objects.all()
        
        if not usuarios or not jogos:
            self.stdout.write(self.style.WARNING('  ⚠ Dados insuficientes para criar avaliações'))
            return
        
        jogo = jogos[0]  # Primeiro jogo
        
        avaliacoes = [
            {
                'texto': 'Jogo incrível! Aprendi muito sobre como agir em situações de emergência.',
                'nota': 5,
                'usuario': usuarios[1],  # Editor
                'jogo': jogo
            },
            {
                'texto': 'Muito educativo, poderia ter mais cenários diferentes.',
                'nota': 4,
                'usuario': usuarios[2],  # Maria
                'jogo': jogo
            },
            {
                'texto': 'Como especialista, posso dizer que o conteúdo é preciso e bem pesquisado.',
                'nota': 5,
                'usuario': usuarios[3],  # Especialista
                'jogo': jogo
            },
            {
                'texto': 'Usei com meus alunos e foi uma experiência muito produtiva!',
                'nota': 5,
                'usuario': usuarios[4],  # Professora
                'jogo': jogo
            }
        ]
        
        for avaliacao_data in avaliacoes:
            if not Avaliacao.objects.filter(usuario=avaliacao_data['usuario'], jogo=jogo).exists():
                Avaliacao.objects.create(**avaliacao_data)
                self.stdout.write(f"  ✓ Avaliação criada: {avaliacao_data['usuario'].nome} - {avaliacao_data['nota']} estrelas")
        
        self.stdout.write(self.style.SUCCESS(f'{len(avaliacoes)} avaliações criadas!'))
    
    def criar_perguntas(self):
        """Cria perguntas para o jogo"""
        self.stdout.write('Criando perguntas...')
        
        usuarios = Usuario.objects.all()
        jogos = Jogo.objects.all()
        
        if not usuarios or not jogos:
            self.stdout.write(self.style.WARNING('  ⚠ Dados insuficientes para criar perguntas'))
            return
        
        jogo = jogos[0]  # Primeiro jogo
        
        # Perguntas do modelo Pergunta (antigo)
        perguntas_antigas = [
            {
                'pergunta': 'Como faço para salvar meu progresso no jogo?',
                'resposta': 'O jogo salva automaticamente seu progresso ao completar cada nível.',
                'usuario': usuarios[1],
                'jogo': jogo
            },
            {
                'pergunta': 'Posso jogar sem conexão com a internet?',
                'resposta': 'Sim, após o download inicial o jogo funciona completamente offline.',
                'usuario': usuarios[2],
                'jogo': jogo
            }
        ]
        
        for pergunta_data in perguntas_antigas:
            if not Pergunta.objects.filter(pergunta=pergunta_data['pergunta'], jogo=jogo).exists():
                Pergunta.objects.create(**pergunta_data)
                self.stdout.write(f"  ✓ Pergunta criada (modelo antigo): {pergunta_data['pergunta'][:50]}...")
        
        # Perguntas do usuário (novo modelo PerguntaUsuario)
        perguntas_usuarios = [
            {
                'pergunta': 'O jogo tem suporte para telas ultrawide?',
                'email': 'gamer@email.com',
                'status': 'respondida',
                'resposta_admin': 'Sim, o jogo tem suporte para resoluções ultrawide (21:9).',
                'usuario': usuarios[2],
                'jogo': jogo
            },
            {
                'pergunta': 'Quando será lançada a próxima atualização?',
                'email': 'curioso@email.com',
                'status': 'pendente',
                'resposta_admin': '',
                'usuario': None,  # Pergunta anônima
                'jogo': jogo
            }
        ]
        
        for pergunta_data in perguntas_usuarios:
            if not PerguntaUsuario.objects.filter(pergunta=pergunta_data['pergunta'], jogo=jogo).exists():
                PerguntaUsuario.objects.create(**pergunta_data)
                self.stdout.write(f"  ✓ Pergunta de usuário criada: {pergunta_data['pergunta'][:50]}...")
        
        # Criar tópicos para desastres
        desastres = Desastre.objects.all()
        for desastre in desastres:
            for i in range(1, 3):
                titulo_topico = f"Prevenção - {desastre.titulo}"
                if not TopicoDesastre.objects.filter(desastre=desastre, titulo=titulo_topico).exists():
                    TopicoDesastre.objects.create(
                        desastre=desastre,
                        titulo=titulo_topico,
                        texto=f"Conteúdo educativo sobre prevenção de {desastre.titulo.lower()}. Este texto contém informações importantes sobre como se preparar e evitar danos."
                    )
        
        self.stdout.write(self.style.SUCCESS('Perguntas e tópicos criados com sucesso!'))