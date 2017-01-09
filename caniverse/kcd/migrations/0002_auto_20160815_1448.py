# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-15 14:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kcd', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='networkdefinition',
            name='document',
        ),
        migrations.AddField(
            model_name='networkdefinition',
            name='author',
            field=models.TextField(blank=True, help_text='The owner or author of the network definition document.'),
        ),
        migrations.AddField(
            model_name='networkdefinition',
            name='company',
            field=models.TextField(blank=True, help_text='The owner company of the network definition document.'),
        ),
        migrations.AddField(
            model_name='networkdefinition',
            name='date',
            field=models.TextField(blank=True, help_text='The release date of this version of the network definition document.'),
        ),
        migrations.AddField(
            model_name='networkdefinition',
            name='name',
            field=models.TextField(blank=True, help_text='Describes the scope of application e.g. the target vehicle or controlled device.'),
        ),
        migrations.AddField(
            model_name='networkdefinition',
            name='version',
            field=models.TextField(blank=True, help_text='The version of the network definition document.'),
        ),
        migrations.DeleteModel(
            name='Document',
        ),
    ]