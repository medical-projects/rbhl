# Generated by Django 2.2.16 on 2021-02-04 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0009_bloods_authorised_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodresult',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]