# passwordChecker.py 

import re

class PasswordChecker:
	"""
	This Password Checker check the input againt the pre-defined password policy 

	Password Policy:
	1. Minimum length with 8 
	2. Maximum lenght with 32 
	3. No Spacing 
	4. Contains at least one Uppercase letter 
	5. Contains at least one Lowercase letter 
	6. Contains at least one Special Character 
	7. Contains at least on digit 

	"""
	@staticmethod
	def validate_password(password):
		if re.match('^(?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9])(?=\S*?[#?!@$%^&*-]).{8,32}$', password):
			return True
		else:
			return False