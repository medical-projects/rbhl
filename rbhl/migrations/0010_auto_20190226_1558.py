# Generated by Django 2.0.9 on 2019-02-26 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbhl', '0009_merge_20190220_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='date_first_appointment',
            field=models.DateField(blank=True, null=True, verbose_name='Date of first appointment offered'),
        ),
    ]
