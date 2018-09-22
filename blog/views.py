# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from blog import models
from forms import RegisterForm
from forms import LoginForm
from utils import EmailSender
from utils import VerificationCode
from utils import AuthIt
import json


validate_dict = {}


# 博客首页
def blog_index(request):

    if request.method == 'GET':
        user_info = request.session.get(request.COOKIES.get('login_cookie', None), None)
        articles = models.Article.objects.all()
        if user_info:
            user_info = json.loads(user_info)
            return render(request, 'blog_index.html', {'user_info': user_info,
                                                       'articles': articles})
        else:
            return render(request, 'blog_index.html', {'user_info': user_info,
                                                       'articles': articles})



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
                        user = models.UserProfile.objects.create(email=user_info.get('email'),
                                                                 password=make_password(user_info.get('password')),
                                                                 nick_name=user_info.get('email'))
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
                        rep.set_cookie('login_cookie', login_cookie, max_age=3600)
                        # 将用户信息放入session中
                        request.session[login_cookie] = models.UserProfile.objects.get(email=email).to_json()
                        return rep






def test(request):

    return render(request, 'Blog Template for Bootstrap.html')
