# Palindrome Checker

A REST API that allows you to save messages and check for palindrome on demand.

## Getting Started

Requirements : You need Docker, Docker-compose installed.
```
  git clone https://github.com/ruehowl/message_pal.git
  cd message_pal
  docker-compose up --build -d
```
The docker container will bind to the port 5000 of the host.
Run the following for checkin the API working
```
curl http://127.0.0.1:5000/api/messages
```
## REST API

API end points

http://127.0.0.1:5000/api/messages   ==> Allow you to list the messages and add new message using GET and POST methods.

GET example:

curl http://127.0.0.1:5000/api/messages?page=0
```
Response:
{
    "count": 8,
    "data": [
        {
            "message": "malayalam",
            "messageId": 15
        },
        {
            "message": "hello",
            "messageId": 1
        }
    ]
}
```

You can specify the page number by passing an argument 'page'. Each page returns the last 10 messages and the response contains total count of messages along with message data.

POST  ==> Allow you to add messages to the list.
```
curl http://127.0.0.1:5000/api/messages?page=0 -X POST -d data='hello'
{
    "message": "hello",
    "messageId": 18
}
```


http://127.0.0.1:5000/api/messages/<messageId>

GET  ==> Returns the messageid, message and palindrome check.

```
curl http://127.0.0.1:5000/api/messages/15

response:

{
    "data": {
        "isPalindrome": true,
        "message": "malayalam",
        "messageId": 15
    }
}

```

PUT  == > Let you edit a given message.

```
curl http://127.0.0.1:5000/api/messages/15 -X PUT -d data='foo bar'
Response:

{
    "data": {
        "message": "foo bar",
        "messageId": "15"
    }
}
```

DELETE ==> Delete a specific message.

```
curl http://127.0.0.1:5000/api/messages/15 -X DELETE
Response:
status code:
HTTP/1.0 204 NO CONTEN
```


## Deployed working demo API.

http://eggpi.tk:5000/api/messages

You can also test the API using a simple UI at http://eggpi.tk
