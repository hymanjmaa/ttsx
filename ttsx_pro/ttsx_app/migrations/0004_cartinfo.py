# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-06 13:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ttsx_app', '0003_auto_20170803_2056'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='数量')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttsx_app.GoodsInfo', verbose_name='商品信息')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '购物车信息',
                'verbose_name_plural': '购物车信息',
            },
        ),
    ]
