from cafe.models import Client
from django.contrib import admin


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass