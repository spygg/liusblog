from django.contrib import admin
from .models import UsrInfo, BlogType, Blog, ReadNumber, Bulletin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UsrInfoInline(admin.StackedInline):
    model = UsrInfo
    #verbose_name_plural = 'UsrInfo'

# Define a new User admin


class UserAdmin(BaseUserAdmin):
    inlines = (UsrInfoInline,)
    list_display = ('username', 'email', 'is_active',
                    'is_staff', 'is_superuser', 'is_bind', )

    def is_bind(self, obj):
        return obj.usrinfo.is_bind

    is_bind.short_description = '邮箱绑定'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UsrInfo)
class UsrInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_bind')


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name', 'parent_id', )


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'blog_type', 'read_number',
                    'author', 'created_time', 'last_modify_time',)
    list_filter = ('blog_type', 'created_time', )
    list_display_links = ('id', 'blog_type', 'title', 'author', )


@admin.register(ReadNumber)
class ReadNumberAdmin(admin.ModelAdmin):
    list_display = ('id', 'read_number', 'blog',)
#admin.site.register(Blog, BlogAdmin)


@admin.register(Bulletin)
class BulletinAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'content',)
