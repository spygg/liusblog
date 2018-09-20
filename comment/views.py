# from django.shortcuts import render, redirect
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
from comment.forms import CommentForm
from .models import Comment
# from django.urls import reverse
from django.http import JsonResponse


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
        # data['content_type'] = commentForm.cleaned_data['content_type']
        # data['user_num'] = 33
        # data['comment_num'] = 69
        # return redirect(refer)
    else:
        data['status'] = 'ERROR'
        data['message'] = list(commentForm.errors.values())[0]
    return JsonResponse(data)
