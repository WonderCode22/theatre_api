# Theatre
Steps to run the app:
1. Create virtualenv for A project: virtualenv -p /usr/bin/python3.7 {virtualenv_name}
2. Setup the environment: pip install -r requirements.txt
3. Create database
    - python manage.py makemigrations
    - python manage.py migrate

4. Run server and test APIs
   - **URL** localhost:8000/api

# REST API

The REST API to the example app is described below.

## Get all movies

### Request

`GET /movie/`

    http://localhost:8000/api/movie

### Response

    Status: 200 OK
    Content-Type: application/json
    Content
    {
        "movies": [
            {
                "id": 1,
                "title": "wonder",
                "screen_time": 120,
                "start_at": "2020-02-24T06:43:04Z"
            },
            {
                "id": 2,
                "title": "Frozen 2",
                "screen_time": 140,
                "start_at": "2020-02-20T12:43:04Z"
            }
        ]
    }

## Get specific movie

### Request

`GET /movie/`

    http://localhost:8000/api/movie/2

### Response

    Status: 200 OK
    Content-Type: application/json
    Content
    {
        "id": 2,
        "title": "Frozen 2",
        "screen_time": 140,
        "start_at": "2020-02-20T12:43:04Z"
    }

## Create a Movie

### Request

`POST /movie/`

    http://localhost:8000/movie
    
    Content
    {
        "title": "To the sky",
        "screen_time": 135,
        "start_at": "2020-02-20T12:43:04Z"
    }

### Response

    Status: 201 Created
    Content-Type: application/json
    Content
    {
        "id": 3,
        "title": "To the sky",
        "screen_time": 135,
        "start_at": "2020-02-20T12:43:04Z"
    }

## Update a Movie

### Request

`PUT /movie/`

    http://localhost:8000/movie/2
    
    Content
    {
        "title": "Frozen 2 - Trailor",
        "start_at": "2020-02-20T12:43:04Z",
        "screen_time": 140
    }

### Response

    Status: 201 Created
    Content-Type: application/json
    Content
    {
        "id": 2,
        "title": "Frozen 2 - Trailor",
        "screen_time": 140,
        "start_at": "2020-02-20T12:43:04Z"
    }