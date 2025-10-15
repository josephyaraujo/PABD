from django.db import models

# Create your models here.

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nome

class Projeto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    proprietario = models.ForeignKey(Usuario, related_name='projetos_criados', on_delete=models.CASCADE)
    membros = models.ManyToManyField(Usuario, related_name='projetos')

    def __str__(self):
        return f"{self.nome} - {self.descricao} - {self.data_criacao} - {self.proprietario.nome}"

class Coluna(models.Model):
    titulo = models.CharField(max_length=50)
    projeto = models.ForeignKey(Projeto, related_name='colunas', on_delete=models.CASCADE)
    ordem = models.PositiveIntegerField()

    class Meta:
        unique_together = ('projeto', 'ordem')
        ordering = ['ordem']

    def __str__(self):
        return f"{self.titulo} ({self.projeto.nome})"

class Etiqueta(models.Model):
    nome = models.CharField(max_length=50)
    cor = models.CharField(max_length=7)  # Exemplo: #RRGGBB

    def __str__(self):
        return self.nome
    
class Tarefa(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    coluna = models.ForeignKey(Coluna, related_name='tarefas', on_delete=models.CASCADE)
    responsavel = models.ForeignKey(Usuario, related_name='tarefas_responsavel', on_delete=models.SET_NULL, blank=True, null=True)
    criador = models.ForeignKey(Usuario, related_name='tarefas_criadas', on_delete=models.CASCADE)
    prioridade = models.CharField(max_length=50, choices=[('Baixa', 'Baixa'), ('Média', 'Média'), ('Alta', 'Alta')], default='Baixa') 
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_conclusao = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField(Etiqueta, related_name='tarefas', blank=True)
   
    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    tarefa = models.ForeignKey(Tarefa, related_name='comentarios', on_delete=models.CASCADE)
    autor = models.ForeignKey(Usuario, related_name='comentarios', on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.autor.nome} na tarefa {self.tarefa.titulo}"
