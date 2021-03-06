# Generated by Django 2.0.13 on 2020-06-23 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbhl', '0031_auto_20200621_1951'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='demographics',
            options={},
        ),
        migrations.AlterField(
            model_name='demographics',
            name='height',
            field=models.IntegerField(blank=True, null=True, verbose_name='Height (cm)'),
        ),
        migrations.AlterField(
            model_name='referral',
            name='referral_type',
            field=models.TextField(blank=True, null=True, verbose_name='Type of referral'),
        ),
    ]
