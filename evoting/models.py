from django.db import models
from django.utils import timezone
from datetime import date

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

    def __str__(self):
        return self.email

class VoteEvent(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="seqNo")
    eventTitle = models.CharField(max_length=200)
    startDate = models.DateField()
    startTime = models.TimeField()
    endDate = models.DateField()
    endTime = models.TimeField()
    eventQuestion = models.CharField(max_length=200)
   

    def __str__(self):
        return self.id


class VoteOption(models.Model):
    id = models.AutoField(primary_key=True)
    voteOption = models.TextField()
    seqNo = models.ForeignKey("VoteEvent", on_delete=models.CASCADE)

    def __str__(self):
        return self.id

class VoterEmail(models.Model):
    id = models.AutoField(primary_key=True)
    voterEmail = models.EmailField()
    seqNo = models.ForeignKey("VoteEvent", on_delete=models.CASCADE)

    def __str__(self):
        return self.id
   