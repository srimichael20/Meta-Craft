"""
Indian Cultural Context Database
Festivals, values, regional contexts, and industry verticals
"""

FESTIVALS = {
    "diwali": {
        "name": "Diwali",
        "native": "दीवाली / திருவிழா",
        "theme": "light over darkness, prosperity, family reunion, new beginnings",
        "emotions": "joy, warmth, togetherness, hope, prosperity",
        "symbols": "diyas, rangoli, sweets, fireworks, gold, Lakshmi",
        "best_for": ["jewellery", "fmcg", "fintech", "ecommerce", "real_estate"],
        "season": "October-November",
    },
    "holi": {
        "name": "Holi",
        "native": "होली",
        "theme": "colours of life, victory of good, spring joy, togetherness",
        "emotions": "fun, exuberance, playfulness, unity across differences",
        "symbols": "colours, pichkari, gulal, sweets, dance",
        "best_for": ["fmcg", "beverage", "fashion", "telecom"],
        "season": "March",
    },
    "eid": {
        "name": "Eid",
        "native": "ईद / عید",
        "theme": "gratitude, sharing, family feasting, new clothes",
        "emotions": "generosity, love, brotherhood, celebration",
        "symbols": "moon, mosque, biryani, seviyan, new clothes",
        "best_for": ["fashion", "food", "jewellery", "fmcg"],
        "season": "Varies",
    },
    "christmas": {
        "name": "Christmas",
        "native": "क्रिसमस",
        "theme": "giving, family, warmth, joy",
        "emotions": "warmth, generosity, joyfulness, hope",
        "symbols": "Christmas tree, Santa, gifts, snow, stars",
        "best_for": ["ecommerce", "retail", "fintech", "telecom"],
        "season": "December",
    },
    "onam": {
        "name": "Onam",
        "native": "ഓണം",
        "theme": "harvest, Kerala culture, King Mahabali, prosperity",
        "emotions": "pride, abundance, joy, cultural heritage",
        "symbols": "pookkalam, sadhya, vallam kali, tiger dance",
        "best_for": ["food", "fmcg", "jewellery", "real_estate"],
        "season": "August-September",
    },
    "pongal": {
        "name": "Pongal",
        "native": "பொங்கல்",
        "theme": "harvest festival, gratitude to sun and cattle, new beginnings",
        "emotions": "gratitude, simplicity, abundance, tradition",
        "symbols": "pongal pot, sugarcane, kolam, cattle",
        "best_for": ["food", "fmcg", "agriculture", "jewellery"],
        "season": "January",
    },
    "navratri": {
        "name": "Navratri / Durga Puja",
        "native": "नवरात्रि / দুর্গাপূজা",
        "theme": "feminine power, victory, dance, devotion",
        "emotions": "devotion, energy, festivity, strength",
        "symbols": "Durga, Garba, dandiya, colours, pandal",
        "best_for": ["fashion", "jewellery", "fmcg", "beverages"],
        "season": "September-October",
    },
    "independence_day": {
        "name": "Independence Day",
        "native": "स्वतंत्रता दिवस",
        "theme": "patriotism, pride, freedom, unity in diversity",
        "emotions": "pride, inspiration, nationalism, hope",
        "symbols": "tricolour, Ashok Chakra, national anthem",
        "best_for": ["telecom", "banking", "ecommerce", "education"],
        "season": "August 15",
    },
    "none": {
        "name": "General (No Festival)",
        "native": "",
        "theme": "everyday life, aspirations, progress",
        "emotions": "relatable, authentic, inspiring",
        "symbols": "family, work, progress, community",
        "best_for": ["all"],
        "season": "Year-round",
    },
}

INDUSTRIES = {
    "telecom": {
        "name": "Telecom",
        "values": "connectivity, speed, reaching loved ones, staying connected",
        "pain_points": "poor network, high bills, slow data",
        "cta_examples": ["अभी सब्सक्राइब करें", "Connect करें", "Download करो"],
    },
    "fmcg": {
        "name": "FMCG / Daily Essentials",
        "values": "quality, trust, everyday goodness, family care",
        "pain_points": "unhealthy options, high price, quality compromises",
        "cta_examples": ["अभी खरीदें", "Try करें", "घर लाएं"],
    },
    "fintech": {
        "name": "Fintech / Banking",
        "values": "security, growth, dreams, financial freedom",
        "pain_points": "savings worry, loan hassles, future uncertainty",
        "cta_examples": ["निवेश करें", "Loan लें", "Save करें"],
    },
    "ecommerce": {
        "name": "E-Commerce / Retail",
        "values": "convenience, deals, variety, fast delivery",
        "pain_points": "bad deals, slow delivery, limited choice",
        "cta_examples": ["Order करें", "Deal पाएं", "खरीदारी करें"],
    },
    "jewellery": {
        "name": "Jewellery",
        "values": "tradition, elegance, love, milestones, heritage",
        "pain_points": "authenticity concerns, price, design",
        "cta_examples": ["खरीदें", "Gift करें", "जश्न मनाएं"],
    },
    "real_estate": {
        "name": "Real Estate",
        "values": "dream home, security, investment, family",
        "pain_points": "affordability, trust, location",
        "cta_examples": ["Book करें", "Visit करें", "Invest करें"],
    },
    "food_beverage": {
        "name": "Food & Beverage",
        "values": "taste, health, family meals, indulgence",
        "pain_points": "unhealthy ingredients, bland taste",
        "cta_examples": ["Try करें", "Order करें", "खाएं"],
    },
    "education": {
        "name": "Education / EdTech",
        "values": "future, careers, learning, ambition",
        "pain_points": "cost, quality, access",
        "cta_examples": ["Enroll करें", "सीखें", "Join करें"],
    },
    "fashion": {
        "name": "Fashion / Clothing",
        "values": "style, identity, confidence, trends",
        "pain_points": "fit, price, fast fashion",
        "cta_examples": ["Shop करें", "Try करें", "Style करें"],
    },
    "automobile": {
        "name": "Automobile",
        "values": "freedom, status, family, performance",
        "pain_points": "fuel costs, maintenance, roads",
        "cta_examples": ["Test Drive करें", "Book करें", "Drive करें"],
    },
}

TONES = {
    "emotional": "heartwarming, moving, family-centric, tear-jerking storytelling",
    "energetic": "high energy, fast-paced, youth-focused, exciting and uplifting",
    "humorous": "fun, witty, light-hearted, includes relatable Indian humour",
    "inspirational": "motivational, aspirational, dream-chasing, empowering",
    "elegant": "sophisticated, premium feel, refined language, aspirational luxury",
    "informative": "clear, factual, trustworthy, educational about the product",
}


def get_festival(festival_key: str) -> dict:
    return FESTIVALS.get(festival_key.lower(), FESTIVALS["none"])


def get_industry(industry_key: str) -> dict:
    return INDUSTRIES.get(industry_key.lower(), INDUSTRIES["fmcg"])


def get_tone(tone_key: str) -> str:
    return TONES.get(tone_key.lower(), TONES["emotional"])


def list_festivals() -> list:
    return [{"key": k, "name": v["name"], "season": v["season"]} for k, v in FESTIVALS.items()]


def list_industries() -> list:
    return [{"key": k, "name": v["name"]} for k, v in INDUSTRIES.items()]


def list_tones() -> list:
    return [{"key": k, "description": v} for k, v in TONES.items()]
