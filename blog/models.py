# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import json

'''数据库模型  Article(文章表)'''


class ArticleContent(models.Model):

    content = models.TextField(verbose_name='文章全文')


class Article(models.Model):

    title = models.CharField(max_length=32, verbose_name='文章标题')
    content = models.TextField(verbose_name='文章简介', null=True, blank=True)
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间', null=True)
    author = models.ForeignKey('UserProfile')
    whole = models.ForeignKey('ArticleContent', null=True, blank=True)

    class META:
        verbose_name = '文章'

    def __unicode__(self):
        return self.title


class Permission(models.Model):

    permission_name = models.CharField(max_length=32, verbose_name='权限名')
    read_own_article = models.SmallIntegerField(verbose_name='阅读自己的文章')
    alter_own_article = models.SmallIntegerField(verbose_name='修改自己的文章')
    delete_own_article = models.SmallIntegerField(verbose_name='删除自己的文章')
    crate_article = models.SmallIntegerField(verbose_name='编写文章')
    read_all_article = models.SmallIntegerField(verbose_name='阅读全部文章')
    alter_all_article = models.SmallIntegerField(verbose_name='修改全部文章')
    delete_all_article = models.SmallIntegerField(verbose_name='删除全部文章')
    create_comment = models.SmallIntegerField(verbose_name='创建评论')
    delete_own_comment = models.SmallIntegerField(verbose_name='删除自己编写的评论')
    delete_other_article = models.SmallIntegerField(verbose_name='删除自己文章下的评论')
    delete_all_comment = models.SmallIntegerField(verbose_name='删除全部评论')

    def __unicode__(self):
        return self.permission_name

    class META:
        verbose_name = '权限表'


class Role(models.Model):

    role_name = models.CharField(max_length=32, verbose_name='角色名')
    permission = models.ForeignKey('Permission')

    def __unicode__(self):
        return self.role_name

    class META:
        verbose_name = '角色表'


class UserProfile(models.Model):

    email = models.EmailField()
    password = models.CharField(max_length=64)
    nick_name = models.CharField(max_length=64)
    gender_choice = (('女', 0),
                     ('男', 1))
    gender = models.CharField(max_length=5, choices=gender_choice, null=True, blank=True)
    avatar = models.CharField(max_length=64, default='/static/img/avatar/user_default_avatar1.jpg')
    role = models.ForeignKey('Role')

    def __unicode__(self):
        return unicode(self.email)

    def get_info(self):
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields] if attr != 'role']))


class Comment(models.Model):

    content = models.TextField(verbose_name='评论内容')
    create_time = models.DateTimeField(auto_created=True, verbose_name='创建时间')
    author = models.ForeignKey('UserProfile')

    class META:
        verbose_name = '评论'


