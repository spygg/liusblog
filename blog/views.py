from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import BlogType, Blog
from django.db.models import Count
from django.db.models import Q
import re

# Create your views here.



def home(request):
    return article_list(request)

def article_list(request):
    context = {}
    #根据输入参数获取文章列表
    # if page_type == "type_index":
    #     blogs_all = Blog.objects.all()
    # elif page_type == "type_page":
    #     if type_name == 'all':
    #         blogs_all = Blog.objects.filter();
    #     else:
    #         blogs_all = Blog.objects.filter(blog_type__type_name = type_name);

    # elif page_type == "type_date":
    #     if year and month:
    #         blogs_all = Blog.objects.filter(created_time__year = year, created_time__month = month);
    #     else:
    #         blogs_all = Blog.objects.filter();
    # else:
    #     raise Exception('Server Error!')
    page_id = request.GET.get('page_id', '1')
    blog_type = request.GET.get('blog_type', '')
    year = request.GET.get('year', '')
    month = request.GET.get('month', '')

    print(blog_type, year, month, page_id)

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
    id = request.GET.get('id', '0')
    print('idis====', id)
    blog = get_object_or_404(Blog, pk=id)
    context['article'] = blog
    #blog_type = request.GET.get('blog_type', '')
    
    pre_url = request.META.get('HTTP_REFERER', '')
    blog_type = ''
    year = ''
    month = ''

    print(pre_url)
    pattern = re.compile(r"blog_type=(?P<blog_type>\w+)");
    result = re.search(pattern, pre_url)
    if result:
        blog_type = result.group('blog_type')
    else:
        print('re', result)

    pattern = re.compile(r"year=(?P<year>.+?)&");
    result = re.search(pattern, pre_url)
    if result:
        year = result.group('year')
        print(year)

    pattern = re.compile(r"month=(?P<month>[0-9][0-9])");
    result = re.search(pattern, pre_url)
    if result:
        month = result.group('month')
        print(month)


    context['url'] = request.get_raw_uri()

    print('####BT', blog_type)

    if blog_type:
        blog_prev = Blog.objects.filter(blog_type__type_name = blog_type, created_time__gt = blog.created_time).last()  
        blog_next = Blog.objects.filter(blog_type__type_name = blog_type, created_time__lt = blog.created_time).first()
    else:
        blog_prev = Blog.objects.filter(created_time__gt = blog.created_time).last()
        blog_next = Blog.objects.filter(created_time__lt = blog.created_time).first()

    print('PRE####', blog_next)

    context['blog_type'] = blog_type
    context['blog_types'] = BlogType.objects.all()
    context['prev_article'] = blog_prev
    context['next_article'] = blog_next
    return render(request, 'article_detail.html', context) 


def about_me(request):
    context = {}
    context['blog_type'] = 'about'
    context['blog_types'] = BlogType.objects.all()
    return render(request, 'about_me.html', context)