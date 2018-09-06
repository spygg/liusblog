from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add = True)

    #评论的类型
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    #某个类型的索引
    object_id = models.PositiveIntegerField()
    #对应具体某个评论对象
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "<Comment, %s, %d>" % (self.content, self.id)

    def get_sub_comments(self):
        print(self.content_object.id, self.id, self.object_id)
        # | Q(self.content_object.content_type_id = self.object_id)
        subcomment = Comment.objects.filter(Q(object_id = self.id)  
             | (Q(object_id = self.object_id) ));

        return subcomment

    class Meta:
        ordering = ['-created_time']