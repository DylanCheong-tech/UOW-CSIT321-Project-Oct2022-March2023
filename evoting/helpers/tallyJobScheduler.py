# tallyJobScheduler.py 

"""
This module consists of the methods to schedule the future datetime by threading fashion. 

A class for the JobScheduler object need to be instantiated before calling the function methods. 
Ths class will be consisting the follwing functions:
- Schedule all the existing work (when the system boots up)
- Schedule an event 
- Cancel a scheduled event 

- tally process 
---- change the vote event status into "VC"
---- start the tally process by calling the homomorphic encryption module 
---- process the tallied result to get the individual vote option counts 
---- write the result into the database 
---- change the vote event status into "FR"

An dictionary object will keep track the scheduled events and subject to be modified if needed 
"""

from ..models import VoteEvent
from ..models import VoteOption
from ..models import Voter
from ..homo_encryption import *

from datetime import datetime

import threading

job_tracker = {}

class JobScheduler:

	# Parameter(s): python native datetime object 
	def get_schedule_time(self, datetime):
		return (datetime - datetime.now()).total_seconds()

	# Parameter(s) : None
	def schedule_existing_event(self):
		# for vote event in PB
		pb_vote_events = VoteEvent.objects.filter(status="PB")
		for pb_event in pb_vote_events:
			schedule_time = self.get_schedule_time(datetime.combine(pb_event.endDate, pb_event.endTime))
			self.schedule_event(pb_event.createdBy.id, pb_event.eventNo, schedule_time)

		# for vote event in VC
		vc_vote_events = VoteEvent.objects.filter(status="VC")
		for vc_event in vc_vote_events:
			self.schedule_event(vc_event.createdBy.id, vc_event.eventNo, 0)

		print("System Boots Tally Schedule Done ...")


	# Parameter(s): int : event owner id, int: vote event id, int: scheule time in seconds 
	def schedule_event(self, event_owner_id:int, event_id:int, schedule_time:int):
		event = threading.Timer(schedule_time, self.tally_task, [event_owner_id, event_id])
		job_tracker[str(event_id)] = event
		event.start()

	# Parameter(s): int : vote event id
	def cancel_scheduled_event(self, event_id:int):
		event = job_tracker.get(str(event_id), None)
		if (event is not None):
			event.cancel()
			del job_tracker[str(event_id)]

	# Parameter(s): int : event owner id, int : vote event id
	def tally_task(self, event_owner_id:int, event_id:int):
		try :
			# Step 1: update the vote event status 
			vote_event = VoteEvent.objects.get(eventNo=event_id)
			vote_event.status = "VC"
			vote_event.save()

			print("Tally Process Starts")

			# Step 2: start the tally process 
			voters = Voter.objects.filter(eventNo_id=event_id)

			# integer array of the casted vote result
			casted_vote = [int(x.castedVote) for x in voters if x.castedVote != "NOT APPLICABLE"]

			(tallied_result_list, tallied_vote_count) = homo_counting(casted_vote)

			# Step 3: process the tallied result to get the individual vote counts 
			(private_key, salt) = read_private_key(event_owner_id, event_id)
			vote_options = VoteOption.objects.filter(eventNo_id=event_id)
			vote_option_encodings_list = [int(x.voteEncoding) for x in vote_options]

			vote_option_counts = result_counting(vote_option_encodings_list, tallied_result_list, tallied_vote_count, private_key, salt)

			# Step 4: write the result into the system database 
			public_key = vote_event.publicKey.split("//")
			public_key = rsa.PublicKey(int(public_key[0]), int(public_key[1]))
			for vote_option in vote_options:
				vote_option.voteTotalCount = encrypt_int(vote_option_counts.get(str(vote_option.voteEncoding), 0) * salt, public_key)
				vote_option.save()

			# Step 5: update to cote event status
			vote_event.status = "FR"
			vote_event.save()

			# remove the scheduled tasks from the tracker 
			if job_tracker.get(str(event_id), None) is not None:
				del job_tracker[str(event_id)]


			print("Tally Process Done")
			return True

		except VoteEvent.DoesNotExist:
			print("Event does not exist !")

		except Exception:
			print("Something went wrong ...")

		return False

# schedule the existing vote event when the system boots once
# (JobScheduler()).schedule_existing_event()
