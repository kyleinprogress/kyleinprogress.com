from django.contrib import admin
from django.contrib.auth.models import User

from .models import Post, Category, Tag

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'published_date', 'is_published')
    prepopulated_fields = {"slug": ("title",)}
    exclude = ('author', 'created_date')
    fieldsets = (
        ('Post Title', {
            'fields': ('title', 'slug')
        }),
        ('Post Content', {
            'fields': ('summary', 'text')
        }),
        ('Publish Info', {
            'fields': ('is_active', 'published_date')
        }),
        ('Images', {
            'fields': ('header_image',)
        }),
        ('Extras', {
            'fields': ('category', 'tags', 'site')
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
