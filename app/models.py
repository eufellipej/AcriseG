from django.db import models

class Funcao(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da função")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Função"
        verbose_name_plural = "Funções"


class TurnoTrabalho(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Turno de trabalho")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Turno de Trabalho"
        verbose_name_plural = "Turnos de Trabalho"


class TipoAnalise(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Tipo de formulário de análise")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Tipo de Análise"
        verbose_name_plural = "Tipos de Análise"


class Cidade(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da cidade")
    uf = models.CharField(max_length=2, verbose_name="UF")

    def __str__(self):
        return f"{self.nome}, {self.uf}"

    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"


class PlataformaJogo(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Plataforma de jogo")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Plataforma de Jogo"
        verbose_name_plural = "Plataformas de Jogo"


class EstudioDesenvolvimento(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do estúdio")
    site = models.CharField(max_length=100, verbose_name="Site")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE, verbose_name="Cidade")
    email = models.EmailField(verbose_name="Email")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Estúdio de Desenvolvimento"
        verbose_name_plural = "Estúdios de Desenvolvimento"


class MembroEquipe(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do membro")
    email = models.EmailField(verbose_name="Email")
    funcao = models.ForeignKey(Funcao, on_delete=models.CASCADE, verbose_name="Função")
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE, verbose_name="Cidade")
    EstudioDesenvolvimento = models.ForeignKey(EstudioDesenvolvimento, on_delete=models.CASCADE, verbose_name="estudio desenvovimento")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    data_admissao = models.DateField(verbose_name="Data de admissão")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Membro da Equipe"
        verbose_name_plural = "Membros da Equipe"


class Jogo(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título do jogo")
    genero = models.CharField(max_length=100, verbose_name="Gênero")
    data_lancamento = models.DateField(verbose_name="Data de lançamento")
    estudio = models.ForeignKey(EstudioDesenvolvimento, on_delete=models.CASCADE, verbose_name="Estúdio de desenvolvimento")
    descricao = models.TextField(verbose_name="Descrição")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Jogo"
        verbose_name_plural = "Jogos"


class Jogo_Plataforma(models.Model):
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE, verbose_name="Jogo")
    plataforma = models.ForeignKey(PlataformaJogo, on_delete=models.CASCADE, verbose_name="Plataforma")

    class Meta:
        verbose_name = "Plataforma do Jogo"
        verbose_name_plural = "Plataformas dos Jogos"


class Alocacao(models.Model):
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE, verbose_name="Jogo")
    membro = models.ForeignKey(MembroEquipe, on_delete=models.CASCADE, verbose_name="Membro da equipe")
    data_inicio = models.DateField(verbose_name="Data de início")
    data_fim = models.DateField(verbose_name="Data de término")
    papel = models.CharField(max_length=100, verbose_name="Papel desempenhado")

    class Meta:
        verbose_name = "Alocação"
        verbose_name_plural = "Alocações"


class EtapaDesenvolvimento(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da etapa")
    data_inicio = models.DateField(verbose_name="Data de início")
    data_fim = models.DateField(verbose_name="Data de término")
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE, verbose_name="Jogo")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Etapa de Desenvolvimento"
        verbose_name_plural = "Etapas de Desenvolvimento"


class Tarefa(models.Model):
    descricao = models.TextField(verbose_name="Descrição")
    prioridade = models.CharField(max_length=50, verbose_name="Prioridade")
    data_limite = models.DateField(verbose_name="Data limite")
    etapa = models.ForeignKey(EtapaDesenvolvimento, on_delete=models.CASCADE, verbose_name="Etapa de desenvolvimento")
    responsavel = models.ForeignKey(MembroEquipe, on_delete=models.CASCADE, verbose_name="Responsável")

    class Meta:
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"


class TarefaDetalhe(models.Model):
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, verbose_name="Tarefa")
    membro = models.ForeignKey(MembroEquipe, on_delete=models.CASCADE, verbose_name="Membro")
    observacoes = models.TextField(verbose_name="Observações")

    class Meta:
        verbose_name = "Detalhamento da Tarefa"
        verbose_name_plural = "Detalhamentos das Tarefas"


class ComponenteProjetoJogo(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do componente")
    carga_horaria = models.IntegerField(verbose_name="Carga horária")
    etapa = models.ForeignKey(EtapaDesenvolvimento, on_delete=models.CASCADE, verbose_name="Etapa de desenvolvimento")
    turno = models.ForeignKey(TurnoTrabalho, on_delete=models.CASCADE, verbose_name="Turno de trabalho")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Componente do Projeto"
        verbose_name_plural = "Componentes do Projeto"




class AssetDigital(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    arquivo = models.ImageField(upload_to='assets/')  # novo campo
    versao = models.CharField(max_length=50)
    autor = models.CharField(max_length=100)
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Asset Digital"
        verbose_name_plural = "Assets Digitais"



class Cenario(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)  # campo descrição
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    arquivo = models.FileField(upload_to='cenarios/', blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Cenário"
        verbose_name_plural = "Cenários"



class Cenario_Asset(models.Model):
    cenario = models.ForeignKey(Cenario, on_delete=models.CASCADE, verbose_name="Cenário")
    asset = models.ForeignKey(AssetDigital, on_delete=models.CASCADE, verbose_name="Asset")

    class Meta:
        verbose_name = "Asset do Cenário"
        verbose_name_plural = "Assets dos Cenários"


class Ocorrencia(models.Model):
    descricao = models.TextField(verbose_name="Descrição")
    data = models.DateField(verbose_name="Data")
    membro = models.ForeignKey(MembroEquipe, on_delete=models.CASCADE, verbose_name="Membro")
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE, verbose_name="Jogo")
    tipo_ocorrencia = models.CharField(max_length=100, verbose_name="Tipo de ocorrência")

    class Meta:
        verbose_name = "Ocorrência"
        verbose_name_plural = "Ocorrências"


class AnaliseProcesso(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título")
    data_preenchimento = models.DateField(verbose_name="Data de preenchimento")
    resultado = models.TextField(verbose_name="Resultado")
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE, verbose_name="Jogo")
    etapa = models.ForeignKey(EtapaDesenvolvimento, on_delete=models.CASCADE, verbose_name="Etapa de desenvolvimento")
    tipoAnalise = models.ForeignKey(TipoAnalise, on_delete=models.CASCADE, verbose_name="Tipo de analise")

    class Meta:
        verbose_name = "Análise do Processo"
        verbose_name_plural = "Análises do Processo"


class UsuarioSistema(models.Model):
    username = models.CharField(max_length=100, verbose_name="Nome de usuário")
    senha_hash = models.CharField(max_length=255, verbose_name="Senha (Hash)")
    membro = models.ForeignKey(MembroEquipe, on_delete=models.CASCADE, verbose_name="Membro associado")
    perfil = models.CharField(max_length=50, verbose_name="Perfil de acesso")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Usuário do Sistema"
        verbose_name_plural = "Usuários do Sistema"


class ConfiguracaoSistema(models.Model):
    nome_opcao = models.CharField(max_length=100, verbose_name="Nome da opção")
    valor = models.CharField(max_length=255, verbose_name="Valor")
    descricao = models.TextField(verbose_name="Descrição")

    class Meta:
        verbose_name = "Configuração do Sistema"
        verbose_name_plural = "Configurações do Sistema"
