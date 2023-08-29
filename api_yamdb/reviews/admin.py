from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Category, Genre, Title, Review, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('slug',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('slug',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'rating', 'description', 'category')
    search_fields = ('name',)
    list_filter = ('year', 'rating',  'category')


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
