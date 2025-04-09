# LibraryManagementAPI

**Library Management System API**

The Library Management System API is designed to manage and organize a library's collection of books. The API provides functionality for managing books, handling book loans, tracking detailed history, and generating insightful reports.

### List of functionalities
- Book management (CRUD)
- Borrowing system
- Display book history (which user borrowed, which book, and when)
- Summaries, e.g., most frequently borrowed books, average number of monthly borrowings by category, etc.

## Features

### 1. Book Management
- Add new books to the library catalog
- Update existing book information
- Delete books from the system
- Search books by title or author
- View book availability status

### 2. Lending System
- Create lending transactions
- Return borrowed books
- Track active lendings
- Manage user borrowing privileges

### 3. Book History Tracking
- View complete lending history for each book
- See which users borrowed specific books and when
- Track return dates and lending durations
- Monitor user lending patterns

### 4. Statistical Analysis
- View top 10 most borrowed books
- Generate monthly borrowing statistics
- Create yearly summaries of lending activity
- Calculate average number of books borrowed per category monthly

## Technologies Used

- **Backend:** Python
- **Database:** PostgreSQL
- **API Design:** RESTful API with FastAPI

## Technical Implementation

The system is built using FastAPI framework with a clean architecture approach, separating domain logic from infrastructure concerns. Authentication is implemented using JWT tokens, ensuring secure access to protected endpoints.

The application follows dependency injection patterns for better testability and maintainability, with clear separation between service interfaces and their implementations.

### Authentication
Authentication is implemented using **JWT tokens**, ensuring secure access to protected endpoints. 

### Architecture
- The system follows **dependency injection patterns** for improved testability and maintainability.
- The application is organized in a way that clearly separates the service interfaces from their implementations.

## Security Features

- Token-based authentication
- Role-based access control
- Secure API endpoints
- Data validation and sanitization

## Installation and Setup

To get the Library Management System API up and running locally, follow the steps below.

### Prerequisites
Before you start, make sure you have the following software installed:

- **Python 3.12**
- **PostgreSQL 17.0**
- **Docker**

### Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/JAQBKRU/LibraryManagementAPI.git
   ```
2. Navigate to the backend directory (/libraryapi).
	```
	cd libraryapi
	```
3. Install production dependencies:
	```
	pip install -r requirements.txt
	```
4. Install development dependencies:
	```
	pip install -r requirements-dev.txt
	```
5. Run the Docker Desktop application (ensure Docker is running).
6. Build the Docker image:
	
	docker compose build
	```
7. Run the application:
	```
	docker compose up
	```
8. The application will be available at: http://localhost:8000/docs (Swagger UI)

## Useful commands
- Install production dependencies: `pip install -r requirements.txt`  
- Install development dependencies: `pip install -r requirements-dev.txt`  
- Start the application server: `uvicorn libraryapi.main:app --host 0.0.0.0 --port 8000`  
- API Documentation (Swagger): `http://localhost:8000/docs`  
- Build the project using Docker: `docker compose build` (to refresh the cache: `docker compose build --no-cache`)  
- Run the project using Docker: `docker compose up` (if the cache hasn't been refreshed: `docker compose up --force-recreate`)  
- Manually execute database queries (example queries in the init.sql file):  
  `-docker exec -it db psql -U postgres`  
  `\c app;`

## Quick Start
- Navigate to the project directory  
- Build the application using Docker: `docker compose build`  
- Run the application using Docker: `docker compose up`  
- Use the Swagger UI at `http://localhost:8000/docs`  
- Create a new user using the `/register` endpoint  
- Log in using the `/token` endpoint  
- Use `Authorize` in Swagger by providing the appropriate `user_token` obtained from logging in  
- Try out the other endpoints
