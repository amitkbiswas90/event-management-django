from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
import os


class CustomUser(AbstractUser):
    
    profile_picture = models.ImageField(
        upload_to='profile_pics',  
        blank=True, 
        null=True,
        default="profile_pics/default-image.png"
    )

    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            r'^\+?1?\d{9,15}$',
            "Enter phone number in the format: '+8801'"
        )],
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username