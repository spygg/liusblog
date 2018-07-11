from django.shortcuts import render, get_object_or_404
from django.http import  HttpResponse
from .models import Blog

# Create your views here.

def home(request):
    content = {}
    content['article_list'] = Blog.objects.all()
    return render(request, 'index.html', content)


def article_detail(request, id):
    content = {}
    
    blog = get_object_or_404(Blog, pk=id)
    content['article'] = blog
    content['prev_article'] = Blog.objects.filter(created_time__gt = blog.created_time).last()
    content['next_article'] = Blog.objects.filter(created_time__lt = blog.created_time).first()
    content['url'] = request.get_raw_uri()
    # print(dir(request.META))
    # print(request.META.values())
    # print(request.get_raw_uri())
    return render(request, 'article_detail.html', content)