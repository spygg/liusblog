from django.shortcuts import render, redirect
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from comment.forms import CommentForm
from .models import Comment
from django.urls import reverse

def comment(request):
    refer = request.META.get('HTTP_REFERER', reverse('home'))
    
    user = request.user
    text = request.POST.get('text', '')
    content_type = request.POST.get('content_type', '')
    object_id = int(request.POST.get('object_id', ''))

    comm = Comment()
    comm.user = user
    comm.content = text
    
    #获取对象
    model_class = ContentType.objects.get(model = content_type).model_class()
    model_obj = model_class.objects.get(pk = object_id)
    comm.content_object = model_obj
    

    comm.save()

    return redirect(refer)
    # if request.method == 'POST':
    #     commentForm = CommentForm(request.POST)
    #     if commentForm.is_valid():
    #         user = commentForm.cleaned_data['user']
            
    #         comm = Comment()
    #         comm.save()

    #         return redirect('/')
    # else:
    #     commentForm = CommentForm()
    
    # context = {}
    # context['commentForm'] = commentForm
    # return render(request, 'login.html', context)

    # comm = Comment(request.POST)


