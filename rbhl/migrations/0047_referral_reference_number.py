# Generated by Django 2.2.16 on 2020-12-10 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbhl', '0046_merge_20201210_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='referral',
            name='reference_number',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Their reference number'),
        ),
    ]
