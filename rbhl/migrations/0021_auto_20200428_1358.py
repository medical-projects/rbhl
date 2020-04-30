# Generated by Django 2.0.13 on 2020-04-28 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbhl', '0020_merge_20200427_1936'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferralReason',
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
        migrations.RenameModel(
            old_name='RBHReferrer',
            new_name='RbhReferralType',
        ),
        migrations.RemoveField(
            model_name='referral',
            name='referral_type',
        ),
        migrations.AddField(
            model_name='referral',
            name='referral_reason_ft',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='referral',
            name='referral_type_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rbhl.RbhReferralType'),
        ),
        migrations.AddField(
            model_name='referral',
            name='referral_type_ft',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='referralreason',
            unique_together={('code', 'system')},
        ),
        migrations.AddField(
            model_name='referral',
            name='referral_reason_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rbhl.ReferralReason'),
        ),
    ]