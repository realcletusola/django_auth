from django.urls import reverse 
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile

User = get_user_model()


class AuthenticationTests(APITestCase):
	"""
	Authentication TestCase

	"""

	def setUp(self):
		"""
		test case set up, this runs before each test

		"""

		self.signup_url = reverse('signup')
		self.signin_url = reverse('signin')
		self.signout_url = reverse('signout')
		self.token_refresh_url = reverse('token_refresh')

		self.user_signup_data = {
			"username":"testuser",
			"email":"testuser@email.com",
			"password":"testUSER23##",
			"password_again":"testUSER23##"
		}

		self.user_signin_data_1 = {
			"login_id":"testuser",
			"password":"testUSER23##"
		}

		self.user_signin_data_2 = {
			"login_id":"testuser@email.com",
			"password":"testUSER23##"
		}


	def test_signup(self):
		"""
		test user signup

		"""
		response = self.client.post(self.signup_url, self.user_signup_data, format='json')
		response_status = response.data["status"] # get status from response data(this approach is optional)
		self.assertEqual(response_status, status.HTTP_201_CREATED)
		self.assertEqual(User.objects.count(), 1) # confirm user count in database is the newly created user
		self.assertEqual(User.objects.get().username, 'testuser') # confirm the username of the counted user is our testuser
		self.assertEqual(UserProfile.objects.count(), 1) # since there's a signal that creates User Profile on signup, we can check to confirm if the profile is created


	def test_signin_1(self):
		"""
		test user signin with username and password 

		"""
		self.client.post(self.signup_url, self.user_signup_data, format='json') # firstly, register the user
		response = self.client.post(self.signin_url, self.user_signin_data_1, format='json') # login the user
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('access', response.data) # confirm access token is included in response data
		
		return response # return response which will be used in the UserUpdateTest below

	def test_signin_2(self):
		"""
		test user signin with email and password

		"""
		self.client.post(self.signup_url, self.user_signup_data, format='json') # firstly, register the user
		response = self.client.post(self.signin_url, self.user_signin_data_2, format='json') # login user
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('access', response.data) # confirm access token is included in response data


	def test_signout(self):
		"""
		test user signout

		"""
		self.client.post(self.signup_url, self.user_signup_data, format='json') # firstly, register the user
		user_signin = self.client.post(self.signin_url, self.user_signin_data_1, format='json') # secondly, signin the user
		refresh_token = user_signin.data['refresh'] # get refresh token from user signin response data
		response = self.client.post(self.signout_url, data={"refresh":refresh_token}, format='json') # signout post request
		self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserViewTest(APITestCase):
	"""
	Test get, put, patch and delete method for user view

	"""

	def setUp(self):
		"""
		setup test 

		"""

		# create user 
		self.new_user = User.objects.create_user(username="newuser", email="newuser@email.com", password="newUSER12##")

		# generate token for user 
		refresh = RefreshToken.for_user(self.new_user)
		self.token = str(refresh.access_token)


		# set credentials with token 
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

		# user url, get user detail by primary key 
		self.user_url = reverse("user_details", kwargs={'pk':self.new_user.pk})

		# this data will be used for put method, since the code does not allow partial update when using put method
		self.user_update_data = {
			"username": "newestuser",
			"email":"newestuser@email.com"
		}

		# this will be used for patch method, since it allows patial edit
		self.user_update_data_2 ={
			"username": "latestusername"
		}

	def test_get_user(self):
		"""
		test GET method on user_details view  

		"""
		response = self.client.get(self.user_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('username', response.data['data'])


	def test_put_user(self):
		"""
		test PUT method on user_details view 

		"""
		response = self.client.put(self.user_url, self.user_update_data, format='json')
		response_status = response.data['status']
		self.assertEqual(response_status, status.HTTP_201_CREATED)
		self.assertIn('success', response.data)


	def test_patch_user(self):
		"""
		test PATCH method on user_detail view

		"""
		response = self.client.patch(self.user_url, self.user_update_data_2, format='json')
		response_status = response.data['status']
		self.assertEqual(response_status, status.HTTP_201_CREATED)
		self.assertIn('success', response.data)


	def test_delete_user(self):
		"""
		test DELETE method on user_details view

		"""
		response = self.client.delete(self.user_url)
		response_status = response.data['status']
		self.assertEqual(response_status, status.HTTP_401_UNAUTHORIZED) # only admin or staff can delete user
		self.assertIn('error', response.data)


class ProfileViewTest(APITestCase):
	"""
	test for profile crud operation

	"""

	def setUp(self):
		"""
		setup test

		"""
		# create user 
		self.new_user = User.objects.create_user(username="newuser", email="newuser@email.com", password="newUSER12##")

		# get user profile 
		self.user_profile = self.new_user.user_profile

		# generate token for user 
		refresh = RefreshToken.for_user(self.new_user)
		self.token = str(refresh.access_token)


		# set credentials with token 
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

		# user url, get user detail by primary key 
		self.profile_url = reverse("profile_details", kwargs={'pk':self.user_profile.pk})

		# this will be used for patch method, since it allows patial edit
		self.profile_update_data ={
			"display_name": "New name"
		}


	def test_get_profile(self):
		"""
		test GET method on profile_details view 

		"""
		response = self.client.get(self.profile_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn("success", response.data)

	def test_patch_profile(self):
		"""
		test PATCH method on profile_details view

		"""
		response = self.client.patch(self.profile_url, self.profile_update_data, format='json')
		response_status = response.data['status']
		self.assertEqual(response_status, status.HTTP_201_CREATED)
		self.assertIn('success', response.data)

	def test_delete_profile(self):
		"""
		test DELETE method on profile_details view 

		"""

		response = self.client.delete(self.profile_url)
		response_status = response.data['status']
		self.assertEqual(response_status, status.HTTP_204_NO_CONTENT)
		self.assertIn('success', response.data)









