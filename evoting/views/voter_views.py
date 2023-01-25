# voter_views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

class VoterVoteForm(View):
	def get(self, request):

		return render(request, "voter/vote_form.html", {})

class VoterViewFinalResult(View):
	def get(self, request):

		return render(request, "voter/result_page.html", {})