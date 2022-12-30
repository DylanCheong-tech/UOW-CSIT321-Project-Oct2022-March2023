# helper: otpGenerator.py

import random as rand
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

        otp_record = OTPManagement(email=self.email, otp=otp)
        otp_record.save()
        
        return otp
