import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.few_shot_examples import get_examples_for_language
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:1b"

seed = {"brand": "Lifebuoy", "tagline": "Swasthya Rakshak", "theme": "Hygiene, health, family", "language": "Marathi", "format": "Radio Spot"}

def generate_script(seed):
    ad_format = seed.get('format', 'TV Ad 30 sec')
    language = seed['language']
    
    few_shot_block = ""
    try:
        examples = get_examples_for_language(language, count=1)
        for ex in examples:
            few_shot_block += f"Input: {ex['input']}\nOutput:\n{ex['output']}\n\n"
    except Exception as e:
        few_shot_block = f"No examples available. Use cinematic time-block format. Error: {e}"

    prompt = f"""
You are a top-tier Indian creative copywriter at a world-class ad agency.
Your task is to write a high-quality, professional, and culturally resonant advertisement script.

--- FEW-SHOT EXAMPLES FOR QUALITY REFERENCE ---
{few_shot_block}
--- END OF EXAMPLES ---

Now generate the script for:
Brand: {seed['brand']}
Format: {ad_format}
Tagline: {seed['tagline']}
Theme: {seed['theme']}
Language: {language}

CRITICAL REQUIREMENTS:
1. DIALOGUE: All spoken parts (DIALOGUE, AUDIO) MUST be in {language} script.
2. FORMAT: Use the cinematic time-block format EXACTLY as shown in the examples above.
3. NO ENGLISH DIALOGUE: Except for brand names.
4. QUALITY: Minimum 3-4 time blocks. Descriptions must be vivid and cinematic.
"""
    
    data = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }).encode("utf-8")
    
    print("Sending request to Ollama...")
    req = urllib.request.Request(OLLAMA_URL, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as f:
        response = json.loads(f.read().decode("utf-8"))
        return response.get("response", "")

print("Testing generation...")
script = generate_script(seed)
print("Generated Script:")
with open("test_output.txt", "w", encoding="utf-8") as f:
    f.write(script)
print("Saved to test_output.txt")
