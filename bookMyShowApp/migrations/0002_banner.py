# Generated by Django 4.1.4 on 2022-12-08 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookMyShowApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_image', models.ImageField(upload_to='banners/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
