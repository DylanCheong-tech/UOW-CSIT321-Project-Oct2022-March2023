# helper: otpGenerator.py

import random as rand
from django.utils import timezone
from ..models import OTPManagement

class OTPGenerator:
    email = None

    def __init__(self, email):
        # assume the input email is cleaned and formatted
        self.email = email

    def generateOTP(self):
        if (self.email is None or len(self.email) == 0):
            return False

        otp = 0
        for i in range(5):
            otp += rand.randint(1, 9)
            otp *= 10

        otp_record, created = OTPManagement.objects.get_or_create(email=self.email)
        otp_record.otp = otp
        otp_record.expireAt = timezone.localtime() + timezone.timedelta(minutes=5)
        otp_record.save()
        
        return otp
