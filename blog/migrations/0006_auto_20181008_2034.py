# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-08 12:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20181008_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='create_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
    ]
