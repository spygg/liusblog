from django.contrib import admin
from .models import BlogType, Blog

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog_type', 'author', 'created_time', 'last_modify_time',)
    list_filter = ('id', 'created_time', )
#admin.site.register(Blog, BlogAdmin)