# Generated by Django 4.1.4 on 2022-12-16 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookMyShowApp', '0010_seat_movie_show'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seat',
            name='movie_show',
        ),
    ]
