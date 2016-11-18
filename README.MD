## Token based authentication REST service
It's just designing and skeleton implements, you must folk and modify for actually authenticate strategy

### APIs can be called like those request:

#### Login
    curl -X POST -H "Content-Type: application/json" -d '{
        "username" : "lena", 
        "password" : "123"
    }' "http://localhost:8080/login"

#### Access protected resource

    curl -X GET -H "Authorization: Bearer token" "http://localhost:8080/resource"

#### Request new access token

    curl -X POST -H "Content-Type: application/json" -d '{
      "refresh_token": "token"
    }' "http://localhost:8080/auth/access_token"


#### Extend refresh token

    curl -X POST -H "Content-Type: application/json" -d '{
      "refresh_token": "token"
    }' "http://localhost:8080/auth/refresh_token/extend"

#### List sessions

    curl -X GET -H "Authorization: Bearer access_token" "http://localhost:8080/auth/sessions"

#### Revoke auth

    curl -X DELETE -H "Authorization: Bearer access_token" "http://localhost:8080/auth/sessions/:session_id"
