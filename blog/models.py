from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


class BlogType(models.Model):
    type_name = models.CharField(max_length = 20)

    def __str__(self):
        return self.type_name

class Blog(models.Model):
    title = models.CharField(max_length = 100)
    blog_type = models.ForeignKey(BlogType, on_delete = models.DO_NOTHING)
    author = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    content = RichTextUploadingField()
    
    # read_number = models.ForeignKey(ReadNumber, on_delete = models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add = True)
    last_modify_time = models.DateTimeField(auto_now = True)

    
    def read_number(self):
        try:
            return self.readnumber
        except ObjectDoesNotExist as e:
            # readnumber = ReadNumber()
            # readnumber.blog = self
            # readnumber.save()
            return 0
    
    def plus_read_number(self):
        if not self.readnumber:
            self.readnumber = ReadNumber()
            self.readnumber.blog = self

        self.readnumber.read_number = self.readnumber.read_number + 1
        self.readnumber.save()
        

    def __str__(self):
        return self.title

    def get_full_url(self):
        return "http://1234.com"
        
    class Meta:
        ordering = ['-created_time']


class ReadNumber(models.Model):
    read_number = models.IntegerField(default=0)
    blog = models.OneToOneField(Blog, on_delete = models.CASCADE)
    
    def __str__(self):
        return str(self.read_number)