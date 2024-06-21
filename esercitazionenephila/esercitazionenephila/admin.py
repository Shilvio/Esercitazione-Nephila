from django.contrib import admin
from utente.models import Utente


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Utente, AuthorAdmin)