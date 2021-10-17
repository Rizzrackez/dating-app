from django.db import models
from django.contrib.auth.models import AbstractUser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Member(AbstractUser):
    """
    модель участников
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    avatar = models.ImageField(upload_to='media/member_avatars')
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    email = models.EmailField(max_length=254, unique=True, blank=False)
    liked_members = models.ManyToManyField('Member', blank=True, related_name='members')

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email