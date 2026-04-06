"""
Script generation routes
"""

from fastapi import APIRouter, HTTPException
from api.schemas import ScriptRequest, ScriptResponse, ErrorResponse
from models.script_generator import generate_script
from models.language_support import list_languages, list_ad_formats
from models.cultural_context import list_festivals, list_industries, list_tones

router = APIRouter()


@router.post(
    "/generate",
    response_model=ScriptResponse,
    tags=["Scripts"],
    summary="Generate a creative Indian language script",
)
async def create_script(request: ScriptRequest):
    """
    Generate a creative advertising/marketing script in the specified Indian language.
    Uses Ollama + Qwen2.5 with few-shot prompting for authentic Indian language output.
    """
    try:
        result = generate_script(
            language=request.language,
            ad_format=request.ad_format,
            theme=request.theme,
            brand_name=request.brand_name,
            tone=request.tone,
            industry=request.industry,
            festival=request.festival,
            target_audience=request.target_audience or "general Indian audience",
            usp=request.usp or "",
            product_description=request.product_description or "",
        )
        return ScriptResponse(
            success=True,
            title=result.title,
            script=result.script,
            language=result.language,
            language_native=result.language_native,
            ad_format=result.ad_format,
            brand_name=result.brand_name,
            estimated_duration=result.estimated_duration,
            model_used=result.model_used,
            generation_time_sec=result.generation_time_sec,
            metadata=result.metadata,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Script generation failed: {str(e)}")


@router.get("/languages", tags=["Scripts"], summary="List all supported Indian languages")
async def get_languages():
    """Returns all 9 supported Indian languages with their native scripts"""
    return {"languages": list_languages()}


@router.get("/formats", tags=["Scripts"], summary="List all supported ad formats")
async def get_formats():
    """Returns all supported ad formats"""
    return {"formats": list_ad_formats()}


@router.get("/festivals", tags=["Scripts"], summary="List all festival contexts")
async def get_festivals():
    return {"festivals": list_festivals()}


@router.get("/industries", tags=["Scripts"], summary="List all industry verticals")
async def get_industries():
    return {"industries": list_industries()}


@router.get("/tones", tags=["Scripts"], summary="List all available tones")
async def get_tones():
    return {"tones": list_tones()}
