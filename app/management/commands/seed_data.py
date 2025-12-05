# app/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from app.models import (
    Usuario, Jogo, CaracteristicaJogo, RequisitoJogo, 
    AtualizacaoJogo, FAQJogo, ImagemJogo,
    Desastre, Acontecimento, Risco, Artigo, Pagina,
    Avaliacao, TopicoArtigo, TopicoDesastre, Pergunta,
    PerguntaUsuario
)
from datetime import date
from django.utils import timezone

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de exemplo'
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando população do banco de dados...'))
        
        # Limpar TODOS os dados existentes primeiro
        self.limpar_dados()
        
        # Criar usuários
        self.criar_usuarios()
        
        # Criar desastres
        self.criar_desastres()
        
        # Criar jogos com todas as relações
        self.criar_jogos()
        
        # Criar artigos para cada desastre
        self.criar_artigos_por_desastre()
        
        # Criar acontecimentos para cada desastre
        self.criar_acontecimentos_por_desastre()
        
        # Criar riscos para cada desastre
        self.criar_riscos_por_desastre()
        
        # Criar páginas para cada desastre
        self.criar_paginas_por_desastre()
        
        # Criar avaliações
        self.criar_avaliacoes()
        
        # Criar perguntas
        self.criar_perguntas()
        
        # Criar tópicos para cada desastre
        self.criar_topicos_por_desastre()
        
        self.stdout.write(self.style.SUCCESS('Banco de dados populado com sucesso!'))
    
    def limpar_dados(self):
        """Limpa todos os dados existentes"""
        self.stdout.write('Limpando dados existentes...')
        
        # Limpar na ordem inversa para evitar erros de chave estrangeira
        PerguntaUsuario.objects.all().delete()
        Pergunta.objects.all().delete()
        Avaliacao.objects.all().delete()
        Pagina.objects.all().delete()
        TopicoDesastre.objects.all().delete()
        TopicoArtigo.objects.all().delete()
        Risco.objects.all().delete()
        Acontecimento.objects.all().delete()
        Artigo.objects.all().delete()
        ImagemJogo.objects.all().delete()
        FAQJogo.objects.all().delete()
        AtualizacaoJogo.objects.all().delete()
        RequisitoJogo.objects.all().delete()
        CaracteristicaJogo.objects.all().delete()
        Jogo.objects.all().delete()
        Desastre.objects.all().delete()
        Usuario.objects.all().delete()
        
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
                'imagem': '',
                'ativo': True
            },
            {
                'nome': 'João Editor',
                'email': 'editor@acriseg.com',
                'senha': 'editor123',
                'tipo': 'editor',
                'imagem': '',
                'ativo': True
            },
            {
                'nome': 'Maria Usuária',
                'email': 'maria@exemplo.com',
                'senha': 'maria123',
                'tipo': 'usuario',
                'imagem': '',
                'ativo': True
            },
            {
                'nome': 'Carlos Especialista',
                'email': 'carlos@especialista.com',
                'senha': 'especialista123',
                'tipo': 'especialista',
                'imagem': '',
                'ativo': True
            },
            {
                'nome': 'Ana Professora',
                'email': 'ana@escola.com',
                'senha': 'professora123',
                'tipo': 'usuario',
                'imagem': '',
                'ativo': True
            },
            {
                'nome': 'Pedro Geólogo',
                'email': 'pedro@geologia.com',
                'senha': 'geologo123',
                'tipo': 'especialista',
                'imagem': '',
                'ativo': True
            },
            {
                'nome': 'Meteorologista Silva',
                'email': 'silva@meteorologia.com',
                'senha': 'meteorologia123',
                'tipo': 'especialista',
                'imagem': '',
                'ativo': True
            }
        ]
        
        for user_data in usuarios:
            usuario = Usuario(
                nome=user_data['nome'],
                email=user_data['email'],
                senha=user_data['senha'],
                tipo=user_data['tipo'],
                imagem=user_data['imagem'],
                ativo=user_data['ativo']
            )
            usuario.save()
            self.stdout.write(f"  ✓ Usuário criado: {user_data['nome']} ({user_data['email']})")
        
        self.stdout.write(self.style.SUCCESS(f'{len(usuarios)} usuários criados!'))
        return Usuario.objects.all()
    
    def criar_desastres(self):
        """Cria desastres naturais"""
        self.stdout.write('Criando desastres...')
        
        desastres = [
            {
                'titulo': 'Enchentes',
                'descricao': 'Inundações causadas por chuvas intensas, transbordamento de rios ou marés altas. Podem causar danos materiais, perda de vidas e deslocamento populacional.',
                'icone': '🌊'
            },
            {
                'titulo': 'Queimadas',
                'descricao': 'Incêndios florestais e urbanos de grandes proporções que destroem vegetação, fauna e podem atingir áreas habitadas.',
                'icone': '🔥'
            },
            {
                'titulo': 'Terremotos',
                'descricao': 'Tremores de terra causados por movimentos tectônicos nas placas da crosta terrestre. Podem variar de leve a catastrófico.',
                'icone': '🌍'
            },
            {
                'titulo': 'Furacões',
                'descricao': 'Tempestades tropicais com ventos de alta velocidade, fortes chuvas e tempestades que podem causar inundações e destruição.',
                'icone': '🌀'
            },
            {
                'titulo': 'Secas',
                'descricao': 'Períodos prolongados de escassez de água que afetam agricultura, abastecimento de água e ecossistemas.',
                'icone': '☀️'
            },
            {
                'titulo': 'Deslizamentos',
                'descricao': 'Movimento de massa de terra e rochas em encostas, geralmente causados por chuvas fortes, desmatamento ou atividades humanas.',
                'icone': '⛰️'
            },
            {
                'titulo': 'Tsunamis',
                'descricao': 'Ondas gigantes causadas por terremotos submarinos, erupções vulcânicas ou deslizamentos no fundo do mar.',
                'icone': '🌊'
            },
            {
                'titulo': 'Erupções Vulcânicas',
                'descricao': 'Liberação de magma, gases e cinzas de vulcões, que podem causar destruição local e afetar o clima global.',
                'icone': '🌋'
            }
        ]
        
        desastre_objs = []
        for desastre_data in desastres:
            desastre = Desastre.objects.create(**desastre_data)
            desastre_objs.append(desastre)
            self.stdout.write(f"  ✓ Desastre criado: {desastre_data['titulo']}")
        
        self.stdout.write(self.style.SUCCESS(f'{len(desastres)} desastres criados!'))
        return desastre_objs
    
    def criar_jogos(self):
        """Cria jogos com todas as relações"""
        self.stdout.write('Criando jogo principal...')
        
        # Criar jogo principal
        jogo = Jogo.objects.create(
            titulo="Survivor: Desafio da Natureza",
            subtitulo="Um jogo educativo imersivo que ensina sobre preparação e resposta a desastres naturais",
            descricao="Desenvolvido em parceria com especialistas em gestão de crises.",
            descricao_detalhada="""Survivor: Desafio da Natureza é um jogo educativo que combina aprendizado com diversão. 
            Através de simulações realistas, os jogadores aprendem a identificar riscos, tomar decisões críticas 
            e implementar medidas de prevenção contra 8 tipos de desastres naturais diferentes. 
            O jogo foi desenvolvido em colaboração com geólogos, meteorologistas e especialistas em defesa civil.""",
            desenvolvedor="A Crise G Studios",
            plataformas="Windows, Android, iOS",
            idade_recomendada="12+ anos",
            tamanho="850MB (PC) / 320MB (Mobile)",
            versao="1.3.2",
            download_windows="https://example.com/download/windows",
            download_android="https://example.com/download/android",
            download_ios="https://example.com/download/ios",
            imagem_capa="https://images.unsplash.com/photo-1593113630400-ea4288922497?w=800",
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
            ("fas fa-bolt", "Simulações realistas de 8 tipos de desastres naturais"),
            ("fas fa-brain", "Sistema de tomada de decisões com consequências reais"),
            ("fas fa-user-check", "Conteúdo validado por especialistas em cada área"),
            ("fas fa-clock", "Modo história com 15+ horas de gameplay"),
            ("fas fa-gamepad", "Desafios rápidos para aprendizagem objetiva"),
            ("fas fa-chart-line", "Estatísticas de desempenho detalhadas"),
            ("fas fa-users", "Modo multiplayer cooperativo (até 4 jogadores)"),
            ("fas fa-trophy", "Sistema de conquistas e recompensas por aprendizado"),
            ("fas fa-book", "Biblioteca de conhecimento integrada sobre desastres"),
            ("fas fa-mobile-alt", "Interface otimizada para dispositivos móveis"),
        ]
        
        for i, (icone, desc) in enumerate(caracteristicas):
            CaracteristicaJogo.objects.create(
                jogo=jogo,
                icone=icone,
                descricao=desc,
                ordem=i
            )
        
        # Requisitos mínimos
        self.stdout.write('  Adicionando requisitos mínimos...')
        requisitos_min = [
            "Windows 10 64-bit ou superior",
            "Processador Intel i3 ou equivalente AMD",
            "4GB RAM",
            "Placa de vídeo com 1GB VRAM (DirectX 11)",
            "2GB de espaço livre em disco",
            "Conexão internet para ativação",
            "Resolução mínima 1280x720"
        ]
        
        for req in requisitos_min:
            RequisitoJogo.objects.create(jogo=jogo, tipo='minimo', descricao=req)
        
        # Requisitos recomendados
        self.stdout.write('  Adicionando requisitos recomendados...')
        requisitos_rec = [
            "Windows 11 64-bit",
            "Processador Intel i5 ou AMD Ryzen 5",
            "8GB RAM",
            "Placa de vídeo com 2GB VRAM (DirectX 12)",
            "4GB de espaço livre em SSD",
            "Conexão internet banda larga",
            "Resolução 1920x1080"
        ]
        
        for req in requisitos_rec:
            RequisitoJogo.objects.create(jogo=jogo, tipo='recomendado', descricao=req)
        
        # Atualizações com foco em diferentes desastres
        self.stdout.write('  Adicionando atualizações...')
        atualizacoes = [
            ("1.3", date(2025, 8, 25), "Novo módulo: Secas Extrema", 
             "Adicionado cenário de gestão de recursos hídricos em períodos de seca prolongada"),
            ("1.2", date(2025, 7, 15), "Módulo de Terremotos aprimorado", 
             "Novas mecânicas de sobrevivência incluindo triângulo da vida e pontos seguros"),
            ("1.1.5", date(2025, 6, 2), "Módulo de Enchentes urbanas", 
             "Simulação de inundações em áreas urbanas com estratégias de evacuação"),
            ("1.1", date(2025, 5, 10), "Sistema de Queimadas melhorado", 
             "Novos algoritmos de propagação do fogo e técnicas de combate"),
            ("1.0.5", date(2025, 4, 1), "Adicionado suporte a 5 novos idiomas", 
             "Espanhol, Francês, Alemão, Italiano e Japonês"),
            ("1.0", date(2024, 1, 15), "Lançamento oficial", 
             "Versão inicial com 4 cenários de desastres (Terremotos, Enchentes, Queimadas, Furacões)")
        ]
        
        for i, (versao, data, desc, detalhes) in enumerate(atualizacoes):
            AtualizacaoJogo.objects.create(
                jogo=jogo,
                versao=versao,
                data=data,
                descricao=desc,
                detalhes=detalhes,
                ordem=i
            )
        
        # FAQs específicas para diferentes tipos de desastres
        self.stdout.write('  Adicionando FAQs...')
        faqs = [
            ("O jogo ensina sobre todos os tipos de desastres?", 
             "Sim! O jogo cobre 8 tipos principais de desastres naturais com simulações específicas para cada um.", 
             "geral"),
            ("Como o jogo simula situações de enchente?", 
             "Usamos algoritmos baseados em dados reais de hidrologia para simular o comportamento da água em diferentes terrenos.", 
             "tecnico"),
            ("Posso aprender sobre prevenção de queimadas?", 
             "Sim! Temos um módulo completo sobre prevenção e combate a incêndios florestais e urbanos.", 
             "pedagogico"),
            ("O jogo é adequado para crianças?", 
             "Sim, o jogo é classificado para maiores de 12 anos e tem conteúdo educativo adaptado para diferentes idades.", 
             "geral"),
            ("Como são tratados os terremotos no jogo?", 
             "Simulamos diferentes magnitudes de terremotos e ensinamos procedimentos de segurança específicos.", 
             "jogabilidade"),
            ("Há conteúdo sobre furacões?", 
             "Sim, temos cenários de furacões com diferentes categorias e estratégias de evacuação.", 
             "jogabilidade"),
            ("Posso usar o jogo em escolas?", 
             "Absolutamente! Temos planos de aula e material didático específico para professores.", 
             "pedagogico"),
            ("O jogo funciona offline?", 
             "Sim, após o download inicial, todo o conteúdo funciona sem necessidade de conexão com a internet.", 
             "tecnico"),
        ]
        
        for i, (pergunta, resposta, categoria) in enumerate(faqs):
            FAQJogo.objects.create(
                jogo=jogo,
                pergunta=pergunta,
                resposta=resposta,
                ordem=i,
                ativo=True,
                visivel=True,
                categoria=categoria
            )
        
        # Imagens representando diferentes desastres
        self.stdout.write('  Adicionando imagens...')
        imagens = [
            ("https://images.unsplash.com/photo-1593113630400-ea4288922497?w=800", 
             "Terremoto nível 7.2 - Escolhas críticas durante abalo sísmico"),
            ("https://images.unsplash.com/photo-1536514498073-50e69d39c6cf?w=800", 
             "Furacão categoria 4 - Evacuação estratégica em zona costeira"),
            ("https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=800", 
             "Simulação de inundação urbana - Altura crítica da água"),
            ("https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800", 
             "Planejamento de rotas de fuga e pontos de encontro"),
            ("https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800", 
             "Kit de emergência virtual - Itens essenciais para sobrevivência"),
            ("https://images.unsplash.com/photo-1561484930-998b6a7b22e8?w=800", 
             "Queimada florestal - Técnicas de combate ao fogo"),
        ]
        
        for i, (url, legenda) in enumerate(imagens):
            ImagemJogo.objects.create(
                jogo=jogo,
                url=url,
                legenda=legenda,
                ordem=i
            )
        
        self.stdout.write(self.style.SUCCESS('Jogo e todas as relações criadas com sucesso!'))
        return jogo
    
    def criar_artigos_por_desastre(self):
        """Cria artigos educativos para cada desastre"""
        self.stdout.write('Criando artigos por desastre...')
        
        usuarios = Usuario.objects.all()
        desastres = Desastre.objects.all()
        
        if not usuarios or not desastres:
            self.stdout.write(self.style.WARNING('  ⚠ Dados insuficientes para criar artigos'))
            return
        
        # Mapeamento de títulos e resumos por tipo de desastre
        artigos_por_desastre = {
            'Enchentes': {
                'titulo': 'Guia Completo de Preparação para Enchentes',
                'resumo': 'Aprenda estratégias eficazes para prevenir danos durante inundações e proteger sua família.',
                'autor': usuarios[2]  # Maria
            },
            'Queimadas': {
                'titulo': 'Prevenção e Combate a Incêndios Florestais',
                'resumo': 'Técnicas comprovadas para evitar queimadas e ações de emergência quando o fogo se aproxima.',
                'autor': usuarios[3]  # Carlos Especialista
            },
            'Terremotos': {
                'titulo': 'Sobrevivendo a Terremotos: O Guia Essencial',
                'resumo': 'Procedimentos de segurança antes, durante e após abalos sísmicos de diferentes magnitudes.',
                'autor': usuarios[5]  # Pedro Geólogo
            },
            'Furacões': {
                'titulo': 'Planejamento para Temporada de Furacões',
                'resumo': 'Como se preparar para tempestades tropicais e executar evacuações seguras.',
                'autor': usuarios[6]  # Meteorologista Silva
            },
            'Secas': {
                'titulo': 'Gestão de Recursos Hídricos em Períodos de Seca',
                'resumo': 'Estratégias para conservação de água e adaptação a condições de escassez prolongada.',
                'autor': usuarios[1]  # Editor
            },
            'Deslizamentos': {
                'titulo': 'Identificação de Áreas de Risco de Deslizamento',
                'resumo': 'Como reconhecer sinais de instabilidade em encostas e tomar medidas preventivas.',
                'autor': usuarios[5]  # Pedro Geólogo
            },
            'Tsunamis': {
                'titulo': 'Sistema de Alerta e Evacuação para Tsunamis',
                'resumo': 'Procedimentos de segurança em regiões costeiras sujeitas a ondas gigantes.',
                'autor': usuarios[6]  # Meteorologista Silva
            },
            'Erupções Vulcânicas': {
                'titulo': 'Vivendo em Zonas Vulcânicas Ativas',
                'resumo': 'Preparação e resposta a erupções vulcânicas e seus efeitos colaterais.',
                'autor': usuarios[5]  # Pedro Geólogo
            }
        }
        
        # Datas de publicação espaçadas
        datas_publicacao = [
            date(2024, 1, 10),
            date(2024, 2, 15),
            date(2024, 3, 20),
            date(2024, 4, 5),
            date(2024, 5, 12),
            date(2024, 6, 18),
            date(2024, 7, 22),
            date(2024, 8, 30)
        ]
        
        artigos_criados = []
        for i, desastre in enumerate(desastres):
            if desastre.titulo in artigos_por_desastre:
                artigo_info = artigos_por_desastre[desastre.titulo]
                data_pub = datas_publicacao[i] if i < len(datas_publicacao) else date.today()
                
                artigo = Artigo.objects.create(
                    titulo=artigo_info['titulo'],
                    resumo=artigo_info['resumo'],
                    dataPublicacao=data_pub,
                    usuario=artigo_info['autor']
                )
                artigos_criados.append((artigo, desastre))
                self.stdout.write(f"  ✓ Artigo criado: {artigo_info['titulo']}")
        
        # Criar tópicos para cada artigo
        for artigo, desastre in artigos_criados:
            for i in range(1, 4):
                TopicoArtigo.objects.create(
                    artigo=artigo,
                    titulo=f"Tópico {i}: Aspectos específicos sobre {desastre.titulo}",
                    texto=f"""Conteúdo detalhado do tópico {i} sobre {desastre.titulo.lower()}. 
                    Este tópico aborda questões específicas relacionadas à prevenção, preparação e resposta a {desastre.titulo.lower()}.
                    Informações baseadas em pesquisas científicas e protocolos internacionais de segurança."""
                )
        
        self.stdout.write(self.style.SUCCESS(f'{len(artigos_criados)} artigos criados!'))
        return artigos_criados
    
    def criar_acontecimentos_por_desastre(self):
        """Cria acontecimentos históricos para cada desastre"""
        self.stdout.write('Criando acontecimentos por desastre...')
        
        desastres = Desastre.objects.all()
        
        acontecimentos_por_desastre = {
            'Enchentes': [
                {
                    'titulo': 'Enchente Histórica em São Paulo - 2023',
                    'descricao': 'A maior enchente registrada na cidade de São Paulo, com níveis de água atingindo 2 metros em algumas regiões e causando prejuízos de R$ 1 bilhão.',
                    'dataAcontecimento': date(2023, 2, 10),
                    'risco': 'Alto'
                }
            ],
            'Queimadas': [
                {
                    'titulo': 'Queimadas na Amazônia - 2022',
                    'descricao': 'Série de incêndios florestais que consumiram mais de 50.000 hectares na floresta amazônica, com impacto no clima regional.',
                    'dataAcontecimento': date(2022, 8, 15),
                    'risco': 'Crítico'
                }
            ],
            'Terremotos': [
                {
                    'titulo': 'Terremoto no Chile - 2021',
                    'descricao': 'Terremoto de magnitude 7.5 que afetou a região central do Chile, gerando alerta de tsunami e causando danos significativos.',
                    'dataAcontecimento': date(2021, 9, 1),
                    'risco': 'Médio'
                }
            ],
            'Furacões': [
                {
                    'titulo': 'Furacão Katrina - 2005',
                    'descricao': 'Um dos furacões mais destrutivos da história dos EUA, causando mais de 1.800 mortes e prejuízos de US$ 125 bilhões.',
                    'dataAcontecimento': date(2005, 8, 29),
                    'risco': 'Extremo'
                }
            ],
            'Secas': [
                {
                    'titulo': 'Seca no Nordeste Brasileiro - 2012-2017',
                    'descricao': 'Período de 5 anos de seca extrema que afetou a agricultura e o abastecimento de água de milhões de pessoas.',
                    'dataAcontecimento': date(2015, 6, 1),
                    'risco': 'Alto'
                }
            ],
            'Deslizamentos': [
                {
                    'titulo': 'Deslizamento em Petrópolis - 2022',
                    'descricao': 'Tragédia que causou mais de 200 mortes após chuvas intensas na região serrana do Rio de Janeiro.',
                    'dataAcontecimento': date(2022, 2, 15),
                    'risco': 'Crítico'
                }
            ],
            'Tsunamis': [
                {
                    'titulo': 'Tsunami no Oceano Índico - 2004',
                    'descricao': 'Um dos tsunamis mais mortais da história, causado por um terremoto de magnitude 9.1, com mais de 230.000 mortes.',
                    'dataAcontecimento': date(2004, 12, 26),
                    'risco': 'Extremo'
                }
            ],
            'Erupções Vulcânicas': [
                {
                    'titulo': 'Erupção do Vulcão Tonga - 2022',
                    'descricao': 'Erupção submarina que gerou tsunami e afetou o clima global, com ondas de choque detectadas ao redor do mundo.',
                    'dataAcontecimento': date(2022, 1, 15),
                    'risco': 'Alto'
                }
            ]
        }
        
        total_criados = 0
        for desastre in desastres:
            if desastre.titulo in acontecimentos_por_desastre:
                for ac_data in acontecimentos_por_desastre[desastre.titulo]:
                    Acontecimento.objects.create(**ac_data)
                    total_criados += 1
                    self.stdout.write(f"  ✓ Acontecimento criado: {ac_data['titulo']}")
        
        self.stdout.write(self.style.SUCCESS(f'{total_criados} acontecimentos criados!'))
    
    def criar_riscos_por_desastre(self):
        """Cria riscos associados a cada desastre"""
        self.stdout.write('Criando riscos por desastre...')
        
        desastres = Desastre.objects.all()
        
        riscos_por_desastre = {
            'Enchentes': [
                {
                    'nome': 'Zona Norte de São Paulo',
                    'nivel': 'Alto',
                    'descricao': 'Área com histórico recorrente de alagamentos durante períodos de chuva intensa, com deficiência no sistema de drenagem.',
                    'localizacao': 'Zona Norte - São Paulo, SP'
                },
                {
                    'nome': 'Vale do Itajaí',
                    'nivel': 'Muito Alto',
                    'descricao': 'Região suscetível a enchentes devido à topografia e proximidade com rios principais.',
                    'localizacao': 'Vale do Itajaí - Santa Catarina'
                }
            ],
            'Queimadas': [
                {
                    'nome': 'Cerrado Brasileiro',
                    'nivel': 'Crítico',
                    'descricao': 'Bioma com vegetação seca na maior parte do ano e condições climáticas favoráveis à propagação rápida do fogo.',
                    'localizacao': 'Cerrado - Centro-Oeste do Brasil'
                }
            ],
            'Terremotos': [
                {
                    'nome': 'Costa Oeste da América do Sul',
                    'nivel': 'Médio',
                    'descricao': 'Região com atividade tectônica constante devido à convergência das placas de Nazca e Sul-Americana.',
                    'localizacao': 'Costa do Chile e Peru'
                }
            ],
            'Furacões': [
                {
                    'nome': 'Costa Nordeste dos EUA',
                    'nivel': 'Alto',
                    'descricao': 'Área frequentemente afetada por furacões durante a temporada de tempestades tropicais.',
                    'localizacao': 'Flórida e Costa Leste - EUA'
                }
            ],
            'Secas': [
                {
                    'nome': 'Semiárido Nordestino',
                    'nivel': 'Crítico',
                    'descricao': 'Região com precipitação irregular e longos períodos de estiagem, afetando agricultura e abastecimento.',
                    'localizacao': 'Sertão Nordestino - Brasil'
                }
            ],
            'Deslizamentos': [
                {
                    'nome': 'Encostas da Região Serrana',
                    'nivel': 'Muito Alto',
                    'descricao': 'Áreas com declividade acentuada, solo instável e ocupação urbana desordenada.',
                    'localizacao': 'Região Serrana - Rio de Janeiro'
                }
            ]
        }
        
        total_criados = 0
        for desastre in desastres:
            if desastre.titulo in riscos_por_desastre:
                for risco_data in riscos_por_desastre[desastre.titulo]:
                    Risco.objects.create(
                        nome=risco_data['nome'],
                        nivel=risco_data['nivel'],
                        descricao=risco_data['descricao'],
                        localizacao=risco_data['localizacao'],
                        desastre=desastre
                    )
                    total_criados += 1
                    self.stdout.write(f"  ✓ Risco criado: {risco_data['nome']} ({desastre.titulo})")
        
        self.stdout.write(self.style.SUCCESS(f'{total_criados} riscos criados!'))
    
    def criar_paginas_por_desastre(self):
        """Cria páginas do site para cada desastre"""
        self.stdout.write('Criando páginas por desastre...')
        
        artigos = Artigo.objects.all()
        desastres = Desastre.objects.all()
        jogos = Jogo.objects.all()
        acontecimentos = Acontecimento.objects.all()
        
        if not artigos or not desastres or not jogos or not acontecimentos:
            self.stdout.write(self.style.WARNING('  ⚠ Dados insuficientes para criar páginas'))
            return
        
        # Encontrar correspondências entre desastres e outros objetos
        desastre_para_artigo = {}
        for artigo in artigos:
            for desastre in desastres:
                if desastre.titulo.lower() in artigo.titulo.lower():
                    desastre_para_artigo[desastre] = artigo
                    break
        
        desastre_para_acontecimento = {}
        for acontecimento in acontecimentos:
            for desastre in desastres:
                if desastre.titulo.lower() in acontecimento.titulo.lower():
                    desastre_para_acontecimento[desastre] = acontecimento
                    break
        
        jogo = jogos[0]
        
        # Criar página para cada desastre
        paginas_criadas = 0
        for desastre in desastres:
            artigo = desastre_para_artigo.get(desastre)
            acontecimento = desastre_para_acontecimento.get(desastre)
            
            if artigo or acontecimento:  # Criar página se houver pelo menos um relacionamento
                pagina = Pagina.objects.create(
                    titulo=f"Portal {desastre.titulo}",
                    descricao=f"Recursos educativos, informações e ferramentas sobre {desastre.titulo.lower()}.",
                    artigo=artigo,
                    desastre=desastre,
                    jogo=jogo,
                    acontecimento=acontecimento
                )
                paginas_criadas += 1
                self.stdout.write(f"  ✓ Página criada: {pagina.titulo}")
        
        # Criar página principal do jogo
        pagina_jogo = Pagina.objects.create(
            titulo="Survivor: Desafio da Natureza",
            descricao="Página oficial do jogo educativo sobre desastres naturais.",
            artigo=None,
            desastre=None,
            jogo=jogo,
            acontecimento=None
        )
        paginas_criadas += 1
        self.stdout.write(f"  ✓ Página criada: {pagina_jogo.titulo}")
        
        self.stdout.write(self.style.SUCCESS(f'{paginas_criadas} páginas criadas!'))
    
    def criar_avaliacoes(self):
        """Cria avaliações para o jogo"""
        self.stdout.write('Criando avaliações...')
        
        usuarios = Usuario.objects.all()
        jogos = Jogo.objects.all()
        
        if not usuarios or not jogos:
            self.stdout.write(self.style.WARNING('  ⚠ Dados insuficientes para criar avaliações'))
            return
        
        jogo = jogos[0]
        
        avaliacoes = [
            {
                'texto': 'Jogo incrível! Como professora, usei com meus alunos e o aprendizado foi significativo. Eles agora sabem como agir em situações de emergência.',
                'nota': 5,
                'usuario': usuarios[4],  # Ana Professora
                'jogo': jogo
            },
            {
                'texto': 'Como especialista em geologia, posso afirmar que o conteúdo sobre terremotos é preciso e bem pesquisado. Parabéns à equipe!',
                'nota': 5,
                'usuario': usuarios[5],  # Pedro Geólogo
                'jogo': jogo
            },
            {
                'texto': 'Interface intuitiva e simulações realistas. Aprendi muito sobre prevenção de queimadas, conteúdo muito relevante para nossa região.',
                'nota': 4,
                'usuario': usuarios[2],  # Maria Usuária
                'jogo': jogo
            },
            {
                'texto': 'O módulo de furacões é particularmente bem feito. Como meteorologista, aprovo a precisão dos dados utilizados.',
                'nota': 5,
                'usuario': usuarios[6],  # Meteorologista Silva
                'jogo': jogo
            },
            {
                'texto': 'Muito educativo, mas poderia ter mais cenários diferentes para cada tipo de desastre. No geral, excelente!',
                'nota': 4,
                'usuario': usuarios[3],  # Carlos Especialista
                'jogo': jogo
            },
            {
                'texto': 'Como editor, acompanhei o desenvolvimento do jogo e fiquei impressionado com a qualidade do conteúdo educativo.',
                'nota': 5,
                'usuario': usuarios[1],  # João Editor
                'jogo': jogo
            }
        ]
        
        for avaliacao_data in avaliacoes:
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
        
        jogo = jogos[0]
        admin_usuario = usuarios[0]
        
        # Perguntas do modelo Pergunta (antigo)
        perguntas_antigas = [
            {
                'pergunta': 'Como faço para salvar meu progresso no jogo?',
                'resposta': 'O jogo salva automaticamente seu progresso ao completar cada nível. Você também pode salvar manualmente nas opções do jogo.',
                'usuario': usuarios[2],
                'jogo': jogo
            },
            {
                'pergunta': 'Posso jogar sem conexão com a internet?',
                'resposta': 'Sim, após o download inicial o jogo funciona completamente offline. Apenas as atualizações requerem conexão.',
                'usuario': usuarios[3],
                'jogo': jogo
            },
            {
                'pergunta': 'Quantos tipos de desastres estão disponíveis no jogo?',
                'resposta': 'Atualmente, o jogo cobre 8 tipos principais de desastres naturais, com planos para adicionar mais em futuras atualizações.',
                'usuario': usuarios[4],
                'jogo': jogo
            }
        ]
        
        for pergunta_data in perguntas_antigas:
            Pergunta.objects.create(**pergunta_data)
            self.stdout.write(f"  ✓ Pergunta criada: {pergunta_data['pergunta'][:50]}...")
        
        # Perguntas do usuário (novo modelo PerguntaUsuario)
        perguntas_usuarios = [
            {
                'pergunta': 'O jogo tem suporte para telas ultrawide (21:9)?',
                'email': 'gamer@email.com',
                'status': 'respondida',
                'resposta_admin': 'Sim, o jogo tem suporte nativo para resoluções ultrawide (21:9) e também para monitores com proporção 32:9.',
                'usuario': usuarios[2],
                'jogo': jogo,
                'admin_respondeu': admin_usuario,
                'data_resposta': timezone.now()
            },
            {
                'pergunta': 'Quando será lançada a próxima atualização com novos desastres?',
                'email': 'curioso@email.com',
                'status': 'pendente',
                'resposta_admin': '',
                'usuario': None,
                'jogo': jogo,
                'admin_respondeu': None,
                'data_resposta': None
            },
            {
                'pergunta': 'O jogo tem material de apoio para professores em formato PDF?',
                'email': 'professor@escola.com',
                'status': 'respondida',
                'resposta_admin': 'Sim, temos material didático completo em PDF disponível para download em nossa área de recursos educativos.',
                'usuario': usuarios[4],
                'jogo': jogo,
                'admin_respondeu': admin_usuario,
                'data_resposta': timezone.now()
            },
            {
                'pergunta': 'É possível jogar em modo cooperativo online?',
                'email': 'multijogador@email.com',
                'status': 'respondida',
                'resposta_admin': 'Atualmente temos apenas modo cooperativo local. O modo online está em desenvolvimento para uma futura atualização.',
                'usuario': usuarios[3],
                'jogo': jogo,
                'admin_respondeu': admin_usuario,
                'data_resposta': timezone.now()
            }
        ]
        
        for pergunta_data in perguntas_usuarios:
            PerguntaUsuario.objects.create(**pergunta_data)
            self.stdout.write(f"  ✓ Pergunta de usuário criada: {pergunta_data['pergunta'][:50]}...")
        
        self.stdout.write(self.style.SUCCESS('Perguntas criadas com sucesso!'))
    
    def criar_topicos_por_desastre(self):
        """Cria tópicos educativos para cada desastre"""
        self.stdout.write('Criando tópicos por desastre...')
        
        desastres = Desastre.objects.all()
        
        topicos_base = [
            {
                'titulo_base': 'Prevenção de {}',
                'conteudo_base': """Medidas preventivas para evitar ou minimizar os impactos de {}:
                
                1. Planejamento urbano adequado
                2. Sistemas de alerta precoce
                3. Educação da população
                4. Manutenção de infraestrutura crítica
                5. Planos de evacuação estabelecidos"""
            },
            {
                'titulo_base': 'Preparação para {}',
                'conteudo_base': """Como se preparar adequadamente para situações de {}:
                
                1. Kit de emergência sempre atualizado
                2. Conhecer rotas de fuga e abrigos
                3. Ter um plano familiar de emergência
                4. Manter documentos importantes em local seguro
                5. Participar de simulações e treinamentos"""
            },
            {
                'titulo_base': 'Resposta a {}',
                'conteudo_base': """Ações a serem tomadas durante {}:
                
                1. Manter a calma e seguir protocolos
                2. Usar equipamentos de proteção adequados
                3. Seguir orientações das autoridades
                4. Ajudar outras pessoas quando seguro
                5. Manter-se informado através de fontes confiáveis"""
            },
            {
                'titulo_base': 'Recuperação após {}',
                'conteudo_base': """Passos para a recuperação após ocorrência de {}:
                
                1. Avaliar danos com segurança
                2. Buscar assistência médica se necessário
                3. Registrar danos para fins de seguro
                4. Participar de esforços comunitários de reconstrução
                5. Aprender com a experiência para melhor preparação futura"""
            }
        ]
        
        total_criados = 0
        for desastre in desastres:
            for i, topico_base in enumerate(topicos_base):
                titulo = topico_base['titulo_base'].format(desastre.titulo)
                conteudo = topico_base['conteudo_base'].format(desastre.titulo.lower())
                
                TopicoDesastre.objects.create(
                    desastre=desastre,
                    titulo=titulo,
                    texto=conteudo
                )
                total_criados += 1
        
        self.stdout.write(f"  ✓ Criados {total_criados} tópicos para {len(desastres)} desastres")
        self.stdout.write(self.style.SUCCESS('Tópicos criados com sucesso!'))