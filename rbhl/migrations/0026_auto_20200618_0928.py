# Generated by Django 2.0.13 on 2020-06-18 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbhl', '0025_auto_20200617_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='referral_disease',
            field=models.CharField(blank=True, choices=[('Asthma', 'Asthma'), ('Asthma / Rhinitis', 'Asthma / Rhinitis'), ('Inhalation injury', 'Inhalation injury'), ('Malignancy', 'Malignancy'), ('Other / Unclear', 'Other / Unclear'), ('Pulmonary fibrosis(eg: Asbestos related disease)', 'Pulmonary fibrosis(eg: Asbestos related disease)')], max_length=256, null=True),
        ),
    ]
