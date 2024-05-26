from django.urls import reverse 
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

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


# class UserViewTest(AuthenticationTests):
# 	"""
# 	Test get, put, and patch for user data
# 	This class inherits the AuthenticationTests class, this allows us to make use of methods in the AuthenticationTests class

# 	"""
# 	def setUp(self):
# 		"""
# 		setup test 

# 		"""
# 		authenticate = self.test_signin_1() # call the signin method in the AuthenticationTests class
