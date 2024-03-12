# Casting-agency

Hosted [Here](https://casting-agency-mc2u.onrender.com)

# My Motivation

Finsl project on the Udacity

1. Database with **postgres** and **sqlalchemy**
2. API with **Flask**
3. Test Driven Development **Unittest**
4. Authentication **Auth0**
5. Deployment on **`Render Cloud Platform`**

## Development Setup

1. **If you havent already, Download the project locally**

```bash
git clone https://github.com/AyishaAlli/Casting-agency.git
cd Casting-agency
```

2. **Install frontend dependencies**

```bash
npm install
```

3. **Initialize and activate a virtualenv using:**

```bash
python3.10 -m venv env
source env/bin/activate
```

> **Note**
>
> - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:

```bash
source env/Scripts/activate
```

4. **Install the dependencies:**

```bash
pip3 install -r requirements.txt
```

5. **Setup Environment Variables**
   The env variables can be set running setup.sh. Before running the script set the database URI string to your local database
   Add your details to line ??????? (Replace USERNAME with your postgres user and add a password if you have one. if you dont have a password please just remove the word 'PASSWORD'):

```bash
DATABASE_URI = 'postgresql://USERNAME:PASSWORD@localhost:5432/casting_agency' # e.g. postgresql://ayishaalli:123@localhost:5432/casting_agency

```

**Then run the below to set the variables**

```bash
sudo chmod +x setup.sh
source ./setup.sh

```

1. **Create Database:**

Please make sure you have postgreSQL installed
To download please see [https://www.postgresql.org/download/](https://www.postgresql.org/download/)

First, start your PostgreSQL database server by running:

```bash
sudo service postgresql start

OR

brew services start postgresql
```

6. **create the database:**

```bash
createdb casting_agency
```

7. **Uncomment lines 22 and 23 in app.py (as seen below) to create tables then comment back out AFTER step 8.** Can be uncommented again to reset the database tables

```python
    with app.app_context():
       db_drop_and_create_all()
```

8. **Run App**

```python
flask run --reload
```

The API will return three types of errors:

- 404 – resource not found
- 422 – unprocessable
- 401 - Unauthorized
- 400 - bad request
- 500 - internal server error
- 403 - Forbidden

### Endpoints

#### GET /actors

- General: Return list of actors in Database
- Sample: `curl -L -X GET 'vast-stream-21858.herokuapp.com/actors' \
-H 'Authorization: Bearer Assisant_Token'`<br>

                {
                    "actors": [
                        {
                            "age": 25,
                            "gender": "male",
                            "id": 3,
                            "name": "mohammad"
                        }
                    ],
                    "success": true
                }

#### GET /movies

- General: Return list of movies in Database
- Sample: `curl -L -X GET 'vast-stream-21858.herokuapp.com/movies' \
-H 'Authorization: Bearer Assisant_Token'`<br>

                {
                    "movies": [],
                    "success": true
                }

#### POST /actors

- General:
  - Create actor using JSON Request Body
  - Return ID of created actor
- Sample: `curl -X POST 'vast-stream-21858.herokuapp.com/actors' \
-H 'Authorization: Bearer Director_Token' \
-H 'Content-Type: application/json' \
--data-raw '{
    "name":"mohammad",
    "age":15,
    "gender":"male"
}'`

                {
                    "created_id": 4,
                    "success": true
                }

#### POST /movies

- General:
  - Create movie using JSON Request Body
  - Return ID of created movie
- Sample: `curl -X POST 'vast-stream-21858.herokuapp.com/movies' \
-H 'Authorization: Bearer Executive_Token' \
-H 'Content-Type: application/json' \
--data-raw '{
    "title":"The Mud",
    "release_date" : "10-10-2016"
}'`

                {
                    "created_id": 2,
                    "success": true
                }

#### PATCH /actors/<actor_id>

- General:
  - Modify actor given id in URL provided the information to update
- Sample: `curl -X PATCH 'vast-stream-21858.herokuapp.com/actors/3' \
-H 'Authorization: Bearer Director_Token' \
-H 'Content-Type: application/json' \
--data-raw '{
    "name" : "mohammad",
    "age" : 25
}'`

                {
                    "actor": {
                        "age": 25,
                        "gender": "male",
                        "id": 3,
                        "name": "mohammad"
                    },
                    "success": true
                }

#### PATCH /movies/<movie_id>

- General:
  - Modify movie given id in URL provided the information to update
- Sample: `curl -X PATCH 'vast-stream-21858.herokuapp.com/movies/2' \
-H 'Authorization: Bearer Director_Token' \
-H 'Content-Type: application/json' \
--data-raw '{
    "title":"Terminator",
    "release_date":"10/19/2019"
}'`

#### DELETE /actors/<actor_id>

- General: Delete an actor given id in URL
- Sample: `curl -X DELETE 'vast-stream-21858.herokuapp.com/actors/3' \
-H 'Authorization: Bearer Executive_Token'`

                {
                    "deleted_id": 3,
                    "success": true
                }

#### DELETE /movies/<movie_id>

- General: Delete movie given id in URL
- Sample: `curl -X DELETE 'vast-stream-21858.herokuapp.com/movies/2' \
-H 'Authorization: Bearer Executive_Token'`

                {
                    "deleted_id": 2,
                    "success": true
                }

TROUBLESHOOTING

If the error 'can be resolved' comes up when you hover over imports
run

```bash
which python
```

Copy and paste the path into your python interpreter (in your command palette type 'python:select interpreter')

Roles:

Casting Assistant
Can view actors and movies

```
assistant@gmail.com
testing12345!
```

Casting Director
All permissions a Casting Assistant has and…
Add or delete an actor from the database

```
castingdirector@gmail.com
testing12345!
```

Modify actors or movies
Executive Producer
All permissions a Casting Director has and…
Add or delete a movie from the database

```
execprod@gmail.com
testing12345!
```
