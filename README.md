# Casting Agency API

## Capstone Project for Udacity's Full Stack Developer Nanodegree
Heroku Link: https://casting-udacity-1993.herokuapp.com/

While running locally: http://localhost:5000

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Virtual Enviornment

Recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

## Running the server

uncomment db_drop_and_create_all() in app.py to drops the database tables and starts fresh when you run in localhost

To run the server, execute:

```bash
set FLASK_APP=app.py
flask run --reload
```

Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` file to find the application. 

Using the `--reload` flag will detect file changes and restart the server automatically.

## API Reference

## Getting Started
Base URL: This application can be run locally. The hosted version is at `https://casting-udacity-1993.herokuapp.com/`.

Authentication: This application requires authentication to perform various actions. All the endpoints require
various permissions, that are passed via the `Bearer` token.

The application has three types of roles:
1- Casting Assistant: Can view actors and movies
2- Casting Director: All permissions a Casting Assistant has, Add or delete an actor from the database and Modify actors or movies
3- Executive Producer: All permissions a Casting Director has and Add or delete a movie from the database


## Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "error": 404,
    "message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
    "success": false
}
```

The API will return the following errors based on how the request fails:
 - 400: Bad Request
 - 401: Unauthorized
 - 403: Forbidden
 - 404: Not Found
 - 405: Method Not Allowed
 - 422: Unprocessable Entity
 - 500: Internal Server Error

## Endpoints

#### GET /actors
 - General
   - gets the list of all the actors
   - requires `get:actors` permission
 
 - Sample Request
   - `https://casting-udacity-1993.herokuapp.com/actors`

<details>
<summary>Sample Response</summary>

```
{
    "actors": [
        {
            "id": 1,
            "name": "Haneen Tayseer"
        },
        {
            "id": 2,
            "name": "Mohammed Khalil"
        },
        {
            "id": 3,
            "name": "Hussam Khalil"
        },
        {
            "id": 4,
            "name": "Ibrahim Khalil"
        }
    ],
    "success": true
}
```

</details>

#### GET /actors/{actor_id}
 - General
   - gets the complete info for an actor
   - requires `get:actors-info` permission
 
 - Sample Request
   - `https://casting-udacity-1993.herokuapp.com/actors/1`

<details>
<summary>Sample Response</summary>

```
{
    "actor": {
        "age": "27",
        "gender": "Female",
        "name": "Haneen Tayseer"
    },
    "success": true
}
```
  
</details>

#### POST /actors
 - General
   - creates a new actor
   - requires `post:actor` permission
 
 - Request Body
   - name: string, required
   - age: integer, required
   - gender: string, required
 
 - Sample Request
   - `https://casting-udacity-1993.herokuapp.com/actors`
   - Request Body
     ```
        {
            "name": "Hisham Khalil",
            "age": "30",
            "gender": "Male"
        }
     ```

<details>
<summary>Sample Response</summary>

```
{
    "created_actor_id": 5,
    "success": true
}
```
  
</details>

#### PATCH /actors/{actor_id}
 - General
   - updates the info for an actor
   - requires `patch:actor` permission
 
 - Request Body (at least one of the following fields required)
   - name: string, required
   - age: integer, required
   - gender: string, required
 
 - Sample Request
   - `https://casting-udacity-1993.herokuapp.com/actors/1`
   - Request Body
     ```
       {
            "name": "Haneen Arrabi"
       }
     ```

<details>
<summary>Sample Response</summary>

```
{
    "actor_info": {
        "name": "Haneen Arrabi",
        "age": "27",
        "gender": "Female"
    },
    "success": true
}
```
  
</details>

#### DELETE /actors/{actor_id}
 - General
   - deletes the actor
   - requires `delete:actor` permission
 
 - Sample Request
   - `https://casting-udacity-1993.herokuapp.com/actors/4`

<details>
<summary>Sample Response</summary>

```
{
    "deleted_actor_id": 4,
    "success": true
}
```
  
</details>

#### GET /movies
 - General
   - gets the list of all the movies
   - requires `get:movies` permission
 
 - Sample Request
   - `https://casting-udacity-1993.herokuapp.com/movies`

<details>
<summary>Sample Response</summary>

```
{
    "movies": [
        {
            "id": 1,
            "release_year": 2013,
            "title": "Wolf of Wall Street"
        },
        {
            "id": 2,
            "release_year": 1994,
            "title": "The Shawshank Redemption"
        }
    ],
    "success": true
}
```

</details>

#### GET /movies/{movie_id}
 - General
   - gets the complete info for a movie
   - requires `get:movies-info` permission
 
 - Sample Request
   - `https://casting-udacity-1993.herokuapp.com/movies/1`

<details>
<summary>Sample Response</summary>

```
{
    "movie": {
        "release_year": 2013,
        "title": "Wolf of Wall Street"
    },
    "success": true
}
```
  
</details>

#### POST /movies
 - General
   - creates a new movie
   - requires `post:movie` permission
 
 - Request Body
   - title: string, required
   - release_year: integer, required
 
 - Sample Request
   - `https://casting-udacity-1993.herokuapp.com/movies`
   - Request Body
     ```
        {
            "title": "The Godfather",
            "release_year": "1971"
        }
     ```

<details>
<summary>Sample Response</summary>

```
{
    "created_movie_id": 3,
    "success": true
}
```
  
</details>

#### PATCH /movie/{movie_id}
 - General
   - updates the info for a movie
   - requires `patch:movie` permission
 
 - Request Body (at least one of the following fields required)
   - title: string, required
   - release_year: integer, required
 
 - Sample Request
   - `https://casting-udacity-1993.herokuapp.com/movies/3`
   - Request Body
     ```
       {
            "release_year": 1972
       }
     ```

<details>
<summary>Sample Response</summary>

```
{
    "movie_info": {
        "release_year": 1972,
        "title": "The Godfather"
    },
    "success": true
}
```
  
</details>

#### DELETE /movies/{movie_id}
 - General
   - deletes the movie
   - requires `delete:movie` permission
 
 - Sample Request
   - `https://casting-udacity-1993.herokuapp.com/movies/1`

<details>
<summary>Sample Response</summary>

```
{
    "deleted_movie_id": 1,
    "success": true
}
```
  
</details>

## Testing
For testing the backend, run the following commands:
```
drop database capstonetest
create database capstonetest
python test.py
```