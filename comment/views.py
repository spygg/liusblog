# from django.shortcuts import render, redirect
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
from comment.forms import CommentForm
from .models import Comment
# from django.urls import reverse
from django.http import JsonResponse
from comment.templatetags.comment_tag import get_comment_number, get_comment_user_number
from django.contrib.contenttypes.models import ContentType


def comment(request):
    # refer = request.META.get('HTTP_REFERER', reverse('home'))
    commentForm = CommentForm(request.POST, user=request.user)

    data = {}
    if commentForm.is_valid():
        comm = Comment()
        comm.user = commentForm.cleaned_data['user']
        comm.content = commentForm.cleaned_data['content']

        # 获取对象
        comm.content_object = commentForm.cleaned_data['content_object']
        comm.top_comment_id = commentForm.cleaned_data['top_comment_id']
        comm.root_object_id = commentForm.cleaned_data['object_id']
        comm.save()

        data['status'] = 'SUCCESS'
        data['username'] = comm.user.username
        data['created_time'] = comm.created_time.strftime(
            '%Y-%m-%d, %H:%M:%S')
        data['content'] = comm.content
        data['top_comment_id'] = comm.top_comment_id
        data['pk'] = comm.pk
        try:
            data['reply_username'] = Comment.objects.get(
                id=comm.object_id).user.username
        except:
            data['reply_username'] = ''

        # 获取评论文章
        content_type = commentForm.cleaned_data['content_type']
        object_id = commentForm.cleaned_data['object_id']
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk=object_id)

        data['comment_user_number'] = get_comment_user_number(model_obj)
        data['comment_number'] = get_comment_number(model_obj)
    else:
        data['status'] = 'ERROR'
        data['message'] = list(commentForm.errors.values())[0]
    return JsonResponse(data)
