# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-22 09:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webmarks_bookmarks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='folders',
            field=models.ManyToManyField(blank=True, related_name='nodes', to='webmarks_bookmarks.Folder'),
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='bookmarks', to='webmarks_bookmarks.Tag'),
        ),
        migrations.AlterField(
            model_name='folder',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='webmarks_bookmarks.Folder'),
        ),
    ]
