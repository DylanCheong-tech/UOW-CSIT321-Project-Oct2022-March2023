from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

# Form imports
from .forms.eventowner import SignupForm
from .forms.eventowner import LoginForm

# Model imports
from .models import UserAccount
from .models import OTPManagement

# Helper module imports
from .helpers.otpGenerator import OTPGenerator


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
            if (data['password'] != data['repeat_password']):
                error_message = "Password not match !"
                status_flag = False

            try:
                # check otp value
                otp_from_db = OTPManagement.objects.get(email=data['email'])
                if otp_from_db.otp != data['otp']:
                    error_message = "OTP value incorrect !"
                    status_flag = False
                else :
                    new_account = UserAccount(
                        email=data['email'],
                        password=data['password'],
                        firstName=data['firstname'],
                        lastName=data['lastname'],
                        gender=data['gender'].upper(),
                    )
                    
                    new_account.save()

            except OTPManagement.DoesNotExist:
                error_message = "No OTP generated !"
                status_flag = False
            
        else:
            status_flag = False

        if status_flag:
            # redirect to login page if success
            return redirect("/evoting/eventowner/login")
        else:
            return render(request, "eventowner/signup.html", {"status": error_message})


class EventOwnerCreateAccountGetOTP(View):
    def get(self, request):
        generator = OTPGenerator(request.GET['email'])
        otp = generator.generateOTP()
        return HttpResponse(otp)


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

            try:
                user_from_db = UserAccount.objects.get(email=data['email'])

                if user_from_db.password != data['password']:
                    status_flag = False
            except UserAccount.DoesNotExist:
                status_flag = False
        else:
            status_flag = False

        if status_flag:
            # redirect to home page if success
            return redirect("/evoting/eventowner/homepage")
        else:
            return render(request, "eventowner/login.html", {"status": error_message})


class EventOwnerHomePage(View):
    def get(self, request):
        # render the static page
        return render(request, "eventowner/homepage.html", {})
