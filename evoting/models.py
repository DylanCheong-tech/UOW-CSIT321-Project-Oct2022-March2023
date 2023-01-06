from django.db import models
from django.utils import timezone

# Create your models here.


class UserAccount(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="accountID")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=32)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)
    createdAt = models.DateTimeField(default=timezone.localtime)

    def __str__(self):
        return self.id


class OTPManagement(models.Model):
    email = models.EmailField()
    otp = models.IntegerField(default=000000)
    expireAt = models.DateTimeField(default=timezone.localtime() + timezone.timedelta(minutes=5))

    def is_expired(self):
        return timezone.localtime() > timezone.localtime(self.expireAt)

    def check_otp_matching(self, input_otp):
        return str(self.otp) == input_otp
        
    def __str__(self):
        return self.email