from decimal import Decimal
from tabnanny import verbose

import django
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator, RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator

from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    phone = models.CharField(verbose_name="Telefonnummer", validators = [phoneNumberRegex], max_length=12)
    image = models.ImageField(default='default_profile_image.png', upload_to='profile_images', verbose_name="Bilde")

    # resizing images
    # def save(self, *args, **kwargs):
    #     super().save()

    #     img = Image.open(self.image.path)

    #     if img.height > 100 or img.width > 100:
    #         new_img = (100, 100)
    #         img.thumbnail(new_img)
    #         img.save(self.image.path)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

LOCATION_CHOICES= [
    ('location', 'Location'),
    ('bergen', 'Bergen'),
    ('oslo', 'Oslo'),
    ('trondheim', 'Trondheim'),
    ('stavanger', 'Stavanger'),
    ('larvik', 'Larvik'),
    ('sandes', 'Sandes'),
    ('annet', 'Annet'),
    ]

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # TODO: Legge til bilde til Post
    title = models.CharField(max_length=255, verbose_name="Tittel")
    description = models.TextField(max_length=1024, default="no_description", verbose_name="Beskrivelse")
    # Er dette salg eller ønsker å kjøpe innlegg?
    is_sale = models.BooleanField(verbose_name="Salgs annonse")
    price = models.DecimalField(max_digits=16, default=0.0, decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.00'))],
                                verbose_name="Pris")
    # Er produktet solgt?
    is_sold = models.BooleanField(default=False, verbose_name="Solgt")
    image = models.ImageField(
        default='default_post_image.jpg',
        upload_to='post_images', verbose_name="Bilde")
    location = models.CharField(max_length=1024, default="location", verbose_name="Lokasjon")
    type = models.CharField(max_length=1024, default="location", verbose_name="Type")

    def __str__(self):
        return self.title

    def is_for_sale(self):
        return self.is_sale
    
    def __str__(self):
        return self.location
    
    def __str__(self):
        return self.type

    
    
class Filter(models.Model):
    price = models.CharField(max_length=255, verbose_name="Høy-Lav")
    
    
def price_high_low(self):
    return self.price


class Rating(models.Model):
    rated_user = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name="rated_user")
    rated_by_user = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name="rated_by_user")
    rating_value = models.PositiveSmallIntegerField(verbose_name="Vurdering", validators=[MinValueValidator(1), MaxValueValidator(5)])
    post = models.ForeignKey(Post, on_delete=models.PROTECT, null=True)
    rated_user_responded = models.BooleanField(verbose_name="Vurdert bruker har vurdert tilbake?", default=False)
    is_seller_rating_buyer = models.BooleanField(verbose_name="Er det selger som vurderer kjøper?", default=False)

    def __str__(self):
        return str(self.rated_by_user.username) + " rated " + str(self.rated_user.username) + " with score " + str(self.rating_value)
        