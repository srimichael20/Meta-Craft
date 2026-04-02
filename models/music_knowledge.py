"""
Indian Music Knowledge Base
Ragas, instruments, moods, tempos, and genre mappings for Indian ad music generation.
"""

RAGAS = {
    "yaman": {
        "name": "Yaman",
        "mood": "romantic, serene, uplifting, elegant",
        "time": "Evening",
        "emotion": "hope, aspiration, beauty",
        "best_for": ["jewellery", "real_estate", "fintech", "fashion"],
        "notes": "Sa Re Ga Ma# Pa Dha Ni Sa",
    },
    "bhairav": {
        "name": "Bhairav",
        "mood": "devotional, intense, powerful, majestic",
        "time": "Early morning",
        "emotion": "strength, devotion, grandeur",
        "best_for": ["automobile", "education", "banking"],
        "notes": "Sa re Ga Ma Pa dha Ni Sa",
    },
    "des": {
        "name": "Des",
        "mood": "patriotic, nostalgic, warm, heartfelt",
        "time": "Late evening",
        "emotion": "nostalgia, patriotism, belonging",
        "best_for": ["telecom", "banking", "fmcg"],
        "notes": "Sa Re Ma Pa Ni Sa / Sa ni Dha Pa Ma Ga Re Sa",
    },
    "pahadi": {
        "name": "Pahadi",
        "mood": "folk, festive, joyful, light",
        "time": "Any",
        "emotion": "celebration, folk happiness, simplicity",
        "best_for": ["fmcg", "food_beverage", "ecommerce"],
        "notes": "Sa Re Ga Pa Dha Sa",
    },
    "bihag": {
        "name": "Bihag",
        "mood": "romantic, dreamy, longing",
        "time": "Late night",
        "emotion": "love, desire, beauty",
        "best_for": ["jewellery", "fashion", "food_beverage"],
        "notes": "Sa Ga Ma Pa Ni Sa",
    },
    "khamaj": {
        "name": "Khamaj",
        "mood": "playful, romantic, light classical",
        "time": "Night",
        "emotion": "flirtation, joy, celebration",
        "best_for": ["fashion", "food_beverage", "ecommerce"],
        "notes": "Sa Re Ga Ma Pa Dha ni Sa",
    },
    "malkauns": {
        "name": "Malkauns",
        "mood": "mysterious, deep, powerful, meditative",
        "time": "Midnight",
        "emotion": "intensity, mystery, depth",
        "best_for": ["automobile", "fintech", "education"],
        "notes": "Sa ga Ma dha ni Sa",
    },
    "bhimpalasi": {
        "name": "Bhimpalasi",
        "mood": "emotional, yearning, afternoon warmth",
        "time": "Afternoon",
        "emotion": "longing, warmth, tenderness",
        "best_for": ["telecom", "fmcg", "jewellery"],
        "notes": "Sa Re ga Ma Pa Ni Dha Pa",
    },
}

INSTRUMENTS = {
    "sitar": {"name": "Sitar", "type": "string", "vibe": "classical, meditative, iconic Indian", "icon": "🎸"},
    "tabla": {"name": "Tabla", "type": "percussion", "vibe": "rhythmic, energetic, groovy", "icon": "🥁"},
    "flute_bansuri": {"name": "Bansuri (Flute)", "type": "wind", "vibe": "serene, pastoral, romantic", "icon": "🎵"},
    "santoor": {"name": "Santoor", "type": "string", "vibe": "ethereal, dreamy, Kashmir", "icon": "✨"},
    "veena": {"name": "Veena", "type": "string", "vibe": "sacred, South Indian, classical", "icon": "🎶"},
    "mridangam": {"name": "Mridangam", "type": "percussion", "vibe": "South Indian, rhythmic, powerful", "icon": "🪘"},
    "dhol": {"name": "Dhol", "type": "percussion", "vibe": "Punjabi, high-energy, celebration", "icon": "🥁"},
    "harmonium": {"name": "Harmonium", "type": "keyboard", "vibe": "devotional, ghazal, qawwali", "icon": "🎹"},
    "sarangi": {"name": "Sarangi", "type": "string", "vibe": "soulful, emotional, melancholic", "icon": "🎻"},
    "shehnai": {"name": "Shehnai", "type": "wind", "vibe": "auspicious, wedding, celebration", "icon": "🎺"},
    "tanpura": {"name": "Tanpura", "type": "drone", "vibe": "meditative, ambient, foundational", "icon": "🕉️"},
}

MODERN_FUSIONS = {
    "lo_fi_indian": {
        "name": "Lo-fi Indian",
        "description": "Tabla + lo-fi hip-hop beats + ambient sitar loops — chill, urban, Gen Z",
        "tempo": "70-85 BPM",
        "instruments": ["tabla", "sitar", "tanpura"],
        "modern_elements": ["lo-fi drum pattern", "vinyl crackle", "reverb pads"],
    },
    "trap_desi": {
        "name": "Desi Trap",
        "description": "808 bass + dhol patterns + hip-hop hi-hats — aggressive, youth, street",
        "tempo": "130-150 BPM",
        "instruments": ["dhol", "tabla"],
        "modern_elements": ["808 bass", "trap hi-hats", "auto-tune vocal chops"],
    },
    "classical_electronic": {
        "name": "Classical Electronic",
        "description": "Sitar/santoor melodies + EDM drops + synth pads — premium, cinematic",
        "tempo": "120-128 BPM",
        "instruments": ["sitar", "santoor", "tabla"],
        "modern_elements": ["synth arps", "EDM build + drop", "sub bass"],
    },
    "bollywood_pop": {
        "name": "Bollywood Pop",
        "description": "Catchy vocal hooks + dholak + modern production — mainstream, mass appeal",
        "tempo": "100-120 BPM",
        "instruments": ["dhol", "harmonium", "flute_bansuri"],
        "modern_elements": ["pop drum kit", "auto-tune", "piano stabs"],
    },
    "ambient_indian": {
        "name": "Ambient Indian",
        "description": "Tanpura drone + bansuri + gentle tabla — meditative, luxury, elegant",
        "tempo": "60-75 BPM",
        "instruments": ["tanpura", "flute_bansuri", "santoor"],
        "modern_elements": ["reverb", "ambient pads", "nature SFX"],
    },
    "folk_modern": {
        "name": "Folk Modern Remix",
        "description": "Traditional folk melodies + modern drums + bass guitar — festive, energetic",
        "tempo": "110-130 BPM",
        "instruments": ["dhol", "harmonium", "shehnai"],
        "modern_elements": ["modern drum kit", "bass guitar", "synth stabs"],
    },
    "qawwali_edm": {
        "name": "Qawwali EDM",
        "description": "Qawwali vocal loops + harmonium + electronic drops — spiritual meets club",
        "tempo": "125-140 BPM",
        "instruments": ["harmonium", "tabla", "tanpura"],
        "modern_elements": ["EDM drops", "vocal chops", "build-ups"],
    },
    "south_indian_fusion": {
        "name": "South Indian Fusion",
        "description": "Veena/mridangam + electronic bass + Carnatic flavour — premium, regional",
        "tempo": "90-110 BPM",
        "instruments": ["veena", "mridangam", "flute_bansuri"],
        "modern_elements": ["electronic bass", "synth pads", "clap patterns"],
    },
}

MOOD_MAP = {
    "emotional": {"ragas": ["bhimpalasi", "yaman", "des"], "fusions": ["ambient_indian", "classical_electronic"], "energy": "low-medium"},
    "energetic": {"ragas": ["pahadi", "khamaj"], "fusions": ["trap_desi", "bollywood_pop", "folk_modern"], "energy": "high"},
    "humorous": {"ragas": ["khamaj", "pahadi"], "fusions": ["bollywood_pop", "lo_fi_indian"], "energy": "medium"},
    "inspirational": {"ragas": ["des", "bhairav", "yaman"], "fusions": ["classical_electronic", "folk_modern"], "energy": "medium-high"},
    "elegant": {"ragas": ["yaman", "bihag", "malkauns"], "fusions": ["ambient_indian", "classical_electronic", "south_indian_fusion"], "energy": "low-medium"},
    "informative": {"ragas": ["yaman", "bhimpalasi"], "fusions": ["lo_fi_indian", "ambient_indian"], "energy": "low"},
}

FESTIVAL_MUSIC = {
    "diwali": {"suggested_ragas": ["yaman", "pahadi"], "suggested_fusions": ["bollywood_pop", "folk_modern"], "vibe": "grand, celebratory, lights, fireworks in music"},
    "holi": {"suggested_ragas": ["khamaj", "pahadi"], "suggested_fusions": ["folk_modern", "bollywood_pop", "trap_desi"], "vibe": "colourful, energetic, playful, dhol-heavy"},
    "eid": {"suggested_ragas": ["yaman", "bhimpalasi"], "suggested_fusions": ["qawwali_edm", "ambient_indian"], "vibe": "warm, spiritual, brotherhood, shehnai"},
    "onam": {"suggested_ragas": ["khamaj"], "suggested_fusions": ["south_indian_fusion", "folk_modern"], "vibe": "harvest joy, Kerala percussion, chenda"},
    "pongal": {"suggested_ragas": ["pahadi"], "suggested_fusions": ["south_indian_fusion", "folk_modern"], "vibe": "harvest, gratitude, nadaswaram, folk drums"},
    "navratri": {"suggested_ragas": ["bhairav", "des"], "suggested_fusions": ["folk_modern", "bollywood_pop"], "vibe": "garba energy, dandiya sticks, dhol-tasha"},
    "christmas": {"suggested_ragas": ["yaman"], "suggested_fusions": ["ambient_indian", "bollywood_pop"], "vibe": "warm, bells, joyful, choral elements"},
    "independence_day": {"suggested_ragas": ["des", "bhairav"], "suggested_fusions": ["classical_electronic", "folk_modern"], "vibe": "patriotic, pride, anthemic, shehnai+drums"},
    "none": {"suggested_ragas": ["yaman", "khamaj"], "suggested_fusions": ["lo_fi_indian", "bollywood_pop"], "vibe": "versatile, modern, urban"},
}


def get_raga(key: str) -> dict:
    return RAGAS.get(key, RAGAS["yaman"])

def get_fusion(key: str) -> dict:
    return MODERN_FUSIONS.get(key, MODERN_FUSIONS["bollywood_pop"])

def get_mood_music(mood: str) -> dict:
    return MOOD_MAP.get(mood.lower(), MOOD_MAP["emotional"])

def get_festival_music(festival: str) -> dict:
    return FESTIVAL_MUSIC.get(festival.lower(), FESTIVAL_MUSIC["none"])

def list_ragas() -> list:
    return [{"key": k, "name": v["name"], "mood": v["mood"], "time": v["time"]} for k, v in RAGAS.items()]

def list_instruments() -> list:
    return [{"key": k, "name": v["name"], "icon": v["icon"], "vibe": v["vibe"]} for k, v in INSTRUMENTS.items()]

def list_fusions() -> list:
    return [{"key": k, "name": v["name"], "description": v["description"], "tempo": v["tempo"]} for k, v in MODERN_FUSIONS.items()]
