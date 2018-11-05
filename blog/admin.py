# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import UserProfile, Article, Comment, Role, Permission, ArticleContent

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(ArticleContent)
