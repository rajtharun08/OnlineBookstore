# Microservices Book Management System

A containerized microservices-based Book Management System built using
FastAPI and PostgreSQL.\
This project demonstrates service-to-service communication, JWT
authentication, and API Gateway routing using Docker Compose.

------------------------------------------------------------------------

## Repository Information

-   **GitHub Branch:** microservice-version
-   **Username:** rajtharun08

------------------------------------------------------------------------

## Architecture Overview

This system follows a microservices architecture pattern where each
service is independently deployable and responsible for a single
business capability.

### Services

#### 1. API Gateway (Port 8000)

-   Acts as the single entry point to the system
-   Routes requests to respective services
-   Enforces OAuth2 and JWT authentication
-   Handles prefix-based routing

#### 2. Auth Service (Port 8001)

-   User registration
-   User authentication
-   JWT token generation
-   Password hashing and verification

#### 3. Book Service (Port 8002)

-   Book inventory management
-   Create, Read, Update, Delete operations
-   Protected using Bearer token authentication

#### 4. Order Service (Port 8003)

-   Order placement
-   Transaction processing
-   Order history tracking
-   Validates user authentication via JWT

------------------------------------------------------------------------

## Tech Stack

-   **Language:** Python 3.11
-   **Framework:** FastAPI
-   **Database:** PostgreSQL
-   **Authentication:** OAuth2 with JWT
-   **Containerization:** Docker
-   **Orchestration:** Docker Compose

------------------------------------------------------------------------

## Project Structure

    ├── api-gateway/
    │   ├── app/
    │   │   ├── core/
    │   │   │   └── config.py
    │   │   └── main.py
    │   ├── Dockerfile
    │   └── requirements.txt
    ├── auth-service/
    │   ├── app/
    │   │   ├── core/
    │   │   ├── models/
    │   │   ├── schemas/
    │   │   └── main.py
    │   ├── Dockerfile
    │   └── requirements.txt
    ├── book-service/
    │   ├── app/
    │   │   ├── models/
    │   │   ├── schemas/
    │   │   └── main.py
    │   ├── Dockerfile
    │   └── requirements.txt
    └── order-service/
        ├── app/
        │   ├── models/
        │   ├── schemas/
        │   └── main.py
        ├── Dockerfile
        └── requirements.txt

------------------------------------------------------------------------

## Setup Instructions

### Prerequisites

-   Python 3.11
-   Docker
-   Docker Compose
-   PostgreSQL (if running manually)

------------------------------------------------------------------------

## Running with Docker Compose (Recommended)

From the root directory:

    docker-compose up --build

This will: - Build all service images - Start containers - Connect
services via Docker network - Expose ports 8000--8003

------------------------------------------------------------------------

## Manual Execution (Without Docker)

Open separate terminals for each service.

### Auth Service

    cd auth-service
    uvicorn app.main:app --port 8001

### Book Service

    cd book-service
    uvicorn app.main:app --port 8002

### Order Service

    cd order-service
    uvicorn app.main:app --port 8003

### API Gateway

    cd api-gateway
    uvicorn app.main:app --port 8000

------------------------------------------------------------------------

## API Endpoints

| Service | Endpoint           | Method | Input Format              |
|----------|-------------------|--------|---------------------------|
| Auth     | /auth/register/   | POST   | JSON                      |
| Auth     | /auth/login/      | POST   | x-www-form-urlencoded     |
| Books    | /books/           | GET    | Bearer Token              |
| Books    | /books/           | POST   | Bearer Token + JSON       |
| Orders   | /orders/          | POST   | Bearer Token + JSON       |



------------------------------------------------------------------------

## Authentication Flow

1.  Register a user using `/auth/register/`
2.  Login using `/auth/login/`
3.  Receive JWT access token
4.  Pass token in Authorization header: Authorization: Bearer <your_token>

5.  Access protected endpoints in Book and Order services

------------------------------------------------------------------------
