# public_views.py

from django.shortcuts import render
from django.views import View

class URLsFallBackView(View):
	def get(self, request):

		return render(request, "error_page.html", {"error_code" : 404, "error_summary_message" : "Page Not Found !", "error_message" : "The page you are looking does not exists. "})

