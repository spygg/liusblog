from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import BlogType, Blog, Bulletin
# from .models import ReadNumber
from django.db.models import Count
# from django.db.models import Q
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .forms import LoginForm, RegisterForm, ResetPassWdForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
import re
# from urllib.request import unquote
import urllib.parse
# from comment.models import Comment
# from comment.forms import CommentForm
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
import random
import string

# Create your views here.


class SendMail(object):
    """docstring for SendMail"""

    def __init__(self, arg):
        super(SendMail, self).__init__()
        self.arg = arg

    def send_email(self):
        send_mail(
            'Subject here',
            'Here is the message.',
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
        )


def home(request):
    return article_list(request)


def article_list(request):
    context = {}

    page_id = request.GET.get('page_id', '1')
    # print(page_id)
    blog_type = request.GET.get('blog_type', '')
    year = request.GET.get('year', '')
    month = request.GET.get('month', '')

    # 默认情况下不会出现同时筛选时间和类型的
    if year and month:
        blogs_all = Blog.objects.filter(
            created_time__year=year, created_time__month=month)
    elif blog_type:
        if blog_type == 'all':
            blogs_all = Blog.objects.all()
        else:
            blogs_all = Blog.objects.filter(blog_type__type_name=blog_type)
    else:
        blogs_all = Blog.objects.all()

    blogs = Paginator(blogs_all, 5)
    # 使用get_age()函数可以自动过滤超限页码
    context['article_list'] = blogs.get_page(page_id)
    print(dir(context['article_list'].object_list))
    context['page_nums'] = blogs.page_range
    context['current_page'] = page_id
    # context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_types'] = BlogType.objects.filter(parent_id=0)
    context['blog_type'] = blog_type
    context['year'] = year
    context['month'] = month
    context['article_num'] = blogs_all.count()
    # .annotate(blog_count = Count('last_modify_time'))
    blog_dates_temp = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates = {}
    for blog_date in blog_dates_temp:
        blog_dates[blog_date] = Blog.objects.filter(
            created_time__year=blog_date.year,
            created_time__month=blog_date.month).\
            count()

    # 为了父节点高亮
    try:
        context['parent_name'] = BlogType.objects.get(
            type_name=blog_type).get_parent_name()
    except:
        pass

    for blog_type in context['blog_types']:
        context[blog_type.type_name +
                '_first'] = Blog.objects.filter(blog_type__type_name=blog_type).first()

    context['blog_dates'] = blog_dates
    context['bulletins'] = Bulletin.objects.all()

    return render(request, 'article_list.html', context)


def article_detail(request):
    context = {}
    blog_type = ''
    # year = ''
    # month = ''

    pre_url = request.META.get('HTTP_REFERER', '')
    id = request.GET.get('id', '0')

    blog = get_object_or_404(Blog, pk=id)

    # 根据上一次访问的类型确定下次要访问的页面类型
    pattern = re.compile(r"blog_type=(?P<blog_type>.+)")
    result = re.search(pattern, pre_url)
    if result:
        blog_type = result.group('blog_type')

    # pattern = re.compile(r"year=(?P<year>[0-9][0-9][0-9][0-9])");
    # result = re.search(pattern, pre_url)
    # if result:
    #     year = result.group('year')

    # pattern = re.compile(r"month=(?P<month>[0-9][0-9])");
    # result = re.search(pattern, pre_url)
    # if result:
    #     month = result.group('month')

    # 阅读计数
    is_read = request.COOKIES.get('aritcle_%s' % id)
    if not is_read == 'YES':
        blog.plus_read_number()

    context['url'] = request.get_raw_uri()

    # 在上一篇和下一篇文章时,这里区分是按时间还是按博客类型进行区分
    if blog_type:
        blog_prev = Blog.objects.filter(
            blog_type__type_name=blog_type, created_time__gt=blog.created_time).last()
        blog_next = Blog.objects.filter(
            blog_type__type_name=blog_type, created_time__lt=blog.created_time).first()
    else:
        blog_prev = Blog.objects.filter(
            created_time__gt=blog.created_time).last()
        blog_next = Blog.objects.filter(
            created_time__lt=blog.created_time).first()

    context['article'] = blog
    context['blog_type'] = blog_type
    context['blog_types'] = BlogType.objects.filter(parent_id=0)
    context['prev_article'] = blog_prev
    context['next_article'] = blog_next

    response = render(request, 'article_detail.html', context)
    response.set_cookie('aritcle_%s' % id, 'YES', max_age=3600)
    return response


def about_me(request):
    context = {}
    context['blog_type'] = 'about'
    context['blog_types'] = BlogType.objects.filter(parent_id=0)
    return render(request, 'about_me.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def thridpaty_login(request, type):
    print(type)
    return HttpResponseRedirect('/')


def login(request):
    #url_from = request.META.get('HTTP_REFERER', reverse('home'))
    pre_url = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            user = loginForm.cleaned_data['user']
            auth.login(request, user)
            return redirect(pre_url)
    else:
        loginForm = LoginForm()
    context = {}
    context['loginForm'] = loginForm
    context['blog_types'] = BlogType.objects.filter(parent_id=0)

    return render(request, 'login.html', context)


def register(request):
    if request.method == 'POST':
        registerForm = RegisterForm(request.POST, request=request)

        if registerForm.is_valid():
            username = registerForm.cleaned_data['username']
            password = registerForm.cleaned_data['password']
            email = registerForm.cleaned_data['email']

            user = User.objects.create_user(username, email, password)
            user.save()

            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            pre_url = request.GET.get('from', reverse('home'))
            return HttpResponseRedirect(pre_url)

    else:
        registerForm = RegisterForm()

    context = {}
    context['registerForm'] = registerForm
    context['blog_types'] = BlogType.objects.filter(parent_id=0)
    return render(request, 'register.html', context)


def userinfo(request):
    context = {}
    context['blog_types'] = BlogType.objects.filter(parent_id=0)
    username = request.GET.get('username', '')

    if username:
        user = User.objects.get(username=username)
        if user.is_active:
            context['userInfo'] = user

    return render(request, 'userinfo.html', context)


def bindemail(request):
    context = {}
    context['blog_types'] = BlogType.objects.filter(parent_id=0)

    return render(request, 'userinfo.html', context)


def verify(request):
    data = {}
    code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
#    print(code)
    email = request.GET.get('email', '')
    request.session['verify_code'] = code

    data['status'] = "ERROR"
    if email.find('@') != -1:
        ok = send_mail(
            subject='注册验证,不要回复本邮件!',
            message='',
            html_message='<div>验证码: <strong>%s</strong></div><div>网站地址: <a  target="_blank" href="http://spygg.pythonanywhere.com">http://spygg.pythonanywhere.com</a></div>' % (
                code, ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email, ],
            fail_silently=False,
        )
        if ok:
            data['status'] = 'SUCCESS'

    return JsonResponse(data)


def resetpasswd(request):
    info = ''
    if request.method == 'POST':
        resetPassWdForm = ResetPassWdForm(request.POST)

        if resetPassWdForm.is_valid():
            email = resetPassWdForm.cleaned_data['email']

            send_mail(
                subject='重设密码,不要回复本邮件!',
                message='',
                html_message='<div><h1>打开网址重设密码</h1><a href="http://spygg.pythonanywhere.com/data/?active=1034">重设密码</a></div>',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email, ],
                fail_silently=False,
            )

            info = '邮件发送成功,请登录邮箱!'
            # return HttpResponseRedirect('/')

    else:
        resetPassWdForm = ResetPassWdForm()
    context = {}
    context['resetPassWdForm'] = resetPassWdForm
    context['info'] = info
    context['blog_types'] = BlogType.objects.filter(parent_id=0)
    return render(request, 'resetpasswd.html', context)
