# helper: otpGenerator.py

import random as rand
from django.utils import timezone
from ..models import OTPManagement

class OTPGenerator:
    email = ""

    def __init__(self, email):
        self.email = email

    def generateOTP(self):
        otp = 0
        for i in range(5):
            otp += rand.randint(1, 9)
            otp *= 10

        otp_record, created = OTPManagement.objects.get_or_create(email=self.email)
        otp_record.otp = otp
        otp_record.expireAt = timezone.localtime() + timezone.timedelta(minutes=5)
        print(otp_record.expireAt)
        otp_record.save()
        
        return otp
