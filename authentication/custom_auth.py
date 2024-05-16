from django.contrib.auth import get_user_model 
from django.contrib.auth.backends import ModelBackend 
from django.db.models import Q 
from django.utils import timezone 
from datetime import timedelta 
from rest_framework.response import Response  
from rest_framework import status  

User = get_user_model()

class CustomAuthenticationBackend(ModelBackend): # login with either username or email 
	def authenticate(self, request, username=None, password=None, **kwargs):
		try:
			# try fetching user by username or email 
			user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))

		except User.DoesNotExist:

			return None

		if user.check_password(password):
			
			return user 

		return None