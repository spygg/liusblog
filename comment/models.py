from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.models.query import QuerySet

#递归查找所有子评论
def do_recursive_find(comment_list, parent_id, level, result_list):
    level += 1
    for comment in comment_list:
        if comment.object_id == parent_id:
            result_list.insert(0, comment)
            do_recursive_find(comment_list, comment.id, level, result_list)


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
        content_type = ContentType.objects.get_for_model(self)
        comment_comments = Comment.objects.filter(content_type = content_type)
   
        result_comments = []
        do_recursive_find(comment_comments, self.id, 0, result_comments)

        #逆序输出
        return result_comments[::-1]

    class Meta:
        ordering = ['-created_time']