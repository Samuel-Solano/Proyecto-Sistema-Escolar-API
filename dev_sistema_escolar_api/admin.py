from django.contrib import admin
from django.utils.html import format_html
from dev_sistema_escolar_api.models import *


admin.site.register(Alumnos)
admin.site.register(Maestros)
admin.site.register(Administradores)
admin.site.register(Eventos)

class ProfilesAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "creation", "update")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")
