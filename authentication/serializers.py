import re 
from rest_framework import serializers 
from django.contrib.auth import get_user_model 

from .models import UserProfile

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
	"""
	Registration serializer using the ModelSerializer

	"""
	username = serializers.CharField(required=True)
	email = serializers.EmailField(required=True)
	password = serializers.CharField(required=True)
	password_again = serializers.CharField(required=True)

	class Meta:
		model = User 
		fields = ('username', 'email', 'password', 'password_again')


	def validate_username(self, value): 
		"""
		Validate username 

		"""

		errors = {}

		if value is None or not value.strip(): # make certain username is not none or filled with white space
			errors["username_value"] = "Username can't be empty or filled with whitespaces only"

		if len(value) < 4 or len(value) > 20:
			errors["username_length"] = "Username length can only be between 4 to 20 characters"

		check_username = User.objects.filter(username__iexact=value) # filter database to check if th username already exists

		if check_username.exists(): # check if username already exists
			errors["username_unavailable"] = f"Username {value} is not available"

		pattern = r'[!@#$%^&*()+\-={}\[\]:;"\'<>,.?/\\|`~]' # pattern containing unallowed chracters 

		if re.search(pattern, value): # check if the username contains any of this character
			errors["username_character"] = "Username should not contain any special character except underscore '_'"

		value = value.replace(" ", "_") # replace whitespace between username with underscore 

		if errors:
			raise serializers.ValidationError(errors)

		return value 


	def validate_email(self, value):
		"""
		Validate email 

		"""

		errors = {}

		if value is None or not value.strip(): # make certain email is not none or filled with whitespace
			errors["email_value"] = "Email can't be empty or filled with whitespaces only"

		if len(value) < 6 or len(value) > 40:
			errors["email_length"] = "Email must be between 6 to 40 characters"

		check_email = User.objects.filter(email__iexact=value) # filter database if email already exists

		if check_email.exists(): # check if email already exists
			errors["email_unavailable"] = f"Email {value} is not available"

		if errors:
			raise serializers.ValidationError(errors)

		return value 


	def validate(self, data):
		""" 
		Validate passwords for additional security 

		"""
		errors = {}
		password = data.get("password")
		password_again = data.get("password_again")

		if not password:
			errors["password_value"] = "Password field can't be empty"

		if len(password) < 8:
			errors["password_length"] = "Password must be at least 8 characters"

		if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
			errors["password_character"] = "Password must contain at least one special character"

		if not any(v.isupper() for v in password):
			errors["password_uppercase"] = "Password must contain at least one uppercase character"

		if not any(v.islower() for v in password):
			errors["password_lowercase"] = "Password must contain at least one lowercase character"

		if not any(v.isdigit() for v in password):
			errors["password_digit"] = "Password must contain at least one digit"

		if password != password_again:
			errors["password_match"] = "Both passwords must match"

		if errors:
			password_error = {"password": [errors]}
			raise serializers.ValidationError(password_error)

		return data


	def create(self, validated_data):
		""" 
		Create user with validated data 

		"""
		username = validated_data["username"]
		email = validated_data["email"]
		password = validated_data["password"]

		user = User.objects.create(username=username, email=email)
		user.set_password(password)
		user.save()

		return user



class SignInSerializer(serializers.Serializer): # login serializer 
	login_id = serializers.CharField(max_length=40, required=True) # login id can be username or email
	password = serializers.CharField(required=True)


class ProfileSerializer(serializers.ModelSerializer):
	"""
	user profile serializer
	
	Method: Get - get user profile
			Post - update user profile (profile picture and display name only) 
	"""
	user = serializers.CharField(required=False) # return user as a char and not an object

	class Meta:
		models = UserProfile
		fields = ('profile_picture', 'display_name', 'user')


class UserSerializer(serializers.ModelSerializer):
	"""
	user serializer 

	Method: Get - get user object 
			Post - update user object (username and email)

	"""
	username = serializers.CharField(required=True)
	email = serializers.EmailField(required=True)

	class Meta:
		model = User 
		fields = ('username', 'email')

	
	def validate_username(self, value): 
		"""
		Validate username 

		"""

		errors = {}

		if value is None or not value.strip(): # make certain username is not none or filled with white space
			errors["username_value"] = "Username can't be empty or filled with whitespaces only"

		if len(value) < 4 or len(value) > 20:
			errors["username_length"] = "Username length can only be between 4 to 20 characters"

		user = self.context['request'].user # get current user 
		current_username = user.username # get the current username of the user 
		check_username = User.objects.filter(username__iexact=value) # filter database to check if th username already exists

		if check_username.exists() and value != current_username: # check if the new username is not the current username and also if the new username already exists
			errors["username_unavailable"] = f"Username {value} is not available"

		pattern = r'[!@#$%^&*()+\-={}\[\]:;"\'<>,.?/\\|`~]' # pattern containing unallowed chracters 

		if re.search(pattern, value): # check if the username contains any of this character
			errors["username_character"] = "Username should not contain any special character except underscore '_'"

		value = value.replace(" ", "_") # replace whitespace between username with underscore 

		if errors:
			raise serializers.ValidationError(errors)

		return value 


	def validate_email(self, value):
		"""
		Validate email 

		"""

		errors = {}

		if value is None or not value.strip(): # make certain email is not none or filled with whitespace
			errors["email_value"] = "Email can't be empty or filled with whitespaces only"

		if len(value) < 6 or len(value) > 40:
			errors["email_length"] = "Email must be between 6 to 40 characters"

		user = self.context['request'].user # get current user object 
		current_email = user.email # get the current email of the user 
		check_email = User.objects.filter(email__iexact=value) # filter database if email already exists

		if check_email.exists() and value != current_email: # check if email already exists and if email isn't the current email
			errors["email_unavailable"] = f"Email {value} is not available"

		if errors:
			raise serializers.ValidationError(errors)

		return value 