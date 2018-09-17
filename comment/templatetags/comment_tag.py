from django import template
from ..models import Comment

register = template.Library()

@register.simple_tag
def get_comment_number(obj):
    return 'hah'

@register.simple_tag
def get_comment_user_number(obj):
    pass

@register.simple_tag
def get_comment_form(obj):
    pass

