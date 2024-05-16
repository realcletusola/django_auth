from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static

from .views import SignUpRequest, SignInRequest, SignOutRequest 
from rest_framework_simplejwt.views import TokenRefreshView 


urlpatterns = [
	path('signup/', SignUpRequest.as_view(), name='signup'), # user sign up url
	path('signin/', SignInRequest.as_view(), name='signin'), # user sign in view url
	path('signout/', SignOutRequest.as_view(), name='signout'), # user sign out url
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Token refresh url
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

