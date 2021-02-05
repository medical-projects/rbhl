# Generated by Django 2.2.16 on 2021-02-01 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbhl', '0047_referral_reference_number'),
        ('lab', '0009_bloods_authorised_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloods',
            name='employment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rbhl.Employment'),
        ),
        migrations.AddField(
            model_name='bloods',
            name='referral',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rbhl.Referral'),
        ),
    ]
