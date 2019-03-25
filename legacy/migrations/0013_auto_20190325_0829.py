# Generated by Django 2.0.13 on 2019-03-25 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legacy', '0012_auto_20190325_0822'),
    ]

    operations = [
        migrations.AddField(
            model_name='skinpricktest',
            name='specific_sp_testnum',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='skinpricktest',
            name='spt',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='skinpricktest',
            name='test_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='skinpricktest',
            name='wheal',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
