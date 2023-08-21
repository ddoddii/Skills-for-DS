### Json Web Token(JWT)
- JWT is a self-contained way to securely transmit data and information between two parties using a JSON object. 
- JSON Web Tokens can be trusted because each JWT can be digitally signed, which in return allows the server to know if the JWT has been changed at all.
- JWT should  be used when dealing with authorization
- JWT is a great way for information to be exchanged between the server and client

### JSON Web Token Structure 
- A JSON Web Token is created of three parts seperated by dots (.) which include:
  - aaaaaa.bbbbbbb.cccccc
  - Header :(a)
  - Payload :(b)
  - Signature :(c)

### JWT Header
- A JWT Header usually consist of who parts:
  - "alg" : The algorithm for signing
  - "typ" : The specific type of token
- The JWT Header is then encoded using Base64 to create the first part of the JWT (a)
- ```json
    {
        "alg" : "HS256",
        "typ" : "JWT" 
    }
    ```


### JWT Payload
- JWT Payload consists of the data. The payload data contains claims, and there are three different types of claims
  - Registered
  - Public
  - Private
- The JWT Payload is then encoded using Base64 to create the second part of the JWT
- ```json
    {
        "sub" : "1234",
        "username" : "ddoddi" ,
        "first_name" : "soeun",
        "last_name" : "uhm",
        "admin" : true
    }
    ```

### JWT Signature
- A JWT Signature is created by using the algorithm in the header to hash out the encoded header, encoded payload with a secret.
- The secret can be anything, but is saved somewhere on the server that the client does not have access to.
- The signature is the third and final part of JWT (c)
- ```json
    HMACSHA256(
    base64UrlEncode(Header) + "." + base64UrlEncode(payload), 
    secret
    )
    ```

### JWT 를 사용하는 이유 
- JWT 의 한 글자라도 바뀌면 서버가 변경사항을 아주 빨리 감지할 수 있다.

### JWT.io 사이트
- [jwt.io](https://jwt.io/) 에서 내가 만든 JWT 를 encode 할 수 있다.