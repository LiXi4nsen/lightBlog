# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

'''数据库模型  Article(文章表)'''


class Article(models.Model):

    title = models.CharField(max_length=32, verbose_name='文章标题')
    content = models.TextField(verbose_name='文章内容')
    create_time = models.DateTimeField(auto_created=True, verbose_name='创建时间')
    author = models.ForeignKey('UserProfile')

    class META:
        verbose_name = '文章'


class UserProfile(models.Model):

    email = models.EmailField()
    password = models.CharField(max_length=64)
    nick_name = models.CharField(max_length=64)
    gender_choice = (('女', 0),
                     ('男', 1))
    gender = models.CharField(max_length=5, choices=gender_choice, null=True, blank=True)

    class META:
        verbose_name = '用户信息'


class Comment(models.Model):

    content = models.TextField(verbose_name='评论内容')
    create_time = models.DateTimeField(auto_created=True, verbose_name='创建时间')
    author = models.ForeignKey('UserProfile')

    verbose_name = '评论'


