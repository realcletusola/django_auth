import os 
from pathlib import Path
from datetime import timedelta 
from dotenv import load_dotenv 

# load environment variables 
load_dotenv()


""" 
This file contains the configurations for drf,
simpleJWT, and django corsheaders

"""

SECRET_KEY = os.getenv('SECRET_KEY')

# rest framework authentication and permission configuration 
REST_FRAMEWORK = {
	"DEFAULT_AUTHENTICATION_CLASSES": (
		"rest_framework_simplejwt.authentication.JWTAuthentication",
	)
}

# django authentication backends 
AUTHENTICATION_BACKENDS = [
    "authentication.custom_auth.CustomAuthenticationBackend", # custom auth backend(login with either username or email
    'django.contrib.auth.backends.ModelBackend', 
]

# rest framework simple jwt configuration 
JWT_AUTH = {
    # handler to include username in jwt payload 
    "JWT_PAYLOAD_HANDLER": "authentication.utils.custom_jwt_payload_handler"
}

SIMPLE_JWT = {
	"ACCESS_TOKEN_LIFETIME": timedelta(days=int(os.getenv('ACCESS_TOKEN_LIFETIME'))),
	"REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.getenv('REFRESH_TOKEN_LIFETIME'))),
	"ROTATE_REFRESH_TOKENS": True,
	"BLACKLIST_AFTER_ROTATION": True,
	"UPDATE_LAST_LOGIN": True,

	"ALGORITHM": os.getenv('JWT_ALGORITHM'),
	"SIGNING_KEY": SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=int(os.getenv('SLIDING_TOKEN_LIFETIME'))),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=int(os.getenv('SLIDING_TOKEN_REFRESH_LIFETIME'))),

}


# corsheaders configuration
CORS_ALLOW_ALL_ORIGIN = True 	# allow all requests 