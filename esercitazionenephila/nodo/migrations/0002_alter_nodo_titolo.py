# Generated by Django 5.0.6 on 2024-06-22 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nodo',
            name='titolo',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
