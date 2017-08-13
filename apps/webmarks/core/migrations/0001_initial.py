# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-13 18:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_dt', models.DateTimeField(auto_now=True)),
                ('created_dt', models.DateTimeField(auto_now_add=True)),
                ('kind', models.CharField(choices=[('NOTE', 'Note'), ('TODO', 'Todo'), ('MAIL', 'Mail'), ('LINK', 'Link'), ('FLDR', 'Folder')], default='NOTE', max_length=10)),
                ('indexed_dt', models.DateTimeField(null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('public', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('node_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='webmarks_core.Node')),
                ('name', models.CharField(max_length=256)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='folderchildren', to='webmarks_core.Folder')),
            ],
            options={
                'abstract': False,
            },
            bases=('webmarks_core.node', models.Model),
        ),
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
            field=models.ManyToManyField(blank=True, related_name='nodes', to='webmarks_core.Folder'),
        ),
    ]