# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-15 10:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20170715_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='ip',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]
