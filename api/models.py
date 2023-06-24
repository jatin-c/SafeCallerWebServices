from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # userID = models.AutoField(primary_key=True)
    
    # username = models.CharField(max_length=150, unique=False) 
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(default=None)
    USERNAME_FIELD = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    # password = models.CharField(max_length=128, default=None)
    # REQUIRED_FIELDS = ['phone_number', 'password']

    def __str__(self):
        return self.name
# @receiver(post_save, sender=User)
# def create_global_contact(sender, instance, created, **kwargs):
#     if created:
#         GlobalContact.objects.create(name=instance.name, phone_number=instance.phone_number)

class Contact(models.Model):
    contactID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    isRegistered = models.BooleanField(default=False)
    isSpam = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number

# class GlobalContact(models.Model):
#     name = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=20)

#     def __str__(self):
#         return self.phone_number

