# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-07 17:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TokenStore',
            fields=[
                ('instance_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('github_token', models.CharField(blank=True, max_length=255)),
                ('slack_token', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'ordering': ('instance_id',),
            },
        ),
    ]
