UB E_Commerce API
=================
  This backend server is designed to manage the backend operations and business logic for any e-commerce web application. It provides API endpoints for seamless communication between the frontend and the server. Companies looking to develop an e-commerce website can leverage this server to handle backend storage, business logic, and essential functionalities efficiently.

Getting started guide
=====================
### Setup

```
$ pip3 install -r requirement.txt
```
### Clone repo

```
$ git clone https://github.com/Uwiringiyimana2/UB_e_commerce_api.git
```
### Run

```
$ python3 -m api.v1.app
```

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

  POST api/v1/login
  --------------------
| **DESCRIPTION**    | This endpoint authenticate user and generate a jwt token |
|--------------------|--------------------------------------------------------|
| **URL Structure**   | http://127.0.0.1:5000/api/v1/login                    |
| **METHODS**         | POST                                                  |
| **Authentication**  | Login credentials (email and password) required       |
### EXAMPLE  
```bash
curl -X POST http://127.0.0.1:5000/api/v1/login \
              -d email="mukapa@gmail.com" \
              -d password="test"
```
### PARAMETERS
| **Name**     | **Description**                       |
|--------------|---------------------------------------|
| `email`      | Email of the user                     |
| `password`   | Password of the user                  |
### RETURNS
```bash
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im11a2FwYUBtZS5jb20iLCJuYW1lIjoiQmVuamFtaW4iLCJleHAiOjE3MjY0ODY0ODB9.R-yTyiRn0F9KscOneqzP_V8xr-iwpw3l4OjT7cs5ibY"
}
```
### ERRORS
```bash
{
    "message": "Invalid credentials!"
}
```

  GET api/v1/users
  --------------------
| **DESCRIPTION**    | This endpoint allows admin to view all users           |
|--------------------|--------------------------------------------------------|
| **URL Structure**   | http://127.0.0.1:5000/api/v1/users                    |
| **METHODS**         | GET                                                   |
| **Authentication**  | token required and user should be admin               |
### EXAMPLE  
```bash
curl -X GET http://127.0.0.1:5000/api/v1/users \
              -H "x-access-token: <token>"
```
### PARAMETERS    
No parameters
### RETURNS
```bash
[
  {
    "__class__": "User",
    "created_at": "2024-09-10T17:52:30.622704",
    "email": "kennedy@me.com",
    "id": 2,
    "name": "Kennedy",
    "role": "",
    "updated_at": "2024-09-10T17:52:30.623020"
  },
  {
    "__class__": "User",
    "created_at": "2024-09-10T17:52:30.622704",
    "email": "mukapa@me.com",
    "id": 3,
    "name": "Benjamin",
    "role": "admin",
    "updated_at": "2024-09-10T17:52:30.623020"
  },
]
```
### ERRORS
```bash
{
    "error": "Unauthorized"
}
```

  GET api/v1/users/<user_id>
  --------------------
| **DESCRIPTION**    | This endpoint allows admin to view one user            |
|--------------------|--------------------------------------------------------|
| **URL Structure**   | http://127.0.0.1:5000/api/v1/users/<user_id>          |
| **METHODS**         | GET                                                   |
| **Authentication**  | token required and user should be admin               |

### EXAMPLE  
```bash
curl -X GET http://127.0.0.1:5000/api/v1/users/<user_id> \
              -H "x-access-token: <token>"
```
### PARAMETERS    
No parameters
### RETURNS
```bash
{
  "__class__": "User",
  "created_at": "2024-09-11T08:03:13.411425",
  "email": "eric@me.com",
  "id": 4,
  "name": "Eric",
  "role": "user",
  "updated_at": "2024-09-11T08:03:13.411962"
}
```
### ERRORSd
```bash
{
    "error": "Unauthorized"
}
```

  DELETE api/v1/users/<user_id>
  --------------------
| **DESCRIPTION**    | This endpoint allows admin to delete specific user           |
|--------------------|--------------------------------------------------------|
| **URL Structure**   | http://127.0.0.1:5000/api/v1/users/<user_id>                    |
| **METHODS**         | DELETE                                                   |
| **Authentication**  | token required and user should be admin               |

### EXAMPLE  

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/users/<user_id> \
              -H "x-access-token: <token>"
```
### PARAMETERS    
No parameters
### RETURNS
```bash
{}
```
### ERRORS
```bash
{
    "error": "Unauthorized"
}
```

Products
========
  GET api/v1/products
  --------------------
| **DESCRIPTION**    | This endpoint allows users to view all products        |
|--------------------|--------------------------------------------------------|
| **URL Structure**   | http://127.0.0.1:5000/api/v1/products                 |
| **METHODS**         | GET                                                   |
| **Authentication**  | Not required               |
### EXAMPLE  
```bash
curl -X GET http://127.0.0.1:5000/api/v1/products
```
### PARAMETERS    
No parameters
### RETURNS
```bash
[
  {
    "__class__": "Product",
    "category": "contraceptive",
    "created_at": "2024-09-11T12:26:11.879616",
    "description": "emergency contraceptive",
    "id": 1,
    "imageURL": "static/images/zee.jpg",
    "inventory": 15,
    "name": "ZEE",
    "price": "2500.00",
    "updated_at": "2024-09-11T12:26:11.879823"
  },
  {
    "__class__": "Product",
    "category": "Antimicrobial",
    "created_at": "2024-09-11T14:29:54.957225",
    "description": "dermatological",
    "id": 2,
    "imageURL": "static/images/candiderm.png",
    "inventory": 5,
    "name": "candiderm",
    "price": "2500.00",
    "updated_at": "2024-09-11T14:29:54.957524"
  }
]
```

  GET api/v1/products/<product_id>
  --------------------------------
| **DESCRIPTION**    | This endpoint allows users to view one product         |
|--------------------|--------------------------------------------------------|
| **URL Structure**   | http://127.0.0.1:5000/api/v1/products/<product_id>    |
| **METHODS**         | GET                                                   |
| **Authentication**  | token required and user should be admin               |

### EXAMPLE  

```bash
curl -X GET http://127.0.0.1:5000/api/v1/products/<product_id>
```
### PARAMETERS    
No parameters
### RETURNS
```bash
{
  "__class__": "Product",
  "category": "Allergy",
  "created_at": "2024-09-11T14:29:54.957225",
  "description": "Solves breathing discomfort",
  "id": 3,
  "imageURL": "static/images/akerol.jpg",
  "inventory": 13,
  "name": "Akerol",
  "price": "4500.00",
  "updated_at": "2024-09-11T14:29:54.957524"
}
```
### ERRORS
```bash
{
  "error": "Not found"
}
```

  POST api/v1/admin/products
  --------------------------
| **DESCRIPTION**    | This endpoint allows admin to create new product       |
|--------------------|--------------------------------------------------------|
| **URL Structure**   | http://127.0.0.1:5000/api/v1/admin/products    |
| **METHODS**         | POST                                                  |
| **Authentication**  | token required and user should be admin               |
### EXAMPLE   
```bash
curl -X POST http://127.0.0.1:5000/api/v1/admin/products \
    -H "x-access-token: <token>"
    -F "name=candid B" \
    -F price=15 \
    -F description="it is used for dermal diseases" \
    -F "inventory=12" \
    -F category="dermatological" \
    -F image="@./MELA_UNIFYING_ULTRA-MOISTURIZING_MILK_500ML-_new__03891.png"
```
### PARAMETERS
| **Name**     | **Description**                       |
|--------------|---------------------------------------|
| `name`       | Name of the product                   |
| `price`      | price of the product                  |
| `password`   | Password of the product               |
| `description`| description of the product            |
| `inventory`  | stock level of the product            |
| `category`   | category of the product               |
| `image`      | image of the product                  |
### RETURNS
```bash
{
  "__class__": "Product",
  "category": "dermatological",
  "created_at": "2024-09-16T15:04:18.447297",
  "description": "it is used for dermal diseases",
  "id": 5,
  "imageURL": "static/images/MELA_UNIFYING_ULTRA-MOISTURIZING_MILK_500ML-_new__03891.png",
  "inventory": 12,
  "name": "candid B",
  "price": 15.0,
  "updated_at": "2024-09-16T15:04:18.447610"
}
```
### ERRORS
```bash
{
  "error": "Missing product's category"
}
```

  PUT api/v1/admin/products/<id>
  --------------------------------
| **DESCRIPTION**    | This endpoint allows admin to update product       |
|--------------------|--------------------------------------------------------|
| **URL Structure**   | http://127.0.0.1:5000/api/v1/admin/products/<id>    |
| **METHODS**         | PUT                                                  |
| **Authentication**  | token required and user should be admin               |
### EXAMPLE  
```bash
curl -X PUT http://127.0.0.1:5000/api/v1/admin/products/6 \
    -H 'x-access-token: <token>'
    -d '{"price": 20, "description": "Treats UTIs"}'
```
### PARAMETERS
```bash
{
    "price": 20, 
    "description": "Treats UTIs",
}
```
### RETURNS
```bash
{
  "__class__": "Product",
  "category": "dermatological",
  "created_at": "2024-09-16T15:04:18.447297",
  "description": "Treats UTIs",
  "id": 6,
  "imageURL": "static/images/MELA_UNIFYING_ULTRA-MOISTURIZING_MILK_500ML-_new__03891.png",
  "inventory": 12,
  "name": "candid B",
  "price": 20,
  "updated_at": "2024-09-16T15:04:18.447610"
}
```
### ERRORS
No specific error

  DELETE api/v1/admin/products/<id>
  --------------------------------
| **DESCRIPTION**    | This endpoint allows admin to delete product       |
|--------------------|--------------------------------------------------------|
| **URL Structure**   | http://127.0.0.1:5000/api/v1/admin/products/<id>    |
| **METHODS**         | DELETE                                                 |
| **Authentication**  | token required and user should be admin               |
### EXAMPLE  
```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/admin/products/6 \
    -H 'x-access-token: <token>'
```
### PARAMETERS
No parameters
### RETURNS
```bash
{}
```
### ERRORS
```bash
{
  "error": "Not found"
}
```

Cart
====
  GET api/v1/cart
  --------------------
| **DESCRIPTION**    | This endpoint allows users to view their cart          |
|--------------------|--------------------------------------------------------|
| **URL Structure**   | http://127.0.0.1:5000/api/v1/cart                 |
| **METHODS**         | GET                                                   |
| **Authentication**  | Required               |
### EXAMPLE  
```bash
curl -X GET http://127.0.0.1:5000/api/v1/cart \
    -H 'x-access-token: <token>'
```
### PARAMETERS    
No parameters
### RETURNS
```bash
{
  "items": [
    {
      "__class__": "CartItem",
      "cart_id": 1,
      "created_at": "2024-09-16T17:15:36.298778",
      "id": 1,
      "product_id": 6,
      "quantity": 10,
      "updated_at": "2024-09-16T17:26:01.216545"
    }
  ],
  "totalPrice": "300.00"
}
```
### ERRORS
```bash
{
  "error": "No Cart found"
}
```

POST api/v1/cart/add/<product_id>
  -------------------------------
| **DESCRIPTION**    | This endpoint allows users to add item to their cart   |
|--------------------|--------------------------------------------------------|
| **URL Structure**   | http://127.0.0.1:5000/api/v1/cart/add/<product_id>    |
| **METHODS**         | POST                                                  |
| **Authentication**  | Required               |

### EXAMPLE  

```bash
curl -X POST http://127.0.0.1:5000/api/v1/cart/add/6 \
    -H 'x-access-token: <token>'
    -d quantity=10
```
### PARAMETERS    
| **quantity** | quantity of the product to add to a cart |
### RETURNS
```bash
{
  "__class__": "CartItem",
  "cart_id": 1,
  "created_at": "2024-09-16T17:15:36.298778",
  "id": 1,
  "product_id": "6",
  "quantity": 10,
  "updated_at": "2024-09-16T17:26:01.216545"
}
```
### ERRORS
```bash
{
  "error": "Only 12 units are available"
}
```

  PUT api/v1/cart/update/<product_id>
  -------------------------------
| **DESCRIPTION**    | This endpoint allows users to update item in their cart|
|--------------------|--------------------------------------------------------|
| **URL Structure**   | http://127.0.0.1:5000/api/v1/cart/update/<product_id> |
| **METHODS**         | PUT                                                   |
| **Authentication**  | Required                                              |
### EXAMPLE  
```bash
curl -X PUT http://127.0.0.1:5000/api/v1/cart/update/4 \
    -H 'x-access-token: <token>'
    -d quantity=10
```
### PARAMETERS    
| **quantity** | `quantity of the product to add to a cart` |
-----------------------------------------------------------
### RETURNS
```bash
{
  "__class__": "CartItem",
  "cart_id": 1,
  "created_at": "2024-09-16T17:15:36.298778",
  "id": 2,
  "product_id": 4,
  "quantity": 5,
  "updated_at": "2024-09-16T17:35:01.848029"
}
```
### ERRORS
```bash
{
  "error": "Missing quantity!"
}
```

  DELETE api/v1/cart/remove/<product_id>
  -------------------------------
| **DESCRIPTION**    | This endpoint allows users to view their cart          |
|--------------------|--------------------------------------------------------|
| **URL Structure**   | http://127.0.0.1:5000/api/v1/cart/remove/<product_id>    |
| **METHODS**         | DELETE                                                  |
| **Authentication**  | Required               |
### EXAMPLE  
```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/cart/remove/ \
    -H 'x-access-token: <token>'
```
### PARAMETERS    
No parameters
### RETURNS
```bash
{}
```
### ERRORS
```bash
{
  "error": "No product found in cart"
}
```

Orders
======
  GET api/v1/orders
  -------------------------------
| **DESCRIPTION**    | This endpoint allows users to view their orders        |
|--------------------|--------------------------------------------------------|
| **URL Structure**   | http://127.0.0.1:5000/api/v1/orders                   |
| **METHODS**         | GET                                                   |
| **Authentication**  | Required                                              |
### EXAMPLE  
```bash
curl -X GET http://127.0.0.1:5000/api/v1/orders \
    -H 'x-access-token: <token>'
```
### PARAMETERS    
No parameters
### RETURNS
```bash
[
  {
    "cart_items": [
      {
        "price": "4500.00",
        "product_id": 3,
        "quantity": 5
      },
      {
        "price": "35000.00",
        "product_id": 4,
        "quantity": 10
      }
    ],
    "order_id": 11,
    "payment_status": "Paid",
    "timestamp": "Sat, 14 Sep 2024 17:32:40 GMT",
    "total_amount": "372500.00",
    "user_id": 3
  }
]
```
### ERRORS
```bash
{
  "error": "No orders found!"
}
```

  POST api/v1/checkout
  --------------------
| **DESCRIPTION**    | This endpoint allows users to pay cart items           |
|--------------------|--------------------------------------------------------|
| **URL Structure**   | http://127.0.0.1:5000/api/v1/checkout                 |
| **METHODS**         | POST                                                  |
| **Authentication**  | Required                                              |
### EXAMPLE  
```bash
curl -X POST http://127.0.0.1:5000/api/v1/checkout \
    -H 'x-access-token: <token>'
```
### PARAMETERS    
| **paymentMethodId** |  `Payment method Id of payment method selected` |
-------------------------------------------------------------------------
### RETURNS
```bash
{
  "payment_intent": "pi_3PzlRiHI4UNrqRh50onGnRIX",
  "status": "succeeded"
}
```
### ERRORS
```bash
{
  "error": "No orders found!"
}
```