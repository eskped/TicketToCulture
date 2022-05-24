# Generated by Django 3.2.12 on 2022-03-24 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_alter_post_description_alter_post_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(max_length=255, verbose_name='Høy-Lav')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='location',
            field=models.TextField(default='location', max_length=1024, verbose_name='Lokasjon'),
        ),
    ]