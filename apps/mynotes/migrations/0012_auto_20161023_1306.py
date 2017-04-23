# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-23 10:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mynotes', '0011_auto_20161022_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalnote',
            name='tags',
            field=models.CharField(default=None, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='historicalnote',
            name='type',
            field=models.CharField(choices=[('NOTE', 'Note'), ('TODO', 'Todo'), ('MAIL', 'Mail')], default='NOTE', max_length=10),
        ),
        migrations.RemoveField(
            model_name='note',
            name='tags',
        ),
        migrations.AddField(
            model_name='note',
            name='tags',
            field=models.CharField(default=None, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='type',
            field=models.CharField(choices=[('NOTE', 'Note'), ('TODO', 'Todo'), ('MAIL', 'Mail')], default='NOTE', max_length=10),
        ),
    ]