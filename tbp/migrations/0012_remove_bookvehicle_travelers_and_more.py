# Generated by Django 4.2.5 on 2024-02-29 20:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tbp', '0011_bookvehicle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookvehicle',
            name='travelers',
        ),
        migrations.RemoveField(
            model_name='bookvehicle',
            name='vehicles',
        ),
        migrations.AddField(
            model_name='bookvehicle',
            name='checkout_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bookvehicle',
            name='traveler',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bookvehicle',
            name='vehicle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tbp.vehicle'),
        ),
    ]