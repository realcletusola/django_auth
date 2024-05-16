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

	def get(self, request, format=None):
		"""
		Handle get request for user profile 

		"""
		try:
			profile = UserProfile.objects.get(user=request.user) # get profile of curently logged in user 
			serializer = self.serializer_class(profile, many=True)
			return Response({
				"success": "Profile fetched successfully",
				"data": serializer.data,
				"status": status.HTTP_200_OK
			})

		except UserProfile.DoesNotExist:		
			return Response({
				"error": "Unable to fetch user profile",
				"status": status.HTTP_404_NOT_FOUND
			})
			
		except Exception as e:
			return Response({
				"error":"An error occured. Please try again later",
				"status": status.HTTP_500_INTERNAL_SERVER_ERROR
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
			return UserProfile.objects.get(pk=pk, user=self.request.user)
		
		except UserProfile.DoesNotExist:
			raise Http404("User profile does not exist.")
		
		except Exception as e:
			raise Http404("An error occurred while retrieving the user profile")
		

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
			serializer.save(user=request.user)
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
			serializer.save(user=request.user)
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
	view for user profile 
	"""
	permission_classes = [permissions.IsAuthenticated, ]
	serializer_class = UserSerializer

	def get(self, request, format=None):
		"""
		Handle get request for user object 

		"""
		try:
			user = User.objects.get(id=request.user.id) # get curently logged in user 
			serializer = self.serializer_class(user, many=True)
			return Response({
				"success": "User fetched successfully",
				"data": serializer.data,
				"status": status.HTTP_200_OK
			})

		except User.DoesNotExist:		
			return Response({
				"error": "Unable to fetch user",
				"status": status.HTTP_404_NOT_FOUND
			})
			
		except Exception as e:
			return Response({
				"error":"An error occured. Please try again later",
				"status": status.HTTP_500_INTERNAL_SERVER_ERROR
			})
		

class UserDetailsRequest(APIView):

	"""
	profile details view 
	"""
	permission_classes = [permissions.IsAuthenticated, ]
	serializer_class = UserSerializer
	
	def get_object(self, pk):
		"""
		Method to get user object

		"""
		try:
			return User.objects.get(pk=pk, id=self.request.user.id)
		
		except User.DoesNotExist:
			raise Http404("User profile does not exist.")
		
		except Exception as e:
			raise Http404("An error occurred while retrieving the user profile")
		

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
		serializer = self.serializer_class(user, data=request.data)
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
		serializer = self.serializer_class(user, data=request.data, partial=True)
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
		user = self.get_object(pk)
		user.delete()
		return Response({
			"success":"User deleted",
			"status": status.HTTP_204_NO_CONTENT
		})

