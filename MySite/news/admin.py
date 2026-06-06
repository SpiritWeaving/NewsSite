from django.contrib import admin
from .models import News, Category, User

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', )
    list_display_links = ('id', 'username')

# Register your models here.
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'category', 'author', 'title', 'created_at', 'updated_at', 'is_published')
    list_display_links = ('title', 'id')
    search_fields = ('title', 'content', 'category__title', 'author')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('title', 'id')
    search_fields = ('title',)

admin.site.register(User, UserAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)