# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.mail import send_mail
from django.shortcuts import redirect
from random import randint
from random import choice
from base64 import b64encode
from blogProject import settings
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from os import remove


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


# 图形验证码生成工具
class VerificationCode(object):
    # 初始化PIL参数
    def __init__(self):
        self.img = Image.new(mode='RGB', size=(120, 44), color=(255, 255, 255))
        self.draw = ImageDraw.Draw(self.img, mode='RGB')
        self.font = ImageFont.truetype('C:\\Windows\\Fonts\\Cambria.ttc', 28)

    # 写入验证码，返回图形和验证码
    def validate_create(self):
        str_text = ''
        for i in range(5):
            char = choice([chr(randint(65, 90)), str(randint(0, 9))])
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
            str_text += char
            self.draw.text([i*24, 0], char, color, font=self.font)
        self.img.save(str_text + '.jpg')
        # 将图形以二进制流返回
        with open(str_text + '.jpg', 'rb') as f:
            img_code = 'data:image/jpg;base64,' + b64encode(f.read())
        # 获取到二进制流后，删除图片
        remove(str_text + '.jpg')
        return img_code, str_text


# 登陆状态验证工具
class AuthIt(object):
    # 初始化COOKIE和request
    def __init__(self, request=None):
        self.cookie = ''
        self.request = request

    # 创建登陆COOKIE
    def login_cookie(self):
        self.cookie = ''
        for i in range(20):
            char = choice([chr(randint(65, 90)), str(randint(0, 9))])
            self.cookie += char
        return self.cookie


def check_cookie(func):

    def inner(request, *args, **kwargs):
        if request.COOKIES.get('login_cookie', None) in request.session.keys():
            print func
            return func(request, *args, **kwargs)
        else:
            return redirect('/blog/login')
    return inner


