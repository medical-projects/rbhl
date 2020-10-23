# Generated by Django 2.0.13 on 2020-10-20 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legacy', '0008_patientnumber_source'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allergen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('system', models.CharField(blank=True, max_length=255, null=True)),
                ('code', models.CharField(blank=True, max_length=255, null=True)),
                ('version', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Exposure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('system', models.CharField(blank=True, max_length=255, null=True)),
                ('code', models.CharField(blank=True, max_length=255, null=True)),
                ('version', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='bloodbook',
            name='exposure',
        ),
        migrations.RemoveField(
            model_name='bloodbookresult',
            name='allergen',
        ),
        migrations.AddField(
            model_name='bloodbook',
            name='exposure_ft',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bloodbookresult',
            name='allergen_ft',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bloodbook',
            name='blood_date',
            field=models.DateField(blank=True, null=True, verbose_name='Sample received'),
        ),
        migrations.AlterField(
            model_name='bloodbook',
            name='report_dt',
            field=models.DateField(blank=True, null=True, verbose_name='Report date'),
        ),
        migrations.AlterField(
            model_name='bloodbook',
            name='report_st',
            field=models.DateField(blank=True, null=True, verbose_name='Report submitted'),
        ),
        migrations.AlterField(
            model_name='bloodbookresult',
            name='igg',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='IgG mg/L'),
        ),
        migrations.AlterField(
            model_name='bloodbookresult',
            name='iggclass',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='IgG Class'),
        ),
        migrations.AlterField(
            model_name='bloodbookresult',
            name='klass',
            field=models.CharField(blank=True, choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], max_length=200, null=True, verbose_name='IgE Class'),
        ),
        migrations.AlterField(
            model_name='bloodbookresult',
            name='kul',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='KU/L'),
        ),
        migrations.AlterField(
            model_name='bloodbookresult',
            name='precipitin',
            field=models.CharField(blank=True, choices=[('-ve', '-ve'), ('+ve', '+ve'), ('Weak +ve', 'Weak +ve'), ('++ve', '++ve')], max_length=200, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='exposure',
            unique_together={('code', 'system')},
        ),
        migrations.AlterUniqueTogether(
            name='allergen',
            unique_together={('code', 'system')},
        ),
        migrations.AddField(
            model_name='bloodbook',
            name='exposure_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='legacy.Exposure'),
        ),
        migrations.AddField(
            model_name='bloodbookresult',
            name='allergen_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='legacy.Allergen'),
        ),
    ]