"""
Script Generator — Core engine using Ollama + Qwen2.5
No API key required. Runs 100% locally.
"""

import os
import re
import time
from dataclasses import dataclass
from typing import Optional

import ollama
from dotenv import load_dotenv

from models.prompt_builder import build_prompt
from models.language_support import get_language, get_ad_format

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:3b")


@dataclass
class ScriptResult:
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


def check_ollama_connection() -> dict:
    """Check if Ollama is running and the model is available"""
    try:
        client = ollama.Client(host=OLLAMA_HOST)
        models = client.list()
        available = [m.model for m in models.models]
        model_ready = any(MODEL_NAME in m for m in available)
        return {
            "connected": True,
            "available_models": available,
            "model_ready": model_ready,
            "model_name": MODEL_NAME,
        }
    except Exception as e:
        return {
            "connected": False,
            "error": str(e),
            "message": f"Ollama is not running. Please start Ollama and ensure '{MODEL_NAME}' is pulled.",
        }


def generate_script(
    language: str,
    ad_format: str,
    theme: str,
    brand_name: str,
    tone: str,
    industry: str,
    festival: str = "none",
    target_audience: str = "general Indian audience",
    usp: str = "",
    product_description: str = "",
) -> ScriptResult:
    """
    Generate a creative script in an Indian language using Ollama + Qwen2.5.
    """
    lang_config = get_language(language)
    format_config = get_ad_format(ad_format)

    # Build the full prompt
    system_prompt, user_message = build_prompt(
        language=language,
        ad_format=ad_format,
        theme=theme,
        brand_name=brand_name,
        tone=tone,
        industry=industry,
        festival=festival,
        target_audience=target_audience,
        usp=usp,
        product_description=product_description,
    )

    # Call Ollama
    client = ollama.Client(host=OLLAMA_HOST)
    start_time = time.time()

    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            options={
                "temperature": 0.85,      # Creative but not chaotic
                "top_p": 0.9,
                "top_k": 40,
                "num_predict": 600,       # Max tokens for output
                "repeat_penalty": 1.1,
            },
        )
        generation_time = round(time.time() - start_time, 2)
        raw_script = response.message.content.strip()

    except Exception as e:
        raise RuntimeError(
            f"Failed to generate script. Is Ollama running with '{MODEL_NAME}'?\nError: {str(e)}"
        )

    # Extract a title from the script or generate one
    title = _extract_title(raw_script, brand_name, theme, lang_config["name"])

    return ScriptResult(
        title=title,
        script=raw_script,
        language=language,
        language_native=lang_config["native"],
        ad_format=format_config["name"],
        brand_name=brand_name,
        estimated_duration=format_config["duration"],
        model_used=MODEL_NAME,
        generation_time_sec=generation_time,
        metadata={
            "tone": tone,
            "industry": industry,
            "festival": festival,
            "theme": theme,
            "script_type": lang_config["script"],
        },
    )


def _extract_title(script: str, brand_name: str, theme: str, language: str) -> str:
    """Extract or generate a meaningful title for the script"""
    # 1. Look for 'Campaign:' line (New Format)
    campaign_match = re.search(r"Campaign:\s*(.+)", script, re.IGNORECASE)
    if campaign_match:
        return _truncate_title(campaign_match.group(1).strip())

    # 2. Look for [TAGLINE] (Old Format)
    tagline_match = re.search(r"\[TAGLINE[^\]]*\]:\s*(.+)", script, re.IGNORECASE)
    if tagline_match:
        return _truncate_title(tagline_match.group(1).strip())

    # 3. Look for (Narrator) line at the end (Dataset Format)
    narrator_match = re.search(r"\(Narrator\)\s*(.+)", script, re.IGNORECASE)
    if narrator_match:
        return _truncate_title(narrator_match.group(1).strip())

    # 4. Fallback
    return f"{brand_name} — {theme.title()} ({language})"


def _truncate_title(text: str) -> str:
    """Helper to truncate long titles"""
    if len(text) > 60:
        return text[:57] + "..."
    return text
