# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-08 06:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ttsx_app', '0004_cartinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetailInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='价格')),
                ('count', models.IntegerField(verbose_name='数量')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttsx_app.GoodsInfo', verbose_name='订单商品')),
            ],
            options={
                'verbose_name': '订单详情',
                'verbose_name_plural': '订单详情',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('oid', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='订单号')),
                ('odate', models.DateTimeField(auto_now_add=True, verbose_name='订单日期')),
                ('oIsPay', models.BooleanField(default=False, verbose_name='支付方式')),
                ('ototal', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='订单总价')),
                ('oaddress', models.CharField(max_length=150, verbose_name='订单地址')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '订单信息',
                'verbose_name_plural': '订单信息',
            },
        ),
        migrations.AddField(
            model_name='orderdetailinfo',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttsx_app.OrderInfo', verbose_name='订单信息'),
        ),
    ]