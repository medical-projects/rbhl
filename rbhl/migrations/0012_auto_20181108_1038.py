# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-08 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbhl', '0011_auto_20181107_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='peakflowday',
            name='flow_0000',
            field=models.IntegerField(blank=True, null=True, verbose_name='00:00'),
        ),
        migrations.AddField(
            model_name='peakflowday',
            name='flow_0100',
            field=models.IntegerField(blank=True, null=True, verbose_name='01:00'),
        ),
        migrations.AddField(
            model_name='peakflowday',
            name='flow_0200',
            field=models.IntegerField(blank=True, null=True, verbose_name='02:00'),
        ),
        migrations.AddField(
            model_name='peakflowday',
            name='flow_0300',
            field=models.IntegerField(blank=True, null=True, verbose_name='03:00'),
        ),
        migrations.AddField(
            model_name='peakflowday',
            name='flow_0400',
            field=models.IntegerField(blank=True, null=True, verbose_name='04:00'),
        ),
        migrations.AddField(
            model_name='peakflowday',
            name='flow_0500',
            field=models.IntegerField(blank=True, null=True, verbose_name='05:00'),
        ),
    ]
