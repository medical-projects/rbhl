# Generated by Django 2.0.13 on 2020-03-11 10:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        ('opal', '0037_auto_20181114_1445'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rbhl', '0018_auto_20200310_1144'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportedFromOccupationalLungDatabase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('trial_number', models.IntegerField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_rbhl_importedfromoccupationallungdatabase_subrecords', to=settings.AUTH_USER_MODEL)),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opal.Episode')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_rbhl_importedfromoccupationallungdatabase_subrecords', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.RemoveField(
            model_name='importedfrompreviousdatabase',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='importedfrompreviousdatabase',
            name='episode',
        ),
        migrations.RemoveField(
            model_name='importedfrompreviousdatabase',
            name='updated_by',
        ),
        migrations.DeleteModel(
            name='ImportedFromPreviousDatabase',
        ),
    ]
