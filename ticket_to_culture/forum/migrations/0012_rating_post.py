# Generated by Django 4.0.2 on 2022-03-22 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0011_rating_is_seller_rating_buyer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='forum.post'),
        ),
    ]
