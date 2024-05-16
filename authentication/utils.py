from rest_framework_simplejwt.utils import jwt_payload_handler  

# function to add username to jwt payload 
def custom_jwt_payload_handler(user):
	payload = jwt_payload_handler(user)

	payload['username'] = user.username  # add username to payload 

	return payload 