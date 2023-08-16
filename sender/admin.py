from django.contrib import admin

from sender.models import Sender, SenderLog


# Register your models here.
@admin.register(Sender)
class SenderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subject', 'message', 'period', 'status', 'time')
    list_display_links = ('subject', )
    search_fields = ('subject', 'client')
    list_filter = ('subject', 'client')


@admin.register(SenderLog)
class SenderLogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'client', 'sender', 'status', 'last_try')
    list_display_links = ('client', 'last_try')
    search_fields = ('client', 'status')
    list_filter = ('client', 'status')
