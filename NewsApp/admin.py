from django.contrib import admin

from NewsApp.models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'ai_status', 'source_link')
    search_fields = ('title', 'intro')
    list_filter = ('status', 'ai_status')