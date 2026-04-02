"""
Health check routes
"""

from fastapi import APIRouter
from api.schemas import HealthResponse
from models.script_generator import check_ollama_connection
import os

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Check if the server and Ollama model are ready"""
    status = check_ollama_connection()
    model_name = os.getenv("MODEL_NAME", "qwen2.5:3b")

    if status.get("connected"):
        return HealthResponse(
            status="ok",
            ollama_connected=True,
            model_ready=status.get("model_ready", False),
            model_name=model_name,
            message=(
                f"✅ Ollama connected. Model '{model_name}' is ready."
                if status.get("model_ready")
                else f"⚠️ Ollama connected but model '{model_name}' not found. Run: ollama pull {model_name}"
            ),
        )
    else:
        return HealthResponse(
            status="ollama_offline",
            ollama_connected=False,
            model_ready=False,
            model_name=model_name,
            message="❌ Ollama is not running. Please start Ollama and run: ollama pull " + model_name,
        )
