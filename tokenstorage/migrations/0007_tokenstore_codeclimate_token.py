# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-17 22:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokenstorage', '0006_auto_20170316_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='tokenstore',
            name='codeclimate_token',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
