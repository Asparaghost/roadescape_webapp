# Generated by Django 4.2.6 on 2023-11-12 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0028_rename_roadsigns_roadsign'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.DeleteModel(
            name='RoadSign',
        ),
    ]