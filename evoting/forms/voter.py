# voter.py --> Forms

from django import forms


class VoteForm(forms.Form):
	voterAuth = forms.CharField(label="Voter Authentication")
	voteOption = forms.CharField(label="Options")
