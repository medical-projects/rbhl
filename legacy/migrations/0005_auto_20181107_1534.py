# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-07 15:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legacy', '0004_auto_20181107_1514'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actionlog',
            name='histamine',
        ),
        migrations.RemoveField(
            model_name='actionlog',
            name='histamine_attendance',
        ),
        migrations.RemoveField(
            model_name='actionlog',
            name='histamine_date',
        ),
        migrations.RemoveField(
            model_name='actionlog',
            name='immunology_oem',
        ),
        migrations.RemoveField(
            model_name='actionlog',
            name='lung_function',
        ),
        migrations.RemoveField(
            model_name='actionlog',
            name='lung_function_attendance',
        ),
        migrations.RemoveField(
            model_name='actionlog',
            name='lung_function_date',
        ),
        migrations.RemoveField(
            model_name='actionlog',
            name='other_gp_info',
        ),
        migrations.RemoveField(
            model_name='actionlog',
            name='other_hospital_info',
        ),
        migrations.RemoveField(
            model_name='actionlog',
            name='other_oh_info',
        ),
        migrations.RemoveField(
            model_name='actionlog',
            name='other_rbh_bloods',
        ),
        migrations.RemoveField(
            model_name='actionlog',
            name='peak_flow',
        ),
        migrations.RemoveField(
            model_name='actionlog',
            name='work_samples',
        ),
    ]
