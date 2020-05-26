# Generated by Django 2.0.13 on 2020-05-26 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbhl', '0031_routinespt_antihistimines'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='routinespt',
            options={'verbose_name': 'Routine SPT'},
        ),
        migrations.AlterModelOptions(
            name='specificskinpricktest',
            options={'verbose_name': 'Specific SPT'},
        ),
        migrations.AddField(
            model_name='skinpricktest',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='skinpricktest',
            name='specific_sp_testnum',
            field=models.IntegerField(blank=True, null=True, verbose_name='Specific SP test num'),
        ),
        migrations.AddField(
            model_name='skinpricktest',
            name='spt',
            field=models.TextField(blank=True, default='', verbose_name='SPT'),
        ),
        migrations.AddField(
            model_name='skinpricktest',
            name='wheal',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='spirometry',
            name='fvc_percentage_predicted',
            field=models.IntegerField(blank=True, null=True, verbose_name='FVC % predicted'),
        ),
    ]
