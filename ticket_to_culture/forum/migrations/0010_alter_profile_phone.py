# Generated by Django 3.2.8 on 2022-03-17 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0009_alter_profile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.IntegerField(),
        ),
    ]