# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from random import randint
from blogProject import settings
from blog import models
from forms import RegisterForm


validate_dict = {}


# 邮件发送
class EmailSender(object):
    # 初始化邮件参数
    def __init__(self, subject=None, msg=None, to_email=None, from_email=settings.EMAIL_HOST_USER, fail_silently=False):
        self.subject = subject
        self.msg = msg
        self.to_email = to_email
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.validate_number = ""

    # 生成简单邮件验证码
    def validate_create(self):
        for n in range(0, 6):
            self.validate_number += str(randint(0, 10))
        return self.validate_number

    # 发送邮件
    def send(self):
        send_mail(self.subject, self.msg, self.from_email, self.to_email, self.fail_silently)


# 博客首页
def blog_index(request):

    if request.method == 'GET':
        return render(request, 'blog_index.html')


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
                validate_dict[str(email)] = email_sender.validate_number
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
                    if request.POST.get('validate') == validate_dict[user_info.get('email')]:
                        user = models.UserProfile.objects.create(email=user_info.get('email'),
                                                                 password=make_password(user_info.get('password')),
                                                                 nick_name=user_info.get('email'))
                        user.save()
        return redirect('/blog')


def test(request):

    return render(request, 'Blog Template for Bootstrap.html')
