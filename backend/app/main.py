import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from app.database import create_db_and_tables
from app.seed import seed_items
from app.scheduler import start_scheduler, stop_scheduler
from app.routers import motorcycle, items, log, status, export, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    seed_items()
    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(title="Click125 Tracker API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(motorcycle.router)
app.include_router(items.router)
app.include_router(log.router)
app.include_router(status.router)
app.include_router(export.router)
app.include_router(settings.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
