import csv

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.utils import timezone
from django.contrib import auth

# Form imports
from .forms.eventowner import SignupForm
from .forms.eventowner import LoginForm
from .forms.eventowner import CreateEventForm

# Model imports
from .models import UserAccount
from .models import OTPManagement
from .models import VoteEvent
from .models import VoteOption
from .models import VoterEmail

# Helper module imports
from .helpers.otpGenerator import OTPGenerator
from .helpers.sendOTPEmail import EmailSender
from .helpers.hasher import Hasher
from .helpers.voterEmailChecker import VoterEmailChecker

class EventOwnerCreateAccountView(View):
    def get(self, request):
        # render the static page
        return render(request, "eventowner/signup.html", {})

    def post(self, request):
        form = SignupForm(request.POST)

        error_message = "Field values invalid"
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
                if (data['password'] != data['repeat_password']):
                    error_message = "Password not match !"
                    status_flag = False

                try:
                    # check otp value
                    otp_from_db = OTPManagement.objects.get(email=data['email'])
                    expireAt = otp_from_db.expireAt
                    if otp_from_db.otp != data['otp'] or timezone.localtime() > timezone.localtime(expireAt):
                        error_message = "OTP value invalid !"
                        status_flag = False

                    else:
                        new_account = UserAccount(
                            email=data['email'],
                            password=Hasher(str(data['password']).encode('utf-8')).messageDigest(),
                            firstName=data['firstname'],
                            lastName=data['lastname'],
                            gender=data['gender'].upper(),
                        )

                        new_account.save()
                        user = auth.models.User(username=data['email'])
                        user.set_password(Hasher(str(data['password']).encode('utf-8')).messageDigest())
                        user.save()

                except OTPManagement.DoesNotExist:
                    error_message = "No OTP generated !"
                    status_flag = False

        else:
            status_flag = False

        if status_flag:
            # redirect to login page if success
            return redirect("/evoting/eventowner/login")
        else:
            return render(request, "eventowner/signup.html", {"status": error_message, "form": form})


class EventOwnerCreateAccountGetOTP(View):
    def get(self, request):
        generator = OTPGenerator(request.GET['email'])
        otp = generator.generateOTP()
        email_sender = EmailSender(request.GET['email'])
        email_sender.sendOTP(otp)
        return HttpResponse("Requested OTP sent to mailbox")


class EventOwnerLogin(View):
    def get(self, request):
        # render the static page
        return render(request, "eventowner/login.html", {})

    def post(self, request):
        form = LoginForm(request.POST)

        error_message = "Incorrect Crendetials"
        status_flag = True

        if form.is_valid():
            data = form.cleaned_data
            user = auth.authenticate(username=data["email"], password=data["password"])

            if user is not None and user.is_active:
                auth.login(request, user)
            else:
                status_flag = False

        else:
            status_flag = False

        if status_flag:
            # redirect to home page if success
            return redirect("/evoting/eventowner/homepage")
        else:
            return render(request, "eventowner/login.html", {"status": error_message, "form": form})


class EventOwnerHomePage(View):
    def get(self, request):
        # check authentication 
        if not request.user.is_authenticated:
            return redirect("/evoting/eventowner/login")

        # render the static page
        return render(request, "eventowner/overview.html", {})


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

        # render the static page
        return render(request, "eventowner/createvoteevent.html", {})

    def post(self,request):
        form = CreateEventForm(request.POST, request.FILES)

        error_message = "Invalid inputs"
        status_flag = True

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

            new_vote_event.save()

            # https://docs.djangoproject.com/en/4.1/ref/models/instances/#auto-incrementing-primary-keys

            options_list = data['voteOption'].split("|")
            for x in options_list:
                if(len(x.strip()) > 0):
                    vote_option = VoteOption(
                        voteOption = x,
                        seqNo_id = new_vote_event.seqNo
                    )
                    vote_option.save()
      
            decoded_file = data['voterEmail'].read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            emailList = []
            for row in reader:
                emailList.append(row)
            
            valid_email, invalid_email = VoterEmailChecker.checkEmails(emailList)

            for x in valid_email:
                voter_email = VoterEmail(
                    voter = x,
                    voterEmail = valid_email[x],
                    seqNo_id = new_vote_event.seqNo
                )
                voter_email.save()
    
        else:
            status_flag = False
            print(form.errors.as_data())

        if status_flag:
            # redirect to home page if success
            return redirect("/evoting/eventowner/homepage")
        else:
            return render(request, "eventowner/createvoteevent.html", {"status": error_message, "form": form, "options" : options_list})



    

        