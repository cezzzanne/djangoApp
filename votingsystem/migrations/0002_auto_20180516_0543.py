# Generated by Django 2.0.5 on 2018-05-16 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votingsystem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures'),
        ),
    ]
