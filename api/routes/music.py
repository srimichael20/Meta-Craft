"""
Music generation API routes
"""

import os
from fastapi import APIRouter, HTTPException

from api.schemas import MusicRequest, MusicResponse
from models.music_generator import generate_music_brief
from models.music_knowledge import list_ragas, list_instruments, list_fusions

router = APIRouter(prefix="/api/music", tags=["Music"])
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:3b")


@router.post("/generate", response_model=MusicResponse)
async def create_music_brief(request: MusicRequest):
    """Generate an Indian music production brief for an ad campaign."""
    try:
        result = generate_music_brief(
            ad_format=request.ad_format,
            tone=request.tone,
            industry=request.industry,
            brand_name=request.brand_name,
            theme=request.theme,
            festival=request.festival,
            fusion_style=request.fusion_style,
            language=request.language,
        )
        return MusicResponse(
            success=True,
            title=result.title,
            brief=result.brief,
            raga=result.raga,
            fusion_style=result.fusion_style,
            tempo=result.tempo,
            instruments=result.instruments,
            model_used=MODEL_NAME,
            generation_time_sec=result.generation_time_sec,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ragas")
async def get_ragas():
    """Get all available Indian ragas."""
    return {"ragas": list_ragas()}


@router.get("/instruments")
async def get_instruments():
    """Get all available Indian instruments."""
    return {"instruments": list_instruments()}


@router.get("/fusions")
async def get_fusions():
    """Get all available fusion styles."""
    return {"fusions": list_fusions()}
