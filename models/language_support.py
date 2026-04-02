"""
Indian Language Support Configuration
Supported: Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi
"""

SUPPORTED_LANGUAGES = {
    "english": {
        "name": "English",
        "native": "English",
        "script": "Latin",
        "code": "en",
        "flag": "🌍",
        "instruction": "Write the entire script in English. Use simple, impactful language suited for Indian audiences.",
        "regions": ["Pan-India", "Urban India", "Global"],
    },
    "hindi": {
        "name": "Hindi",
        "native": "हिन्दी",
        "script": "Devanagari",
        "code": "hi",
        "flag": "🇮🇳",
        "instruction": "Write the entire script in Hindi using Devanagari script (हिन्दी में लिखें). Do NOT use English unless it is a brand name.",
        "regions": ["North India", "Central India", "UP", "Delhi", "MP", "Rajasthan"],
    },
    "tamil": {
        "name": "Tamil",
        "native": "தமிழ்",
        "script": "Tamil",
        "code": "ta",
        "flag": "🏛️",
        "instruction": "Write the script in natural spoken Tamil (Tanglish allowed where natural). Use Tamil script (தமிழ்) for dialogues but English for technical terms/brand names. Make it punchy and colloquial.",
        "regions": ["Tamil Nadu", "Puducherry", "Sri Lanka Tamils"],
    },
    "telugu": {
        "name": "Telugu",
        "native": "తెలుగు",
        "script": "Telugu",
        "code": "te",
        "flag": "🌺",
        "instruction": "Write the entire script in Telugu using Telugu script (తెలుగులో రాయండి). Do NOT use English unless it is a brand name.",
        "regions": ["Andhra Pradesh", "Telangana"],
    },
    "bengali": {
        "name": "Bengali",
        "native": "বাংলা",
        "script": "Bengali",
        "code": "bn",
        "flag": "🐯",
        "instruction": "Write the entire script in Bengali using Bengali script (বাংলায় লিখুন). Do NOT use English unless it is a brand name.",
        "regions": ["West Bengal", "Bangladesh", "Assam"],
    },
    "marathi": {
        "name": "Marathi",
        "native": "मराठी",
        "script": "Devanagari",
        "code": "mr",
        "flag": "🦁",
        "instruction": "Write the entire script in Marathi using Devanagari script (मराठीत लिहा). Do NOT use English unless it is a brand name.",
        "regions": ["Maharashtra", "Goa"],
    },
    "gujarati": {
        "name": "Gujarati",
        "native": "ગુજરાતી",
        "script": "Gujarati",
        "code": "gu",
        "flag": "💎",
        "instruction": "Write the entire script in Gujarati using Gujarati script (ગુજરાતીમાં લખો). Do NOT use English unless it is a brand name.",
        "regions": ["Gujarat", "Surat", "Ahmedabad"],
    },
    "kannada": {
        "name": "Kannada",
        "native": "ಕನ್ನಡ",
        "script": "Kannada",
        "code": "kn",
        "flag": "🌟",
        "instruction": "Write the entire script in Kannada using Kannada script (ಕನ್ನಡದಲ್ಲಿ ಬರೆಯಿರಿ). Do NOT use English unless it is a brand name.",
        "regions": ["Karnataka", "Bengaluru"],
    },
    "malayalam": {
        "name": "Malayalam",
        "native": "മലയാളം",
        "script": "Malayalam",
        "code": "ml",
        "flag": "🌴",
        "instruction": "Write the entire script in Malayalam using Malayalam script (മലയാളത്തിൽ എഴുതുക). Do NOT use English unless it is a brand name.",
        "regions": ["Kerala", "Lakshadweep"],
    },
    "punjabi": {
        "name": "Punjabi",
        "native": "ਪੰਜਾਬੀ",
        "script": "Gurmukhi",
        "code": "pa",
        "flag": "🌾",
        "instruction": "Write the entire script in Punjabi using Gurmukhi script (ਪੰਜਾਬੀ ਵਿੱਚ ਲਿਖੋ). Do NOT use English unless it is a brand name.",
        "regions": ["Punjab", "Chandigarh", "Haryana"],
    },
}

AD_FORMATS = {
    "tv_ad_30": {
        "name": "TV Ad (30 sec)",
        "icon": "📺",
        "duration": "30 seconds",
        "word_count": "~75 words",
        "structure": "Hook (5s) → Problem (8s) → Solution (10s) → Brand Reveal (5s) → Tagline (2s)",
        "instructions": "Write a punchy 30-second TV advertisement script. Format as:\n[SCENE]: describe visual\n[VO/DIALOGUE]: spoken words\nKeep it emotional and memorable.",
    },
    "tv_ad_60": {
        "name": "TV Ad (60 sec)",
        "icon": "🎬",
        "duration": "60 seconds",
        "word_count": "~150 words",
        "structure": "Story setup (15s) → Conflict (15s) → Resolution with product (20s) → Tagline (10s)",
        "instructions": "Write a 60-second TV advertisement with a mini story arc. Format as:\n[SCENE]: describe visual\n[VO/DIALOGUE]: spoken words",
    },
    "radio_spot": {
        "name": "Radio Spot (30 sec)",
        "icon": "📻",
        "duration": "30 seconds",
        "word_count": "~80 words",
        "structure": "Attention hook → Key message → Call to action → Jingle/Tagline",
        "instructions": "Write a 30-second radio spot (audio only, no visuals). Format as:\n[ANNOUNCER]: text\n[JINGLE/SFX]: description\nMake it catchy and easy to remember.",
    },
    "social_reel": {
        "name": "Social Media Reel (15-30 sec)",
        "icon": "📱",
        "duration": "15-30 seconds",
        "word_count": "~40-60 words",
        "structure": "Hook (3s) → Content (20s) → CTA (5s)",
        "instructions": "Write a short, punchy social media reel script. Format as:\n[CAPTION]: on-screen text\n[VO]: voiceover\n[ACTION]: visual action\nMake it trendy and shareable.",
    },
    "ott_preroll": {
        "name": "OTT Pre-roll (15 sec)",
        "icon": "🎥",
        "duration": "15 seconds",
        "word_count": "~35 words",
        "structure": "Brand hook (5s) → Offer (7s) → CTA (3s)",
        "instructions": "Write a 15-second unskippable OTT pre-roll. Must grab attention in the first 2 seconds. Format as:\n[SCENE]: visual\n[VO]: words",
    },
}


def get_language(lang_key: str) -> dict:
    return SUPPORTED_LANGUAGES.get(lang_key.lower(), SUPPORTED_LANGUAGES["hindi"])


def get_ad_format(format_key: str) -> dict:
    return AD_FORMATS.get(format_key, AD_FORMATS["tv_ad_30"])


def list_languages() -> list:
    return [
        {
            "key": k,
            "name": v["name"],
            "native": v["native"],
            "flag": v["flag"],
            "script": v["script"],
        }
        for k, v in SUPPORTED_LANGUAGES.items()
    ]


def list_ad_formats() -> list:
    return [
        {"key": k, "name": v["name"], "icon": v["icon"], "duration": v["duration"]}
        for k, v in AD_FORMATS.items()
    ]
