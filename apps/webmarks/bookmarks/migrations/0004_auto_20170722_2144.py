# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-22 18:44
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webmarks_bookmarks', '0003_auto_20170722_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='webmarks_bookmarks.Folder'),
        ),
    ]
