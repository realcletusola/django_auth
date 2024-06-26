from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, get_user_model 
from django.db.models import Q
from django.http import Http404
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignUpSerializer, SignInSerializer, ProfileSerializer, UserSerializer
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
				"success": "Account created successfully",
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
						"success":"Login successful",
						"refresh": str(refresh),
						"access":str(refresh.access_token),
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
			    		if user_profile.last_failed_login:
						time_since_last_failed_login = timezone.now() - user_profile.last_failed_login
						if time_since_last_failed_login > timedelta(hours=24):
							user_profile.reset_login_trails()

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
			refresh_token = request.data["refresh"] # get refresh token from sign out request
			if refresh_token:

				token = RefreshToken(refresh_token) 
				token.blacklist() # blacklist token
				return Response({
					"success": "Logout successful",
					"status": status.HTTP_200_OK
				})
			
			else:
				return Response({
					"error": "Unable to log you out. Refresh token not provided",
					"status": status.HTTP_400_BAD_REQUEST
				})

		except Exception as e:
			return Response({
				"error": "An error occured. Please try again",
				"status": status.HTTP_500_INTERNAL_SERVER_ERROR
			})


class ProfileRequest(APIView):
	"""
	view for user profile 
	"""
	permission_classes = [permissions.IsAuthenticated, ]
	serializer_class = ProfileSerializer

	def get_queryset(self):
		"""
		Get profile queryset based on user permission

		"""
		user = self.request.user
		try: 
			if user.is_staff or user.is_superuser: # staff or admin users can view all profiles
				return UserProfile.objects.all()			
			else:
				return UserProfile.objects.get(user=user) # basic users can get their profile objects only

		except UserProfile.DoesNotExist:
			return Http404("User profile does not exist")

		except Exception as e:
			return Response({
				"error": "Error retrieving profile data",
				"status": status.HTTP_500_INTERNAL_SERVER_ERROR
			})

	def get(self, request, format=None):
		"""
		Handle get request for user profile 

		"""
		profile = self.get_queryset() # get profile based on queryset permission 
		serializer = self.serializer_class(profile, many=True)
		return Response({
			"success": "Profile fetched successfully",
			"data": serializer.data,
			"status": status.HTTP_200_OK
		})


		
class ProfileDetailsRequest(APIView):

	"""
	profile details view 
	"""
	permission_classes = [permissions.IsAuthenticated, ]
	serializer_class = ProfileSerializer
	
	def get_object(self, pk):
		"""
		Method to get profile object

		"""
		try:
			return UserProfile.objects.get(pk=pk) # get user profile by pk
		 
		except UserProfile.DoesNotExist:
			raise Http404("User profile does not exist.")
		
		except Exception as e:
			return Response({
				"error": "Error retrieving profile data",
				"status": status.HTTP_500_INTERNAL_SERVER_ERROR
			})
		

	def get(self, request, pk, format=None):
		"""
		Method to get user profile details 
		
		"""
		profile = self.get_object(pk)
		serializer = self.serializer_class(profile)
		return Response({
			"success":"success",
			"data":serializer.data,
			"status":status.HTTP_200_OK
		})
	
	def put(self, request, pk, format=None):
		"""
		Put method for user profile update
		
		"""
		profile = self.get_object(pk)
		serializer = self.serializer_class(profile, data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save(user=self.request.user)
			return Response({
				"success": "Profile updated successfully",
				"status": status.HTTP_201_CREATED
			})

		else:
			return Response({
				"error":"Unable to update profile",
				"details": serializer.errors,
				"status":status.HTTP_400_BAD_REQUEST
			})
		
	def patch(self, request, pk, format=None):
		"""
		Patch method for user profile update

		"""
		profile = self.get_object(pk)
		serializer = self.serializer_class(profile, data=request.data, partial=True)
		if serializer.is_valid(raise_exception=True):
			serializer.save(user=self.request.user)
			return Response({
				"success":"Profile updated successfully",
				"status": status.HTTP_201_CREATED
			})
		
		else:
			return Response({
				"error":"Unable to update profile",
				"details": serializer.errors,
				"status": status.HTTP_400_BAD_REQUEST
			})
		
	def delete(self, request, pk, format=None):
		"""
		Delete method for user profile 

		"""
		profile = self.get_object(pk)
		profile.delete()
		return Response({
			"success":"Profile deleted",
			"status": status.HTTP_204_NO_CONTENT
		})


class UserRequest(APIView):
	"""
	view for user object. This view is used to get all users,
	it should be used by staff or admin users only. 
	"""
	permission_classes = [permissions.IsAuthenticated, ]
	serializer_class = UserSerializer

	def get_queryset(self):
		""" 
		get user object based on user permission
		
		"""
		user = self.request.user 
		try:
			if user.is_staff or user.is_superuser:
				return User.objects.all() # staff or admin can view all users

			else:
				return User.objects.get(id=self.request.user.id) # basic users can view their user object only

		except User.DoesNotExist:
			raise Http404("User does not exist")

		except Exception as e:
			return Response({
				"error": "Error retrieving user data",
				"status": status.HTTP_500_INTERNAL_SERVER_ERROR
			})

			
	def get(self, request, format=None):
		"""
		Handle get request for user object 

		"""
		user = self.get_queryset() # get all users 
		serializer = self.serializer_class(user, many=True)
		return Response({
			"success": "User fetched successfully",
			"data": serializer.data,
			"status": status.HTTP_200_OK
		})
		

class UserDetailsRequest(APIView):

	"""
	user details view. This should be used by staff or admin users only

	"""
	permission_classes = [permissions.IsAuthenticated, ]
	serializer_class = UserSerializer
	
	def get_object(self, pk):
		"""
		Method to get user object

		"""
		try:
			return User.objects.get(pk=pk) # get currently logged in user 
		
		except User.DoesNotExist:
			raise Http404("User profile does not exist.")
		
		except Exception as e:
			return Response({
				"error": "Error retrieving user data",
				"status": status.HTTP_500_INTERNAL_SERVER_ERROR
			})
		

	def get(self, request, pk, format=None):
		"""
		Method to get user details 
		
		"""
		user = self.get_object(pk)
		serializer = self.serializer_class(user)
		return Response({
			"success":"success",
			"data":serializer.data,
			"status":status.HTTP_200_OK
		})
	
	def put(self, request, pk, format=None):
		"""
		Put method for user update
		
		"""
		user = self.get_object(pk)
		serializer = self.serializer_class(user, data=request.data, context={'request': request})
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response({
				"success": "User details updated successfully",
				"status": status.HTTP_201_CREATED
			})

		else:
			return Response({
				"error":"Unable to update user details",
				"details": serializer.errors,
				"status":status.HTTP_400_BAD_REQUEST
			})
		
	def patch(self, request, pk, format=None):
		"""
		Patch method for user update

		"""
		user = self.get_object(pk)
		serializer = self.serializer_class(user, data=request.data, context={'request': request}, partial=True)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response({
				"success":"User details updated successfully",
				"status": status.HTTP_201_CREATED
			})
		
		else:
			return Response({
				"error":"Unable to update user details",
				"details": serializer.errors,
				"status": status.HTTP_400_BAD_REQUEST
			})
		
	def delete(self, request, pk, format=None):
		"""
		Delete method for user  

		"""
		request_user = self.request.user 

		if request_user.is_staff or request_user.is_superuser: # only staff or admin user can delete user
			user = self.get_object(pk)

			user.delete()
			return Response({
				"success":"User deleted",
				"status": status.HTTP_204_NO_CONTENT
			})
		else:
			return Response({
				"error":"You are not authorized to delete user",
				"status": status.HTTP_401_UNAUTHORIZED
			})


