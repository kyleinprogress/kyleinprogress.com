from django.contrib import admin
from django.contrib.auth.models import User

from .models import Post, Category, Image

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
            'fields': ('header_image', 'images')
        }),
        ('Extras', {
            'fields': ('category', 'site')
        }),
    )
    filter_horizontal = ('images',)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment', 'image', 'upload_date')
    exclude = ('upload_date', 'image_height', 'image_width')
    readonly_fields = ('image_thumbnail',)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Post, PostAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Category, CategoryAdmin)
