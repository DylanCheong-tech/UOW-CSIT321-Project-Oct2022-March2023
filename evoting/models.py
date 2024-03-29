from django.db import models
from django.utils import timezone
from django.utils import dateparse
from datetime import datetime

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
        return str(self.otp) == str(input_otp)
        
    def __str__(self):
        return self.email

class VoteEvent(models.Model):
    eventNo = models.BigAutoField(primary_key=True)
    eventTitle = models.BinaryField()
    startDate = models.DateField()
    startTime = models.TimeField()
    endDate = models.DateField()
    endTime = models.TimeField()
    eventQuestion = models.BinaryField()
    status = models.CharField(max_length=2, default="PC")
    createdBy = models.ForeignKey("UserAccount", on_delete=models.CASCADE)
    publicKey = models.TextField(default="NOT APPLICABLE")

    def is_event_datetime_valid(self, type):
        start_datetime = dateparse.parse_datetime(str(self.startDate) + " " + str(self.startTime))
        end_datetime = dateparse.parse_datetime(str(self.endDate) + " " + str(self.endTime))

        if type == "Creation":
            if start_datetime < datetime.now():
                return False
        if type == "Published":
            if end_datetime < datetime.now():
                return False

        if start_datetime > end_datetime:
            return False

        return True   

    def get_start_datetime(self):
        start_datetime = dateparse.parse_datetime(str(self.startDate) + " " + str(self.startTime))

        return start_datetime

    def __str__(self):
        return self.eventNo


class VoteOption(models.Model):
    voteOption = models.BinaryField()
    eventNo = models.ForeignKey("VoteEvent", on_delete=models.CASCADE)
    voteEncoding = models.TextField(default=0)
    voteTotalCount = models.TextField(default=0)

    def __str__(self):
        return self.id

class Voter(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    eventNo = models.ForeignKey("VoteEvent", on_delete=models.CASCADE)
    token = models.CharField(max_length=64, default="NOT APPLICABLE")
    voteStatus = models.CharField(max_length=1, default="0")

    def __str__(self):
        return self.id


class VotingPool(models.Model):
    eventNo = models.ForeignKey("VoteEvent", on_delete=models.CASCADE)
    castedVote = models.TextField(default="NOT APPLICABLE")


   