# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-22 04:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_auto_20200719_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, '正常'), (0, '删除')], default=1, verbose_name='状态'),
        ),
    ]
