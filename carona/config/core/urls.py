from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsuarioViewSet, PerfilUsuarioViewSet, VeiculoViewSet,
    CaronaViewSet, SolicitacaoViewSet, AvaliacaoViewSet, ChatViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'perfis', PerfilUsuarioViewSet, basename='perfil')
router.register(r'veiculos', VeiculoViewSet, basename='veiculo')
router.register(r'caronas', CaronaViewSet, basename='carona')
router.register(r'solicitacoes', SolicitacaoViewSet, basename='solicitacao')
router.register(r'avaliacoes', AvaliacaoViewSet, basename='avaliacao')
router.register(r'chats', ChatViewSet, basename='chat')

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
]