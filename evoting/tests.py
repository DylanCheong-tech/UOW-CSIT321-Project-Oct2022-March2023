from django.test import TestCase
from django.utils import timezone

from .helpers.hasher import Hasher
from .helpers.otpGenerator import OTPGenerator
from .helpers.sendOTPEmail import EmailSender
from .helpers.passwordChecker import PasswordChecker
from .helpers.voterEmailChecker import VoterEmailChecker

from .models import OTPManagement
from .models import VoteEvent

# Sprint 1 Unit Tests
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

	def testCheckOTPIsMatchingByProvidingCorrectOTP(self):
		"""
		class method 'check_otp_matching' accepts one argument, OTP values as a String

		Test Data:
			- Email : abc@gmail.com
			- OTP : 543273
			- Expire Tiemstamp = django.utils.timezone.localtime() - django.utils.timezone.timedelta(minutes=5)
			- matching OTP values : 543273
		"""

		otp_record = OTPManagement()
		otp_record.email = "abc@gmail.com"
		otp_record.otp = 543273
		otp_record.expireAt = timezone.localtime() - timezone.timedelta(minutes=5)

		# assert is expired, True
		self.assertIs(otp_record.check_otp_matching("543273"), True)

	def testCheckOTPIsMatchingByProvidingIncorrectOTP(self):
		"""
		class method 'check_otp_matching' accepts one argument, OTP values as a String

		Test Data:
			- Email : abc@gmail.com
			- OTP : 543273
			- Expire Tiemstamp = django.utils.timezone.localtime() - django.utils.timezone.timedelta(minutes=5)
			- matching OTP values : 998273
		"""

		otp_record = OTPManagement()
		otp_record.email = "abc@gmail.com"
		otp_record.otp = 543273
		otp_record.expireAt = timezone.localtime() - timezone.timedelta(minutes=5)

		# assert is expired, True
		self.assertIs(otp_record.check_otp_matching("998273"), False)


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
	# def testSendEmailWithProvidedEmail(self):
	# 	"""
	# 	Test Data : cheongwaihong44@gmail.com
	# 	OTP value : 123456

	# 	Expected Result: A response object with a status_code of 202
	# 	"""

	# 	emailSender = EmailSender("cheongwaihong44@gmail.com")
	# 	response = emailSender.sendOTP(123456);

	# 	self.assertEqual(response.status_code, 202)

	# def testSendEmailWithProvidedEmailAsEmptyString(self):
	# 	"""
	# 	Test Data : ""
	# 	OTP value : 123456

	# 	Expected Result: A response with False 
	# 	"""

	# 	emailSender = EmailSender("")
	# 	response = emailSender.sendOTP(123456);

	# 	self.assertIs(response, False)


class HelperPasswordCheckerTest(TestCase):
	"""
	- The PasswordChecker provides a static method "validate_password", accepts an argument, which is the password sting to be checked 
	"""

	def testValidatePasswordWithValidPassword(self):
		"""
		Test Data : "Barbara*1123"

		Expected Result : True
		"""

		result = PasswordChecker.validate_password("Barbara*1123")

		self.assertIs(result, True)


	def testValidatePasswordWithShorterPassword(self):
		"""
		Test Data : "Barb*13"

		Test invalid format:
		-- Length = 7

		Expected Result : False
		"""

		result = PasswordChecker.validate_password("Barb*13")

		self.assertIs(result, False)


	def testValidatePasswordWithLongerPassword(self):
		"""
		Test Data : "*BarbaraCarlifonia*112366546352112134223"

		Test invalid format:
		-- Length = 40

		Expected Result : False
		"""

		result = PasswordChecker.validate_password("*BarbaraCarlifonia*112366546352112134223")

		self.assertIs(result, False)


	def testValidatePasswordWithSpacingPassword(self):
		"""
		Test Data : "Barbara *1123"

		Test invalid format:
		-- contains spacing

		Expected Result : False
		"""

		result = PasswordChecker.validate_password("Barbara *1123")

		self.assertIs(result, False)


	def testValidatePasswordWithNotContainUppercasePassword(self):
		"""
		Test Data : "barbara*1123"

		Test invalid format:
		-- not contains uppercase letter 

		Expected Result : False
		"""

		result = PasswordChecker.validate_password("barbara*1123")

		self.assertIs(result, False)

	def testValidatePasswordWithNotContainLowercasePassword(self):
		"""
		Test Data : "BARBARA*1123"

		Test invalid format:
		-- not contains lowercase letter 

		Expected Result : False
		"""

		result = PasswordChecker.validate_password("BARBARA*1123")

		self.assertIs(result, False)

	def testValidatePasswordWithNotContainSpecialCharacterPassword(self):
		"""
		Test Data : "Barbara1123"

		Test invalid format:
		-- not contains special character  

		Expected Result : False
		"""

		result = PasswordChecker.validate_password("Barbara1123")

		self.assertIs(result, False)

	def testValidatePasswordWithNotContainDigitPassword(self):
		"""
		Test Data : "Barbara_Password"

		Test invalid format:
		-- not contains digit

		Expected Result : False
		"""

		result = PasswordChecker.validate_password("Barbara_Password")

		self.assertIs(result, False)

	def testValidatePasswordWithInvalidPassword(self):
		"""
		Test Data : "Barbara_Password"

		Test invalid format:
		-- not contains uppercase letter 
		-- not contains special character 
		-- contains spacing

		Expected Result : False
		"""

		result = PasswordChecker.validate_password("Barbara_Password")

		self.assertIs(result, False)


# Sprint 2 Unit Tests 

class ModelVoteEventTest(TestCase):
	"""
	- Vote Event Model class stores all the information about a vote event 
	- The relationship between vote options and vote emails are one to many 

	Vote event have a start datetime and a end datetime value, these value must be make sense when creating a vote event record
	Valid Datetime settings:
	- start datetime is current or after the timestamp when creating 
	- end datetime must be before the start datetime 
	"""

	def testDateTimeIsValid(self):
		"""
		(Time aware testing: make sure the start datetime value is after the timestamp when performing the test)

		Test Data: 
		- Start Date: 2024-06-18
		- Start Time: 18:00
		- End Date: 2024-06-30
		- End Time: 18:00

		Expected Result: True
		"""

		vote_event = VoteEvent()
		vote_event.startDate = "2024-06-18"
		vote_event.startTime = "18:00"
		vote_event.endDate = "2024-06-30"
		vote_event.endTime = "18:00"

		self.assertIs(vote_event.is_event_datetime_valid(), True)

	def testDateTimeIsNotValidByPreviousStartDateTime(self):
		"""
		(Time aware testing: make sure the start datetime value is before the timestamp when performing the test)

		Test Data: 
		- Start Date: 2020-06-18
		- Start Time: 18:00
		- End Date: 2020-06-30
		- End Time: 18:00
		"""

		vote_event = VoteEvent()
		vote_event.startDate = "2020-06-18"
		vote_event.startTime = "18:00"
		vote_event.endDate = "2020-06-30"
		vote_event.endTime = "18:00"

		self.assertIs(vote_event.is_event_datetime_valid(), False)

	def testDateTimeIsNotValidByEndDateTimeBeforeStartDateTime(self):
		"""
		(Time aware testing: make sure the start datetime value is after the timestamp when performing the test)
		Condition: The Start Date Time must be current or after the timestamp when executing the test


		Test Data: 
		- Start Date: 2023-06-18
		- Start Time: 15:00
		- End Date: 2020-06-17
		- End Time: 11:00
		"""

		vote_event = VoteEvent()
		vote_event.startDate = "2023-06-18"
		vote_event.startTime = "15:00"
		vote_event.endDate = "2023-06-17"
		vote_event.endTime = "11:00"

		self.assertIs(vote_event.is_event_datetime_valid(), False)


class HelperVoterEmailCheckerTest(TestCase):
	"""
	VoterEmailChecker class has a static method named 'VoterEmailChecker'
	This static method accepts one argument as a 2d list of name and email and return two dictionary objects, valid emails and non-valid emails respectively 
	"""

	def testCheckEmailsByProvidingAllCorrectEmails(self):
		"""
		Test Data:
		Emails : [
			[Alice1 , alice@mail.com],
			[Alice2 , alice@mail.au.edu],
			[Alice3 , alice.uow.csit@mail.com],
			[Alice4 , alice-csit@mail.com],
			[Alice5 , alice1234@mail.com],
			[Alice6 , alice-1234.csit@mail.com]
		]

		Expected Result: All names and emails present in the 'valid_emails' dictionary, no item entry in 'non_valid_emails''
		"""

		emails = [
			["Alice1" , "alice@mail.com"],
			["Alice2" , "alice@mail.au.edu"],
			["Alice3" , "alice.uow.csit@mail.com"],
			["Alice4" , "alice-csit@mail.com"],
			["Alice5" , "alice1234@mail.com"],
			["Alice6" , "alice-1234.csit@mail.com"]
		]

		valid_emails, non_valid_emails = VoterEmailChecker.checkEmails(emails)

		self.assertEqual(len(valid_emails.items()), 6)
		self.assertEqual(len(non_valid_emails.items()), 0)

	def testCheckEmailsByProvidingAllIncorrectEmails(self):
		"""
		Test Data:
		Emails : [
			[Alice1 , alice-@mail.com],
			[Alice2 , alice@mail..au..edu],
			[Alice3 , alice..uow..csit@mail.com],
			[Alice4 , .alice-csit@mail.com],
			[Alice5 , alice1234@mail#csit.com],
			[Alice6 , alice#1234.csit@mail.com],
			[Alice7 , alice_1234.csit@mail.com.y]
		]

		Expected Result: All names and emails present in the 'non_valid_emails' dictionary, no item entry in 'valid_emails''
		"""

		emails = [
			["Alice1" , "alice-@mail.com"],
			["Alice2" , "alice@mail..au..edu"],
			["Alice3" , "alice..uow..csit@mail.com"],
			["Alice4" , ".alice-csit@mail.com"],
			["Alice5" , "alice1234@mail#csit.com"],
			["Alice6" , "alice#1234.csit@mail.com"],
			["Alice7" , "alice_1234.csit@mail.com.y"]
		]

		valid_emails, non_valid_emails = VoterEmailChecker.checkEmails(emails)

		self.assertEqual(len(valid_emails.items()), 0)
		self.assertEqual(len(non_valid_emails.items()), 7)

	def testCheckEmailsByProvidingMultipleEmailCases(self):
		"""
		Test Data:
		Emails : [
			[Alice1 , alice1234@mail.com],
			[Alice2 , alice@mail.au#edu],
			[Alice3 , alice-uow-csit@mail.com],
			[Alice4 , .alice.csit@mail.com],
			[Alice5 , alice1234@mail.csit.com.au],
			[Alice6 , alice-csit.csit@mail_csit.com],
			[Alice7 , alice_1234.csit@mail.com.y]
		]

		Expected Result: All names and emails present in the 'non_valid_emails' dictionary, no item entry in 'valid_emails''
		"""

		emails = [
			["Alice1" , "alice1234@mail.com"],
			["Alice2" , "alice@mail.au#edu"],
			["Alice3" , "alice-uow-csit@mail.com"],
			["Alice4" , ".alice.csit@mail.com"],
			["Alice5" , "alice1234@mail.csit.com.au"],
			["Alice6" , "alice-csit.csit@mail_csit.com"],
			["Alice7" , "alice_1234.csit@mail.com.y"]
		]

		valid_emails, non_valid_emails = VoterEmailChecker.checkEmails(emails)

		print(valid_emails)
		print(non_valid_emails)

		self.assertEqual(len(valid_emails.items()), 3)
		self.assertEqual(len(non_valid_emails.items()), 4)

		assert_valid_emails = {
			"Alice1" : "alice1234@mail.com",
			"Alice3" : "alice-uow-csit@mail.com",
			"Alice5" : "alice1234@mail.csit.com.au",
		}

		assert_non_valid_emails = {
			"Alice2" : "alice@mail.au#edu",
			"Alice4" : ".alice.csit@mail.com",
			"Alice6" : "alice-csit.csit@mail_csit.com",
			"Alice7" : "alice_1234.csit@mail.com.y"
		}

		self.assertEqual(valid_emails, assert_valid_emails)
		self.assertEqual(non_valid_emails, assert_non_valid_emails)