# Generated by Django 2.0.13 on 2020-06-25 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbhl', '0036_auto_20200623_1531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliniclog',
            name='diagnosis_made',
        ),
    ]
