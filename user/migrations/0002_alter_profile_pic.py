# Generated by Django 4.0 on 2021-12-09 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pic',
            field=models.ImageField(blank=True, default='media/avatar.png', upload_to='.'),
        ),
    ]
