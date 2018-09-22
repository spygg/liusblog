from django import template
# from ..models import Comment
from comment.models import Comment
from comment.forms import CommentForm
# from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# from django.db.models import Count

register = template.Library()


@register.simple_tag
def get_top_comments(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(
        object_id=obj.pk, content_type=content_type)
    return comments


@register.simple_tag
def get_subcomments(obj):
    content_type = ContentType.objects.get_for_model(obj)
    print('content_type: ', content_type, type(content_type))
    sub_comments = Comment.objects.filter(
        content_type=content_type, top_comment_id=obj.id).order_by('created_time')

    return sub_comments


@register.simple_tag
def get_comment_number(obj):
    # comment_numbers = 0
    # for comment in get_top_comments(obj):
    #     comment_numbers = comment_numbers + len(get_subcomments(comment)) + 1
    comment_numbers = Comment.objects.filter(root_object_id=obj.pk).count()
    return comment_numbers


@register.simple_tag
def get_comment_user_number(obj):
    comments = Comment.objects.filter(
        root_object_id=obj.pk)

    user_set = set()
    for comment in comments:
        user_set.add(comment.user)

    return len(user_set)


@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    commentForm = CommentForm(initial={
        'content_type': content_type.model,
        'object_id': obj.pk,
        'reply_comment_id': 0})
    return commentForm


@register.simple_tag
def get_reply_username(obj):
    reply = Comment.objects.get(id=obj.object_id)
    return reply.user.username
