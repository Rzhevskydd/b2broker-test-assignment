# B2Broker Test Assignment

This project is a Django REST API for managing wallets and transactions, using JSON:API specification.

## Features

- RESTful API with Django REST framework
- JSON:API compliant
- MySQL database
- Dockerized setup
- OpenAPI schema with Swagger UI and Redoc

## Quick Start Guide

### Prerequisites

- Docker
- Docker Compose
- Python 3.11+
- Poetry

### Setup and Installation

1. **Clone the repository:**

   ```sh
   git clone <your-repo-url>
   cd b2broker-test-assignment
   ```


**Install dependencies:**

```sh
Копировать код
poetry install
Create a .env file:
MYSQL_DATABASE=mydatabase
MYSQL_USER=myuser
MYSQL_PASSWORD=mypassword
MYSQL_ROOT_PASSWORD=mypassword
```

**Build and start Docker containers:**

```docker-compose up --build```

**Apply migrations:**

```poetry run python manage.py migrate```


**Create a superuser:**

```poetry run python manage.py createsuperuser```

**Access the API:**

```API root: http://localhost:8000/api/
Swagger UI: http://localhost:8000/api/schema/swagger-ui/
Redoc: http://localhost:8000/api/schema/redoc/
```

**Running Tests**

```docker-compose run test
```
