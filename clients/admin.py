from django.contrib import admin

from clients.models import Client


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'email')
    list_display_links = ('first_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')
