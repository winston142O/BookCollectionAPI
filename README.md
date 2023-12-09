# Book Collection API

## Overview

The Book Collection API is a straightforward RESTful service designed for managing a collection of books. It provides endpoints for common CRUD (Create, Read, Update, Delete) operations on books and user-related actions such as sign-up, login, and fetching user details.

## Documentation

Documentation for the API is available through Swagger and ReDoc. To access the documentation:

- Swagger UI: [http://your-api-url/swagger/](http://your-api-url/swagger/)
- ReDoc: [http://your-api-url/redoc/](http://your-api-url/redoc/)

## Project Structure

The project is organized with the following key components:

- `BookCollectionAPI`: Main Django project folder.
- `books`: App handling book-related functionality.
- `users`: App managing user-related features.
- `Dockerfile`: Docker configuration for containerization.
- `docker-compose.yml`: Docker Compose file for managing the application stack.

## Additional Notes

- The application uses SQLite for the database, which is suitable for small to medium-sized projects.
