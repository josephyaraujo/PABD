from core.models import Usuario, Veiculo, Carona, Solicitacao
from django.contrib.auth.hashers import make_password

# Criar usuários
usuarios = [
    {"username": "motorista1", "email": "motorista1@email.com", "password": make_password("123456"), "tipo": "MOTORISTA"},
    {"username": "motorista2", "email": "motorista2@email.com", "password": make_password("123456"), "tipo": "MOTORISTA"},
    {"username": "passageiro1", "email": "passageiro1@email.com", "password": make_password("123456"), "tipo": "PASSAGEIRO"},
    {"username": "passageiro2", "email": "passageiro2@email.com", "password": make_password("123456"), "tipo": "PASSAGEIRO"},
    {"username": "usuario_ambos", "email": "ambos@email.com", "password": make_password("123456"), "tipo": "AMBOS"},
]
usuarios_objs = [Usuario.objects.create(**u) for u in usuarios]

# Criar veículos (motorista1, motorista2, usuario_ambos podem ser motoristas)
veiculos = [
    {"motorista": usuarios_objs[0], "modelo": "Corsa", "marca": "Chevrolet", "cor": "Prata", "ano": 2010, "placa": "AAA1111", "num_lugares": 4, "ativo": True},
    {"motorista": usuarios_objs[1], "modelo": "Fiesta", "marca": "Ford", "cor": "Vermelho", "ano": 2012, "placa": "BBB2222", "num_lugares": 5, "ativo": True},
    {"motorista": usuarios_objs[4], "modelo": "HB20", "marca": "Hyundai", "cor": "Branco", "ano": 2018, "placa": "CCC3333", "num_lugares": 5, "ativo": True},
]
veiculos_objs = [Veiculo.objects.create(**v) for v in veiculos]

# Criar caronas
from datetime import datetime, timedelta
caronas = [
    {"motorista": usuarios_objs[0], "veiculo": veiculos_objs[0], "origem": "A", "destino": "B", "data_hora_saida": datetime.now()+timedelta(days=1), "vagas_disponiveis": 3, "preco_por_pessoa": 10.0, "status": "DISPONIVEL"},
    {"motorista": usuarios_objs[1], "veiculo": veiculos_objs[1], "origem": "B", "destino": "C", "data_hora_saida": datetime.now()+timedelta(days=2), "vagas_disponiveis": 2, "preco_por_pessoa": 15.0, "status": "DISPONIVEL"},
    {"motorista": usuarios_objs[4], "veiculo": veiculos_objs[2], "origem": "C", "destino": "D", "data_hora_saida": datetime.now()+timedelta(days=3), "vagas_disponiveis": 3, "preco_por_pessoa": 12.0, "status": "DISPONIVEL"},
    {"motorista": usuarios_objs[0], "veiculo": veiculos_objs[0], "origem": "A", "destino": "C", "data_hora_saida": datetime.now()+timedelta(days=4), "vagas_disponiveis": 1, "preco_por_pessoa": 8.0, "status": "DISPONIVEL"},
    {"motorista": usuarios_objs[1], "veiculo": veiculos_objs[1], "origem": "B", "destino": "D", "data_hora_saida": datetime.now()+timedelta(days=5), "vagas_disponiveis": 2, "preco_por_pessoa": 20.0, "status": "DISPONIVEL"},
]
caronas_objs = [Carona.objects.create(**c) for c in caronas]

# Criar solicitações (exemplo: todos os passageiros e ambos solicitam vagas nas caronas)
for i in range(10):
    Solicitacao.objects.create(
        carona=caronas_objs[i % 5],
        passageiro=usuarios_objs[(i+2) % 5], # alterna entre passageiros e ambos
        num_lugares=1,
        status="PENDENTE"
    )

print("Banco de dados povoado com sucesso!")
