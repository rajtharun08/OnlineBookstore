# Online Bookstore API
API for online bookstore

# Tech Stack
- Framework: FastAPI 
- ORM: SQLAlchemy
- Database: PostgreSQL 

# project structure
```bash
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