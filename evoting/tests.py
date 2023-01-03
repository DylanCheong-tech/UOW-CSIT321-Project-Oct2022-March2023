from django.test import TestCase
from django.utils import timezone

from .helpers.hasher import Hasher
from .helpers.otpGenerator import OTPGenerator
from .helpers.sendOTPEmail import EmailSender

from .models import OTPManagement


class ModelOTPManagementTest(TestCase):
	"""
	- OTPManagement Model class stored the email, otp value and the expiry timestamp if the otp
	"""

	def testOTPValueIsNotExpired(self):
		"""
		Test Data:
			- Email : abc@gmail.com
			- OTP : 123456
			- Expire Tiemstamp = django.utils.timezone.localtime() + django.utils.timezone.timedelta(minutes=5)

		Expected Result: False
		"""

		otp_record = OTPManagement()
		otp_record.email = "abc@gmail.com"
		otp_record.otp = 123456
		otp_record.expireAt = timezone.localtime() + timezone.timedelta(minutes=5)

		# assert is not expired, False
		self.assertIs(otp_record.is_expired(), False)

	def testOTPValueIsExpired(self):
		"""
		Test Data:
			- Email : abc@gmail.com
			- OTP : 123456
			- Expire Tiemstamp = django.utils.timezone.localtime() - django.utils.timezone.timedelta(minutes=5)

		Expected Result: False
		"""

		otp_record = OTPManagement()
		otp_record.email = "abc@gmail.com"
		otp_record.otp = 123456
		otp_record.expireAt = timezone.localtime() - timezone.timedelta(minutes=5)

		# assert is expired, True
		self.assertIs(otp_record.is_expired(), True)


class HelperHasherTest(TestCase):
	def testHasherDigestMessageCorrectly(self):
		"""
		- Hasher class constructor accepts one arguments, which is the message going to be hashed
		- class method messageDigest() will produce and return the hash value of the message (which is defined when construct the object)

		Test Data:
		Message : "Hello Testing"
		Hash Output : 8b1e7e7c7c2a80e04e033b92a9924bca
		"""

		hasher = Hasher("Hello Testing")
		hash = hasher.messageDigest()
		self.assertEqual(hash, "8b1e7e7c7c2a80e04e033b92a9924bca")


class HelperOTPGeneratorTest(TestCase):
	"""
	- OTPGenerator class constructor accepts one arguments, which is the request user Email address 
	- class method generateOTP() will produce a 6-digits integer number, each digit in range of [0, 9]
		- the generated OTP will be inserted or updated (if existed in database) into the database 
		the generated OTP value will be returned from the function as well
	"""
	def testGenerateOTPWithProvidedEmail(self):
		"""
		Test Data: abc@gmail.com
		Expected Result:
			- OTP generated with random and with 6 digits
			- Only one database record for the test email will be existed 
			- Email and OTP value will be same as test data in the database records
		"""

		generator = OTPGenerator("abc@gmail.com")
		otp = generator.generateOTP()

		otp_from_db = OTPManagement.objects.filter(email="abc@gmail.com")

		# check the otp is exact 6 digits
		self.assertEqual(len(str(otp)), 6)

		# check there is only one records in the database only, (even run this test number of times)
		self.assertEqual(otp_from_db.count(), 1)

		# check the email and otp is matched with the input data
		self.assertEqual(otp_from_db[0].email, "abc@gmail.com")
		self.assertEqual(otp_from_db[0].otp, otp)


	def testGenerateOTPWithProvidedEmailAsNone(self):
		"""
		Test Data : None
		Expected Output: the function will return False
		"""

		generator = OTPGenerator(None)
		otp = generator.generateOTP()

		self.assertIs(otp, False)

	def testGenerateOTPWithProvidedEmailAsEmptyString(self):
		"""
		Test Data : ""
		Expected Output: the function will return False
		"""

		generator = OTPGenerator("")
		otp = generator.generateOTP()

		self.assertIs(otp, False)

class HelperSendOTPEmailTest(TestCase):
	"""
	- The OTP EmailSender class constructor accepts one argument, which is the email receiver address
	- class method sendOTP requires an augument, the OTP to be encapsulate in the email body to send out
	"""
	def testSendEmailWithProvidedEmail(self):
		"""
		Test Data : cheongwaihong44@gmail.com
		OTP value : 123456

		Expected Result: A response object with a status_code of 202
		"""

		emailSender = EmailSender("cheongwaihong44@gmail.com")
		response = emailSender.sendOTP(123456);

		self.assertEqual(response.status_code, 202)

	def testSendEmailWithProvidedEmailAsEmptyString(self):
		"""
		Test Data : ""
		OTP value : 123456

		Expected Result: A response with False 
		"""

		emailSender = EmailSender("")
		response = emailSender.sendOTP(123456);

		self.assertIs(response, False)
