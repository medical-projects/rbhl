# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-15 09:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import opal.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('opal', '0036_merge_20181030_1654'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('attendance', models.NullBooleanField()),
                ('date_first_appointment', models.DateField(blank=True, null=True)),
                ('firefighter', models.NullBooleanField()),
                ('active', models.NullBooleanField()),
                ('general_notes', models.TextField(blank=True, null=True)),
                ('finaldays', models.IntegerField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_legacy_actionlog_subrecords', to=settings.AUTH_USER_MODEL)),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opal.Episode')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_legacy_actionlog_subrecords', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '18 Week Database',
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='BloodBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('reference_number', models.CharField(blank=True, max_length=200, null=True)),
                ('employer', models.CharField(blank=True, max_length=200, null=True)),
                ('oh_provider', models.CharField(blank=True, max_length=100, null=True)),
                ('blood_date', models.DateField(blank=True, null=True)),
                ('blood_number', models.CharField(blank=True, max_length=200, null=True)),
                ('method', models.CharField(blank=True, max_length=200, null=True)),
                ('blood_collected', models.CharField(blank=True, max_length=200, null=True, verbose_name='EDTA blood collected')),
                ('date_dna_extracted', models.CharField(blank=True, max_length=200, null=True)),
                ('information', models.CharField(blank=True, max_length=200, null=True)),
                ('assayno', models.CharField(blank=True, max_length=200, null=True)),
                ('assay_date', models.DateField(blank=True, null=True)),
                ('blood_taken', models.DateField(blank=True, null=True)),
                ('blood_tm', models.DateField(blank=True, null=True)),
                ('report_dt', models.DateField(blank=True, null=True)),
                ('report_st', models.DateField(blank=True, null=True)),
                ('store', models.CharField(blank=True, max_length=200, null=True)),
                ('exposure', models.CharField(blank=True, max_length=200, null=True)),
                ('antigen_date', models.DateField(blank=True, null=True)),
                ('antigen_type', models.CharField(blank=True, max_length=200, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('batches', models.TextField(blank=True, null=True)),
                ('room', models.TextField(blank=True, null=True)),
                ('freezer', models.TextField(blank=True, null=True)),
                ('shelf', models.TextField(blank=True, null=True)),
                ('tray', models.TextField(blank=True, null=True)),
                ('vials', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_legacy_bloodbook_subrecords', to=settings.AUTH_USER_MODEL)),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opal.Episode')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_legacy_bloodbook_subrecords', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='BloodBookResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('result', models.CharField(blank=True, max_length=200, null=True)),
                ('allergen', models.CharField(blank=True, max_length=200, null=True)),
                ('antigenno', models.CharField(blank=True, max_length=200, null=True)),
                ('kul', models.CharField(blank=True, max_length=200, null=True)),
                ('klass', models.CharField(blank=True, max_length=200, null=True)),
                ('rast', models.CharField(blank=True, max_length=200, null=True)),
                ('precipitin', models.CharField(blank=True, max_length=200, null=True)),
                ('igg', models.CharField(blank=True, max_length=200, null=True)),
                ('iggclass', models.CharField(blank=True, max_length=200, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_legacy_bloodbookresult_subrecords', to=settings.AUTH_USER_MODEL)),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opal.Episode')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_legacy_bloodbookresult_subrecords', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PeakFlowIdentifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('occmendo', models.IntegerField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_legacy_peakflowidentifier_subrecords', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opal.Patient')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_legacy_peakflowidentifier_subrecords', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
    ]
