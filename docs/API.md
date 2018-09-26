# API Documentation
### General API Information
* The base endpoint is: [http://localhost:5000/](http://localhost:5000/)
* All endpoints return either a JSON object or array.
* All time and timestamp related fields are in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format.
* HTTP `4XX` return codes are used for for malformed requests;
  the issue is on the sender's side.
* HTTP `5XX` return codes are used for internal errors; the issue is on WebTemplate's side. 
  It is important to not treat this as a failure operation; 
  the execution status is unknown and could have been a success.
* Any endpoint can return an error; the error payload is as follows:
```json
{
    "message": "Payload is invalid",
    "errors": [
        "missing attribute username", 
        "missing attribute email"
    ],
    "statusCode": 400
}
```

* For `POST`, `PUT`, and `DELETE` endpoints, the parameters should be sent
  in the `request body` with content type `application/json`.
* Parameters may be sent in any order.

* Login token's are passed into the Rest API via the `Access-Token` header.
* Login token's and password's **are case sensitive**.

### Authentication API
##### Get your Account Information
* HTTP Method: `GET`
* URL: `/api/auth`
* Headers:
  * Access-Token
* Body:
* Sample call: 
    ```bash
    $ curl -X GET http://localhost:5000/api/auth \
        -H "Access-Token: ac6b5333-4bbf-41a2-9a97-38c9fcd81c72"
    {
      "data": {
        "created": "2018-08-25T22:58:48", 
        "displayName": "Testine Test", 
        "email": "test@testine.de", 
        "lastLogin": "2018-09-26T09:45:09", 
        "publicId": "bed2d91f-a63d-4a1b-ad6b-7de4a2ab6f73", 
        "role": {
          "description": "Admin", 
          "name": "admin"
        }, 
        "username": "test"
      }, 
      "statusCode": 200
    }
    ```

##### Login
* HTTP Method: `POST`
* URL: `/api/auth`
* Headers:
* Body:
  * username
  * password
* Sample call: 
    ```bash
    $ curl -X POST http://localhost:5000/api/auth \
        -H "Content-Type: application/json" \
        -d '{"username": "test", "password": "test"}'
    {
      "errors": [], 
      "message": "Authentication was successfully", 
      "statusCode": 200, 
      "token": "baa70b70-a841-471b-aa3b-7c45fc0fe09b"
    }
    ```

##### Logout
* HTTP Method: `DELETE`
* URL: `/api/auth`
* Headers:
  * Access-Token
* Body:
* Sample call: 
    ```bash
    $ curl -X DELETE http://localhost:5000/api/auth \
        -H "Access-Token:baa70b70-a841-471b-aa3b-7c45fc0fe09b"
    {
      "data": "Successfully logged out.", 
      "statusCode": 200
    }
    ```

### Roles API
##### Get all roles
* HTTP Method: `GET`
* URL: `/api/roles`
* Headers:
  * Access-Token
* Body:
* Sample call: 
    ```bash
    $ curl -X GET http://localhost:5000/api/roles \
        -H "Access-Token: df65fbd4-9156-4e8b-9c2e-219e50fb8a5b"
    {
      "data": [
        {
          "description": "Admin", 
          "name": "admin"
        }, 
        {
          "description": "User", 
          "name": "user"
        }
      ], 
      "statusCode": 200
    }
    ```

##### Get a role
* HTTP Method: `GET`
* URL: `/api/roles/<name:String>`
* Headers:
  * Access-Token
* Body:
* Sample call: 
    ```bash
    $ curl -X GET http://localhost:5000/api/roles/admin \
        -H "Access-Token: df65fbd4-9156-4e8b-9c2e-219e50fb8a5b"
    {
      "data": {
        "description": "Admin", 
        "name": "admin"
      }, 
      "statusCode": 200
    }
    ```

##### Create a role (Admin)
* HTTP Method: `POST`
* URL: `/api/roles`
* Headers:
  * Access-Token
* Body:
  * name
  * description
* Sample call: 
    ```bash
    $ curl -X POST http://localhost:5000/api/roles \
        -H "Access-Token: df65fbd4-9156-4e8b-9c2e-219e50fb8a5b" \
        -H "Content-Type: application/json" \
        -d '{"name": "test", "description": "test"}'
    {
      "data": {
        "description": "test", 
        "name": "test"
      }, 
      "statusCode": 201
    }
    ```

##### Modify a role (Admin)
* HTTP Method: `PUT`
* URL: `/api/roles/<name:String>`
* Headers:
  * Access-Token
* Body:
  * description
* Sample call: 
    ```bash
    $ curl -X PUT http://localhost:5000/api/roles/test \
        -H "Access-Token: df65fbd4-9156-4e8b-9c2e-219e50fb8a5b" \
        -H "Content-Type: application/json" \
        -d '{"description": "test2"}'
    {
      "data": {
        "description": "test2", 
        "name": "test"
      }, 
      "statusCode": 200
    }
    ```

##### Delete a role (Admin)
* HTTP Method: `DELETE`
* URL: `/api/roles/<name:String>`
* Headers:
  * Access-Token
* Body:
* Sample call:
    ```bash
    $ curl -X DELETE http://localhost:5000/api/roles/test \
        -H "Access-Token: df65fbd4-9156-4e8b-9c2e-219e50fb8a5b"
    {
      "data": "Successfully deleted role.", 
      "statusCode": 200
    }
    ```

### Users API
##### Get all users (Admin)
* HTTP Method: `GET`
* URL: `/api/users`
* Headers:
  * Access-Token
* Body:
* Sample call: 
    ```bash
    $ curl -X GET http://localhost:5000/api/users \
        -H "Access-Token: df65fbd4-9156-4e8b-9c2e-219e50fb8a5b"
    {
      "data": [
        {
          "created": "2018-08-25T22:58:48", 
          "displayName": "Testine Test", 
          "email": "test@testine.de", 
          "lastLogin": "2018-09-26T10:17:40", 
          "publicId": "bed2d91f-a63d-4a1b-ad6b-7de4a2ab6f73", 
          "role": {
            "description": "Admin", 
            "name": "admin"
          }, 
          "username": "test"
        }
      ], 
      "statusCode": 200
    }
    ```

##### Get an user (admin)
* HTTP Method: `GET`
* URL: `/api/users/<publicId:String>`
* Headers:
  * Access-Token
* Body:
* Sample call: 
    ```bash
    $ curl -X GET http://localhost:5000/api/users/bed2d91f-a63d-4a1b-ad6b-7de4a2ab6f73 \
        -H "Access-Token: df65fbd4-9156-4e8b-9c2e-219e50fb8a5b"
    {
      "data": {
        "created": "2018-08-25T22:58:48", 
        "displayName": "Testine Test", 
        "email": "test@testine.de", 
        "lastLogin": "2018-09-26T10:17:40", 
        "publicId": "bed2d91f-a63d-4a1b-ad6b-7de4a2ab6f73", 
        "role": {
          "description": "Admin", 
          "name": "admin"
        }, 
        "username": "test"
      }, 
      "statusCode": 200
    }
    ```

##### Create an user (Admin)
* HTTP Method: `POST`
* URL: `/api/users`
* Headers:
  * Access-Token
* Body:
  * username
  * email
  * role
  * password
* Sample call: 
    ```bash
    $ curl -X POST http://localhost:5000/api/users \
        -H "Access-Token: df65fbd4-9156-4e8b-9c2e-219e50fb8a5b" \
        -H "Content-Type: application/json" \
        -d '{"username": "JohnDoe", "password": "MyPassword", "email": "john@doe.de", "role": "user"}'
    {
      "data": {
        "created": "2018-09-26T10:27:44", 
        "displayName": null, 
        "email": "john@doe.de", 
        "lastLogin": null, 
        "publicId": "0e011408-30f8-4fd6-8897-3901a85cf787", 
        "role": {
          "description": "User", 
          "name": "user"
        }, 
        "username": "JohnDoe"
      }, 
      "statusCode": 201
    }
    ```

##### Modify an user (Admin)
* HTTP Method: `PUT`
* URL: `/api/users/<publicId:String>`
* Headers:
  * Access-Token
* Body:
  * username
  * email
  * role
  * password
  * displayName
* Sample call: 
    ```bash
    $ curl -X PUT http://localhost:5000/api/users/0e011408-30f8-4fd6-8897-3901a85cf787 \
        -H "Access-Token: df65fbd4-9156-4e8b-9c2e-219e50fb8a5b" \
        -H "Content-Type: application/json" \
        -d '{"displayName": "John Doe", "email": "john@doe.com"}'
    {
      "data": {
        "created": "2018-09-26T10:27:44", 
        "displayName": "John Doe", 
        "email": "john@doe.com", 
        "lastLogin": null, 
        "publicId": "0e011408-30f8-4fd6-8897-3901a85cf787", 
        "role": {
          "description": "User", 
          "name": "user"
        }, 
        "username": "JohnDoe"
      }, 
      "statusCode": 200
    }

    ```

##### Modify your own user
* HTTP Method: `PUT`
* URL: `/api/users/me`
* Headers:
  * Access-Token
* Body:
  * email
  * password
  * displayName
* Sample call:
    ```bash
    $ curl -X PUT http://localhost:5000/api/users/me \
        -H "Access-Token: df65fbd4-9156-4e8b-9c2e-219e50fb8a5b" \
        -H "Content-Type: application/json" \
        -d '{"displayName": "John Doe", "email": "john@doe.com"}'
    {
      "data": {
        "created": "2018-09-26T10:27:44", 
        "displayName": "John Doe", 
        "email": "john@doe.com", 
        "lastLogin": null, 
        "publicId": "0e011408-30f8-4fd6-8897-3901a85cf787", 
        "role": {
          "description": "User", 
          "name": "user"
        }, 
        "username": "JohnDoe"
      }, 
      "statusCode": 200
    }
    ```

##### Delete an user (Admin)
* HTTP Method: `DELETE`
* URL: `/api/users/<publicId:String>`
* Headers:
  * Access-Token
* Body:
* Sample call:
    ```bash
    $ curl -X DELETE http://localhost:5000/api/users/0e011408-30f8-4fd6-8897-3901a85cf787 \
        -H "Access-Token: df65fbd4-9156-4e8b-9c2e-219e50fb8a5b"
    {
      "data": "Successfully deleted user.", 
      "statusCode": 200
    }
    ```

##### Delete your own user
* HTTP Method: `DELETE`
* URL: `/api/users/me`
* Headers:
  * Access-Token
* Body:
* Sample call:
    ```bash
    $ curl -X DELETE http://localhost:5000/api/users/me \
        -H "Access-Token: df65fbd4-9156-4e8b-9c2e-219e50fb8a5b"
    {
      "data": "Successfully deleted user.", 
      "statusCode": 200
    }
    ```
