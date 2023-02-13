# public_views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

class MainPublicPage(View):
	def get(self, request):

		return render(request, "public/index.html", {})

class AboutPublicPage(View):
	def get(self, request):

		return render(request, "public/about.html", {})

