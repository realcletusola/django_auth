<h3>Introduction:</h3>
<p>This API provides authentication services using Django Rest Framework (DRF) along with SimpleJWT for token-based authentication. Additionally, it includes CRUD operations for managing user profiles and users.</p>

<h3 style="color: red;">Authentication Endpoints:</h3>
<li><span style="color: red;">- POST /api/auth/signup/: </span> <span style="color: green;">Register a new user.</li>
<li><span style="color: red;">- POST /api/auth/signin/: </span> <span style="color: green;">Obtain a JWT token by providing valid credentials.</span></li>
<li><span style="color: red;">- POST /api/auth/token/refresh/: </span> <span style="color: green;">Refresh the JWT token.</span></li>
<li><span style="color: red;">- POST /api/auth/signout/: </span> <span style="color: green;">Logout and invalidate the JWT token.</span></li>


<h3 style="color: red;">User Profile Endpoints:</h3>
<li><span style="color: red;">- GET /api/auth/profile/: </span> <span style="color: green;">Retrieve the profile of the authenticated user.</span></li>
<li><span style="color: red;">- PUT /api/auth/profile_details/<id>/: </span>  <span style="color: green;">Update the profile of the authenticated user.</span></li> 
<li><span style="color: red;"> PATCH /api/auth/profile_details/<id>/: </span>  <span style="color: green;">Update the profile of the authenticated user.</span></li>
<li><span style="color: red;">- DELETE /api/auth/profile_details/<id>/: </span>  <span style="color: green;">Delete the profile of the authenticated user.</span></li>

<p>Example of the put, patch and delete url path: <span style="color: green;">"/api/auth/profile_details/7/"</span> - (if the profile id is 7)</p>


<h3 style="color: red;">User Management Endpoints:</h3>
<li><span style="color: red;">- GET /api/auth/users/: </span> <span style="color: green;">Retrieve a list of all users.</span></li>
<li><span style="color: red;">- GET /api/user_details/<id>/: </span> <span style="color: green;">Retrieve details of a specific user.</span></li>
<li><span style="color: red;">- PUT /api/user_details/<id>/: </span> <span style="color: green;">Update details of a specific user.</span></li>
<li><span style="color: red;">- PATCH /api/user_details/<id>/: </span> <span style="color: green;">Update details of a specific user.</span></li>
<li><span style="color: red;">- DELETE /api/users/<id>/:</span> <span style="color: green;">Delete a specific user.</span></li>


<h3 style="color: red;">Request Format:</h3>

<h4> SignUp Resquest: </h4>
<p style="color: red;">- Method:</p><span style="color: green;">POST</span>
<p style="color: red;">- URL: </p><span style="color: green;">/api/auth/signup/</span>
<p style="color: red;">- Headers:</p>
<li style="color: red;">- Content-Type: </li><span style="color: green;">application/json</span>
<li style="color: red;">- Body:</li>
  {
      <span style="color:red">"username": </span> <span style="color: green;">"example_user",</span>
      <span style="color:red">"email": </span> <span style="color: green;">"example@email.com",</span>
      <span style="color:red">"password": </span> <span style="color: green;">"example_password",</span>
      <span style="color:red">"password_again": </span> <span style="color: green;">"example_password",</span>
  }
<h3 style="color: red;">Response Format:</h3>
<p style="color: red;">- Status Code: </p> <span style="color: green;">201 CREATED</span>
<p style="color: red;">- Body:</p>
  {
    <span style="color:red">"success": </span> <span style="color: green;">"Account created successfully",</span>
  }



<h4> SignIn  Request: </h4>
<p style="color: red;">- Method:</p><span style="color: green;">POST</span>
<p style="color: red;">- URL: </p><span style="color: green;">/api/auth/signin/</span>
<p style="color: red;">- Headers:</p>
<li style="color: red;">- Content-Type: </li><span style="color: green;">application/json</span>
<li style="color: red;">- Body:</li>
  {
      <span style="color:red">"login_id": </span> <span style="color: green;">"example_user",</span>
      <span style="color:red">"password": </span> <span style="color: green;">"example_password",</span>
  }

  OR

  {
    <span style="color:red">"login_id": </span> <span style="color: green;">"example_email",</span>
    <span style="color:red">"password": </span> <span style="color: green;">"example_password",</span>
  }

<h3 style="color: red;">Response Format:</h3>
<p style="color: red;">- Status Code: </p> <span style="color: green;">200 OK</span>
<p style="color: red;">- Body:</p>
  {
    <span style="color:red">"success": </span> <span style="color: green;">"Login successful",</span>
    <span style="color:red">"access": </span> <span style="color: green;">"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",</span>
    <span style="color:red">"refresh": </span> <span style="color: green;">"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."</span>
  }




<h4> SignOut  Request: </h4>
<p style="color: red;">- Method:</p><span style="color: green;">POST</span>
<p style="color: red;">- URL: </p><span style="color: green;">/api/auth/signout/</span>
<p style="color: red;">- Headers:</p>
<li style="color: red;">- Content-Type: </li><span style="color: green;">application/json</span>
<li style="color: red;">- Body:</li>
  {
      <span style="color:red">"refresh": </span> <span style="color: green;">"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",</span>
  }

<h3 style="color: red;">Response Format:</h3>
<p style="color: red;">- Status Code: </p> <span style="color: green;">200 OK</span>
<p style="color: red;">- Body:</p>
  {
    <span style="color:red">"success": </span> <span style="color: green;">"Logout successful",</span>
  }



<h4> Token Refresh Request: </h4>
<p style="color: red;">- Method:</p><span style="color: green;">POST</span>
<p style="color: red;">- URL: </p><span style="color: green;">/api/auth/token/refresh/</span>
<p style="color: red;">- Headers:</p>
<li style="color: red;">- Content-Type: </li><span style="color: green;">application/json</span>
<li style="color: red;">- Body:</li>
  {
      <span style="color:red">"refresh": </span> <span style="color: green;">"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",</span>

  }

<h3 style="color: red;">Response Format:</h3>
<p style="color: red;">- Status Code: </p> <span style="color: green;">200 OK</span>
<p style="color: red;">- Body:</p>
  {
    <span style="color:red">"access": </span> <span style="color: green;">"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",</span>
    <span style="color:red">"refresh": </span> <span style="color: green;">"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."</span>
  }



<h4 style="color: red;">NOTE: <span style="color:green">The access token must be included in the Authorization header as a "Bearer" type when making requests to the User or User Profile end points.</span></h4>
<h4 style="color: red;">NOTE: <span style="color:green">Only the PATCH request method allow partial update. If you are using PUT method, you should be updating all fields.</span></h4>

<h4> User or Profile Request: </h4>
<p style="color: red;">- Method:</p><span style="color: green;">GET/POST/PUT/PATCH/DELETE</span>
<p style="color: red;">- URL: </p><span style="color: green;">/api/auth/token/refresh/</span>
<p style="color: red;">- Headers:</p>
<li style="color: red;">- Content-Type: </li><span style="color: green;">application/json</span>
<li style="color: red;">- Authorization: </li><span style="color: green;"> Bearer access_token</span>



<h3 style="color: red;">Error Handling:</h3>

  - Status Code: <span style="color: red;">400</span> Bad Request
    {
        "errors":<br> 
            <li><span style="color: green;">"Failed to create account."(Invalid data format, this will return the field errors)</span></li>
            <li><span style="color: green;">"Invalid username or password."</span></li>
            <li><span style="color: green;">"Unable to log you out. Refresh token not provided"</span></li>
            <li><span style="color: green;">"Unable to update profile."(Invalid data format, this will return the field errors)</span></li>
            <li><span style="color: green;">"Unable to update user details."(Invalid data format, this will return the field errors)</span></li>


    }
  - Status Code: <span style="color: red;">401</span> Unauthorized
    {
        "error":<br>
        <li><span style="color: green;">"Account disabled."(This error will occur if the user account is inactive)</span></li>
    }
  
<h3 style="color: red;">NOTE: Include the refresh_token in the SignOut request Header.</h3>