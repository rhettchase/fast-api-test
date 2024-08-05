# Dynamic Questionnaire App

This repository contains a dynamic questionnaire application built using React for the frontend and FastAPI for the backend. The application allows users to answer a series of questions, with the subsequent question or message being determined by their previous responses.

## Architecture Overview

The application is structured into two main components:

1. **Frontend:** Built with React and Redux, this component handles the user interface and interacts with the backend to fetch questions and submit answers.

2. **Backend:** Powered by FastAPI, the backend processes requests from the frontend, maintains the question flow logic, and interacts with the database.

## Technologies

### Frontend

- **React:** The frontend is built with React, using the `@rjsf/core` library to dynamically generate forms based on the question data received from the backend.
- **Redux:** State management is handled using Redux, with asynchronous actions for fetching form configurations and submitting responses.

### Backend

The backend is structured using a three-layer architecture:

1. **API Layer:** Handles HTTP requests and responses. It is responsible for routing, validation, and error handling. The API layer interacts with the service layer to process business logic.

2. **Service Layer:** Contains the business logic of the application. This layer processes requests from the API layer, applies rules or logic, and coordinates data flow between the API and the data layer.

3. **Data Layer:** Manages data storage and retrieval. This layer interacts with the database using SQLAlchemy ORM to execute CRUD operations and queries.

- **FastAPI:** Provides RESTful endpoints to serve questions and handle user responses.
- **SQLAlchemy:** Used for ORM and database interactions.
- **Rule-Based System:** The backend uses a rule-based system to determine the next question or message based on the user's response.

### Database Integration

- **PostgreSQL:** This project uses PostgreSQL as the relational database to store questions, answers, and related metadata. PostgreSQL is accessed through SQLAlchemy, which serves as the ORM layer.

## Dependencies

### Frontend

- **React**: A JavaScript library for building user interfaces.
- **@rjsf/core**: A library for building dynamic forms in React.
- **Redux**: A state management library for JavaScript apps.
- **Redux Toolkit**: The official, recommended way to write Redux logic.

### Backend

- **FastAPI**: A modern, fast web framework for building APIs with Python.
- **SQLAlchemy**: A SQL toolkit and ORM for Python.
- **uvicorn**: A lightning-fast ASGI server for Python.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **PostgreSQL**: A powerful, open-source object-relational database system.

## API Routes

- **`POST /questions/`**

  Creates a new question in the database.
  - Request Body: JSON object containing the question text and options.
  - Response: The created question object.

- **`GET /questions/{question_id}`**

  Retrieves a specific question by its ID.
  - Response: The question object or a 404 error if not found.

- **`GET /questions/`**

  Retrieves all questions from the database.
  - Response: A list of all question objects.

- **`POST /answers/`**

  Submits an answer for a specific question.
  - Request Body: JSON object containing the question ID and the response.
  - Response: The created answer object.

- **`POST /next-question/`**

  Determines the next question based on the current question ID and response.
  - Request Body: JSON object containing the current question ID and the response.
  - Response: The next question object or a message indicating the end of the questionnaire.

- **`GET /form-config/{question_id}`**

  Retrieves the form configuration for a specific question, including the schema used to render the form.
  - Response: A JSON object containing the form configuration.

## Setup and Installation

### Prerequisites

- Node.js (for frontend)
- Python 3.8+ (for backend)
- PostgreSQL (or another database supported by SQLAlchemy)

### Database Setup

1. **Install PostgreSQL** if it is not already installed. You can download it from the [official PostgreSQL website](https://www.postgresql.org/download/).

2. **Create a new database** for the application:

   ```bash
   psql -U postgres
   CREATE DATABASE questionnaire_db;
   ```

3. Set up the database URL in your environment or a .env file, replacing `<username>`, `<password>`, `<host>`, and `<port>` with your PostgreSQL credentials:

```.env
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/questionnaire_db
```

4. Run database migrations (if applicable):

```bash
alembic upgrade head
```

### Backend Setup

1. Create and activate a virtual environment
2. Navigate to the backend directory `cd backend`
3. Install dependencies `pip install -r requirements.txt`
4. Start the FastAPI server: `uvicorn app.main:app --reload`
    - The API will be available at `http://localhost:8000`

### Frontend Setup

1. Install Node.js if not already installed
2. Navigate to frontend directory: `cd frontend`
3. Install dependencies `npm install`
4. Start the development server `npm start`
    - App available at `http://localhost:3000`