# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.core.paginator import Paginator
from django.core import serializers
from django.contrib.auth.hashers import make_password, check_password
from blog import models
from forms import RegisterForm
from forms import LoginForm
from utils import EmailSender
from utils import VerificationCode
from utils import AuthIt
from utils import check_cookie
import json
import random
import redis
import time


validate_dict = {}


# 博客首页
def blog_index(request):

    index_page = 1
    articles = models.Article.objects.all()[:5]
    paginator = Paginator(articles, 5)
    if request.method == 'GET':
        user_info = request.session.get(request.COOKIES.get('login_cookie', None), None)
        if user_info:
            user_info = json.loads(user_info)
            return render(request, 'blog_index.html', {'user_info': user_info,
                                                       'articles': paginator.page(index_page).object_list})
        else:
            return render(request, 'blog_index.html', {'articles': paginator.page(index_page).object_list})
    else:
        if request.is_ajax():
            page = float(request.POST.get('page', None))
            articles = models.Article.objects.all()[page * 5:page * 5 + 5]
            paginator = Paginator(articles, 5)
            if paginator.count != 0:

                page_data = paginator.page(1).object_list
                return render(request, 'blog_contain.html', {'articles': page_data})
            else:
                return HttpResponse('max')


# 展示用户博客
@check_cookie
def user_article(request, *args):

    if request.method == 'GET':
        user_info = json.loads(request.session.get(request.COOKIES.get('login_cookie', None), None))
        articles = models.Article.objects.filter(author=user_info.get('id'))
        return render(request, 'user_articles.html', {'user_info': user_info,
                                                      'articles': articles})


# 展示博客全文
@check_cookie
def article_detail(request, article_id):
    if request.method == 'GET':
        article = models.Article.objects.filter(id=article_id).first()
        user_info = json.loads(request.session.get(request.COOKIES.get('login_cookie', None), None))
        return render(request, 'article_detail.html', {'user_info': user_info,
                                                       'article': article})


# 编辑博客页面
@check_cookie
def article_edit(request):
    # 创建redis连接池
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True, db=0)
    # 创建链接
    draft = redis.Redis(connection_pool=pool)
    # 创建redis缓存草稿的key
    user_info = json.loads(request.session.get(request.COOKIES.get('login_cookie', None), None))
    key = user_info['nick_name']

    if request.method == 'GET':
        if request.is_ajax():
            title = draft.hget(key, 'title')
            content = draft.hget(key, 'content')
            data = {'title': title,
                    'content': content}
            data = json.dumps(data)
            return HttpResponse(data)
        else:
            return render(request, 'article_edit.html', {'user_info': user_info})
    else:
        # 文章草稿存入redis中
        if request.POST.get('content', False):
            title = request.POST.get('title')
            content = request.POST.get('content')
            draft.hset(key, 'title', title)
            draft.hset(key, 'content', content)
            draft.expire(key, 1800)

            return HttpResponse('保存完毕')
        # 当用户发布文章后，将文章从redis中取出存入mysql
        elif request.POST.get('pop', False):
            title = draft.hget(key, 'title')
            content = draft.hget(key, 'content')
            user = models.UserProfile.objects.filter(nick_name=user_info['nick_name']).first()
            summary = content[:300] + "..."
            article_content = models.ArticleContent.objects.create(content=content)
            article_content.save()
            article = models.Article.objects.create(title=title,
                                                    content=summary,
                                                    author=user,
                                                    whole=article_content)

            article.save()
            print 'okok'
            draft.hdel(key, 'pop', 'title', 'content')

            return HttpResponse('发布成功')


# 注册博客
def blog_register(request):
    # GET访问返回空注册表单
    if request.method == 'GET':
        register_form = RegisterForm()
        return render(request, 'blog_register.html', {'register_form': register_form})
    # POST访问
    else:
        # 初始化邮件发送
        email_sender = EmailSender()
        # 如果以AJAX访问则发送验证码
        if request.POST.get('ajax_email'):
            email = request.POST.get('ajax_email')
            if models.UserProfile.objects.filter(email=email):
                return HttpResponse('该邮箱已注册，您可以直接登陆')
            else:
                email_sender.to_email = [email]
                email_sender.subject = '欢迎注册lightBlog'
                email_sender.validate_number = email_sender.validate_create()
                # 将验证码信息放入字典便于验证
                request.session[str(email)+' register'] = email_sender.validate_number
                email_sender.msg = '欢迎注册lightBlog，您的验证码为: ' + email_sender.validate_number
                try:
                    email_sender.send()
                    return HttpResponse('请登陆邮箱查看验证邮件')
                except Exception:
                    return HttpResponse('邮箱格式错误!')
        # 如果提交表单，则进行注册验证
        else:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                user_info = register_form.clean()
                if user_info.get('password') == user_info.get('password2'):
                    if request.POST.get('validate') == request.session[str(user_info.get('email')+' register')]:
                        default_avatar_number = random.randint(1, 14)
                        default_role = models.Role.objects.filter(role_name='customer').first()
                        user = models.UserProfile.objects.create(email=user_info.get('email'),
                                                                 password=make_password(user_info.get('password')),
                                                                 nick_name=user_info.get('email'),
                                                                 avatar='/static/img/avatar/user_default_avatar' +
                                                                        str(default_avatar_number) + '.jpg',
                                                                 role=default_role)
                        user.save()
        return redirect('/blog')


# 用户登陆函数
def blog_login(request):
    # 如果是get请求，则返回登陆表单
    if request.method == 'GET':
        login_form = LoginForm()
        return render(request, 'blog_login.html')
    # 如果是post请求，则有验证码请求和登陆请求两种情况
    else:
        # 如果是ajax请求，则返回图形验证码
        if request.POST.get('ajax_email'):
            email = request.POST.get('ajax_email')
            if models.UserProfile.objects.filter(email=email):
                # 调用验证码生成类 img_code为图片URI地址，validate为验证码字符串
                validate_create = VerificationCode()
                img_code, validate = validate_create.validate_create()
                # 将验证码字符串放入session中便于验证
                request.session[email+' login'] = validate
                return HttpResponse(img_code)
            else:
                return HttpResponse('该邮箱未注册，请先前往注册')
        # 如果是表单提交请求，则进行登陆验证
        else:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                login_info = login_form.clean()
                email = login_info.get('email')
                password = login_info.get('password')
                validate = login_info.get('validate')
                # 验证码比对
                if validate == request.session.get(email+' login'):
                    user_profile = models.UserProfile.objects.filter(email=email)
                    # 密码比对
                    if check_password(password, user_profile[0].password):
                        # 调用COOKIES生成工具，设置登陆状态cookie
                        login_cookie = AuthIt().login_cookie()
                        rep = redirect('/blog')
                        rep.set_cookie('login_cookie', login_cookie, max_age=36000)
                        # 将用户信息放入session中
                        request.session[login_cookie] = models.UserProfile.objects.get(email=email).get_info()
                        return rep


def blog_logout(request):

    login_session = request.COOKIES.get('login_cookie', None)
    print request.session[login_session]
    del request.session[login_session]

    return redirect('/blog/login')


def test(request):

    return render(request, 'Blog Template for Bootstrap.html')
