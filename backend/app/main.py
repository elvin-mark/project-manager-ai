from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import tasks

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

app.include_router(tasks.router, prefix="/api", tags=["Tasks"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Adept AI Project Manager API"}
