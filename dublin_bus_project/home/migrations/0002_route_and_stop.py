# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 14:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='route_and_stop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_id', models.CharField(max_length=10)),
                ('stop_count', models.CharField(max_length=20)),
                ('stop_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.stop_locations')),
            ],
        ),
    ]
