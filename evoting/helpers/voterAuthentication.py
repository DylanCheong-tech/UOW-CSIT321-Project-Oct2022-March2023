# voterAuthentication.py 

import random
import string

class VoterAuthentication:
	"""
	This VoterAuthentication module handles all the voter authentication features.
	It consists of :
	- authentication token generation 
	"""

	@staticmethod
	def generateTokenString():
		"""
		Generates a toke string in length of 64
		"""
		return "".join(random.choices(string.ascii_letters + string.digits, k=64))

