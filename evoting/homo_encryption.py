# homo_encryption.py 

"""
This module consists of all the core functionalities of Homomorphic Encryption. 
We will be using RSA cryptosystem as the encryption scheme and utilize its key generation function. 

This module covers the following functions:
- Key Generation with writing the private key to the local file system 
- Private Keys file reader 
- Encryption 
- Decryption 
- Multiplicative Homomorphic Operation 
- Vote Counting 
"""

# rsa module library 
import rsa 
import csv 
import os

"""
Function : Key Generation
Parameter(s) : int : event owner id, int : vote event id, int : Key Size  
Return(s) : rsa.PublicKey

rsa.PublicKey consists of "n" and "e"
rsa.PrivateKey consists of "n", "e", "d", "p", "q"

This function will write the public key to the localfile system as csv file
"""
def key_generation(event_owner_id:int, vote_event_id:int, key_size:int) -> rsa.PublicKey:
	public, private = rsa.newkeys(key_size)

	keys_file = open(os.getcwd() + "/evoting/.private", "a")
	file_writer = csv.writer(keys_file)

	file_writer.writerow([event_owner_id, vote_event_id, private["n"], private["e"], private["d"], private["p"], private["q"]])

	return public

"""
Function : Private Key File Reader
Parameter(s) : int : event owner id, int : vote event id
Return(s) : rsa.PrivateKey
"""
def read_private_key(event_owner_id:int, vote_event_id:int) -> rsa.PrivateKey:
	keys_file = open(os.getcwd() + "/evoting/.private", "r")
	file_reader = csv.reader(keys_file)

	for row in file_reader:
		if (int(row[0]) == event_owner_id and int(row[1]) == vote_event_id):
			return rsa.PrivateKey(int(row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[6]))

"""
Function: Encryption 
Parameter(s) : int : value to be encrypted, int : "e" from public key, int : "n" from public key
Return(s) : int : encrypted value, cipher

Algorithm:
cipher = (message) ^ e modulo n
"""
def encrypt(value:int, e:int, n:int) -> int:
	return pow(value, e, n)

"""
Function: Decryption  
Parameter(s) : int : value to be decrypted, cipher, int : "d" from private key, int : "n" from private key
Return(s) : int : messsage/original value 

Algorithm:
value/message = (cipher) ^ d modulo n
"""
def decrypt(cipher:int, d:int, n:int) -> int:
	return pow(cipher, d, n)


"""
Function: Multiplicative Homomorphic Operation (Vote Tally Process)
Parameter(s) : list : list of individual encrypted values 
Return(s) : list : subresult for every 10 values

Algorithm:
For every 10 records, do:
	subresult = enc_value_1 * enc_value_2 * ... * enc_value_10
	append the subresult into the list 
return the list
"""
def homo_counting(casted_votes:list) -> list:
	return_list = []
	subresult = 1

	for index, vote in zip(range(len(casted_votes)), casted_votes):
		subresult = subresult * vote

		if (index + 1) % 10 == 0:
			return_list.append(subresult)
			subresult = 1


	if subresult != 1:
		return_list.append(subresult)

	return return_list


"""
Function: Vote Result Counting 
Parameter(s) : list: all the original vote option value, list : subresults, d : int, n : int
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
def result_counting(vote_options:list, subresults:list, d:int, n:int) -> dict:
	return_dict = {}

	for subresult in subresults:
		decrypted_subresult = decrypt(subresult, d, n)
		for option in vote_options:
			while (decrypted_subresult != 1 and decrypted_subresult % option == 0):
				return_dict[str(option)] = return_dict.get(str(option), 0) + 1
				decrypted_subresult = decrypted_subresult / option

	return return_dict


