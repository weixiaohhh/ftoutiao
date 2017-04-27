# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-22 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='followers',
        ),
        migrations.AddField(
            model_name='profile',
            name='follwers',
            field=models.ManyToManyField(blank=True, related_name='_profile_follwers_+', to='account.Profile'),
        ),
    ]
