from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_KOREA = "kr"
    LANGUAGE_ENGLISH = "en"

    LANGUAGE_CHOICES = (
        (LANGUAGE_KOREA, "Korean"),
        (LANGUAGE_ENGLISH, "English"),
    )

    CURRENCY_KR = 'krw'
    CURRENCY_EN = "usd"

    CURRENCY_CHOICES = (
        (CURRENCY_EN, "USD"),
        (CURRENCY_KR, "KRW"),
    )

    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, null=True, blank=True)
    bio = models.TextField(default="", blank=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2, null=True, blank=True)
    birthdate = models.DateField(null=True)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, null=True, blank=True)
    superhost = models.BooleanField(default=False)

