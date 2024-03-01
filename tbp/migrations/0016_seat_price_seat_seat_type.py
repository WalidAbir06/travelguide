# Generated by Django 4.2.5 on 2024-03-01 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tbp', '0015_plane_arrival_country_plane_departure_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='seat',
            name='seat_type',
            field=models.CharField(choices=[('Economy', 'Economy'), ('Business', 'Business'), ('First Class', 'First Class')], default='Economy', max_length=20),
        ),
    ]
