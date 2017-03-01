#coding:utf-8
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models

#******define your own fields here*******

#if we want to reduce the length of context, compress when save it into db, decompress it when read it from db,we should define a CompressedTextField
class CompressedTextField(models.TextField):
    """
    model Fields for storing text in a compressed format (bz2 by default)
    """

    def from_db_value(self, value, expression, connection, context):
        if not value:
            return value
        try:
            return value.decode('base64').decode('bz2').decode('utf-8')
        except Exception:
            return value

    def to_python(self, value):
        if not value:
            return value
        try:
            return value.decode('base64').decode('bz2').decode('utf-8')
        except Exception:
            return value

    def get_prep_value(self, value):
        if not value:
            return value
        try:
            value.decode('base64')
            return value
        except Exception:
            try:
                return value.encode('utf-8').encode('bz2').encode('base64')
            except Exception:
                return value



#if we want to save a list into table, and we can read it by List format,we should define a ListField
import ast

class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)  # use str(value) in Python 3

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

# Create your models here.
# **********test code**********
class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()

    def my_property(self):
        return self.first_name+' '+self.last_name
    my_property.short_description= "Full name of the person"

    full_name = property(my_property)

    def __unicode__(self):
        return u'%s %s' % (self.first_name,self.last_name)

class Author(models.Model):
    name = models.CharField(max_length=50)
    qq = models.CharField(max_length=10,default='null')
    addr = models.TextField(default='null')
    email = models.EmailField()

    def __unicode__(self):  # __str__ on Python 3
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=30)
    # labels = ListField(default='null')
    author = models.ForeignKey(Author,default='')
    content = models.TextField(default='Please input your words...')
    score = models.IntegerField(default=0)
    tags = models.ManyToManyField('Tag')

    def __unicode__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name
#
#

class Blog(models.Model):
    title = models.CharField(u'Title',max_length=256)
    content = models.TextField(u'Content')
    type = models.CharField(max_length=256,null=True)
    author = models.CharField(u'Writer',max_length=256,null = True)
    pub_date = models.DateTimeField(u'Publish_time',auto_now_add = True,editable = True)
    update_time = models.DateTimeField(u'Update_time',auto_now = True,null = True)

    def __unicode__(self):
        return u'[Title]%s, [Content]%s, [PubDate]%s' % (self.title,self.content,self.pub_date)

    class Meta:
        ordering = ['-pub_date']
#
# class Blog(models.Model):
#     name = models.CharField(max_length=100)
#     tagline = models.TextField()
#
#     def __unicode__(self):  # __str__ on Python 3
#         return self.name
# #
#
#
# class Entry(models.Model):
#     blog = models.ForeignKey(Blog)
#     headline = models.CharField(max_length=255)
#     body_text = models.TextField()
#     pub_date = models.DateField()
#     mod_date = models.DateField()
#     authors = models.ManyToManyField(Author)
#     n_comments = models.IntegerField()
#     n_pingbacks = models.IntegerField()
#     rating = models.IntegerField()
#
#     def __unicode__(self):  # __str__ on Python 3
#         return self.headline


#**********test code end**********

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    def __unicode__(self):
        return u'%s %s' % (self.name,self.website)

class Author2(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    # headshot = models.ImageField(upload_to='/tmp')

    def __unicode__(self):
        return u'%s %s' % (self.first_name,self.last_name)

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author2)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField(blank=True,null=True)

    def __unicode__(self):
        return self.title


