# Generated by Django 2.0.13 on 2020-06-21 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbhl', '0030_auto_20200619_1400'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='demographics',
            options={'verbose_name_plural': 'Demographics'},
        ),
        migrations.AddField(
            model_name='asthmadetails',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='rhinitisdetails',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='height',
            field=models.IntegerField(blank=True, null=True, verbose_name='Height(cm)'),
        ),
        migrations.AlterField(
            model_name='referral',
            name='referral_type',
            field=models.TextField(blank=True, null=True, verbose_name='Type of Referral'),
        ),
    ]
