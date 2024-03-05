# Casting-agency

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

```python
source env/Scripts/activate
```

4. **Install the dependencies:**

```python
pip3 install -r requirements.txt
```

5. Setup Environment Variables
   The env variables can be set running setup.sh. Before running the script set the database URI string to your local database
   Add your details to line ??????? (Replace USERNAME with your postgres user and add a password if you have one. if you dont have a password please just remove the word 'PASSWORD'):

```bash
SQLALCHEMY_DATABASE_URI = 'postgresql://USERNAME:PASSWORD@localhost:5432/fyyur' # e.g. postgresql://ayishaalli:123@localhost:5432/fyyur

```

Then run:

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
createdb casting-agency
```

````

1. **Uncomment lines 22 and 23 in app.py (as seen below) to create tables then comment back out AFTER step 8.** Can be uncommented again to reset the database tables

```python
    with app.app_context():
       db_drop_and_create_all()
````

8. **Run App**

```python
flask run --reload
```
