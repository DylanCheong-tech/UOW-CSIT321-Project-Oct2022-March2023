# sendOYPEmail.py

import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

import os
from dotenv import load_dotenv

class EmailSender:
    def __init__(self, email):
        self.receiver_email = email
        load_dotenv()
        self.SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY");
        self.TEMPLATE_ID = "d-84a1e28f68554373b977e237e634f6bf"

    def sendOTP(self, otp):
        # receiver email must be defined
        if (self.receiver_email is None or len(self.receiver_email) == 0):
            return False

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

        return response
