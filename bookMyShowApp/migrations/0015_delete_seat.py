# Generated by Django 4.1.4 on 2022-12-16 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookMyShowApp', '0014_remove_booking_seat_booking_booked_seats'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Seat',
        ),
    ]
