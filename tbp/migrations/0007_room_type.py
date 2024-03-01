# Generated by Django 4.2.5 on 2024-02-29 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tbp', '0006_remove_bookroom_rooms_bookroom_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='type',
            field=models.CharField(choices=[('Standard', 'Standard'), ('Deluxe', 'Deluxe'), ('Suite', 'Suite')], default='Standard', max_length=20),
        ),
    ]
