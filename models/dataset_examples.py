"""
Dataset Examples — Loads dataset.json and retrieves the most relevant
examples to inject as few-shot context into the prompt.

Matching strategy:
  1. Exact language match (highest priority)
  2. Industry/product keyword match from the instruction field
  3. Falls back to any same-language example
"""

import json
import os
import random
from typing import Optional

_RAW_DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataset.json")
_SYNTHETIC_DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "synthetic_data.json")
_DATASET_CACHE: list | None = None


# Map user-facing industry keys to keywords that appear in dataset instructions
INDUSTRY_KEYWORDS = {
    "fmcg": ["soap", "ghee", "oil", "snack", "tea", "spices", "pickle", "dairy", "honey"],
    "jewellery": ["jewelry", "jewellery", "gold", "swarna", "haram"],
    "telecom": ["data", "network", "call", "internet", "5g", "recharge"],
    "fintech": ["loan", "bank", "credit", "money", "invest", "insurance", "upi"],
    "ecommerce": ["cushion", "sale", "online", "app", "delivery", "fashion"],
    "real_estate": ["home", "apartment", "villa", "plot", "investment"],
    "food_beverage": ["restaurant", "cafe", "drink", "food", "biryani", "pizza", "burger"],
    "education": ["school", "college", "course", "learn", "study", "university"],
    "fashion": ["cloth", "shirt", "saree", "dress", "jeans", "wear"],
    "automobile": ["car", "bike", "scooter", "vehicle", "mileage", "engine"],
}


def _load_dataset() -> list:
    """Load and blend both raw and synthetic datasets."""
    global _DATASET_CACHE
    if _DATASET_CACHE is not None:
        return _DATASET_CACHE

    combined = []

    # 1. Load Synthetic Data (High Quality - Priority)
    if os.path.exists(_SYNTHETIC_DATASET_PATH):
        try:
            with open(_SYNTHETIC_DATASET_PATH, "r", encoding="utf-8") as f:
                synthetic = json.load(f)
                for item in synthetic:
                    item["is_synthetic"] = True  # Mark as high quality
                    combined.append(item)
        except Exception:
            pass

    # 2. Load Raw Data (Volume - Fallback)
    if os.path.exists(_RAW_DATASET_PATH):
        try:
            with open(_RAW_DATASET_PATH, "r", encoding="utf-8") as f:
                raw = json.load(f)
                # Deduplicate raw data
                seen = set()
                for item in raw:
                    resp = item.get("response", {})
                    key = (resp.get("Brand", ""), resp.get("Language", ""))
                    if key not in seen:
                        seen.add(key)
                        item["is_synthetic"] = False
                        combined.append(item)
        except Exception:
            pass

    _DATASET_CACHE = combined
    return _DATASET_CACHE


def _normalize_language(lang: str) -> str:
    """Normalize language key to match dataset Language field."""
    mapping = {
        "hindi": "Hindi",
        "tamil": "Tamil",
        "telugu": "Telugu",
        "bengali": "Bengali",
        "marathi": "Marathi",
        "gujarati": "Gujarati",
        "kannada": "Kannada",
        "malayalam": "Malayalam",
        "punjabi": "Punjabi",
        "odia": "Odia",
    }
    return mapping.get(lang.lower(), lang.title())


def get_dataset_examples(
    language: str,
    industry: str = "",
    product_description: str = "",
    theme: str = "",
    count: int = 2,
) -> list[dict]:
    """
    Retrieve the best-matching dataset examples.
    Prioritizes Synthetic/High-Quality examples.
    """
    dataset = _load_dataset()
    if not dataset:
        return []

    target_lang = _normalize_language(language)

    # Filter matches
    refined_pool = []
    
    for item in dataset:
        is_synthetic = item.get("is_synthetic", False)
        
        # Synthetic data is usually in English/Mixed describing a visual, 
        # so we can use it for ANY language as a "Visual Reference" if we translate the thought.
        # But for strictly language-based retrieval, we stick to the target language 
        # OR use synthetic data (which is language-agnostic in its visual description).
        
        response = item.get("response", {})
        item_lang = response.get("Language", "English") # Synthetic might not have Language field or be English
        
        # If it's synthetic, we treat it as a "Style Match" regardless of language 
        # unless it explicitly clashes.
        
        if not is_synthetic and item_lang.lower() != target_lang.lower():
            continue # Skip raw data from other languages
            
        refined_pool.append(item)

    # Score candidates
    search_text = f"{industry} {product_description} {theme}".lower()
    industry_keys = INDUSTRY_KEYWORDS.get(industry.lower(), [])

    scored = []
    for item in refined_pool:
        is_synthetic = item.get("is_synthetic", False)
        instruction = item.get("instruction", "").lower()
        response = item.get("response", {})
        
        # Normalized fields for scoring
        if is_synthetic:
            brand = " ".join(response.get("Campaign", "").split("-")[:1])
            bg_theme = response.get("Content", "")
        else:
            brand = response.get("Brand", "")
            bg_theme = response.get("Background_Theme", "")

        score = 0
        
        # Base score for synthetic (Flow/Quality bias)
        if is_synthetic:
            score += 5 

        # Industry keyword matching
        for kw in industry_keys:
            if kw in instruction or kw.lower() in str(brand).lower() or kw in str(bg_theme).lower():
                score += 3

        # Product description matching
        if product_description:
            desc_words = [w for w in product_description.lower().split() if len(w) > 3]
            for word in desc_words:
                if word in instruction or word in str(brand).lower() or word in str(bg_theme).lower():
                    score += 2

        # Theme matching
        if theme:
            theme_words = [w for w in theme.lower().split() if len(w) > 3]
            for word in theme_words:
                if word in instruction or word in str(bg_theme).lower():
                    score += 1

        scored.append((score, item))

    # Sort by score descending
    scored.sort(key=lambda x: x[0], reverse=True)

    # Pick top unique items
    selected = []
    seen_ids = set()
    for score, item in scored:
        # Create a rough content hash to avoid dupes
        content_hash = hash(str(item.get("response")))
        if content_hash not in seen_ids:
            selected.append(item)
            seen_ids.add(content_hash)
            if len(selected) >= count:
                break
    
    return selected


def format_dataset_example(item: dict) -> str:
    """Format an example for the prompt."""
    resp = item.get("response", {})
    
    # Check if it's our new Synthetic format
    if "Format" in resp and resp["Format"] == "Visual/Audio/Dialogue":
        return f"""Campaign: {resp.get('Campaign', 'N/A')}
{resp.get('Content', '')}"""

    # Fallback to Old Raw Format
    dialogues = resp.get("Dialogues", [])
    dialogue_text = "\n".join(f"  {d}" for d in dialogues)

    return f"""Brand: {resp.get('Brand', 'N/A')}
Background Theme: {resp.get('Background_Theme', 'N/A')}
Dialogues:
{dialogue_text}
Making Cost: {resp.get('Making_Cost', 'N/A')}
Language: {resp.get('Language', 'N/A')}"""


def format_dataset_few_shot_block(
    language: str,
    industry: str = "",
    product_description: str = "",
    theme: str = "",
    count: int = 2,
) -> str:
    """
    Build a formatted few-shot block from the dataset for prompt injection.
    """
    examples = get_dataset_examples(
        language=language,
        industry=industry,
        product_description=product_description,
        theme=theme,
        count=count,
    )

    if not examples:
        return ""

    block = ""
    for i, item in enumerate(examples, 1):
        block += f"\n--- REFERENCE EXAMPLE {i} ---\n"
        block += f"BRIEF: {item.get('instruction', 'N/A')}\n"
        block += f"RESULT:\n{format_dataset_example(item)}\n"

    return block
