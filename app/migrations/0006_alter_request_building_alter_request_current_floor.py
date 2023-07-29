# Generated by Django 4.2.3 on 2023-07-28 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_rename_bulding_building_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='building',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_requests', to='app.floor'),
        ),
        migrations.AlterField(
            model_name='request',
            name='current_floor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_requests', to='app.floor'),
        ),
    ]
