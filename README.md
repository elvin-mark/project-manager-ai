# Project Manager

**A project management platform designed to help organize and track software development projects.**

## Features Implemented

-   **AI-powered Task Generation:** Utilizes Large Language Models (LLMs) like Ollama, OpenAI, or Gemini to break down high-level objectives into detailed, actionable tasks.
-   **Persistent Storage:** Tasks and projects are now stored in a database (SQLite by default, configurable for others via SQLAlchemy) ensuring data persistence across application restarts.
-   **User Authentication & Authorization:** Secure user registration, login, and JWT-based authentication to protect API endpoints.
-   **Organizations:** Projects are grouped under organizations, enabling multi-user collaboration.
-   **Organization Member Management:** Functionality to add and remove users from organizations.
-   **Task Assignment:** Tasks can be assigned to users within the same organization, and any member of an organization can reassign tasks to themselves.
-   **Frontend UI:** A Vue.js and TypeScript frontend provides a user-friendly interface for managing organizations, projects, and tasks, including login/logout, project creation, task generation, editing, and assignment.





This project consists of a backend API and a frontend web application.

### Backend

The backend is built with Python and FastAPI. It handles data ingestion and task management.

-   `backend/app/main.py`: The main FastAPI application entry point.
-   `backend/app/api/`: Contains API endpoints for tasks, projects, authentication, organizations, and users.
-   `backend/app/core/`: Configuration settings (including database and JWT secrets) and database session management.
-   `backend/app/models/`: Database models for `User`, `Organization`, `Project`, and `Task`.
-   `backend/app/services/`: Business logic and AI services (e.g., LLM service for task generation).

### Frontend

The frontend is a web application built with Vue.js and TypeScript, providing the user interface for interacting with the project manager.

-   `frontend/src/App.vue`: The main Vue.js application component.
-   `frontend/src/main.ts`: Frontend application entry point.
-   `frontend/src/components/`: Reusable Vue.js components, including authentication forms, organization/project/task lists, and member management.
-   `frontend/src/models/`: TypeScript interfaces for frontend data models (e.g., `Task.ts`, `Project.ts`, `Organization.ts`).
-   `frontend/src/router/`: Vue Router configuration for navigation and authentication guards.
-   `frontend/src/services/`: Frontend services for API communication.

## Getting Started

To set up and run the project locally, follow these steps:

### Prerequisites

-   Python 3.9+
-   Node.js (LTS recommended)
-   npm or yarn

### Backend Setup

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Create a `.env` file in the `backend` directory based on `.env.example` and fill in your API keys and desired database URL (e.g., `DATABASE_URL="sqlite:///./sql_app.db"`).
5.  Run the FastAPI application:
    ```bash
    uvicorn app.main:app --reload
    ```
    The backend API will be running at `http://localhost:8000`.

### Frontend Setup

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install the dependencies:
    ```bash
    npm install # or `yarn install`
    ```
3.  Run the Vue.js development server:
    ```bash
    npm run dev # or `yarn dev`
    ```
    The frontend application will be accessible at `http://localhost:5173` (or another port if 5173 is in use).

### Usage

1.  Open your browser and go to the frontend URL (e.g., `http://localhost:5173`).
2.  Register a new user or log in with existing credentials.
3.  Create new organizations and projects.
4.  Generate tasks for your projects and assign them to users within your organization.

## Contributing

_(This section will be filled out as the project develops)_