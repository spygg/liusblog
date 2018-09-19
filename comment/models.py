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

# 回复分两种情况:
# 1.回复博客,直接设置object_id为"博客id"和content_type,root_id为0
# 2.回复评论也分两种情况:
# ①.回复顶级评论,设置root_id为被回复者的"评论id",object_id也一样
# ②.回复非顶级评论,root_id设置为被回复者的根id(向上追溯),object_id为被回复者的"评论ID"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    # 有两个功能:
    # 1.设置该值为博客的id
    # 2.设置该值为某个评论的id
    # 3.可以用来反向查询某条的回复
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # 某个子评论的根ID等于本博客评论的ID
    # 1.为0时说明是评论博客
    # 2.非0则需对应某条博客根评论的id
    root_id = models.IntegerField(default=0)
    # 回复谁的ID
    #reply_to_id = models.IntegerField(default=0)

    # root = models.ForeignKey(
    #     'self', related_name='root_comment', null=True, on_delete=models.CASCADE)
    # parent = models.ForeignKey(
    #     'self', related_name='parent_comment', null=True, on_delete=models.CASCADE)
    # reply_to = models.ForeignKey(
    #     User, related_name="replies", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "<Comment, %s, %d, %d, %d>" % (self.content, self.id, self.object_id, self.root_id)

    class Meta:
        ordering = ['-created_time']
