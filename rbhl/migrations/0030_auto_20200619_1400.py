# Generated by Django 2.0.13 on 2020-06-19 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbhl', '0029_auto_20200619_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employment',
            name='employed_in_suspect_occupation',
            field=models.BooleanField(default=False, verbose_name='suspect occcupation'),
        ),
    ]
