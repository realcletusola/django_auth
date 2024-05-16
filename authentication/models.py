from django.db import models 
from django.contrib.auth.models import AbstractUser, UserManager, Group, Permission
from PIL import Image 


class CustomUserManager(UserManager): # custom user manager  
	
	def create_user(self, username, email, password, **extra_fields): # create user function

		if not username:
			raise ValueError("Username is required")
		
		if not email:
			raise ValueError("Email is required")

		email = self.normalize_email(email)
		user = self.model(username=username, email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user 

	def create_superuser(self, username, email, password, **extra_fields): # create super user
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
	username = models.CharField(max_length=25, unique=True)
	email = models.EmailField(max_length=40, unique=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	groups = models.ManyToManyField(Group, blank=True, related_name="users")
	user_permissions = models.ManyToManyField(Permission, blank=True, related_name="users")
	time = models.DateTimeField(auto_now_add=True)


	USERNAME_FIELD = "username"
	REQUIRED_FIELDS = ["email"]

	objects = CustomUserManager()

	def __str__(self):
		return self.username

	class Meta:
		ordering = ['-time']
		verbose_name = 'CustomUser'
		verbose_name_plural = 'CustomUsers'


class UserProfile(models.Model): # user profile model 
	profile_picture = models.ImageField(upload_to="profile_picture", default='default.jpeg', blank=True, null=True)
	display_name = models.CharField(max_length=35, blank=True, null=True)
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="user_profile")
	login_trials = models.IntegerField(default=0)
	max_login_trials = models.IntegerField(default=5)
	time = models.DateTimeField(auto_now_add=True)


	def increment_login_trials(self): # function to increase login trials 
		self.login_trials += 1
		self.save()

	def reset_login_trials(self): # function to reset login trials
		self.login_trials = 0
		self.save()

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		# open profile image
		img = Image.open(self.profile_picture.path)

		# set default image size 
		default_size = (200, 200)
		img.thumbnail(default_size)

		# save the resized image 
		img.save(self.profile_picture.path)


	class Meta:
		ordering = ['-time']
		verbose_name = 'UserProfile'
		verbose_name_plural = 'UserProfiles'

