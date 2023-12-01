from django.contrib import admin
from .models import Tareas

class tareasAdmin(admin.ModelAdmin):
    readonly_fields = ('creado', )

# Register your models here.

admin.site.register(Tareas, tareasAdmin)