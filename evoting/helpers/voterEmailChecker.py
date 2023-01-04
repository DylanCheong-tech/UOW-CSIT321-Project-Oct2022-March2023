# voterEmailChecker.py

import re 

class VoterEmailChecker:

	@staticmethod
	def checkEmails(emailDict):
		valid_email = {}
		invalid_email = {}

		for x in emailDict:
			if re.match(r'[^@]+@[^@]+\.[^@]+', x[1]):
				valid_email[x[0]] = x[1]
			else:
				invalid_email[x[0]] = x[1]


		return valid_email, invalid_email
