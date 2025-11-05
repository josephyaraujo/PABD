import django_filters
from .models import Carona

class CaronaFilter(django_filters.FilterSet):
    preco_min = django_filters.NumberFilter(field_name="preco_por_pessoa", lookup_expr='gte')
    preco_max = django_filters.NumberFilter(field_name="preco_por_pessoa", lookup_expr='lte')
    data_min = django_filters.DateTimeFilter(field_name="data_hora_saida", lookup_expr='gte')
    data_max = django_filters.DateTimeFilter(field_name="data_hora_saida", lookup_expr='lte')

    class Meta:
        model = Carona
        fields = ['origem', 'destino', 'preco_min', 'preco_max', 'data_min', 'data_max']
