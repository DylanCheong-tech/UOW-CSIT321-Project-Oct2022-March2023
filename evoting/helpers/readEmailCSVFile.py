# readEmailCSVFile.py 

class EmailCSVReader:
	def __init__(self, file):
		# this file is the request.FILES object, UploadedFile object 
		self.file = file

	def getVoterEmailsDict(self):
		voterEmails = ""
		for x in self.file.chunks():
			voterEmails += str(x)

		# remove the 'b' and the single quotes
		voterEmails = voterEmails[2:len(voterEmails)-1]
		voterEmails = voterEmails.replace('\\r', '')
		# voterEmails = voterEmails.replace('\\n', ',')

		# split the list 
		voterEmailList = voterEmails.split("\\n")
		voterEmailDict = { item.split(",")[0] : item.split(",")[1] for item in voterEmailList}

		return voterEmailDict