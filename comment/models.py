from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add = True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "<Comment, %s>" % self.user

    class Meta:
        ordering = ['-created_time']