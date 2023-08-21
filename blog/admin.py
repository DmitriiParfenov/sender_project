from django.contrib import admin

from blog.models import Blog


# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'view_count', 'content', 'published', 'email',)
    list_display_links = ('title', 'view_count', 'email',)
    search_fields = ('title', 'view_count')
