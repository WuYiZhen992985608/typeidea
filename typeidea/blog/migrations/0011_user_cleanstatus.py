# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-08-30 11:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20200830_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cleanStatus',
            field=models.BooleanField(default=True, verbose_name='注销'),
        ),
    ]