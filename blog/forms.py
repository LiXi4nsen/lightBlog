# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms


class RegisterForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(min_length=8, max_length=64)
    password2 = forms.CharField(min_length=8, max_length=64)


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(min_length=8, max_length=64)
    validate = forms.CharField(max_length=6)
