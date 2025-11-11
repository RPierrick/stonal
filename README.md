# Stonal

## About

This repository is a python3.11 repository.
The API is powered by :
- FastAPI for the API ; 
- SQLAlchemy, Alembic and psycopg2 for the database query, migration and connection ;
- Pytest for the unit tests ;

## How to

### Install repository locally 

Install dependencies using following commands :

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Run the postgres image

To run the postgres image from the docker-compose config, run the following command :

```bash
make run_db
```

### Run the database migration

To create the table and insert the given date, run the following command : 

```bash
make migrate
```

### Run FastAPI server

You can run separetly the API and the database using the following command : 

```bash
make run_api
```

Or run both with the following command :

```bash
make run_server
```

### Launch test

You can launch unit tests using the following command : 

```bash
make test
```

### Pylint

You can access the pylint score using the following command :

```bash
make score
```

## Swagger

### Access

API Swagger can be access on following URLs : 
- http://localhost:8000/docs
- http://localhost:8000/redoc

You can use this swagger to create / retrive / update / delete / list employees.
Or you can run command.

### Create an employee

Run the following command :

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/employees/' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic YWRtaW46MTIzNA==' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "birth_date": "2025-11-11",
  "hire_date": "2025-11-11",
  "position": "string",
  "salary": 0
}'
```

### Retrive an employee

Run the following command :

```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/employees/id' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic YWRtaW46MTIzNA==' \
  -H 'Content-Type: application/json'
```

### Update an employee

Run the following command :

```bash
curl -X 'PATCH' \
  'http://localhost:8000/api/v1/employees/id' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic YWRtaW46MTIzNA==' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "birth_date": "2025-11-11",
  "hire_date": "2025-11-11",
  "position": "string",
  "salary": 0
}'
```

### Delete an employee

Run the following command :

```bash
curl -X 'DELETE' \
  'http://localhost:8000/api/v1/employees/id' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic YWRtaW46MTIzNA==' \
  -H 'Content-Type: application/json' 
```

### List employee

Run the following command : 

```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/employees/?offset=X&limit=Y&position=Z&min_salary=M&max_salary=N' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic YWRtaW46MTIzNA==' \
  -H 'Content-Type: application/json'
```


## Architecture

### API folder

Inside the **api/** folder, we store only the endpoints that we want to expose in our API. Their is no business logic in this folder.

### Core folder

Inside the **core/** folder, we store code that can be use by all the other services.

### DB folder

Inside the **db/** folder, we store the database models. 
To reduce of import line in alembic/env.py, all models have to be imported in the db/__init__.py file.

### Models folder

Inside the **models/** folder, we store the input / output of our endpoints.
We also store pydantic representation of our database models.
To go further : 
- We could use this librairy : [SQLModel](https://sqlmodel.tiangolo.com/) to reduce duplicate code between the SQL part and the API part


### Services folder

Inside **services/** folder, we store the business logic of our application.

## To add

- LogMiddleware to help monitor the application
- CORS Middleware for frontend
