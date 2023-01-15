from threading import Timer 
import csv

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib import auth
from django.forms.models import model_to_dict

# Form imports
from .forms.eventowner import SignupForm
from .forms.eventowner import LoginForm
from .forms.eventowner import VoteEventForm

# Model imports
from .models import UserAccount
from .models import OTPManagement
from .models import VoteEvent
from .models import VoteOption
from .models import VoterEmail

# Helper module imports
from .helpers.otpGenerator import OTPGenerator
from .helpers.emailSender import EmailSender
from .helpers.hasher import Hasher
from .helpers.passwordChecker import PasswordChecker
from .helpers.voterEmailChecker import VoterEmailChecker

class EventOwnerCreateAccountView(View):
    def get(self, request):
        # render the static page
        return render(request, "eventowner/signup.html", {})

    def post(self, request):
        form = SignupForm(request.POST)

        error_message = "Field Values Invalid !"
        status_flag = True
        if form.is_valid():
            # access the form data
            data = form.cleaned_data

            # check if the account is registered here 
            count = UserAccount.objects.filter(email=data['email']).count()
            if (count > 0):
                error_message = "User Account Existed !"
                status_flag = False
            else: 
                try:
                    # check otp value
                    otp_from_db = OTPManagement.objects.get(email=data['email'])
                    if otp_from_db.is_expired() or otp_from_db.check_otp_matching(data['otp']):
                        error_message = "OTP Value Invalid!"
                        status_flag = False

                    elif(data['password'] != data['repeat_password']):
                        error_message = "Passwords Do Not Match !"
                        status_flag = False

                    elif not PasswordChecker.validate_password(data['password']):
                        error_message = "Password Format Invalid !"
                        status_flag = False

                    else:
                        new_account = UserAccount(
                            email=data['email'],
                            password=Hasher(data['password']).messageDigest(),
                            firstName=data['firstname'],
                            lastName=data['lastname'],
                            gender=data['gender'].upper(),
                        )

                        new_account.save()
                        user = auth.models.User(username=data['email'])
                        user.set_password(Hasher(data['password']).messageDigest())
                        user.save()

                except OTPManagement.DoesNotExist:
                    error_message = "No OTP Generated !"
                    status_flag = False

        else:
            status_flag = False

        if status_flag:
            # redirect to login page if success
            return redirect("/evoting/eventowner/login")
        else:
            return render(request, "eventowner/signup.html", {"status": error_message, "form": form}, status=400)

class EventOwnerCreateAccountGetOTP(View):
    def get(self, request):
        # check the email is provided 
        if not request.GET['email']:
            return HttpResponse(content="No Email Address Is Provided", status=404)

        generator = OTPGenerator(request.GET['email'])
        otp = generator.generateOTP()
        email_sender = EmailSender(request.GET['email'])
        email_sender.sendOTP(otp)
        return HttpResponse("Requested OTP sent to mailbox")

class EventOwnerLogin(View):
    user_login_failed_attempts = {}

    def get(self, request):
        # render the static page
        return render(request, "eventowner/login.html", {})

    def post(self, request):
        form = LoginForm(request.POST)

        error_message = "Incorrect Credentials"
        status_flag = True

        if form.is_valid():
            data = form.cleaned_data
            user = auth.authenticate(username=data["email"], password=data["password"])

            if user is not None and user.is_active:
                auth.login(request, user)
            else:
                self.user_login_failed_attempts[data["email"]] = self.user_login_failed_attempts.get(data["email"], 0) + 1
                if self.user_login_failed_attempts[data["email"]] > 4 :
                    try :
                        deactivate_user = auth.models.User.objects.get(username=data["email"])
                        deactivate_user.is_active = False
                        deactivate_user.save()
                        error_message = "Login Failed Attempts Exceed. Please Try Again in 5 Minutes !"

                        # schedule the timeout task once only
                        if self.user_login_failed_attempts[data["email"]] == 5:
                            # unclock the accoount in 5 minutes 
                            unlock_timer = Timer(300, self.unlock_user_account, (data["email"],))
                            unlock_timer.start()
                        
                    except auth.models.User.DoesNotExist:
                        print("No User Account Existed !")

                status_flag = False
            print(self.user_login_failed_attempts)
        else:
            status_flag = False

        if status_flag:
            # redirect to home page if success
            return redirect("/evoting/eventowner/homepage")
        else:
            return render(request, "eventowner/login.html", {"status": error_message, "form": form},status=401)

    def unlock_user_account(self, email):
        deactivate_user = auth.models.User.objects.get(username=email)
        deactivate_user.is_active = True
        deactivate_user.save()

        del self.user_login_failed_attempts[email]

        print("User Activated !")

class EventOwnerHomePage(View):
    def get(self, request):
        # check authentication 
        if not request.user.is_authenticated:
            return redirect("/evoting/eventowner/login")

        # render the overview page with information
        current_user = UserAccount.objects.get(email=request.user.username)
        VoteEventList = VoteEvent.objects.filter(createdBy_id=current_user).order_by('eventNo')
        VoteEventCount = VoteEventList.count()
        OngoingEvent = VoteEvent.objects.filter(createdBy_id=current_user, status='PC').count()
        CompletedEvent = VoteEventCount - OngoingEvent
        EventCount = [VoteEventCount, OngoingEvent, CompletedEvent]
        EventLabels = ["Total Vote Events : ","Ongoing Vote Events : ","Completed Vote Events : "]
        EventDetails = zip(EventCount, EventLabels)

        return render(request, "eventowner/overview.html", {'VoteEvents': VoteEventList,'UserDetails': current_user,'EventDetail': EventDetails})

class EventOwnerLogout(View):
    def post(self, request):
        # redirect back to the login page
        auth.logout(request)
        return redirect("/evoting/eventowner/login")

class EventOwnerCreateNewVoteEvent(View):
    def get(self, request):
        # check authentication 
        if not request.user.is_authenticated:
            return redirect("/evoting/eventowner/login")

        #  get the current authenticated user
        current_user = UserAccount.objects.get(email=request.user.username)
        current_user = {"email" : current_user.email, "firstName": current_user.firstName, "lastName": current_user.lastName}

        # render the static page
        return render(request, "eventowner/voteevent_form.html", {"title" : "Create New Vote Event", "form_action" : "/evoting/eventowner/createevent", "UserDetails":current_user})

    def post(self,request):
        # check authentication 
        if not request.user.is_authenticated:
            return redirect("/evoting/eventowner/login")

        form = VoteEventForm(request.POST, request.FILES)

        error_message = "Field Values Invalid !"
        status_flag = True
        options_list = []

        if form.is_valid():
            data = form.cleaned_data

            # the user must be existed in the database, since user need to logged in to be able to create event
            current_user = UserAccount.objects.get(email=request.user.username)

            new_vote_event = VoteEvent(
                eventTitle = data['eventTitle'],
                startDate = data['startDate'],
                startTime = data['startTime'],
                endDate = data['endDate'],
                endTime = data['endTime'],
                eventQuestion = data['eventQuestion'],
                createdBy_id = current_user.id
            )

            options_list = data['voteOption'].split("|")

            if not new_vote_event.is_event_datetime_valid():
                status_flag = False
                error_message = "Date Time Settings Invalid !"

            elif len(options_list) < 2:
                status_flag = False
                error_message = "At Least Two Vote Options Are Needed !"

            else:
                new_vote_event.save()

                for x in options_list:
                    if(len(x.strip()) > 0):
                        vote_option = VoteOption(
                            voteOption = x,
                            eventNo_id = new_vote_event.eventNo
                        )
                        vote_option.save()
          
                decoded_file = data['voterEmail'].read().decode('utf-8').splitlines()
                reader = csv.reader(decoded_file)
                emailList = []
                for row in reader:
                    emailList.append(row)
                
                valid_email, invalid_email = VoterEmailChecker.checkEmails(emailList)

                for x, y in valid_email.items():
                    voter_email = VoterEmail(
                        voter = x,
                        voterEmail = y,
                        eventNo_id = new_vote_event.eventNo
                    )
                    voter_email.save()
    
        else:
            status_flag = False
            print(form.errors.as_data())

        if status_flag:
            # redirect to home page if success
            return redirect("/evoting/eventowner/homepage")
        else:
            return render(request, "eventowner/voteevent_form.html", {"title" : "Create New Vote Event", "form_action" : "/evoting/eventowner/createevent", "status": error_message, "form": form, "voteOptions" : options_list},status=400)  

class EventOwnerUpdateVoteEvent(View):
    def get(self, request, eventNo):
        # check authentication 
        if not request.user.is_authenticated:
            return redirect("/evoting/eventowner/login")

        #  get the current authenticated user
        current_user = UserAccount.objects.get(email=request.user.username)

        #  get the vote event object 
        vote_event = VoteEvent.objects.filter(createdBy=current_user, eventNo=eventNo)

        # if no object retreive from the database, redirect to the homepage
        """
        This may happened when the user access the other user vote event objects
        """
        if (vote_event.count() == 0):
            return redirect("/evoting/eventowner/homepage")

        options = VoteOption.objects.filter(eventNo=vote_event[0].eventNo)
        options_list = []
        for item in options :
            options_list.append(item.voteOption)

        data = vote_event.values()[0]

        # reformat the date time object to be able recognise by HTML Form input element
        data["startDate"] = data["startDate"].strftime("%Y-%m-%d")
        data["startTime"] = data["startTime"].strftime("%H:%M")
        data["endDate"] = data["endDate"].strftime("%Y-%m-%d")
        data["endTime"] = data["endTime"].strftime("%H:%M")

        form = VoteEventForm(data)
        current_user = {"email" : current_user.email, "firstName": current_user.firstName, "lastName": current_user.lastName}

        # render the static page
        return render(request, "eventowner/voteevent_form.html", {"title" : "Update Vote Event", "form_action" : "/evoting/eventowner/updateevent/" + str(eventNo), "form": form, "voteOptions" : options_list, "event_status" : data["status"], "UserDetails":current_user})


    def post(self, request, eventNo):
        # check authentication 
        if not request.user.is_authenticated:
            return redirect("/evoting/eventowner/login")

        form = VoteEventForm(request.POST, request.FILES)

        error_message = "Field Values Invalid !"
        status_flag = True

        if form.is_valid():
            data = form.cleaned_data

            # the user must be existed in the database, since user need to logged in to be able to create event
            current_user = UserAccount.objects.get(email=request.user.username)
            try:
                vote_event = VoteEvent.objects.get(createdBy=current_user, eventNo=eventNo)

            except VoteEvent.DoesNotExist:
                # if no object retreive from the database, redirect to the homepage
                """
                This may happened when the user access the other user vote event objects
                """
                return redirect("/evoting/eventowner/homepage")

            vote_event_status = vote_event.status

            if vote_event_status == "PC" or vote_event_status == "PB":
                """
                Vote Event in PC status can modify any information 
                status: Pending Confirmation (PC)
                """
                if vote_event_status == "PC":
                    vote_event.eventTitle = data['eventTitle']
                    vote_event.startDate = data['startDate']
                    vote_event.startTime = data['startTime']
                    vote_event.eventQuestion = data['eventQuestion']

                """
                Vote Event in PC or Published, PB can modify the end datetime 
                """
                vote_event.endDate = data['endDate']
                vote_event.endTime = data['endTime']

                options_list = data['voteOption'].split("|")

                if not vote_event.is_event_datetime_valid():
                    status_flag = False
                    error_message = "Date Time Settings Invalid !"

                elif len(options_list) < 2:
                    status_flag = False
                    error_message = "At Least Two Vote Options Are Needed !"

                else:
                    vote_event.save()

                    """
                    Only the Vote Event in PC status can modify the vote options
                    status: Pending Confirmation (PC)
                    """
                    if vote_event_status == "PC":
                        # remove the existing options from the database 
                        VoteOption.objects.filter(eventNo_id=vote_event.eventNo).delete()

                        for x in options_list:
                            if(len(x.strip()) > 0):
                                vote_option = VoteOption(
                                    voteOption = x,
                                    eventNo_id = vote_event.eventNo
                                )
                                vote_option.save()

                    decoded_file = data['voterEmail'].read().decode('utf-8').splitlines()
                    reader = csv.reader(decoded_file)
                    emailList = []
                    for row in reader:
                        emailList.append(row)
                    
                    valid_email, invalid_email = VoterEmailChecker.checkEmails(emailList)

                    # query the existing voter email list 
                    email_query_set = VoterEmail.objects.filter(eventNo_id=vote_event.eventNo)
                    existing_email_list = [x.voterEmail for x in email_query_set]

                    for x, y in valid_email.items():
                        if y not in existing_email_list:
                            voter_email = VoterEmail(
                                voter = x,
                                voterEmail = y,
                                eventNo_id = vote_event.eventNo
                            )
                            voter_email.save()
            else:
                error_message = "Vote Event Not Modifiable !"
                status_flag = False
    
        else:
            status_flag = False
            print(form.errors.as_data())

        if status_flag:
            # redirect to home page if success
            return redirect("/evoting/eventowner/homepage")
        else:
            return render(request, "eventowner/voteevent_form.html", {"title" : "Update Vote Event", "form_action" : "/evoting/eventowner/updateevent/" + str(eventNo), "status": error_message, "form": form, "voteOptions" : options_list})  

class EventOwnerViewVoteEvent(View):
    def get(self, request, eventNo):
        # check authentication 
        if not request.user.is_authenticated:
            return redirect("/evoting/eventowner/login")
        
        #  get the current authenticated user
        current_user = UserAccount.objects.get(email=request.user.username)

        # get the vote event object
        try:
            vote_event = VoteEvent.objects.get(createdBy=current_user, eventNo=int(eventNo))

        except VoteEvent.DoesNotExist:
            # if no object retreive from the database, redirect to the homepage
            """
            This may happened when the user access the other user vote event objects
            """
            return redirect("/evoting/eventowner/homepage")

        # get the current vote event details
        vote_option = VoteOption.objects.filter(eventNo_id=vote_event)
        participants = VoterEmail.objects.filter(eventNo_id=vote_event)

        current_user = {"email" : current_user.email, "firstName": current_user.firstName, "lastName": current_user.lastName}

        # render static page just for viewing event details (commented out for now as no front end html yet, use homepage for now)
        return render(request, "eventowner/voteevent_details.html", {"title": "View Vote Events","VoteDetails": vote_event,"VoteOptions": vote_option, "Voter": participants, "UserDetails":current_user})

class EventOwnerDeleteVoteEvent(View):
    def post(self, request, eventNo):
        # check authentication 
        if not request.user.is_authenticated:
            return redirect("/evoting/eventowner/login")

        # get the current authenticated user
        current_user = UserAccount.objects.get(email=request.user.username)

        try :
            # query the vote event to be deleted
            vote_event = VoteEvent.objects.get(createdBy=current_user, eventNo=eventNo)

            vote_event.delete()

        except VoteEvent.DoesNotExist:
            print("Error On Deleting a Vote Event, eventNo = " + str(eventNo))

        # redirect to the same page as a refresh 
        return redirect("/evoting/eventowner/homepage")
