"""
FastAPI Application Entry Point
Indian Creative AI — Script Generation System
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from api.routes import scripts, health, music

app = FastAPI(
    title="Indian Creative AI — Script Generator",
    description="AI-powered creative script generation in 9 Indian languages using Ollama + Qwen2.5",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — allow frontend to talk to API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(health.router, prefix="/api")
app.include_router(scripts.router, prefix="/api/scripts")
app.include_router(music.router)

# Serve frontend static files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


@app.get("/", include_in_schema=False)
async def serve_frontend():
    """Serve the frontend UI"""
    index_path = os.path.join(frontend_dir, "index.html")
    return FileResponse(index_path)


@app.get("/api", tags=["Info"])
async def api_info():
    return {
        "name": "Indian Creative AI — Script Generator",
        "version": "1.0.0",
        "description": "Generate creative scripts & music briefs in 10 Indian languages",
        "supported_languages": 10,
        "endpoints": {
            "health": "/api/health",
            "generate_script": "POST /api/scripts/generate",
            "generate_music": "POST /api/music/generate",
            "list_languages": "/api/scripts/languages",
            "list_formats": "/api/scripts/formats",
            "list_ragas": "/api/music/ragas",
            "list_instruments": "/api/music/instruments",
            "list_fusions": "/api/music/fusions",
            "docs": "/docs",
        },
    }
