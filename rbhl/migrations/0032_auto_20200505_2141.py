# Generated by Django 2.0.13 on 2020-05-05 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbhl', '0031_auto_20200505_2119'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chronicairflowlimitation',
            old_name='copd_occupational',
            new_name='occupational',
        ),
    ]