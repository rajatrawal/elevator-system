# Generated by Django 4.2.3 on 2023-07-28 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_rename_destination_floors_request_destination_floor'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='status',
            field=models.CharField(blank=True, choices=[('ongoing', 'ongoing'), ('completed', 'completed')], max_length=9, null=True),
        ),
    ]
