from django.shortcuts import render
from django.http import HttpResponse
from .models import Article

def home(request):
    articles = Article.objects.all()
    return render(request, 'blog/index.html', {"articles" : articles})
    return HttpResponse("Hello")

def edit(request, id):
    if request.method == 'POST':

        title = request.POST.get("title")
        content = request.POST.get("content")
        if id == '0':
            Article.objects.create(title = title, content = content)

        else:
            article = Article.objects.get(id = id)
            article.title = title
            article.content = content
            article.save()

        articles = Article.objects.all()
        return render(request, 'blog/index.html', {"articles" : articles})
    else:
        article = []
        if id != '0':
            article = Article.objects.get(id = id)
        return render(request, 'blog/edit.html', {"article": article})


def delete(request, id):
    article = Article.objects.get(id = id)
    article.delete()
    articles = Article.objects.all()
    return render(request, "blog/index.html", {"articles": articles})


def detail(request, id):    
    article = Article.objects.get(id = id)
    return render(request, 'blog/detail.html', {"article" : article})
    return HttpResponse("Hello")
