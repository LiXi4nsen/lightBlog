# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-20 06:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('\u5973', 0), ('\u7537', 1)], max_length=5, null=True),
        ),
    ]