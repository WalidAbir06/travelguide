# Generated by Django 4.2.5 on 2024-02-29 17:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tbp', '0010_agency_vehicle'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookVehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField()),
                ('travelers', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('vehicles', models.ManyToManyField(to='tbp.vehicle')),
            ],
        ),
    ]
