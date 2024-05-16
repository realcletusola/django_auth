from django.contrib.auth import authenticate, get_user_model 
from django.db.models import Q
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignUpSerializer, SignInSerializer
from .models import UserProfile 

User = get_user_model()


class SignUpRequest(APIView):

	""" 
	View for user sign up

	"""

	def post(self, request):
		""" 	
		Handle POST request for user sign up.

		Parameters:
			request (Request): The Http request object 

		Return:
			Response: A JSON response indicating the result of the sign up request.
			
		"""

		serializer = SignUpSerializer(data=request.data)

		if serializer.is_valid(raise_exception=True): 
			serializer.save()

			return Response({
				"message": "Account created successfully",
				"status": status.HTTP_201_CREATED
			})

		else:
			# return error response if sign up request fails 
			return Response({
				"error": "Failed to create account.",
				"details": serializer.errors,
				"status": status.HTTP_400_BAD_REQUEST
			})


class SignInRequest(APIView):

	""" 
	View for user sign in 

	"""

	def post(self, request):
		""" 	
		Handle POST request for user sign in.

		Parameters:
			request (Request): The Http request object 

		Return:
			Response: A JSON response indicating the result of the sign in request.
				
		"""
		serializer = SignInSerializer(data=request.data)

		if serializer.is_valid(raise_exception=True):
			loginId = serializer.validated_data["login_id"] # get loginId from request
			password = serializer.validated_data["password"] # get password from request
			
			user = authenticate(request, username=loginId, password=password) # authenticate user

			if user is not None:
				if user.is_active: # check if user account is active
					refresh = RefreshToken.for_user(user) # generate token for user
					user_profile = UserProfile.objects.get(user=user)
					user_profile.reset_login_trials() # reset login trials on successful authentication

					return Response({
						"message":"Login successful",
						"refresh_token": str(refresh),
						"access_token":str(refresh.access_token),
						"status": status.HTTP_200_OK
					})

				else: 
					# return error response if user account is inactive
					return Response({
						"error": "Account disabled. Please contact support for help",
						"status": status.HTTP_401_UNAUTHORIZED
					})

			else:
				try:
					user = User.objects.get(Q(username__iexact=loginId) | Q(email__iexact=loginId)) # search database for user with the provided 
					user_profile = user.user_profile # get user profile

					if user_profile.login_trials < 5: # if user hasn't exceeded login trials 
						user_profile.increment_login_trials() # add 1 to the current login trial counter
						return Response({
							"error": "Invalid username or password",
							"status": status.HTTP_401_UNAUTHORIZED
							})

					else:
						return Response({
							"error": "You've tried to login too many times. Please try again after 24 hours",
							"status": status.HTTP_401_UNAUTHORIZED
						})

				except:
					# return error response if there's no user with the loginId provide 
					return Response({
						"error": "Invalid username or password",
						"status": status.HTTP_401_UNAUTHORIZED
					})

		else:
			return Response({ 
				#  return error response if serializer is not valid
				"error": "Authentication failed. Please check your credentials",
				"details": serializer.errors,
				"status": status.HTTP_400_BAD_REQUEST
			})


class SignOutRequest(APIView):
	"""
	View for user sign out 

	"""
	def post(self, request):
	
		""" 	
		Handle POST request for user sign out.

		Parameters:
			request (Request): The Http request object 

		Return:
			Response: A JSON response indicating the result of the sign out request.
				
		"""
		try:
			refresh_token = request.data["refresh_token"] # get refresh token from sign out request
			if refresh_token:

				token = RefreshToken(refresh_token) 
				token.blacklist() # blacklist token
				return Response({
					"message": "Logout successful",
					"status": status.HTTP_200_OK
				})
			
			else:
				return Response({
					"error": "Refresh token not provided",
					"status": status.HTTP_400_BAD_REQUEST
				})

		except Exception as e:
			return Response({
				"error": "Unable to log you out. Please try again",
				"status": status.HTTP_400_BAD_REQUEST
			})

