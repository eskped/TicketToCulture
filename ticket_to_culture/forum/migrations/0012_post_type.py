# Generated by Django 3.2.12 on 2022-03-24 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0011_post_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='type',
            field=models.CharField(default='location', max_length=1024, verbose_name='Type'),
        ),
    ]
