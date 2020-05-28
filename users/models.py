import uuid
from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.shortcuts import reverse


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
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2, null=True, blank=True, default=LANGUAGE_KOREA)
    birthdate = models.DateField(null=True)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, null=True, blank=True, default=CURRENCY_KR)
    superhost = models.BooleanField(default=False)
    email_verify = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=120, default="", blank=True)

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

    def verify_email(self):
        if self.email_verify is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string("emails/verify_email.html", {"secret": secret})
            send_mail(
                "Verify AirbnbClone Account",
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return
