# hasher.py 

import hashlib

class Hasher:
	def __init__ (self, message):
		self.message = message

	def messageDigest(self):
		hasher = hashlib.md5()
		hasher.update(self.message)
		hashed_message = hasher.hexdigest()

		return hashed_message