"""
Indian Ad Music Brief Generator
Uses Ollama + Qwen2.5 to generate detailed music production briefs
for Indian ad campaigns — including raga suggestions, instruments, fusion styles, and timing.
"""
import os
import time
from dataclasses import dataclass

from models.music_knowledge import (
    get_raga, get_fusion, get_mood_music, get_festival_music,
    RAGAS, INSTRUMENTS, MODERN_FUSIONS,
)

try:
    import ollama
except ImportError:
    ollama = None

MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:3b")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")


MUSIC_SYSTEM_PROMPT = """You are an elite Indian music director and ad jingle composer — think A.R. Rahman meets modern ad scoring.
You create detailed music briefs for Indian advertising campaigns that production teams can execute.

Your expertise:
- Deep knowledge of Indian ragas, taals, and their emotional effects
- Fusion of Indian classical with modern genres (lo-fi, trap, EDM, ambient, pop)
- Scoring for different ad formats (30s TV spots, 15s reels, 60s brand films)
- Understanding of how music drives emotion in advertising

OUTPUT FORMAT — You MUST follow this exact structure:

🎵 MUSIC BRIEF: [Title]

**CONCEPT:** [1-2 line creative vision for the music]

**RAGA/SCALE:** [Primary raga or scale + why it fits]

**TEMPO:** [Exact BPM + feel description]

**INSTRUMENTS:**
- Lead: [Primary instrument + role]
- Rhythm: [Percussion + pattern]
- Texture: [Supporting instruments + pads]
- Modern: [Electronic/production elements]

**STRUCTURE (for [duration]):**
- 0:00-0:XX — [Section: what happens musically]
- 0:XX-0:XX — [Section: build/drop/transition]
- 0:XX-end — [Section: resolution + tagline hit]

**MOOD PROGRESSION:** [How the emotion shifts through the track]

**REFERENCE VIBE:** [2-3 real-world references the producer can relate to]

**PRODUCTION NOTES:** [Mixing tips, key moments, any special instructions]
"""


@dataclass
class MusicResult:
    title: str
    brief: str
    raga: str
    fusion_style: str
    tempo: str
    instruments: list
    generation_time_sec: float


def generate_music_brief(
    ad_format: str,
    tone: str,
    industry: str,
    brand_name: str = "",
    theme: str = "",
    festival: str = "none",
    fusion_style: str = "auto",
    language: str = "hindi",
) -> MusicResult:
    """Generate a detailed Indian music production brief for an ad campaign."""

    if ollama is None:
        raise RuntimeError("ollama package not installed. Run: pip install ollama")

    client = ollama.Client(host=OLLAMA_HOST)
    start_time = time.time()

    # Auto-select fusion style based on mood if set to auto
    mood_music = get_mood_music(tone)
    festival_music = get_festival_music(festival)

    if fusion_style == "auto":
        # Pick best fusion from mood + festival intersection
        mood_fusions = set(mood_music["fusions"])
        fest_fusions = set(festival_music["suggested_fusions"])
        common = mood_fusions & fest_fusions
        selected_fusion_key = list(common)[0] if common else mood_music["fusions"][0]
    else:
        selected_fusion_key = fusion_style

    fusion_data = get_fusion(selected_fusion_key)

    # Pick best raga
    mood_ragas = mood_music["ragas"]
    fest_ragas = festival_music.get("suggested_ragas", [])
    common_ragas = [r for r in mood_ragas if r in fest_ragas]
    selected_raga_key = common_ragas[0] if common_ragas else mood_ragas[0]
    raga_data = get_raga(selected_raga_key)

    # Get instrument details for the fusion
    instrument_names = [INSTRUMENTS[i]["name"] for i in fusion_data["instruments"] if i in INSTRUMENTS]

    # Build the prompt
    user_prompt = f"""Create a detailed music production brief for this Indian ad campaign:

BRAND: {brand_name if brand_name else 'Generic brand'}
INDUSTRY: {industry}
AD FORMAT: {ad_format}
THEME/CONCEPT: {theme if theme else 'Modern Indian lifestyle'}
TONE/MOOD: {tone}
FESTIVAL CONTEXT: {festival if festival != 'none' else 'No specific festival'}
TARGET LANGUAGE/REGION: {language}

MUSIC DIRECTION:
- Suggested Raga: {raga_data['name']} ({raga_data['mood']}) — Notes: {raga_data['notes']}
- Fusion Style: {fusion_data['name']} — {fusion_data['description']}
- Suggested Tempo: {fusion_data['tempo']}
- Key Instruments: {', '.join(instrument_names)}
- Modern Elements: {', '.join(fusion_data['modern_elements'])}
- Energy Level: {mood_music['energy']}
- Festival Vibe: {festival_music['vibe']}

Generate a DETAILED, PRODUCTION-READY music brief that a music producer can directly use.
Be specific about timing, transitions, and emotional beats.
Include specific Indian musical references (ragas, taals, folk traditions).
"""

    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": MUSIC_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            options={
                "temperature": 0.8,
                "top_p": 0.9,
                "top_k": 40,
                "num_predict": 800,
                "repeat_penalty": 1.1,
            },
        )
        brief_text = response["message"]["content"].strip()
    except Exception as e:
        raise RuntimeError(
            f"Failed to generate music brief. Is Ollama running with '{MODEL_NAME}'?\nError: {str(e)}"
        )

    elapsed = round(time.time() - start_time, 2)

    # Extract title from the brief
    title = f"{brand_name} {tone.title()} {fusion_data['name']} Score"
    for line in brief_text.split("\n"):
        if "MUSIC BRIEF:" in line:
            title = line.split("MUSIC BRIEF:")[-1].strip()
            break

    return MusicResult(
        title=title,
        brief=brief_text,
        raga=raga_data["name"],
        fusion_style=fusion_data["name"],
        tempo=fusion_data["tempo"],
        instruments=instrument_names,
        generation_time_sec=elapsed,
    )
