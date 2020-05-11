# Generated by Django 2.0.13 on 2020-05-11 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbhl', '0024_auto_20200511_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnosis',
            name='asthma_options',
            field=models.TextField(blank=True, choices=[('Occupational caused by sensitisation', 'Occupational caused by sensitisation'), ('Exacerbated by work', 'Exacerbated by work'), ('Irritant induced', 'Irritant induced'), ('Non occupational', 'Non occupational')], default=''),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='rhinitis_options',
            field=models.TextField(blank=True, choices=[('Occupational caused by sensitisation', 'Occupational caused by sensitisation'), ('Exacerbated by work', 'Exacerbated by work'), ('Non occupational', 'Non occupational')], default=''),
        ),
    ]
