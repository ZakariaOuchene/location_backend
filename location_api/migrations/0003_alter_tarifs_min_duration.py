# Generated by Django 4.1.7 on 2023-12-16 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location_api', '0002_car_gearbox'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarifs',
            name='min_duration',
            field=models.IntegerField(blank=True),
        ),
    ]