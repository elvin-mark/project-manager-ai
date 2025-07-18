from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import tasks, projects, comments
from app.core.db import Base, engine
from app.api import auth
from app.api import organizations
from app.api import users

app = FastAPI(
    title="Adept AI Project Manager",
    description="An AI-powered project management platform.",
    version="0.1.0",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(engine)


app.include_router(tasks.router, prefix="/api", tags=["Tasks"])
app.include_router(projects.router, prefix="/api", tags=["Projects"])
app.include_router(auth.router, prefix="/api", tags=["Auth"])
app.include_router(organizations.router, prefix="/api", tags=["Organizations"])
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(comments.router, prefix="/api", tags=["Comments"])


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Adept AI Project Manager API"}
