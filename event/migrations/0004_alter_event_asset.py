# Generated by Django 5.1.6 on 2025-02-20 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_alter_event_asset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='asset',
            field=models.ImageField(blank=True, default='event_asset/default-image.png', null=True, upload_to='event_asset'),
        ),
    ]
