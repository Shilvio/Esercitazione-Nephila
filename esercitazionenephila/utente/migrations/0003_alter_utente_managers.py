# Generated by Django 5.0.6 on 2024-06-22 10:35

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utente', '0002_utente_last_login'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='utente',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
