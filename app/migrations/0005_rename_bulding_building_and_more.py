# Generated by Django 4.2.3 on 2023-07-28 03:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_elevator_elevator_no'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bulding',
            new_name='Building',
        ),
        migrations.RenameField(
            model_name='elevator',
            old_name='bulding',
            new_name='building',
        ),
        migrations.RenameField(
            model_name='request',
            old_name='bulding',
            new_name='building',
        ),
    ]
