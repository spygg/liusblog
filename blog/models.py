from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length = 200)
    content = models.TextField(null = True, blank = True)

    def __str__(self):
        return self.title
    
    def __unicode__(self):
        return self.title

