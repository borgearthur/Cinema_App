from django.contrib import admin

from .models import UserAluno
from .models import Dados_saude
from .models import MensagemContato
from .models import Frequencia_Aluno

admin.site.register(UserAluno)
admin.site.register(Dados_saude)
admin.site.register(MensagemContato)
admin.site.register(Frequencia_Aluno)