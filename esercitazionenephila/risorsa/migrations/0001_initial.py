# Generated by Django 5.0.6 on 2024-06-19 21:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nodo', '0001_initial'),
        ('utente', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Risorsa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('responsabile', models.BooleanField(default=False)),
                ('operatore', models.BooleanField(default=False)),
                ('titolo', models.CharField(max_length=40)),
                ('contenuto', models.TextField()),
                ('nodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='risorse', to='nodo.nodo')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='risorse', to='utente.utente')),
            ],
        ),
    ]
