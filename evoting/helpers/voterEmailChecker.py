# voterEmailChecker.py

import re 

class VoterEmailChecker:

	@staticmethod
	def checkEmails(emailList):
		valid_email = {}
		invalid_email = {}

		for x in emailList:
			if re.match(r'^[A-Za-z0-9]+([_\.-][A-za-z0-9]+)*@[A-Za-z0-9]+(-[A-Za-z0-9]+)*(\.[A-Za-z0-9]+(-[A-Za-z0-9]+)*)*(\.[A-Za-z]{2,})$', x[1].strip()):
				valid_email[x[0]] = x[1]
			else:
				invalid_email[x[0]] = x[1]

		return valid_email, invalid_email
