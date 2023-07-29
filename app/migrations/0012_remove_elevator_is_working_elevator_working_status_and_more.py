# Generated by Django 4.2.3 on 2023-07-29 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_request_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='elevator',
            name='is_working',
        ),
        migrations.AddField(
            model_name='elevator',
            name='working_status',
            field=models.CharField(choices=[('working', 'working'), ('under maintenance', 'under maintenance')], default='working', max_length=18),
        ),
        migrations.AlterField(
            model_name='elevator',
            name='status',
            field=models.CharField(choices=[('stoped', 'stoped'), ('up', 'up'), ('down', 'down')], default='stoped', max_length=10),
        ),
    ]