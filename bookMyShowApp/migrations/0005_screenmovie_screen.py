# Generated by Django 4.1.4 on 2022-12-09 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookMyShowApp', '0004_cinema_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='screenmovie',
            name='screen',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bookMyShowApp.screens'),
            preserve_default=False,
        ),
    ]
