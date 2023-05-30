from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils import timezone


class User(AbstractUser):
    image = models.ImageField(upload_to="users_images", blank=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={"email": self.user.email, "code": self.code})
        disc_link = f'{settings.DOMAIN_NAME}{link}'
        subject = 'Подтверждение электронной почты'
        text = 'Для подтверждения эл. почты {} перейдите по ссылке {}'.format(
            self.user.email,
            disc_link,
        )
        send_mail(
            subject=subject,
            message=text,
            from_email='server-no-reply@yandex.com',
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if timezone.now() >= self.expiration else False


# Create your models here.
