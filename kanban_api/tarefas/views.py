from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters_drf
from .models import Tarefa, Coluna, Projeto, Usuario, Etiqueta, Comentario
from .serializers import TarefaSerializer, ColunaSerializer, ProjetoSerializer, UsuarioSerializer, EtiquetaSerializer, ComentarioSerializer

# Create your views here.

# Filtros personalizados
class TarefaFilter(filters_drf.FilterSet):
    prioridade = filters_drf.ChoiceFilter(
        choices=[('Baixa', 'Baixa'), ('Média', 'Média'), ('Alta', 'Alta')]
    )
    coluna = filters_drf.NumberFilter(field_name='coluna__id')
    projeto = filters_drf.NumberFilter(field_name='coluna__projeto__id')
    responsavel = filters_drf.NumberFilter(field_name='responsavel__id')
    criador = filters_drf.NumberFilter(field_name='criador__id')
    tags = filters_drf.NumberFilter(field_name='tags__id')
    data_criacao_inicio = filters_drf.DateTimeFilter(field_name='data_criacao', lookup_expr='gte')
    data_criacao_fim = filters_drf.DateTimeFilter(field_name='data_criacao', lookup_expr='lte')
    
    class Meta:
        model = Tarefa
        fields = ['prioridade', 'coluna', 'projeto', 'responsavel', 'criador', 'tags']

class ProjetoFilter(filters_drf.FilterSet):
    proprietario = filters_drf.NumberFilter(field_name='proprietario__id')
    membro = filters_drf.NumberFilter(field_name='membros__id')
    data_criacao_inicio = filters_drf.DateTimeFilter(field_name='data_criacao', lookup_expr='gte')
    data_criacao_fim = filters_drf.DateTimeFilter(field_name='data_criacao', lookup_expr='lte')
    
    class Meta:
        model = Projeto
        fields = ['proprietario', 'membro']

class ColunaFilter(filters_drf.FilterSet):
    projeto = filters_drf.NumberFilter(field_name='projeto__id')
    
    class Meta:
        model = Coluna
        fields = ['projeto']

class ComentarioFilter(filters_drf.FilterSet):
    tarefa = filters_drf.NumberFilter(field_name='tarefa__id')
    autor = filters_drf.NumberFilter(field_name='autor__id')
    data_criacao_inicio = filters_drf.DateTimeFilter(field_name='data_criacao', lookup_expr='gte')
    data_criacao_fim = filters_drf.DateTimeFilter(field_name='data_criacao', lookup_expr='lte')
    
    class Meta:
        model = Comentario
        fields = ['tarefa', 'autor']

# ViewSets com filtros
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'email']
    ordering_fields = ['nome', 'email']
    ordering = ['nome']

class ProjetoViewSet(viewsets.ModelViewSet):
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjetoFilter
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'data_criacao']
    ordering = ['-data_criacao']

    @action(detail=True, methods=['post'])
    def add_membro(self, request, pk=None):
        """
        Adicionar membro ao projeto
        POST /api/projetos/{id}/add_membro/
        Body: {"user_id": 5}
        """
        projeto = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            usuario = Usuario.objects.get(id=user_id)
            projeto.membros.add(usuario)
            return Response(
                {'message': f'Usuário {usuario.nome} adicionado ao projeto {projeto.nome}'}, 
                status=status.HTTP_200_OK
            )
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Usuário não encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def minhas_tarefas(self, request, pk=None):
        """
        Listar tarefas por usuário em um projeto
        GET /api/projetos/{id}/minhas_tarefas/
        """
        projeto = self.get_object()
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id é obrigatório como query parameter'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Buscar tarefas do usuário neste projeto
            tarefas = Tarefa.objects.filter(
                coluna__projeto=projeto,
                responsavel_id=user_id
            )
            serializer = TarefaSerializer(tarefas, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class ColunaViewSet(viewsets.ModelViewSet):
    queryset = Coluna.objects.all()
    serializer_class = ColunaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ColunaFilter
    search_fields = ['titulo']
    ordering_fields = ['ordem', 'titulo']
    ordering = ['ordem']

class EtiquetaViewSet(viewsets.ModelViewSet):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome']
    ordering_fields = ['nome']
    ordering = ['nome']

class TarefaViewSet(viewsets.ModelViewSet):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TarefaFilter
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['titulo', 'prioridade', 'data_criacao', 'data_conclusao']
    ordering = ['-data_criacao']

    @action(detail=True, methods=['post'])
    def atribuir(self, request, pk=None):
        """
        Atribuir responsável à tarefa
        POST /api/tarefas/{id}/atribuir/
        Body: {"user_id": 5}
        """
        tarefa = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            usuario = Usuario.objects.get(id=user_id)
            tarefa.responsavel = usuario
            tarefa.save()
            
            serializer = self.get_serializer(tarefa)
            return Response(
                {
                    'message': f'Tarefa "{tarefa.titulo}" atribuída a {usuario.nome}',
                    'tarefa': serializer.data
                }, 
                status=status.HTTP_200_OK
            )
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Usuário não encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ComentarioFilter
    search_fields = ['texto']
    ordering_fields = ['data_criacao']
    ordering = ['-data_criacao']
