# Generated by Django 2.0.13 on 2020-04-28 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legacy', '0006_auto_20200428_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='date_referral_received',
            field=models.DateField(blank=True, null=True),
        ),
    ]