# voterEmailChecker.py

import re 

class VoterEmailChecker:

	@staticmethod
	def checkEmails(emailList):
		valid_email = {}
		invalid_email = {}

		for x in emailList:
			if re.match(r'[^@]+@[^@]+\.[^@]+', x[1]):
				valid_email[x[0]] = x[1]
			else:
				invalid_email[x[0]] = x[1]

		return valid_email, invalid_email
