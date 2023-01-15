# emailSender.py

import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

import os
from dotenv import load_dotenv

class EmailSender:
    def __init__(self, email):
        self.receiver_email = email
        load_dotenv()
        self.SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

    def sendOTP(self, otp):
        """
        Required data for dynamic email template:
        - otp values
        """

        # receiver email must be defined
        if (self.receiver_email is None or len(self.receiver_email) == 0):
            return False

        # assign your API key to the SendGrid API client
        my_sg = sendgrid.SendGridAPIClient(api_key=self.SENDGRID_API_KEY)

        # sender email
        from_email = Email("FYP22S402@gmail.com")

        # recipient email
        to_email = To(self.receiver_email)

        mail = Mail(from_email, to_email)
        mail.dynamic_template_data = {
            "otp" : otp
        }
        mail.template_id = "d-84a1e28f68554373b977e237e634f6bf";

        response = my_sg.send(mail)

        return response

    def sendInvitation(self, host, auth, voter_name, event_owner_name, vote_event_name):
        """
        Required data for dynamic email template:
        - Current application host url (eg. http://host.com/xxx/xxx)
        - Voter Authentication String 
        - Voter Name 
        - Event Owner 
        - Vote Event Name
        """

        # receiver email must be defined
        if (self.receiver_email is None or len(self.receiver_email) == 0):
            return False

        # check the required parameters 
        if not host or not auth or not voter_name or not event_owner_name or not vote_event_name:
            return False

        # assign your API key to the SendGrid API client
        my_sg = sendgrid.SendGridAPIClient(api_key=self.SENDGRID_API_KEY)

        # sender email
        from_email = Email("FYP22S402@gmail.com")

        # recipient email
        to_email = To(self.receiver_email)

        mail = Mail(from_email, to_email)
        mail.dynamic_template_data = {
            "invitation_link" : host + "?auth=" + auth,
            "voter_name" : voter_name,
            "event_owner" : event_owner_name,
            "vote_event_name" : vote_event_name
        }
        mail.template_id = "d-246ddef4a5484ac9ae8ceca46d99efd1";

        response = my_sg.send(mail)

        return response

    def sendFinalResult(self, host, auth, voter_name, vote_event_name):
        """
        Required data for dynamic email template:
        - Current application host url (eg. http://host.com/xxx/xxx)
        - Voter Authentication String 
        - Voter Name 
        - Vote Event Name
        """

        # receiver email must be defined
        if (self.receiver_email is None or len(self.receiver_email) == 0):
            return False

        # check the required parameters 
        if not host or not auth or not voter_name or not vote_event_name:
            return False

        # assign your API key to the SendGrid API client
        my_sg = sendgrid.SendGridAPIClient(api_key=self.SENDGRID_API_KEY)

        # sender email
        from_email = Email("FYP22S402@gmail.com")

        # recipient email
        to_email = To(self.receiver_email)

        mail = Mail(from_email, to_email)
        mail.dynamic_template_data = {
            "url_link" : host + "?auth=" + auth,
            "voter_name" : voter_name,
            "vote_event_name" : vote_event_name
        }
        mail.template_id = " d-dbe55bedb15441a3a85fd462a96fb736";

        response = my_sg.send(mail)

        return response
