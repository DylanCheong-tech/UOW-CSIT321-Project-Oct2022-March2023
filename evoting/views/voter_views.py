# voter_views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from django.db.models import Q

# Models imports
from ..models import VoteEvent
from ..models import VoteOption
from ..models import Voter
from ..models import VotingPool

# Forms imports 
from ..forms.voter import VoteForm

# Helper module imports
from ..helpers.hasher import Hasher

# Homomorphic Encryption Module 
from ..homo_encryption import *

class VoterVoteForm(View):
	def get(self, request):

		try :

			# initialise the error message
			error_message = "Something went wrong ... "
			error_summary_message = "Bad Request Received"
			error_code = 400

			# check if the authentication infromation is provided 
			if (len(request.GET.getlist("auth")) != 1):
				error_message = "Access Link Invalid !"
				error_summary_message = "Bad Request Received"
				raise Exception

			# get the voter authentication information 
			auth_token = Hasher(request.GET["auth"]).messageDigest()

			# check the voter is exists, if not an exception will be raised 
			voter = Voter.objects.get(token=auth_token)

			# get the vote event which the voter associated 
			vote_event_id = voter.eventNo_id

			# get the vote event object 
			vote_event = VoteEvent.objects.get(eventNo=vote_event_id)

			# check if the vote event is in the Published state
			# voter will not be get access the PC event, in this state, no auth token will be generated for the voters 
			if (vote_event.status != "PB"):
				error_message = "Vote Event has been ended !"
				error_summary_message = "Forbidden Request !"
				error_code = 403
				raise Exception

			# check if the voter is casted the vote before 
			voter_voted_count = VotingPool.objects.filter(Q(eventNo_id=vote_event_id) & Q(voter_id=voter.id)).count()
			if voter_voted_count > 0:
				error_message = "Voter has been voted, no access allowed !"
				error_summary_message = "Forbidden Request Received"
				error_code = 403
				raise Exception

			vote_options = VoteOption.objects.filter(eventNo_id=vote_event_id)

			# get the private keys to decrypt the option name
			(private_key, salt) = read_private_key(vote_event.createdBy_id, vote_event_id)

			# organise the vote event information to be rendered on the page 
			vote_event_info = {
				"eventTitle" : decrypt_str(vote_event.eventTitle, private_key, salt),
				"eventQuestion" : decrypt_str(vote_event.eventQuestion, private_key, salt),
				"voteOptions" : [{"option" : decrypt_str(x.voteOption, private_key, salt), "encoding" : x.voteEncoding} for x in vote_options]
			}

			# organise the voter information to be rendered on the page 
			voter_info = {
				"name" : voter.name,
				"token" : voter.token
			}

			return render(request, "voter/vote_form.html", {"vote_event_info" : vote_event_info, "voter_info" : voter_info})


		except Voter.DoesNotExist:
			print("No Voter Information Founded !")
			error_message = "Voter Information Not Founded !"

		except VoteEvent.DoesNotExist:
			print("No Vote Event Information Founded !")
			error_message = "Vote Event Information Not Founded !"

		except Exception:
			print("Error occurred !")

		return render(request, "error_page.html", {"error_code" : error_code, "error_summary_message" : error_summary_message, "error_message" : error_message})
	

	def post(self, request):
		# obtain the form data
		form = VoteForm(request.POST)

		# initialise the error message
		error_message = "Something went wrong ... "
		error_summary_message = "Bad Request Received"
		error_code = 400

		if form.is_valid():
			data = form.cleaned_data

			try:
				# obtain the voter authentication token 
				auth_token = Hasher(data["voterAuth"]).messageDigest()

				# check the voter is exists, if not an exception will be raised 
				voter = Voter.objects.get(token=auth_token) 
				
				# get the vote event which the voter associated 
				vote_event_id = voter.eventNo_id

				# get the vote event object 
				vote_event = VoteEvent.objects.get(eventNo=vote_event_id)

				# check if the vote event is in the Published state
				# voter will not be get access the PC event, in this state, no auth token will be generated for the voters 
				if (vote_event.status != "PB"):
					error_message = "Invitation Link Expired !"
					error_summary_message = "Forbidden Request Received"
					error_code = 403
					raise Exception

				# check if the voter is casted the vote before 
				voter_voted_count = VotingPool.objects.filter(Q(eventNo_id=vote_event_id) & Q(voter_id=voter.id)).count()
				if voter_voted_count > 0:
					error_message = "Voter Has Already Voted !"
					error_summary_message = "Forbidden Request Received"
					error_code = 403
					raise Exception

				# write the casted vote option to the system database 
				vote_record = VotingPool(
					eventNo_id = vote_event_id,
					voter_id = voter.id,
					castedVote = data["voteOption"]
				)
				vote_record.save()

				return render(request, "voter/vote_form.html", {"vote_status" : "success"})

			except Voter.DoesNotExist:
				print("No Voter Information Founded !")
				error_message = "Invitation Link Invalid !"
				error_summary_message = "Unauthorized Request Received"
				error_code = 401

			except VoteEvent.DoesNotExist:
				print("No Vote Event Information Founded !")
				error_message = "Invitation Link Expired !"
				error_summary_message = "Unauthorized Request Received"
				error_code = 401

			except Exception:
				print("Error occurred !")

		else:
			error_message = "Vote Submission Invalid !"

		return render(request, "error_page.html", {"error_code" : error_code, "error_summary_message" : error_summary_message, "error_message" : error_message})

class VoterViewFinalResult(View):
	def get(self, request):
		
		try:

			# chec# initialise the error message
			error_message = "Something went wrong ... "
			error_summary_message = "Bad Request Received"
			error_code = 400

			# if the authentication infromation is provided 
			if (len(request.GET.getlist("auth")) != 1):
				error_message = "Access Link Invalid !"
				error_summary_message = "Bad Request Received"
				raise Exception

			# get the voter authentication information 
			auth_token = Hasher(request.GET["auth"]).messageDigest()
			print(auth_token)

			# check the voter is exists, if not an exception will be raised 
			voter = Voter.objects.get(token=auth_token) 

			# get the vote event which the voter associated 
			vote_event_id = voter.eventNo_id

			# get the vote event object 
			vote_event = VoteEvent.objects.get(eventNo=vote_event_id)

			# get the event owner id
			event_owner_id = vote_event.createdBy_id

			# check if the vote event is in the Result Published (RP) state
			# logically, the vote will not get pass to this point, 
			# due to the authentication token will be generated iff the event owner published the final result
			if (vote_event.status != "RP"):
				error_message = "Access Link Invalid !"
				error_summary_message = "Unauthorized Request Received"
				error_code = 401
				raise Exception

			vote_options = VoteOption.objects.filter(eventNo_id=vote_event_id)

			(private_key, salt) = read_private_key(event_owner_id, vote_event_id)

			# organise the vote event information to be rendered on the page 
			final_result_info = {
				"eventTitle" : decrypt_str(vote_event.eventTitle, private_key, salt),
				"eventQuestion" : decrypt_str(vote_event.eventQuestion, private_key, salt),
				"voteOptions" : [{"option" : decrypt_str(x.voteOption, private_key, salt), "counts" : int((decrypt_int(int(x.voteTotalCount), private_key) - salt) / int(salt))} for x in vote_options],
			}
			# get the majority vote option name
			final_result_info["majorVoteOption"] = max(final_result_info["voteOptions"], key=lambda k : k["counts"], default="None")["option"]

			return render(request, "voter/result_page.html", {"final_result_info": final_result_info})

		except Voter.DoesNotExist:
			print("No Voter Information Founded !")
			error_summary_message = "Unauthorized Request !"
			error_code = 401
			error_message = "Access Link Invalid !"

		except VoteEvent.DoesNotExist:
			print("No Vote Event Information Founded !")
			error_summary_message = "Unauthorized Request !"
			error_code = 401
			error_message = "Access Link Invalid !"

		except Exception:
			print("Error occurred !")

		return render(request, "error_page.html", {"error_code" : error_code, "error_summary_message" : error_summary_message, "error_message" : error_message})

