# homo_encryption.py 

"""
This module consists of all the core functionalities of Homomorphic Encryption. 
We will be using RSA cryptosystem as the encryption scheme and utilize its key generation function. 

This module covers the following functions:
- Key Generation with writing the private key to the local file system 
- Private Keys file reader 
- Vote Option Encoding 
- Encryption 
- Decryption 
- Multiplicative Homomorphic Operation 
- Vote Counting 
"""

# rsa module library 
import rsa 
import csv 
import os
import random 

"""
Function : Key Generation
Parameter(s) : int : event owner id, int : vote event id, int : Key Size  
Return(s) : rsa.PublicKey, int : salt

rsa.PublicKey consists of "n" and "e"
rsa.PrivateKey consists of "n", "e", "d", "p", "q"

A salt number will be generated for the vote option encryption
This function will write the private key and the salt to the localfile system as csv file
"""
def key_generation(event_owner_id:int, vote_event_id:int, key_size:int) -> (rsa.PublicKey, int):
	public, private = rsa.newkeys(key_size)

	keys_file = open(os.getcwd() + "/evoting/.private", "a")
	file_writer = csv.writer(keys_file)

	salt = random.randint(10, 999)

	file_writer.writerow([event_owner_id, vote_event_id, private["n"], private["e"], private["d"], private["p"], private["q"], salt])

	return (public, salt)

"""
Function : Private Key File Reader
Parameter(s) : int : event owner id, int : vote event id
Return(s) : rsa.PrivateKey and the salt number
"""
def read_private_key(event_owner_id:int, vote_event_id:int) -> (rsa.PrivateKey, int):
	keys_file = open(os.getcwd() + "/evoting/.private", "r")
	file_reader = csv.reader(keys_file)

	for row in file_reader:
		if (int(row[0]) == event_owner_id and int(row[1]) == vote_event_id):
			return (rsa.PrivateKey(int(row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[6])), int(row[7]))

"""
Function : Vote Option Encoding 
Parameter(s) : int : number of options need to encode, int : salt value
Return(s) : list : generated encoding values

Vote option will be encoded by randomly selecting a prime number in between 11 to 97 and multiply the prime with the salt value 
"""
def vote_option_encoding_generation(vote_options_num:int, salt:int) -> list :
	prime_list = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

	return_list = []

	for i in range(vote_options_num):
		prime = random.choice(prime_list)
		return_list.append(prime * salt)
		prime_list.remove(prime)

	return return_list


"""
Function: Encryption 
Parameter(s) : int : value to be encrypted, rsa.PublicKey : public key
Return(s) : int : encrypted value, cipher

Algorithm:
cipher = (message) ^ e modulo n
"""
def encrypt(value:int, public:rsa.PublicKey) -> int:
	return pow(value, public["e"], public["n"])

"""
Function: Decryption  
Parameter(s) : int : value to be decrypted, cipher, rsa.PrivateKey : private key
Return(s) : int : messsage/original value 

Algorithm:
value/message = (cipher) ^ d modulo n
"""
def decrypt(cipher:int, private:rsa.PrivateKey) -> int:
	return pow(cipher, private["d"], private["n"])


"""
Function: Multiplicative Homomorphic Operation (Vote Tally Process)
Parameter(s) : list : list of individual encrypted values 
Return(s) : list : subresult for every 10 values, int : total number of votes counted in 

Algorithm:
For every 10 records, do:
	subresult = enc_value_1 * enc_value_2 * ... * enc_value_10
	append the subresult into the list 
return the list
"""
def homo_counting(casted_votes:list) -> (list, int):
	return_list = []
	subresult = 1
	counted_vote = 0

	for index, vote in zip(range(len(casted_votes)), casted_votes):
		subresult = subresult * vote
		counted_vote = counted_vote + 1

		if (index + 1) % 10 == 0:
			return_list.append(subresult)
			subresult = 1


	if subresult != 1:
		return_list.append(subresult)

	return return_list, counted_vote


"""
Function: Vote Result Counting 
Parameter(s) : list: all the original vote option value, list : subresults, int: total number of voted counted in, int : d, int : n, int : the salt number generated in the key_generation function 
Return(s) : dict :  key-value of orginal value and it counting 

Algorithm: 
For every subresult in the list, do:
	decrypt the subresult 
	For each vote option value in the list, do
		Loop while subresult module vote option value equals 0
			increment the vote option counter 
			divide the subresult with the vote option value 
			add the key-value of the vote option and the counting into the dict 
"""
def result_counting(vote_options:list, subresults:list, total_counted_vote:int, private:rsa.PrivateKey, salt:int) -> dict:
	return_dict = {}

	for index, subresult in zip(range(len(subresults)), subresults):
		decrypted_subresult = decrypt(subresult, private)

		# removing the salt value from the subresults
		if index == len(subresults) - 1:
			decrypted_subresult = decrypted_subresult / pow(salt, total_counted_vote % 10)
		else:
			decrypted_subresult = decrypted_subresult / pow(salt, 10)

		for option in vote_options:
			# get the original option encoding (prime number)
			decrypted_option = int(decrypt(option, private) / salt)
			while (decrypted_subresult != 1 and decrypted_subresult % decrypted_option == 0):
				return_dict[str(option)] = return_dict.get(str(option), 0) + 1
				decrypted_subresult = decrypted_subresult / decrypted_option

	return return_dict