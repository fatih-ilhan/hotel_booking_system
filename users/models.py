from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, User, AbstractUser, BaseUserManager


class User(AbstractUser):
    is_hotel_manager = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    zip_code = models.BigIntegerField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
