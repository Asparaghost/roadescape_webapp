# Generated by Django 4.2.6 on 2023-10-30 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0014_alter_incidentreport_imageurls'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidentreport',
            name='imageUrls',
            field=models.ImageField(upload_to='incident_reports/'),
        ),
    ]