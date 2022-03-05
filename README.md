# PhemexAPI
A client to experiment with RESTful API Requests to retrieve data from the phemex crypto trading platform.

Datbase is running on MongoDB that is accessed via RestAPI

Official API Documentation of Phemex: https://github.com/phemex/phemex-api-docs/blob/master/Public-Contract-API-en.md#restapi

Official API Documentation MongoDB: https://docs.mongodb.com/drivers/python/

## Endpoints

***

``GET /accounts/accountPositions?currency=BTC``

Example api call to retrieve the current balance of an account

```json header
>> {
    "x-phemex-access-token": "",    //
    "x-phemex-request-expiry": "",     //Usually Now() + 1 minute
    "x-phemex-request-signature": "",     //. HMAC SHA256 Hash (URL PATH + Query String + Expiry + body)
    "optional - x-phemex-request-tracing": ""  //Unique string to trace request (<40 byte)
}
```
```json body
>> {
    "":""
    "":""
    "":""
    "":""
}
```

*** Response Object from Phemex: 
```json
<< {
    "code": <code>, # 0 == success, != 0 == error
    "msg": <msg>,
    "data": <data>
}


```
***
