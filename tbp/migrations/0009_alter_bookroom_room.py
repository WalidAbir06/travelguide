# Generated by Django 4.2.5 on 2024-02-29 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tbp', '0008_bookroom_checkout_date_alter_bookroom_booking_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookroom',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tbp.room'),
        ),
    ]
