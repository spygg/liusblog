from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class BlogType(models.Model):
    type_name = models.CharField(max_length = 20)

    def __str__(self):
        return self.type_name

class Blog(models.Model):
    title = models.CharField(max_length = 100)
    blog_type = models.ForeignKey(BlogType, on_delete = models.DO_NOTHING)
    author = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    content = RichTextField()

    created_time = models.DateTimeField(auto_now_add = True)
    last_modify_time = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

    def get_full_url(self):
        return "http://1234.com"
        
    class Meta:
        ordering = ['-created_time']