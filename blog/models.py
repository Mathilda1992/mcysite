from __future__ import unicode_literals

from django.db import models

# Create your models here.
#2017-3-1

# coding:utf8


from django.db import models

# Create your models here.
class Catagory(models.Model):

    name = models.CharField('name',max_length=30)

    def __unicode__(self):
        return self.name



class Tag(models.Model):

    name = models.CharField('name',max_length=16)

    def __unicode__(self):
        return self.name



class Blog(models.Model):

    title = models.CharField('title',max_length=32)
    author = models.CharField('author',max_length=16)
    content = models.TextField('content')
    created = models.DateTimeField('issuetime',auto_now_add=True)
    catagory = models.ForeignKey(Catagory,verbose_name='catagory')
    tags = models.ManyToManyField(Tag,verbose_name='tags')

    def __unicode__(self):
        return self.title


class Comment(models.Model):

    blog = models.ForeignKey(Blog,verbose_name='blog')
    name = models.CharField('username',max_length=16)
    email = models.EmailField('email')
    content = models.CharField('content',max_length=240)
    created = models.DateTimeField('issuetime',auto_now_add=True)

    def __unicode__(self):
        return self.content