from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from .models import Comment

# 回复分两种情况:
# 1.回复博客,直接设置object_id为"博客id"和content_type,root_id为0
# 2.回复评论也分两种情况:
# ①.回复顶级评论,设置root_id为被回复者的"评论id",object_id为被回复者的"评论ID"
# ②.回复非顶级评论,root_id设置为被回复者的根id(向上追溯),object_id为被回复者的"评论ID"


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput())
    object_id = forms.IntegerField(widget=forms.HiddenInput())
    content = forms.CharField(widget=CKEditorWidget(
        config_name='comment_ckeditor'), error_messages={'required': '评论内容不能为空'})

    reply_comment_id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'id': 'reply_comment_id'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')

        super(CommentForm, self).__init__(*args, **kwargs)

    # def clean_reply_comment_id(self):

    #     reply_comment_id = self.cleaned_data['reply_comment_id']
    #     if reply_comment_id:
    #         # 回复的是评论
    #         try:
    #             reply_obj = Comment.objects.get(id=reply_comment_id)
    #             if reply_obj.root_id:
    #                 # 存在则赋值为父对象②.回复非顶级评论
    #                 self.cleaned_data['root_id'] = reply_obj.root_id
    #             else:
    #                 # 不存在则说明回复的是顶级评论
    #                 self.cleaned_data['root_id'] = reply_comment_id

    #         except ObjectDoesNotExist:
    #             raise forms.ValidationError('评论对象不存在!')
    #     else:
    #         # 回复的是博客
    #         self.cleaned_data['root_id'] = 0

    #     print('####################################')
    #     print(reply_comment_id)
    #     return reply_comment_id

    def clean(self):
        # 用户登录验证
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录!')

        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id:
            # 回复的是评论
            try:
                reply_obj = Comment.objects.get(id=reply_comment_id)
                if reply_obj.root_id:
                    # 存在则赋值为父对象②.回复非顶级评论
                    self.cleaned_data['root_id'] = reply_obj.root_id
                else:
                    # 不存在则说明回复的是顶级评论
                    self.cleaned_data['root_id'] = reply_comment_id
            except ObjectDoesNotExist:
                raise forms.ValidationError('评论对象不存在!')
        else:
            # 回复的是博客
            self.cleaned_data['root_id'] = 0

        if not self.cleaned_data['reply_comment_id']:
            # 评论对象是博客
            content_type = self.cleaned_data['content_type']
            object_id = self.cleaned_data['object_id']
        else:
            # 评论对象是评论
            content_type = 'comment'
            object_id = self.cleaned_data['reply_comment_id']

        try:
            model_class = ContentType.objects.get(
                model=content_type).model_class()
            # print(model_class)
            model_obj = model_class.objects.get(pk=object_id)

            self.cleaned_data['content_object'] = model_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论的对象不存在!')

        return self.cleaned_data
