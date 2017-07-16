from django.contrib import admin
from .models import Category, Post,Comments

class PostForAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    class Meta:
        model = Post

class CategoryForAdmin(admin.ModelAdmin):
    prepopulated_fields = {'categorySlug': ('categoryName',)}
    class Meta:
        model = Category

# Register your models here.
admin.site.register(Category,CategoryForAdmin)
admin.site.register(Post,PostForAdmin)
admin.site.register(Comments)