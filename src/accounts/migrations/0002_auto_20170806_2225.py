# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-06 22:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, upload_to='users/%Y/%m/%d', verbose_name='Image de profil'),
        ),
    ]