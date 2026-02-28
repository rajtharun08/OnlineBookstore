# Online Bookstore API
API for online bookstore

### PROJECT BRANCHES
```
* **main**: Stable monolithic architecture (Default)
* **microservices-version**: Decoupled architecture with API Gateway and Service Discovery
  * To switch: `git checkout microservices-version`
```
# Tech Stack
- Framework: FastAPI 
- ORM: SQLAlchemy
- Database: PostgreSQL 

# project structure
    ```
        online-bookstore/
        ├── app/
        │   ├── main.py
        │   ├── core/
        │   │   ├── config.py
        │   │   ├── database.py
        │   │   ├── security.py
        │   │   └── dependencies.py
        │   ├── models/
        │   │   ├── base.py
        │   │   ├── user.py
        │   │   ├── book.py
        │   │   ├── order.py
        │   │   └── order_item.py
        │   ├── schemas/
        │   │   ├── auth_schema.py
        │   │   ├── user_schema.py
        │   │   ├── book_schema.py
        │   │   ├── order_schema.py
        │   │   └── pagination_schema.py
        │   ├── repositories/
        │   │   ├── user_repository.py
        │   │   ├── book_repository.py
        │   │   ├── order_repository.py
        │   │   └── order_item_repository.py
        │   ├── services/
        │   │   ├── auth_service.py
        │   │   ├── user_service.py
        │   │   ├── book_service.py
        │   │   └── order_service.py
        │   ├── api/
        │   │   ├── router.py
        │   │   └── routes/
        │   │       ├── auth.py
        │   │       ├── users.py
        │   │       ├── books.py
        │   │       └── orders.py
        │   ├── middleware/
        │   │   ├── cors.py
        │   │   ├── logging_middleware.py
        │   │   └── rate_limiter.py
        │   ├── exceptions/
        │   │   ├── custom_exceptions.py
        │   │   └── exception_handlers.py
        │   └── utils/
        │       ├── constants.py
        │       └── validators.py
        ├── alembic/
        │   └── alembic.ini
        ├── tests/
        │   ├── test_auth.py
        │   ├── test_users.py
        │   ├── test_books.py
        │   └── test_orders.py
        ├── .env
        ├── .gitignore
        ├── Dockerfile
        ├── docker-compose.yml
        ├── README.md
        └── requirements.txt
    ```
# SETUP AND EXECUTION
```
 1. Configure environment variables in .env.docker
 Ensure DATABASE_URL and POSTGRES credentials are set.

 2. Build and start the containers
docker-compose up --build -d

 3. Apply database migrations
docker-compose exec web alembic upgrade head

 4. Check application logs
docker-compose logs -f

5. Stop services
docker-compose down
```


##  API Endpoints
```

| Method | Endpoint        | Description                     |
|--------|-----------------|---------------------------------|
| POST   | /users/register | User registration               |
| POST   | /users/login    | User authentication             |
| GET    | /books          | Retrieve all books              |
| GET    | /books/{id}     | Retrieve specific book details  |
| POST   | /books          | Create new book entry           |
| PUT    | /books/{id}     | Update existing book            |
| DELETE | /books/{id}     | Remove book entry               |
| POST   | /orders         | Process new order               |
| GET    | /orders/{id}    | Retrieve order status           |

```

# DOCUMENTATION ACCESS
Swagger UI: http://localhost:8000/docs
