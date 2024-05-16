from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static

from .views import(
    SignUpRequest, SignInRequest, SignOutRequest,
    ProfileRequest, ProfileDetailsRequest,
    UserRequest, UserDetailsRequest
)
from rest_framework_simplejwt.views import TokenRefreshView 


urlpatterns = [
	path('signup/', SignUpRequest.as_view(), name='signup'), # user sign up url
	path('signin/', SignInRequest.as_view(), name='signin'), # user sign in view url
	path('signout/', SignOutRequest.as_view(), name='signout'), # user sign out url
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Token refresh url
    path('profile/', ProfileRequest.as_view(), name='profile'), # user profile url path
    path('profile_details/<int:pk>/', ProfileDetailsRequest.as_view(), name='profile_details'),  # profile details url path
    path('user/', UserRequest.as_view(), name='user'), # user info url path
    path('user_details/<int:pk>/', UserDetailsRequest.as_view(), name='user_details'), # user details url path
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

