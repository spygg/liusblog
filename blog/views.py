from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import BlogType, ReadNumber, Blog
from django.db.models import Count
from django.db.models import Q
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
import re
from urllib.request import unquote
import urllib.parse
from .forms import LoginForm

# Create your views here.

def google(request, keyworkd):
    #response = HttpResponseRedirect('http://www.bing.com/search?q=%s' % keyworkd)

    url = 'http://cn.bing.com/search?q='

    #使用网址转码
    key = urllib.parse.quote(keyworkd)
    url = url + key
    url = r'https://cn.bing.com/search?q=love&go=Submit&qs=n&form=QBLH&sp=-1&pq=djiango+redirect&sc=0-16&sk=&cvid=F80B2756E77344B4ABE42413E60AD7A4'
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf-8')

    html = html.replace('href="/', 'href="https://cn.bing.com/')
    html = html.replace('src="/', 'src="https://cn.bing.com/')
    with open("google.html", "w") as f:
        f.write(html)
    response = HttpResponse(html)
    #print(response)
    return response

def home(request):
    return article_list(request)

def article_list(request):
    context = {}

    page_id = request.GET.get('page_id', '1')
    blog_type = request.GET.get('blog_type', '')
    year = request.GET.get('year', '')
    month = request.GET.get('month', '')

    #默认情况下不会出现同时筛选时间和类型的
    if year and month:
        blogs_all = Blog.objects.filter(created_time__year = year, created_time__month = month);
    elif blog_type:
        if blog_type == 'all':
            blogs_all = Blog.objects.filter();
        else:
            blogs_all = Blog.objects.filter(blog_type__type_name = blog_type);
    else:
        blogs_all = Blog.objects.all()

    blogs = Paginator(blogs_all, 5);
    #使用get_age()函数可以自动过滤超限页码
    context['article_list'] = blogs.get_page(page_id)
    context['page_nums'] = blogs.page_range
    context['current_page'] = page_id
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog')) 
    context['blog_type'] = blog_type
    context['year'] = year
    context['month'] = month
    context['article_num'] = blogs_all.count()
    # .annotate(blog_count = Count('last_modify_time'))
    blog_dates_temp = Blog.objects.dates('created_time', 'month', order = 'DESC')    
    blog_dates = {}
    for blog_date in blog_dates_temp:
        blog_dates[blog_date] = Blog.objects.filter(\
                                    created_time__year = blog_date.year,\
                                    created_time__month = blog_date.month).\
                                    count()
    context['blog_dates'] = blog_dates

    return render(request, 'article_list.html', context)


def article_detail(request):
    context = {}
    blog_type = ''
    year = ''
    month = ''

    pre_url = unquote(request.META.get('HTTP_REFERER', ''))
    id = request.GET.get('id', '0')
    blog = get_object_or_404(Blog, pk=id)

    

    #根据上一次访问的类型确定下次要访问的页面类型
    pattern = re.compile(r"blog_type=(?P<blog_type>.+)");
    result = re.search(pattern, pre_url)
    if result:
        blog_type = result.group('blog_type')

    pattern = re.compile(r"year=(?P<year>[0-9][0-9][0-9][0-9])");
    result = re.search(pattern, pre_url)
    if result:
        year = result.group('year')

    pattern = re.compile(r"month=(?P<month>[0-9][0-9])");
    result = re.search(pattern, pre_url)
    if result:
        month = result.group('month')
   
    #阅读计数
    is_read = request.COOKIES.get('aritcle_%s' % id)    
    if not is_read == 'YES':
        blog.plus_read_number();

    context['url'] = request.get_raw_uri()
    if blog_type:
        blog_prev = Blog.objects.filter(blog_type__type_name = blog_type, created_time__gt = blog.created_time).last()  
        blog_next = Blog.objects.filter(blog_type__type_name = blog_type, created_time__lt = blog.created_time).first()
    else:
        blog_prev = Blog.objects.filter(created_time__gt = blog.created_time).last()
        blog_next = Blog.objects.filter(created_time__lt = blog.created_time).first()

    context['article'] = blog
    context['blog_type'] = blog_type
    context['blog_types'] = BlogType.objects.all()
    context['prev_article'] = blog_prev
    context['next_article'] = blog_next


    response = render(request, 'article_detail.html', context) 
    response.set_cookie('aritcle_%s' % id, 'YES', max_age = 3600)
    return response


def about_me(request):
    context = {}
    context['blog_type'] = 'about'
    context['blog_types'] = BlogType.objects.all()
    return render(request, 'about_me.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def login(request):
    if request.method == 'POST':
        
        loginForm = LoginForm(request.POST)

        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            # username = request.POST['username']
            # password = request.POST['password']
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
            #     # Redirect to a success page.
            # else:
            #     # Return an 'invalid login' error message.
            
            return HttpResponseRedirect('/')
    else:
        loginForm = LoginForm()
        return render(request, 'login.html', {'loginForm': loginForm})