from django.contrib import admin
from .models import Usuario, Projeto, Coluna, Etiqueta, Tarefa, Comentario

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Projeto)
admin.site.register(Coluna)
admin.site.register(Etiqueta)
admin.site.register(Tarefa)
admin.site.register(Comentario)
