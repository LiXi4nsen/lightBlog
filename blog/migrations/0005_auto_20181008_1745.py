# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-08 09:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_userprofile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='create_time',
            field=models.DateTimeField(auto_created=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.URLField(default='/static/img/avatar/user_default_avatar1.jpg'),
        ),
    ]
