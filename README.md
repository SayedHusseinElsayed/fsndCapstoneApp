# Coffee Shop Backend

Web service tool for helping students to find the available items in the coffee shop and ask for ordering it.
Admin user have high access for adding, delete, and edit the items.

Motivation is like: Why did you make this project?
Few Examples:

I am in this specific industry where such a tool will help the people do their job efficiently
I developed this project to make use of the knowledge you acquired in this nanodegree and hence gain confidence in these skills.
I wanted to contribute something to the open-source community by building this tool.

## Getting Started
## Local Database Setup
Once you create the database, open your terminal, navigate to the root folder, and run:

flask db init
flask db migrate -m "Initial migration."
flask db upgrade
After running, don't forget modify 'SQLALCHEMY_DATABASE_URI' variable.


#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

python -m venv venv
venv/bin/activate


#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.
-[Flask_Migrate]
-[flask_cors]


## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

export FLASK_APP=app
export FLASK_DEBUG=true
export FLASK_ENV=development
flask run

Setting the FLASK_ENV variable to development will detect file changes and
restart the server automatically.


## Project URL
https://capstoneappsayed.herokuapp.com
https://capstoneappsayed.herokuapp.com/categories
https://capstoneappsayed.herokuapp.com/drinks

## On Linux : export
export FLASK_APP=app.py;

## On Windows : set
set FLASK_APP=app.py;

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:drinks-detail`
   - `post:drinks`
   - `patch:drinks`
   - `delete:drinks`
   - `get:categories`
   - `post:categories`
   - `delete:categories`
6. Create new roles for:
   - Barista
     - can `get:drinks-detail`
     - can `get:categories`
   - Manager
     - can perform all actions
     
7. Test your endpoints with [Postman](https://getpostman.com).
   - Register 2 users - assign the Barista role to one and Manager role to the other.
   - Sign into each account and make note of the JWT.
   - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
   - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
   - Run the collection and correct any errors.
   - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

1. `./src/auth/auth.py`
2. `./src/app.py`
3. `./src/manage.py`
4. `./src/models.py`



### Endpoints

GET '/categories'
GET '/drinks'
POST '/drinks'
POST '/categories'
delete '/drinks/1'
PATCH '/drinks/1'

-----------------------------------
GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.

{"categories":[{"id":2,"name":"soft drinks"},{"id":1,"name":"hot drinls"},{"id":3,"name":"mix"},{"id":6,"name":"test2"},{"id":7,"name":"test4"},{"id":8,"name":"test10"}],"success":true}
-----------------------------------
GET '/drinks'
- Fetches all drinks related with category name from the database
- Request Arguments: None
- Returns: An object of drinks with related categories.
{"drinks":[{"category_id":2,"id":8,"recipe":[{"color":"yellow","parts":1}],"title":"orange"},{"category_id":2,"id":13,"recipe":[{"color":"green","parts":1}],"title":"Fanta"},{"category_id":2,"id":11,"recipe":[{"color":"blue","parts":1}],"title":"Water5"},{"category_id":2,"id":19,"recipe":[{"color":"blue","parts":1}],"title":"Water4"}],"success":true}
-----------------------------------

POST '/drinks'

- Create a new drink, which will require the recipe and title text, and category id.
- Request Arguments: jwt
- Returns: True success in case of successful adding and add this drink to the end of list page.

-----------------------------------

DELETE '/drinks/<int:drink_id>'

- delete single drink based on drink_id.
- Request Arguments: drink_id
- Returns: a refresh of questions after deleting process.


------------------------------------
PATCH '/drinks/<int:drink_id>'

- UPDATE single drink based on drink_id.
- Request Arguments: drink_id




