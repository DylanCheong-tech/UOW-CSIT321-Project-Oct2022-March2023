from django.db import models

# Create your models here.

class UserAccount(models.Model):
    accountID = models.DecimalField(decimal_places=0, max_digits=10)
    email = models.EmailField()
    password = models.CharField(max_length=22)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)
    createdAt = models.DateTimeField()

    def __str__(self):
        return self.accountID