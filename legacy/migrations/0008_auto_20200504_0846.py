# Generated by Django 2.0.13 on 2020-05-04 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legacy', '0007_auto_20200430_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otherfields',
            name='attendance_date',
        ),
        migrations.AddField(
            model_name='details',
            name='attendance_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
