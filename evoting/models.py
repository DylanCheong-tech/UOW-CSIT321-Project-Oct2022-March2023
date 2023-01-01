from django.db import models
from django.utils import timezone

# Create your models here.


class UserAccount(models.Model):
    accountID = models.BigAutoField(primary_key=True, default=1)
    email = models.EmailField()
    password = models.CharField(max_length=22)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)
    createdAt = models.DateTimeField(default=timezone.localtime)

    def __str__(self):
        return self.accountID


class OTPManagement(models.Model):
    email = models.EmailField()
    otp = models.IntegerField(default=000000)
    expireAt = models.DateTimeField()

    def __str__(self):
        return self.email