from rest_framework import serializers
from .models import Tarefa, Coluna, Projeto, Usuario, Etiqueta, Comentario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = '__all__'

class ComentarioSerializer(serializers.ModelSerializer):
    autor_nome = serializers.CharField(source='autor.nome', read_only=True)
    
    class Meta:
        model = Comentario
        fields = ['id', 'texto', 'data_criacao', 'autor', 'autor_nome', 'tarefa']

class TarefaSerializer(serializers.ModelSerializer):
    responsavel_info = UsuarioSerializer(source='responsavel', read_only=True)
    criador_info = UsuarioSerializer(source='criador', read_only=True)
    tags_nomes = serializers.SerializerMethodField()
    comentarios_count = serializers.SerializerMethodField()
    comentarios = ComentarioSerializer(many=True, read_only=True)
    
    class Meta:
        model = Tarefa
        fields = [
            'id', 'titulo', 'descricao', 'prioridade', 'data_criacao', 
            'data_conclusao', 'coluna', 'responsavel', 'responsavel_info',
            'criador', 'criador_info', 'tags', 'tags_nomes', 
            'comentarios_count', 'comentarios'
        ]
    
    def get_tags_nomes(self, obj):
        return [tag.nome for tag in obj.tags.all()]
    
    def get_comentarios_count(self, obj):
        return obj.comentarios.count()

class ColunaSerializer(serializers.ModelSerializer):
    tarefas = TarefaSerializer(many=True, read_only=True)
    projeto_nome = serializers.CharField(source='projeto.nome', read_only=True)
    
    class Meta:
        model = Coluna
        fields = ['id', 'titulo', 'ordem', 'projeto', 'projeto_nome', 'tarefas']

class ProjetoSerializer(serializers.ModelSerializer):
    colunas = ColunaSerializer(many=True, read_only=True)
    membros_nomes = serializers.SerializerMethodField()
    proprietario_nome = serializers.CharField(source='proprietario.nome', read_only=True)
    tarefas_totais = serializers.SerializerMethodField()
    
    class Meta:
        model = Projeto
        fields = [
            'id', 'nome', 'descricao', 'data_criacao', 'proprietario', 
            'proprietario_nome', 'membros', 'membros_nomes', 'colunas', 'tarefas_totais'
        ]
    
    def get_membros_nomes(self, obj):
        return [membro.nome for membro in obj.membros.all()]
    
    def get_tarefas_totais(self, obj):
        # Conta todas as tarefas de todas as colunas do projeto
        total = 0
        for coluna in obj.colunas.all():
            total += coluna.tarefas.count()
        return total
