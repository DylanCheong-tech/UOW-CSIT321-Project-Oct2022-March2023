from threading import Timer 

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib import auth

# Form imports
from .forms.eventowner import SignupForm
from .forms.eventowner import LoginForm

# Model imports
from .models import UserAccount
from .models import OTPManagement

# Helper module imports
from .helpers.otpGenerator import OTPGenerator
from .helpers.sendOTPEmail import EmailSender
from .helpers.hasher import Hasher
from .helpers.passwordChecker import PasswordChecker

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
                if (data['password'] != data['repeat_password']):
                    error_message = "Passwords Do Not Match !"
                    status_flag = False

                try:
                    # check otp value
                    otp_from_db = OTPManagement.objects.get(email=data['email'])
                    if otp_from_db.is_expired() or otp_from_db.check_otp_matching(data['otp']):
                        error_message = "OTP Value Invalid!"
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
            return render(request, "eventowner/signup.html", {"status": error_message, "form": form})


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
            return render(request, "eventowner/login.html", {"status": error_message, "form": form})

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

        # render the static page
        return render(request, "eventowner/homepage.html", {})


class EventOwnerLogout(View):
    def post(self, request):
        # redirect back to the login page
        auth.logout(request)
        return redirect("/evoting/eventowner/login")
