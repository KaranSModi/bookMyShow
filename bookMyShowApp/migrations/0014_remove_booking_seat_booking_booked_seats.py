# Generated by Django 4.1.4 on 2022-12-16 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookMyShowApp', '0013_seat_available'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='seat',
        ),
        migrations.AddField(
            model_name='booking',
            name='booked_seats',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
