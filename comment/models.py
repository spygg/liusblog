from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.models.query import QuerySet

# 递归查找所有子评论
# def do_recursive_find(comment_list, parent_id, level, result_list):
#     level += 1
#     for comment in comment_list:
#         if comment.object_id == parent_id:
#             result_list.insert(0, comment)
#             do_recursive_find(comment_list, comment.id, level, result_list)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    #某个子评论的根ID等于本博客评论的ID
    root_id = models.IntegerField(default=0)
    #回复谁的ID
    reply_to_id = models.IntegerField(default=0)

    def get_subcomments(self):
        sub_comments = Comment.objects.filter(root_id=self.id)
        return sub_comments

    # root = models.ForeignKey(
    #     'self', related_name='root_comment', null=True, on_delete=models.CASCADE)
    # parent = models.ForeignKey(
    #     'self', related_name='parent_comment', null=True, on_delete=models.CASCADE)
    # reply_to = models.ForeignKey(
    #     User, related_name="replies", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "<Comment, %s, %d>" % (self.content, self.id)

    class Meta:
        ordering = ['-created_time']
