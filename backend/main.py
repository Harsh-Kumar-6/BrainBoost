"""
AI tutor Backend - FastAPI entry point
Confusion-Aware Adaptive Learning System (CAALS)
Team: Data Dragons | AI for Bharat Hackathon
"""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routes.explain import router as explain_router
from api.routes.practice import router as practice_router
from models.schemas import HealthResponse

# ── Logging ────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("AI Tutor Backend starting up...")
    logger.info(f"   LLM Provider : {os.getenv('LLM_PROVIDER', 'openai')}")
    logger.info(f"   LLM Model    : {os.getenv('LLM_MODEL', 'gpt-4o-mini')}")
    yield
    logger.info("AI Tutor Backend shutting down...")

app = FastAPI(
    title="AI Tutor - confusion aware adaptive learning system (CAALS)",
    description = (
        "An adaptive AI tutoring system that diagnoses why a learner is struck"
        " and generates personized, confusion aware explanations"
        "build for the aws ai for bharat hakathon by team Data Dragons."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS (cross origin resource sharing)──────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ─────────────────────────────────────────────────────
app.include_router(explain_router)
app.include_router(practice_router)

