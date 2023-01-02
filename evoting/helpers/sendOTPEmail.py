# sendOYPEmail.py

import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content


class EmailSender:
    def __init__(self, email):
        self.receiver_email = email
        self.SENDGRID_API_KEY = "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";
        self.TEMPLATE_ID = "d-84a1e28f68554373b977e237e634f6bf"

    def sendOTP(self, otp):
        # assign your API key to the SendGrid API client
        my_sg = sendgrid.SendGridAPIClient(
            api_key=self.SENDGRID_API_KEY)

        # sender email
        from_email = Email("FYP22S402@gmail.com")

        # recipient email
        to_email = To(self.receiver_email)

        mail = Mail(from_email, to_email)
        mail.dynamic_template_data = {
            'otp' : otp
        }
        mail.template_id = self.TEMPLATE_ID;

        response = my_sg.send(mail)