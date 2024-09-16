UB E_Commerce API
=================
-> An Outline
  ===========
  This backend server is an app that handles the backend and business logic of any e_commerce web application. It provides the endpoint for communicating with the server. Any company that want to develop an e_commere website can utilize this server to handle their backend storage and business logic.

-> Tutorials || Getting started guide
  > install dependencies
  > clone the repo
  > start a server
  > make api call
  > The API returns request responses in JSON format. When an API request returns an error, it is sent in the JSON response as an error key.
  > Authentication error response
      If an API key is missing, malformed, or invalid, you will receive an HTTP 401 Unauthorized response code.


-> Authentication
  > use token_based authentication, JWT(Json Web Token) authentication
  > after logging in with your email and password, a token is generated and returned in the response body. It expires within 10 minutes after generation.

  Endpoint definition
  ===================
  users
  -----
  POST api/v1/register
  --------------------
| **DESCRIPTION**    | This endpoint creates a new user account in the system |
|--------------------|--------------------------------------------------------|
| **URL Structure**   | `http://127.0.0.1:5000/api/v1/register`               |
| **METHODS**         | POST                                                  |
| **Authentication**  | Not required                                           |

### EXAMPLE  

```bash
curl -X POST http://127.0.0.1:5000/api/v1/register \
              -d name="Alice" \
              -d email="alice@gmail.com" \
              -d role="user" \
              -d password="test"
```
### PARAMETERS
| **Name**     | **Description**                       |
|--------------|---------------------------------------|
| `name`       | Name of the user                      |
| `email`      | Email of the user                     |
| `password`   | Password of the user                  |
| `role`       | Role of the user, e.g., admin or user |

### RETURNS

```bash
{
  "User": {
    "__class__": "User",
    "created_at": "2024-09-16T10:25:31.150238",
    "email": "pamela@gmail.com",
    "id": 6,
    "name": "Pamela",
    "role": "user",
    "updated_at": "2024-09-16T10:25:31.150597"
  },
  "message": "pamela@gmail.com registered successful"
}
```
### ERRORS

```bash
{
    "message": "Already registered!" 
}
```


-> Status and error codes

-> Examples

-> Glossary