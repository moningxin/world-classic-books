from django.contrib import admin
from .models import Category, Book, User

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']  # 添加 id
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'publisher', 'category', 'price', 'likes', 'is_active', 'created_at']  # 添加 id 和 is_active
    list_filter = ['category', 'created_at', 'is_active']
    search_fields = ['title', 'author', 'publisher']
    list_editable = ['price', 'is_active']  # 确保 is_active 在 list_display 中

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'phone', 'reading_hobbies']  # 添加 id
    search_fields = ['username', 'phone']