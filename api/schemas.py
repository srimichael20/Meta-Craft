"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional


class ScriptRequest(BaseModel):
    language: str = Field(
        default="hindi",
        description="Target language key (hindi, tamil, telugu, bengali, marathi, gujarati, kannada, malayalam, punjabi)",
    )
    ad_format: str = Field(
        default="tv_ad_30",
        description="Ad format key (tv_ad_30, tv_ad_60, radio_spot, social_reel, ott_preroll)",
    )
    brand_name: str = Field(..., description="Name of the brand")
    theme: str = Field(..., description="Core creative theme / message")
    tone: str = Field(
        default="emotional",
        description="Tone of the script (emotional, energetic, humorous, inspirational, elegant, informative)",
    )
    industry: str = Field(
        default="fmcg",
        description="Industry vertical (telecom, fmcg, fintech, ecommerce, jewellery, real_estate, food_beverage, education, fashion, automobile)",
    )
    festival: str = Field(
        default="none",
        description="Festival context (diwali, holi, eid, christmas, onam, pongal, navratri, independence_day, none)",
    )
    target_audience: Optional[str] = Field(
        default="general Indian audience",
        description="Target audience description",
    )
    usp: Optional[str] = Field(
        default="",
        description="Unique Selling Point of the brand/product",
    )
    product_description: Optional[str] = Field(
        default="",
        description="Description of the product/service being advertised",
    )


class ScriptResponse(BaseModel):
    success: bool
    title: str
    script: str
    language: str
    language_native: str
    ad_format: str
    brand_name: str
    estimated_duration: str
    model_used: str
    generation_time_sec: float
    metadata: dict


class HealthResponse(BaseModel):
    status: str
    ollama_connected: bool
    model_ready: bool
    model_name: str
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: str


class MusicRequest(BaseModel):
    ad_format: str = Field(
        default="tv_ad_30",
        description="Ad format key (tv_ad_30, tv_ad_60, radio_spot, social_reel, ott_preroll)",
    )
    brand_name: str = Field(default="", description="Name of the brand (optional)")
    theme: str = Field(default="", description="Creative theme for the music")
    tone: str = Field(
        default="emotional",
        description="Mood/tone (emotional, energetic, humorous, inspirational, elegant, informative)",
    )
    industry: str = Field(
        default="fmcg",
        description="Industry vertical",
    )
    festival: str = Field(
        default="none",
        description="Festival context",
    )
    fusion_style: str = Field(
        default="auto",
        description="Music fusion style (auto, lo_fi_indian, trap_desi, classical_electronic, bollywood_pop, ambient_indian, folk_modern, qawwali_edm, south_indian_fusion)",
    )
    language: str = Field(
        default="hindi",
        description="Target language/region for cultural context",
    )


class MusicResponse(BaseModel):
    success: bool
    title: str
    brief: str
    raga: str
    fusion_style: str
    tempo: str
    instruments: list
    model_used: str
    generation_time_sec: float
