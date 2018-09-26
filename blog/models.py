from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
# from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


class UsrInfo(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='邮箱绑定')
    is_bind = models.BooleanField(verbose_name='邮箱绑定')

    def __str__(self):
        return self.user.username


class Bulletin(models.Model):
    url = models.URLField()
    content = models.CharField(max_length=100)

    def __str__(self):
        return self.content


class BlogType(models.Model):
    type_name = models.CharField(max_length=20)
    parent_id = models.IntegerField(default=0)

    def get_sub_types(self):
        get_sub_types = BlogType.objects.filter(parent_id=self.id)
        return get_sub_types

    def get_parent_name(self):
        try:
            parent_name = ''
            parent_name = BlogType.objects.get(id=self.parent_id).type_name
            return parent_name
        except:
            return ''

    def get_first_article_id(self):
        try:
            return self.blog_set.get_queryset().first().id
        except:
            return 0

    def __str__(self):
        return self.type_name


class Blog(models.Model):
    title = models.CharField(max_length=100)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextUploadingField(
        # extra_plugins=['syntaxhighlight'],
        # # CKEDITOR.plugins.addExternal(...)
        # external_plugin_resources=[(
        #     'syntaxhighlight',
        #     '/static/ckeditor/ckeditor/plugins/syntaxhighlight/',
        #     'plugin.js',
        # )],
    )

    # read_number = models.ForeignKey(ReadNumber, on_delete = models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    last_modify_time = models.DateTimeField(auto_now=True)

    def read_number(self):
        try:
            return self.readnumber
        except ObjectDoesNotExist:
            # readnumber = ReadNumber()
            # readnumber.blog = self
            # readnumber.save()
            return 0

    def plus_read_number(self):
        try:
            self.readnumber
        except ObjectDoesNotExist:
            self.readnumber = ReadNumber()
            self.readnumber.blog = self

        self.readnumber.read_number += 1
        self.readnumber.save()

    def __str__(self):
        return self.title

    def get_full_url(self):
        return "http://1234.com"

    class Meta:
        ordering = ['-created_time']


class ReadNumber(models.Model):
    read_number = models.IntegerField(default=0)
    blog = models.OneToOneField(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.read_number)
