# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-29 08:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('webmarks_directory', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='user_cre',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='node_user_cre', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='node',
            name='user_upd',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='node_user_upd', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='node',
            name='folders',
            field=models.ManyToManyField(blank=True, related_name='nodes', to='webmarks_directory.Folder'),
        ),
        migrations.AddField(
            model_name='folder',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='webmarks_directory.Folder'),
        ),
    ]