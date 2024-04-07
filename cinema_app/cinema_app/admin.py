from django.contrib import admin

from .models import Horario
from .models import Filme

admin.site.register(Filme)
admin.site.register(Horario)