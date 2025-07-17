# Adept AI Project Manager

**An AI-powered project management platform designed to understand, plan, and guide software development projects, acting as a synthetic team lead for human developers.**

---

## Core Philosophy

Traditional project management tools are passive databases. They store tasks, but they don't understand the project's context, the codebase's nuances, or the developers' strengths. This leads to manual toil, misaligned priorities, and knowledge gaps.

Adept is an active, intelligent agent. By leveraging a Large Language Model (LLM) with Retrieval-Augmented Generation (RAG), Adept maintains a deep, holistic understanding of a software project. It reads the code, the documentation, and the feature requests, and uses this knowledge to build and execute a development plan, assigning granular, well-defined tasks to human developers.

The goal is not to replace developers, but to augment them, freeing them from the complexities of project tracking and task breakdown so they can focus on what they do best: writing excellent code.

## Key Features

-   **Holistic Project Ingestion:** Adept connects directly to your project's ecosystem.
    -   **Code Repositories:** Clones and continuously analyzes your Git repositories to understand the current state of the codebase.
    -   **Documentation:** Parses Markdown files, wikis, and other documents to learn project goals and standards.
    -   **Ticket Systems:** Integrates with tools like Jira or Linear to ingest user stories, bug reports, and epics.

-   **Dynamic Task Generation:** Given a high-level objective (e.g., "Implement OAuth 2.0 login"), Adept analyzes the relevant context from its knowledge base and generates a detailed, step-by-step task list.

-   **Intelligent Task Assignment:** Adept can learn which developers have expertise in different parts of the codebase and assign tasks accordingly, optimizing for efficiency and quality.

-   **Context-Rich Tasks:** Every task assigned by Adept is accompanied by links to the most relevant code snippets, documentation sections, and related tickets, giving the developer all the context they need to start immediately.

-   **Autonomous Progress Tracking:** By monitoring commits and pull requests, Adept can automatically detect when a task is complete, update the project plan, and assign the next task in the sequence.

## How It Works (High-Level Architecture)

1.  **Data Ingestion Layer:** A set of connectors periodically pulls data from configured sources (GitHub, Jira, local files, etc.).
2.  **Knowledge Base (Vector Database):** All ingested data is chunked, converted into vector embeddings, and stored in a vector database (e.g., ChromaDB, Pinecone). This forms the "retrieval" backbone for the RAG system.
3.  **Core AI Engine (LLM):** When a new high-level objective is given, the engine:
    a.  Queries the vector database to retrieve the most relevant context (code, docs, tickets).
    b.  Constructs a detailed prompt containing the objective and the retrieved context.
    c.  Sends the prompt to an LLM (e.g., Gemini, GPT-4) to generate the project plan and tasks.
4.  **Task Dispatcher:** The generated tasks are stored and assigned to developers.
5.  **Web Interface:** A clean, simple UI where developers can view and manage their assigned tasks.

## Project Structure

This project consists of a backend API and a frontend web application.

### Backend

The backend is built with Python and FastAPI. It handles data ingestion, AI processing, and task management.

-   `backend/app/main.py`: The main FastAPI application entry point.
-   `backend/app/api/`: Contains API endpoints for tasks.
-   `backend/app/core/`: Configuration settings for the application.
-   `backend/app/models/`: Data models (e.g., `Task`).
-   `backend/app/services/`: Business logic and AI services (e.g., RAG service).

### Frontend

The frontend is a web application built with Vue.js and TypeScript, providing the user interface for interacting with the project manager.

-   `frontend/src/App.vue`: The main Vue.js application component.
-   `frontend/src/main.ts`: Frontend application entry point.
-   `frontend/src/components/`: Reusable Vue.js components (e.g., `Header`, `TaskList`).
-   `frontend/src/models/`: TypeScript interfaces for frontend data models (e.g., `Task.ts`).
-   `frontend/src/router/`: Vue Router configuration for navigation.
-   `frontend/src/services/`: Frontend services for API communication.

## Getting Started

_(This section will be filled out as the project develops)_

## Contributing

_(This section will be filled out as the project develops)_
