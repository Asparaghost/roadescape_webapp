# Generated by Django 4.2.6 on 2023-11-11 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0026_roadsigns_remove_contact_id_contact_contact_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='contact_id',
        ),
        migrations.AddField(
            model_name='contact',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
