<h3>Introduction:</h3>
<p>This API provides authentication services using Django Rest Framework (DRF) along with SimpleJWT for token-based authentication. Additionally, it includes CRUD operations for managing user profiles and users.</p>

<h3>Authentication Endpoints:</h3>
<li><span>- POST /api/auth/signup/: </span> <span>Register a new user.</li>
<li><span>- POST /api/auth/signin/: </span> <span>Obtain a JWT token by providing valid credentials.</span></li>
<li><span>- POST /api/auth/token/refresh/: </span> <span>Refresh the JWT token.</span></li>
<li><span>- POST /api/auth/signout/: </span> <span>Logout and invalidate the JWT token.</span></li>


<h3>User Profile Endpoints:</h3>
<li><span>- GET /api/auth/profile/: </span> <span>Retrieve the profile of the authenticated user.</span></li>
<li><span>- PUT /api/auth/profile_details/<id>/: </span>  <span>Update the profile of the authenticated user.</span></li> 
<li><span> PATCH /api/auth/profile_details/<id>/: </span>  <span>Update the profile of the authenticated user.</span></li>
<li><span>- DELETE /api/auth/profile_details/<id>/: </span>  <span>Delete the profile of the authenticated user.</span></li>

<p>Example of the put, patch and delete url path: <span>"/api/auth/profile_details/7/"</span> - (if the profile id is 7)</p>


<h3>User Management Endpoints:</h3>
<li><span>- GET /api/auth/users/: </span> <span>Retrieve a list of all users.</span></li>
<li><span>- GET /api/user_details/<id>/: </span> <span>Retrieve details of a specific user.</span></li>
<li><span>- PUT /api/user_details/<id>/: </span> <span>Update details of a specific user.</span></li>
<li><span>- PATCH /api/user_details/<id>/: </span> <span>Update details of a specific user.</span></li>
<li><span>- DELETE /api/users/<id>/:</span> <span>Delete a specific user.</span></li>


<h3>Request Format:</h3>

<h4> SignUp Resquest: </h4>
<p>- Method:</p><span>POST</span>
<p>- URL: </p><span>/api/auth/signup/</span>
<p>- Headers:</p>
<li>- Content-Type: </li><span>application/json</span>
<li>- Body:</li>
  {
      <span>"username": </span> <span>"example_user",</span>
      <span>"email": </span> <span>"example@email.com",</span>
      <span>"password": </span> <span>"example_password",</span>
      <span>"password_again": </span> <span>"example_password",</span>
  }
<h3>Response Format:</h3>
<p>- Status Code: </p> <span>201 CREATED</span>
<p>- Body:</p>
  {
    <span>"success": </span> <span>"Account created successfully",</span>
  }



<h4> SignIn  Request: </h4>
<p>- Method:</p><span>POST</span>
<p>- URL: </p><span>/api/auth/signin/</span>
<p>- Headers:</p>
<li>- Content-Type: </li><span>application/json</span>
<li>- Body:</li>
  {
      <span>"login_id": </span> <span>"example_user",</span>
      <span>"password": </span> <span>"example_password",</span>
  }

  OR

  {
    <span>"login_id": </span> <span>"example_email",</span>
    <span>"password": </span> <span>"example_password",</span>
  }

<h3>Response Format:</h3>
<p>- Status Code: </p> <span>200 OK</span>
<p>- Body:</p>
  {
    <span>"success": </span> <span>"Login successful",</span>
    <span>"access": </span> <span>"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",</span>
    <span>"refresh": </span> <span>"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."</span>
  }




<h4> SignOut  Request: </h4>
<p>- Method:</p><span>POST</span>
<p>- URL: </p><span>/api/auth/signout/</span>
<p>- Headers:</p>
<li>- Content-Type: </li><span>application/json</span>
<li>- Body:</li>
  {
      <span>"refresh": </span> <span>"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",</span>
  }

<h3>Response Format:</h3>
<p>- Status Code: </p> <span>200 OK</span>
<p>- Body:</p>
  {
    <span>"success": </span> <span>"Logout successful",</span>
  }



<h4> Token Refresh Request: </h4>
<p>- Method:</p><span>POST</span>
<p>- URL: </p><span>/api/auth/token/refresh/</span>
<p>- Headers:</p>
<li>- Content-Type: </li><span>application/json</span>
<li>- Body:</li>
  {
      <span>"refresh": </span> <span>"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",</span>

  }

<h3>Response Format:</h3>
<p>- Status Code: </p> <span>200 OK</span>
<p>- Body:</p>
  {
    <span>"access": </span> <span>"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",</span>
    <span>"refresh": </span> <span>"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."</span>
  }



<h4>NOTE: <span>The access token must be included in the Authorization header as a "Bearer" type when making requests to the User or User Profile end points.</span></h4>
<h4>NOTE: <span>Only the PATCH request method allow partial update. If you are using PUT method, you should be updating all fields.</span></h4>

<h4> User or Profile Request: </h4>
<p>- Method:</p><span>GET/POST/PUT/PATCH/DELETE</span>
<p>- URL: </p><span>/api/auth/token/refresh/</span>
<p>- Headers:</p>
<li>- Content-Type: </li><span>application/json</span>
<li>- Authorization: </li><span> Bearer access_token</span>



<h3>Error Handling:</h3>

  - Status Code: <span>400</span> Bad Request
    {
        "errors":<br> 
            <li><span>"Failed to create account."(Invalid data format, this will return the field errors)</span></li>
            <li><span>"Invalid username or password."</span></li>
            <li><span>"Unable to log you out. Refresh token not provided"</span></li>
            <li><span>"Unable to update profile."(Invalid data format, this will return the field errors)</span></li>
            <li><span>"Unable to update user details."(Invalid data format, this will return the field errors)</span></li>


    }
  - Status Code: <span>401</span> Unauthorized
    {
        "error":<br>
        <li><span>"Account disabled."(This error will occur if the user account is inactive)</span></li>
    }
  
<h3>NOTE: Include the refresh_token in the SignOut request Header.</h3>