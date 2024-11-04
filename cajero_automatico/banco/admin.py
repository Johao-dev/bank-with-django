from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Usuarios)
admin.site.register(Tarjetas)
admin.site.register(Transferencias)
admin.site.register(Depositos)
admin.site.register(Retiros)
admin.site.register(Cuentas)
admin.site.register(Consultas)