# Generated by Django 2.0.13 on 2020-06-30 16:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import opal.models
import plugins.lab.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0038_auto_20191206_1449'),
        ('lab', '0006_merge_20200626_0859'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consistency_token', models.CharField(max_length=8)),
                ('clinical_info', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=256, null=True)),
                ('test_name', models.CharField(blank=True, max_length=256, null=True)),
                ('test_code', models.CharField(blank=True, max_length=256, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            bases=(plugins.lab.models.SerializeRelated, opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consistency_token', models.CharField(max_length=8)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
                ('observation_name', models.CharField(blank=True, max_length=256, null=True)),
                ('observation_number', models.CharField(blank=True, max_length=256, null=True)),
                ('observation_value', models.TextField(blank=True, null=True)),
                ('reference_range', models.CharField(blank=True, max_length=256, null=True)),
                ('units', models.CharField(blank=True, max_length=256, null=True)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.LabTest')),
            ],
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Specimen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('reference_number', models.CharField(blank=True, default='', max_length=200)),
                ('blood_date', models.DateField(blank=True, null=True)),
                ('blood_number', models.CharField(blank=True, default='', max_length=200)),
                ('method', models.CharField(blank=True, choices=[('ImmunoCAP', 'ImmunoCAP'), ('UniCAP', 'UniCAP'), ('CAP', 'CAP'), ('RAST', 'RAST'), ('CAP & RAST', 'CAP & RAST'), ('RAST & UniCAP', 'RAST & UniCAP'), ('PRECIPITINS', 'PRECIPITINS')], default='', max_length=256)),
                ('information', models.CharField(blank=True, default='', max_length=200)),
                ('assay_no', models.CharField(blank=True, default='', max_length=256)),
                ('assay_date', models.DateField(blank=True, null=True)),
                ('blood_taken', models.DateField(blank=True, null=True)),
                ('report_dt', models.DateField(blank=True, null=True)),
                ('report_st', models.DateField(blank=True, null=True)),
                ('store', models.NullBooleanField()),
                ('exposure', models.CharField(blank=True, choices=[('LAB ANIMALS', 'LAB ANIMALS'), ('FLOUR', 'FLOUR'), ('ISOCYANATES', 'ISOCYANATES'), ('LATEX', 'LATEX'), ('GEN ANIMALS', 'GEN ANIMALS'), ('ENZYMES', 'ENZYMES'), ('HOUSE DUST MITES', 'HOUSE DUST MITES')], default='', max_length=256)),
                ('antigen_type', models.CharField(blank=True, choices=[('STANDARD', 'STANDARD'), ('BESPOKE', 'BESPOKE')], default='', max_length=256)),
                ('comment', models.TextField(blank=True, null=True)),
                ('vials', models.FloatField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_lab_specimen_subrecords', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opal.Patient')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_lab_specimen_subrecords', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(plugins.lab.models.SerializeRelated, opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.AddField(
            model_name='labtest',
            name='specimen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.Specimen'),
        ),
    ]
