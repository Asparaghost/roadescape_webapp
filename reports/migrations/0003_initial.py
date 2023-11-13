# Generated by Django 4.0 on 2023-10-14 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('reports', '0002_delete_customuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncidentReport',
            fields=[
                ('incident_id', models.AutoField(primary_key=True, serialize=False)),
                ('obstruction', models.CharField(max_length=20)),
                ('imageUrl', models.ImageField(blank=True, null=True, upload_to='incident_photo/')),
                ('description', models.CharField(max_length=200)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('status', models.CharField(max_length=20)),
                ('createdAt', models.DateTimeField(auto_now=True)),
                ('createdBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='auth.user')),
            ],
            options={
                'db_table': 'IncidentReport',
            },
        ),
    ]
