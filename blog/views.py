# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from forms import RegisterForm


# 博客首页视图
def blog_index(request):

    if request.method == 'GET':
        return render(request, 'blog_index.html')


def blog_register(request):

    if request.method == 'GET':
        register_form = RegisterForm()

        return render(request, 'blog_register.html', {'register_form': register_form})


def test(request):

    return render(request, 'Blog Template for Bootstrap.html')
