from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'preview', 'number_views', 'date_of_creation', 'sign_publication', 'owner',)
