from django import template
# from ..models import Comment
from comment.models import Comment
from comment.forms import CommentForm
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.simple_tag
def get_top_comments(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(
        object_id=obj.pk, content_type=content_type)
    return comments


@register.simple_tag
def get_comment_number(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return 'hah'


@register.simple_tag
def get_comment_user_number(obj):
    pass


@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    commentForm = CommentForm(initial={
                              'content_type': content_type.model,
                              'object_id': obj.pk,
                              'reply_comment_id': 0})
    return commentForm


@register.simple_tag
def get_subcomments(obj):
    sub_comments = Comment.objects.filter(root_id=obj.id)
    return sub_comments.order_by('created_time')


@register.simple_tag
def get_reply_username(obj):
    reply = Comment.objects.get(id=obj.object_id)
    return reply.user.username
