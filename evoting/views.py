from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# Create your views here.

class EventOwnerCreateAccountView(View):
    def get(self, request):
        # render the static page
        return render(request, "eventowner/signup.html", {})

    def post(self, request):
        print(request.POST['username'])
        print(request.POST['email'])
        print(request.POST['password'])

        # redirect to login page if success
        return render(request, "eventowner/login.html", {})

        