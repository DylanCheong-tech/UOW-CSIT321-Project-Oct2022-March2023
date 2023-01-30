from django.test import TestCase
from django.utils import timezone

from .helpers.hasher import Hasher
from .helpers.otpGenerator import OTPGenerator
from .helpers.emailSender import EmailSender
from .helpers.passwordChecker import PasswordChecker
from .helpers.voterEmailChecker import VoterEmailChecker
from .helpers.tallyJobScheduler import JobScheduler
from .helpers.voterAuthentication import VoterAuthentication

from .models import OTPManagement
from .models import VoteEvent

from .homo_encryption import *

import rsa
import random
from datetime import datetime
import mysql.connector
import threading 

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


# Sprint 3 Unit Tests

class HomomorphicEncryptionModuleTest(TestCase):
	"""
	This homomorphic module consists the core functions for security encryption on the voting information. 
	There are 10 functions within this module
	"""

	def testReadExistingPrivateKey(self):
		"""
		Test Data:
		- event owner id : 4
		- vote event id : 35

		Expected Result:
			The Private Key and salt value will be returned to the caller
		"""

		(private, salt) = read_private_key(4, 35)

		self.assertIsInstance(private, rsa.PrivateKey)
		self.assertIsInstance(salt, int)

	def testReadNonExistingPrivateKey(self):
		"""
		Test Data:
		- event owner id : 4
		- vote event id : 45

		Expected Result:
			A tuple of None will be return 
		"""

		(private, salt) = read_private_key(4, 45)

		self.assertEqual(private, None)
		self.assertEqual(salt, None)

	def testKeyGeneration(self):
		"""
		Test Data:
		- event owner id : 999
		- vote event id : 259
		- key_size : 1024

		Expected Result: 
			A pair of cryptographic keys, salt value are generates. 
			Private key and salt value will be written into the key file.
			Public key and salt value will be returned to the caller 
		"""

		(public, salt) = key_generation(999, 259, 1024)

		self.assertIsInstance(public, rsa.PublicKey)
		self.assertIsInstance(salt, int)

		(_, salt_from_file) = read_private_key(999, 259)

		self.assertEqual(salt, salt_from_file)


	def testRemoveExistingPrivateKey(self):
		"""
		Test Data:
		- event owner id : 999
		- vote event id : 259

		Expected Result : The private key and salt value will be removed from the key file, no value can be retreiveid after removal
		"""

		remove_status = remove_private_key(999, 259)

		self.assertIs(remove_status, True)

		(private, salt) = read_private_key(999, 259)

		self.assertEqual(private, None)
		self.assertEqual(salt, None)


	def testRemoveNonExistingPrivateKey(self):
		"""
		Test Data:
		- event owner id : 998
		- vote event id : 234

		Expected Result : No removal action will be taken 
		"""

		remove_status = remove_private_key(998, 234)

		self.assertIs(remove_status, False)

		(private, salt) = read_private_key(998, 234)

		self.assertEqual(private, None)
		self.assertEqual(salt, None)


	def testGenerateOptionEncoding(self):
		"""
		Test Data:
		- Number of Vote Options : 3
		- Salt value : based on the key generation 

		A pair of keys will be generated before generate the vote option, in the end of this test, the generated keys will be removed

		Expected Result: 
			Return a list of specified number of vote options encoding values
			All the option (prime) value are multiplied by salt value
		"""

		(public, salt) = key_generation(567, 567, 1024)
		(private, _) = read_private_key(567, 567)

		option_encodings = vote_option_encoding_generation(3, salt)
		self.assertEqual(len(option_encodings), 3)

		prime_list = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

		for encoding in option_encodings:
			prime = int(encoding / salt)
			self.assertIs(prime in prime_list, True)

		remove_private_key(567, 567)


	def testGeneratePaddingValues(self):
		"""
		Test Data :
		- salt : 564

		Expected Resuts:
			Resutl a string with length of (564 % 8) = 4 random characters and digits value
		"""

		padding_value = padding_values_generation(564)

		self.assertEqual(len(padding_value), 4)


	def testIntegerEncryptionAndDecryptionOnSameKeys(self):
		"""
		Test Data:
		- Value : 18
		- public key : based on the key generation 
		- private key : based on the key generation 

		Exoected Result : 
			The Encryption should produce a cipher as integer (a bunch of digits)
			The Decryption should be able to reveal back the original value as integer from the cipher 
		"""

		(public, _) = key_generation(567, 567, 1024)
		(private, _) = read_private_key(567, 567)

		cipher = encrypt_int(18, public)

		self.assertIsInstance(cipher, int)

		plaintext = decrypt_int(cipher, private)
		
		self.assertIsInstance(plaintext, int)
		self.assertEqual(plaintext, 18)

		remove_private_key(567, 567)


	def testIntegerEncryptionAndDecryptionOnDifferentKeys(self):
		"""
		Test Data:
		- Value : 45
		- public key : based on the key generation 
		- private key : based on the key generation 

		Exoected Result : 
			The Encryption should produce a cipher as integer (a bunch of digits)
			The Decryption will be produced a integer value 
			The Decryption would not be able to reveal back the original value from the cipher 
		"""

		(public_1, _) = key_generation(567, 567, 1024)

		key_generation(234, 234, 1024)
		(private_2, _) = read_private_key(234, 234)

		cipher = encrypt_int(18, public_1)

		self.assertIsInstance(cipher, int)

		plaintext = decrypt_int(cipher, private_2)

		self.assertIsInstance(plaintext, int)
		self.assertNotEqual(plaintext, 45)

		remove_private_key(567, 567)
		remove_private_key(234, 234)


	def testStringEncryptionAndDecryptionOnSameKeys(self):
		"""
		Test Data:
		- Value : Secret Message !
		- public key : based on the key generation 
		- private key : based on the key generation 

		Exoected Result : 
			The Encryption should produce a cipher as bytes
			The Decryption should be able to reveal back the original value as string from the cipher 
		"""

		(public, salt_1) = key_generation(567, 567, 1024)
		(private, salt_2) = read_private_key(567, 567)

		cipher = encrypt_str("Secret Message !", public, salt_1)

		self.assertIsInstance(cipher, bytes)

		plaintext = decrypt_str(cipher, private, salt_2)
		
		self.assertIsInstance(plaintext, str)
		self.assertEqual(plaintext, "Secret Message !")

		remove_private_key(567, 567)


	def testStringEncryptionAndDecryptionOnDifferentKeys(self):
		"""
		Test Data:
		- Value : Another Secret Message !
		- public key : based on the key generation 
		- private key : based on the key generation 

		Exoected Result : 
			The Encryption should produce a cipher as bytes 
			The Decryption will be produced a string value 
			The Decryption would not be able to reveal back the original value from the cipher 
		"""

		(public_1, salt_1) = key_generation(567, 567, 1024)

		key_generation(234, 234, 1024)
		(private_2, salt_2) = read_private_key(234, 234)

		cipher = encrypt_str("Another Secret Message !", public_1, salt_1)

		self.assertIsInstance(cipher, bytes)

		self.assertRaisesMessage(rsa.pkcs1.DecryptionError, "Decryption failed", decrypt_str, cipher, private_2, salt_2, )

		remove_private_key(567, 567)
		remove_private_key(234, 234)


	def testTallyCastedVote(self):
		"""
		Test Data:
		- vote options : 3
		- voted_list : 23, value based on the encryption key

		Expected Result:
			Return a list with three encrypted subresult, as each for 10 votes, and a number of tallied votes
		"""

		(public, salt) = key_generation(567, 567, 1024)

		# generate the vote options encodings
		vote_options = vote_option_encoding_generation(3, salt)

		voted_list = [encrypt_int(random.choice(vote_options), public) for x in range(23)]

		result_list, tallied_votes = homo_counting(voted_list)

		self.assertEqual(len(result_list), 3)
		self.assertEqual(tallied_votes, 23)

		remove_private_key(567, 567)


	def testResultCountingWithMatchingKeys(self):
		"""
		Test Data:
		- vote options list (in primes) : [3, 5, 7]
		- voted list : 13 x "3", 15 x "5", and 9 x "7"
		- subresult list : value depended on the encryption key 
		- total tallied votes : 23

		Expected Result: 
			Resutl a dictionary for each counting of vote option 
		"""

		(public, salt) = key_generation(567, 567, 1024)
		(private, _) = read_private_key(567, 567)

		vote_options = [encrypt_int(x * salt, public) for x in [3, 5, 7]]

		# create a voted data list and shuffle 
		voted_list = [vote_options[0]] * 13 + [vote_options[1]] * 15 + [vote_options[2]] * 9
		random.shuffle(voted_list)

		result_list, tallied_votes = homo_counting(voted_list)

		result_dict = result_counting(vote_options, result_list, tallied_votes, private, salt)

		self.assertEqual(len(result_dict.items()), 3)
		self.assertEqual(result_dict[str(vote_options[0])], 13)
		self.assertEqual(result_dict[str(vote_options[1])], 15)
		self.assertEqual(result_dict[str(vote_options[2])], 9)


class HelperJobSchedulerTest(TestCase):
	"""
	This helper module responsible to perform the tally job based on the given time (future)

	"""

	def testGetAScheduleTimeByProvidingAFutureTime(self):
		"""
		Test Data:
		- datetime : (python datetime object) 12-10-2024 15:00

		Expected Result:
			return a value of seconds as positive integer from the current running datetime 
		"""

		future_datetime = datetime(2024, 10, 12, 15, 0)
		scheduled_seconds = JobScheduler().get_schedule_time(future_datetime)

		self.assertIs(scheduled_seconds > 0, True)


	def testGetAScheduleTimeByProvidingAPassedTime(self):
		"""
		Test Data:
		- datetime : (python datetime object) 21-08-2020 18:00

		Expected Result:
			return a invalid value of seconds as negative integer from the current running datetime 
		"""

		future_datetime = datetime(2020, 8, 21, 18, 0)
		scheduled_seconds = JobScheduler().get_schedule_time(future_datetime)

		self.assertIs(scheduled_seconds > 0, False)


	def testScheduleATaskEventWithValidDateTime(self):
		"""
		Test Data : 
		- event owner id : 123
		- Event ID : 45
		- schedule time : 2023-09-14 15:00 (future date)

		Expected Result:
			A scheduled task will be created and added into the job tracker dictionary object 
		"""

		job_scheduler = JobScheduler()
		schedule_time = job_scheduler.get_schedule_time(datetime(2023, 9, 14, 15, 0))
		status = job_scheduler.schedule_event(123, 45, schedule_time)

		# the job_tracker is from the module itself
		self.assertIs(status, True)
		self.assertIsInstance(job_scheduler.get_schedule_event(45), threading.Timer)
		self.assertIs(job_scheduler.get_schedule_event(45).is_alive(), True)

		job_scheduler.cancel_scheduled_event(45)


	def testScheduleATaskEventWithNonValidDateTime(self):
		"""
		Test Data : 
		- event owner id : 123
		- Event ID : 45
		- schedule time : 2020-09-14 15:00 (future date)

		Expected Result:
			A scheduled task will be created and added into the job tracker dictionary object 
		"""

		job_scheduler = JobScheduler()
		schedule_time = job_scheduler.get_schedule_time(datetime(2020, 9, 14, 15, 0))
		status = job_scheduler.schedule_event(123, 45, schedule_time)

		# the job_tracker is from the module itself
		self.assertIs(status, False)
		self.assertEqual(job_scheduler.get_schedule_event(45), None)

	def testGetAnExistingScheduledTaskEvent(self):
		"""
		Test Data : 
		- Event ID : 134
		- The Schedule Task is created 

		Expected Result:
			Returns a Timer object of the scheduled task event 
		"""

		job_scheduler = JobScheduler()
		schedule_time = job_scheduler.get_schedule_time(datetime(2023, 9, 14, 15, 0))
		status = job_scheduler.schedule_event(123, 134, schedule_time)

		# make sure the taks event is created
		self.assertIs(status, True)

		self.assertIsInstance(job_scheduler.get_schedule_event(134), threading.Timer)

		job_scheduler.cancel_scheduled_event(134)


	def testGetANonExistingScheduledTaskEvent(self):
		"""
		Test Data : 
		- Event ID : 145
		- The Schedule Task is not created 

		Expected Result:
			Returns a Timer object of the scheduled task event 
		"""

		job_scheduler = JobScheduler()

		self.assertEqual(job_scheduler.get_schedule_event(134), None)


	def testCancelAnExistingScheduledTaskEvent(self):
		"""
		Test Data : 
		- Event ID : 45
		- The event is created for the purpose to cancel 

		Expected Result : 
			A Scheduled task will be cancel and removed from the job tracker list 
			Return a boolean True value indicates as successful cancellation 
		"""

		job_scheduler = JobScheduler()
		schedule_time = job_scheduler.get_schedule_time(datetime(2023, 9, 14, 15, 0))
		status = job_scheduler.schedule_event(123, 45, schedule_time)

		# make sure the taks event is created
		self.assertIs(status, True)

		cancel_status = job_scheduler.cancel_scheduled_event(45)

		self.assertIs(cancel_status, True)
		self.assertEqual(job_scheduler.get_schedule_event(45), None)


	def testCancelANonExistingScheduledTaskEvent(self):
		"""
		Test Data : 
		- Event ID : 45
		- The event is not created

		Expected Result : 
			No actions are taken 
			Return a boolean False value indicates as fail cancellation 
		"""

		job_scheduler = JobScheduler()

		cancel_status = job_scheduler.cancel_scheduled_event(45)

		self.assertIs(cancel_status, False)
		self.assertEqual(job_scheduler.get_schedule_event(45), None)


class HelperVoterAuthenticationHelperTest(TestCase):
	"""
	This helper module responsible to generate the authentication string for voter to access the voting booth and final result booth 

	"""

	def testGenerateTokenString(self):
		"""
		Test Data : None

		Expected Results:
			Returns a random string with length of 64
		"""

		token = VoterAuthentication.generateTokenString()

		self.assertEqual(len(token), 64)


class HelperEmailSenderTest(TestCase):
	"""
	In this sprint increment, the Email Sender helper class added two new functions.
	- Send out the vote invitation link 
	- Send out the view final result access link 
	"""

	def testSendInvitationEmailWithProvidedEmail(self):
		"""
		Test Data : 
		- email : cheongwaihong44@gmail.com
		- host : www.evoting.com
		- auth : 123456789
		- voter name : Dylan
		- event owner name : James Smith
		- vote event name : Are you a vegetarian or vegan ? 

		Expected Result: A response object with a status_code of 202
		"""

		emailSender = EmailSender("cheongwaihong44@gmail.com")
		response = emailSender.sendInvitation("www.evoting.com", "123456789", "Dylan", "James Smith", "Are you a vegetarian or vegan ?");

		self.assertEqual(response.status_code, 202)

	def testSendInvitationEmailWithProvidedEmailAsEmptyString(self):
		"""
		Test Data : 
		- email : cheongwaihong44@gmail.com
		- host : www.evoting.com
		- auth : 123456789
		- voter name : Dylan
		- event owner name : James Smith
		- vote event name : Are you a vegetarian or vegan ? 

		Expected Result: A response with False 
		"""

		emailSender = EmailSender("")
		response = emailSender.sendInvitation("www.evoting.com", "123456789", "Dylan", "James Smith", "Are you a vegetarian or vegan ?");

		self.assertIs(response, False)


	def testSendFinalResultAccessLinkEmailWithProvidedEmail(self):
		"""
		Test Data : 
		- email : cheongwaihong44@gmail.com
		- host : www.evoting.com
		- auth : 123456789
		- voter name : Dylan
		- event owner name : James Smith

		Expected Result: A response object with a status_code of 202
		"""

		emailSender = EmailSender("cheongwaihong44@gmail.com")
		response = emailSender.sendFinalResult("www.evoting.com", "123456789", "Dylan", "Are you a vegetarian or vegan ?");

		self.assertEqual(response.status_code, 202)

	def testSendFinalResultAccessLinkEmailWithProvidedEmailAsEmptyString(self):
		"""
		Test Data : 
		- email : cheongwaihong44@gmail.com
		- host : www.evoting.com
		- auth : 123456789
		- voter name : Dylan
		- event owner name : James Smith

		Expected Result: A response with False 
		"""

		emailSender = EmailSender("")
		response = emailSender.sendFinalResult("www.evoting.com", "123456789", "Dylan", "Are you a vegetarian or vegan ?");

		self.assertIs(response, False)




