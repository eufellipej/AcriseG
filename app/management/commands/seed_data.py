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
                'imagem': '',  # Sem imagem para evitar problema de tamanho
                'ativo': True
            },
            {
                'nome': 'João Editor',
                'email': 'editor@acriseg.com',
                'senha': 'editor123',
                'tipo': 'editor',
                'imagem': '',  # Sem imagem para evitar problema de tamanho
                'ativo': True
            },
            {
                'nome': 'Maria Usuária',
                'email': 'maria@exemplo.com',
                'senha': 'maria123',
                'tipo': 'usuario',
                'imagem': '',  # Sem imagem para evitar problema de tamanho
                'ativo': True
            },
            {
                'nome': 'Carlos Especialista',
                'email': 'carlos@especialista.com',
                'senha': 'especialista123',
                'tipo': 'especialista',
                'imagem': '',  # Sem imagem para evitar problema de tamanho
                'ativo': True
            },
            {
                'nome': 'Ana Professora',
                'email': 'ana@escola.com',
                'senha': 'professora123',
                'tipo': 'usuario',
                'imagem': '',  # Sem imagem para evitar problema de tamanho
                'ativo': True
            }
        ]
        
        for user_data in usuarios:
            # Criar usuário com senha em texto claro - o modelo fará o hash
            usuario = Usuario(
                nome=user_data['nome'],
                email=user_data['email'],
                senha=user_data['senha'],  # Texto claro
                tipo=user_data['tipo'],
                imagem=user_data['imagem'],
                ativo=user_data['ativo']
            )
            usuario.save()  # O método save() fará o hash da senha
            self.stdout.write(f"  ✓ Usuário criado: {user_data['nome']} ({user_data['email']})")
        
        self.stdout.write(self.style.SUCCESS(f'{len(usuarios)} usuários criados!'))
    
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
            Desastre.objects.create(**desastre_data)
            self.stdout.write(f"  ✓ Desastre criado: {desastre_data['titulo']}")
        
        self.stdout.write(self.style.SUCCESS(f'{len(desastres)} desastres criados!'))
    
    def criar_jogos(self):
        """Cria jogos com todas as relações"""
        self.stdout.write('Criando jogo principal...')
        
        # Criar jogo principal
        jogo = Jogo.objects.create(
            titulo="Survivor: Desafio da Natureza",
            subtitulo="Um jogo educativo imersivo que ensina sobre preparação e resposta a desastres naturais",
            descricao="Desenvolvido em parceria com especialistas em gestão de crises.",
            descricao_detalhada="Survivor: Desafio da Natureza é um jogo educativo que combina aprendizado com diversão.",
            desenvolvedor="A Crise G Studios",
            plataformas="Windows, Android, iOS",
            idade_recomendada="12+ anos",
            tamanho="850MB (PC) / 320MB (Mobile)",
            versao="1.3.2",
            download_windows="https://example.com/download/windows",
            download_android="https://example.com/download/android",
            download_ios="https://example.com/download/ios",
            imagem_capa="https://i.imgur.com/abc123.jpg",  # URL curta
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
            "Windows 10 64-bit",
            "Intel i3 ou equivalente AMD",
            "4GB RAM",
        ]
        
        for req in requisitos_min:
            RequisitoJogo.objects.create(jogo=jogo, tipo='minimo', descricao=req)
        
        # Requisitos recomendados
        self.stdout.write('  Adicionando requisitos recomendados...')
        requisitos_rec = [
            "Windows 11 64-bit",
            "Intel i5 ou equivalente AMD Ryzen 5",
            "8GB RAM",
        ]
        
        for req in requisitos_rec:
            RequisitoJogo.objects.create(jogo=jogo, tipo='recomendado', descricao=req)
        
        # Atualizações
        self.stdout.write('  Adicionando atualizações...')
        atualizacoes = [
            ("1.3", date(2025, 8, 25), "Novo cenário de seca extrema adicionado", "Inclui mecânicas de gestão de recursos hídricos"),
            ("1.2", date(2025, 7, 15), "Módulo de terremotos com novas mecânicas de sobrevivência", "Triângulo da vida, pontos seguros"),
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
        
        # FAQs
        self.stdout.write('  Adicionando FAQs...')
        faqs = [
            ("O jogo é gratuito?", "Sim, a versão básica do jogo é completamente gratuita.", "geral"),
            ("Posso usar em sala de aula?", "Absolutamente! Temos material de apoio pedagógico.", "pedagogico"),
            ("Precisa de internet para jogar?", "Não, após o download o jogo funciona totalmente offline.", "tecnico"),
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
        
        # Imagens
        self.stdout.write('  Adicionando imagens...')
        imagens = [
            ("https://i.imgur.com/abc123.jpg", "Terremoto nível 7.2"),
            ("https://i.imgur.com/def456.jpg", "Furacão categoria 4"),
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
                'resumo': 'Guia completo com dicas práticas para se preparar e responder a enchentes.',
                'dataPublicacao': date(2024, 3, 10),
                'usuario': usuarios[1]  # Editor
            },
            {
                'titulo': 'Prevenção de Queimadas em Áreas Rurais',
                'resumo': 'Estratégias eficazes para prevenir incêndios florestais.',
                'dataPublicacao': date(2024, 4, 15),
                'usuario': usuarios[2]  # Maria
            },
        ]
        
        for artigo_data in artigos:
            artigo = Artigo.objects.create(**artigo_data)
            self.stdout.write(f"  ✓ Artigo criado: {artigo_data['titulo']}")
            
            # Criar tópicos para o artigo
            for i in range(1, 3):
                TopicoArtigo.objects.create(
                    artigo=artigo,
                    titulo=f"Seção {i}: {artigo.titulo[:20]}...",
                    texto=f"Conteúdo da seção {i} do artigo sobre {artigo.titulo}."
                )
        
        self.stdout.write(self.style.SUCCESS(f'{len(artigos)} artigos criados!'))
    
    def criar_acontecimentos(self):
        """Cria acontecimentos históricos"""
        self.stdout.write('Criando acontecimentos...')
        
        acontecimentos = [
            {
                'titulo': 'Enchente Histórica em São Paulo - 2023',
                'descricao': 'A maior enchente registrada na cidade de São Paulo.',
                'dataAcontecimento': date(2023, 2, 10),
                'risco': 'Alto'
            },
            {
                'titulo': 'Queimadas na Amazônia - 2022',
                'descricao': 'Série de incêndios florestais na floresta amazônica.',
                'dataAcontecimento': date(2022, 8, 15),
                'risco': 'Crítico'
            },
        ]
        
        for ac_data in acontecimentos:
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
                'descricao': 'Área com histórico de alagamentos.',
                'localizacao': 'Zona Norte - São Paulo',
                'desastre': desastres[0]  # Enchentes
            },
            {
                'nome': 'Risco de Incêndio Florestal',
                'nivel': 'Crítico',
                'descricao': 'Região com vegetação seca.',
                'localizacao': 'Chapada Diamantina - BA',
                'desastre': desastres[1]  # Queimadas
            },
        ]
        
        for risco_data in riscos:
            Risco.objects.create(**risco_data)
            self.stdout.write(f"  ✓ Risco criado: {risco_data['nome']}")
        
        self.stdout.write(self.style.SUCCESS(f'{len(riscos)} riscos criados!'))
    
    def criar_paginas(self):
        """Cria páginas do site"""
        self.stdout.write('Criando páginas...')
        
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
                'descricao': 'Página com informações sobre prevenção e resposta a enchentes.',
                'artigo': artigos[0],
                'desastre': desastres[0],
                'jogo': jogos[0],
                'acontecimento': acontecimentos[0]
            },
        ]
        
        for pagina_data in paginas:
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
        
        jogo = jogos[0]
        
        avaliacoes = [
            {
                'texto': 'Jogo incrível! Aprendi muito.',
                'nota': 5,
                'usuario': usuarios[1],
                'jogo': jogo
            },
            {
                'texto': 'Muito educativo.',
                'nota': 4,
                'usuario': usuarios[2],
                'jogo': jogo
            },
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
                'resposta': 'O jogo salva automaticamente seu progresso.',
                'usuario': usuarios[1],
                'jogo': jogo
            },
        ]
        
        for pergunta_data in perguntas_antigas:
            Pergunta.objects.create(**pergunta_data)
            self.stdout.write(f"  ✓ Pergunta criada: {pergunta_data['pergunta'][:50]}...")
        
        # Perguntas do usuário (novo modelo PerguntaUsuario)
        perguntas_usuarios = [
            {
                'pergunta': 'O jogo tem suporte para telas ultrawide?',
                'email': 'gamer@email.com',
                'status': 'respondida',
                'resposta_admin': 'Sim, o jogo tem suporte para resoluções ultrawide.',
                'usuario': usuarios[2],
                'jogo': jogo,
                'admin_respondeu': admin_usuario,
                'data_resposta': timezone.now()
            },
        ]
        
        for pergunta_data in perguntas_usuarios:
            PerguntaUsuario.objects.create(**pergunta_data)
            self.stdout.write(f"  ✓ Pergunta de usuário criada: {pergunta_data['pergunta'][:50]}...")
        
        # Criar tópicos para desastres
        desastres = Desastre.objects.all()
        for desastre in desastres:
            TopicoDesastre.objects.create(
                desastre=desastre,
                titulo=f"Prevenção de {desastre.titulo}",
                texto=f"Conteúdo educativo sobre prevenção de {desastre.titulo.lower()}."
            )
        
        self.stdout.write(self.style.SUCCESS('Perguntas e tópicos criados com sucesso!'))