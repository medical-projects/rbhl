# Generated by Django 2.0.13 on 2020-09-21 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('opal', '0038_auto_20191206_1449'),
        ('legacy', '0008_patientnumber_source'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodBookEpisode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_number', models.CharField(blank=True, max_length=256, null=True)),
                ('blood_date', models.DateField(blank=True, null=True)),
                ('oh_provider', models.CharField(blank=True, max_length=256, null=True)),
                ('employer', models.CharField(blank=True, max_length=256, null=True)),
                ('referrer_name', models.CharField(blank=True, max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BloodBookPatient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hospital_number', models.CharField(blank=True, max_length=256, null=True)),
                ('first_name', models.CharField(blank=True, max_length=256, null=True)),
                ('surname', models.CharField(blank=True, max_length=256, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='opal.Patient')),
            ],
        ),
        migrations.AddField(
            model_name='bloodbookepisode',
            name='blood_book_patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='legacy.BloodBookPatient'),
        ),
        migrations.AddField(
            model_name='bloodbookepisode',
            name='episode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='opal.Episode'),
        ),
    ]
