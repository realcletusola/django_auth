<h3>Introduction:</h3>
<p>This API provides authentication services using Django Rest Framework (DRF) along with SimpleJWT for token-based authentication. Additionally, it includes CRUD operations for managing user profiles and users.</p>

<h3>Authentication Endpoints:</h3>

     POST /api/auth/signup/: Register a new user.
     POST /api/auth/signin/: Obtain a JWT token by providing valid credentials.
     POST /api/auth/token/refresh/: Refresh the JWT token.
     POST /api/auth/signout/: Logout and invalidate the JWT token.


<h3>User Profile Endpoints:</h3>

     GET /api/auth/profile/: Retrieve the profile of the authenticated user.
     PUT /api/auth/profile_details/<id>/:  Update the profile of the authenticated user. 
     PATCH /api/auth/profile_details/<id>/:  Update the profile of the authenticated user.
     DELETE /api/auth/profile_details/<id>/:  Delete the profile of the authenticated user.

<p>Example of the put, patch and delete url path: "/api/auth/profile_details/7/"- (if the profile id is 7)</p>


<h3>User Management Endpoints:</h3>

     GET /api/auth/users/: Retrieve a list of all users.
     GET /api/user_details/<id>/: Retrieve details of a specific user.
     PUT /api/user_details/<id>/: Update details of a specific user.
     PATCH /api/user_details/<id>/: Update details of a specific user.
     DELETE /api/users/<id>/:Delete a specific user.


<h4> SignUp Resquest: </h4>

<p>- Method: POST</p>
<p>- URL: /api/auth/signup/</p>
<p>- Headers: "content-type: application/json" </p>
<p>- Body: </p> <br>

    {
      "username": "example_user",
      "email": "example@email.com",
      "password": "example_password",
      "password_again": "example_password"
    }
    
<h5> SignUp Response Format: </h5> <br>
  
    {
      Status Code:  201 CREATED,
      "success": "Account created successfully"
    }

<h4> SignIn  Request: </h4>
<p>- Method: POST</p>
<p>- URL: /api/auth/signin/</p>
<p>- Headers: "content-type: application/json" </p>
<p>- Body: </p> <br>

    {
      "login_id": "example_user", 
      "password": "example_password"
    }  
    OR  
    {
      "login_id": "example_email", 
      "password": "example_password"
    } 

<h5> SignIn Response Format:</h5>
<p>- Status Code:  200 OK</p>
<p>- Response: </p> <br>
      
      {
      "success": "Login successful",
      "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
      }
      
<h4> SignOut  Request: </h4>
<p>- Method:POST</p>
<p>- URL: /api/auth/signout/</p>
<p>- Headers: "content-type: application/json" </p>
<p>- Body: </p> <br>

    {
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    } 

<h5> SignOut Response Format:</h5><br>
    
    {
      Status Code: 200 OK,
      "success": "Logout successful"
    }

<h4> Token Refresh Request: </h4>
<p>- Method:POST</p>
<p>- URL: /api/auth/token/refresh/</p>
<p>- Headers:"content-type: application/json"</p>
<p>- Body:</p><br>

    {
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    } 

<h5>Token Refresh Response Format:</h5>
<p>- Status Code:  200 OK</p>
<p>- Response: </p> <br>
  
    {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." 
    }


<h4>NOTE: The access token must be included in the Authorization header as a "Bearer" type when making requests to the User or User Profile end points.</h4>
<h4>NOTE: Only the PATCH request method allow partial update. If you are using PUT method, you should be updating all fields.</h4>

<h4> User or Profile Request: </h4>
<p>- Method: GET/POST/PUT/PATCH/DELETE</p>
<p>- URL: /api/auth/token/refresh/</p>
<p>- Headers: "content-type: application/json"</p>
<p>- Authorization: Bearer access_token</p>



<h3>Error Handling:</h3>

  - Status Code: 400 Bad Request <br>
  
        "errors": 
            - "Failed to create account."(Invalid data format, this will return the field errors)
            - "Invalid username or password."
            - "Unable to log you out. Refresh token not provided"
            - "Unable to update profile."(Invalid data format, this will return the field errors)
            - "Unable to update user details."(Invalid data format, this will return the field errors) 

  - Status Code: 401 Unauthorized <br>
    
        "error":
        - "Account disabled."(This error will occur if the user account is inactive)
    
