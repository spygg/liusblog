from django.shortcuts import render, get_object_or_404
from django.http import  HttpResponse
from .models import Blog

# Create your views here.

def home(request):
    content = {}
    content['article_list'] = Blog.objects.all()
    return render(request, 'index.html', content)


def article_detail(request, id):
    print('get %d' % id)
    content = {}
    content['article'] = get_object_or_404(Blog, pk=id)
    print(content['article'].title)
    return render(request, 'article_detail.html', content)