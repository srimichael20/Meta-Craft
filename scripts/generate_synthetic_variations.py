import json
import os
import time
import re
import urllib.request

# Configuration
URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:1b" # Use base model for variety or 'metacraft' for consistency
OUTPUT_PATH = "data/synthetic_ads_dataset.json"

# Highly Varied Seeds for Pan-India Coverage
BRANDS = [
    {"brand": "Amul", "tagline": "The Taste of India", "themes": ["Morning breakfast", "Tiffin box", "Rainy day tea", "Nation pride"]},
    {"brand": "Maggi", "tagline": "2-Minute Noodles", "themes": ["Hostel late night", "Quick snack", "Rainy weather", "Mom making it"]},
    {"brand": "Thums Up", "tagline": "Taste the Thunder", "themes": ["Action stunt", "Summer heat", "Bravery", "Friendship"]},
    {"brand": "Zomato", "tagline": "Every craving satisfied", "themes": ["Late night hunger", "Office lunch", "Party order", "Raining outside"]},
    {"brand": "Blinkit", "tagline": "Delivery in 10 mins", "themes": ["Forgot milk", "Last minute guests", "Pooja essentials", "Emergency fix"]},
    {"brand": "Ariel", "tagline": "Share The Load", "themes": ["Equality", "School uniform", "Diwali cleaning", "Father and daughter"]},
    {"brand": "Tata Tea", "tagline": "Jaago Re", "themes": ["Social awakening", "Morning routine", "Village meeting", "Inspiration"]},
    {"brand": "Mahindra", "tagline": "Rise", "themes": ["Rural strength", "Farm work", "Family road trip", "Empowerment"]},
    {"brand": "Mysore Sandal", "tagline": "Tradition of Fragrance", "themes": ["Heritage", "Beauty routine", "Wedding purnea", "Royal feel"]},
    {"brand": "Senco Gold", "tagline": "Karigari of Bengal", "themes": ["Durga Puja", "Wedding jewellery", "Mother-daughter bond", "Traditional art"]},
    {"brand": "PhonePe", "tagline": "Karte Ja. Badhte Ja.", "themes": ["Small shop payment", "Travel ease", "Trust", "Youth spirit"]},
]

LANGUAGES = ["Hindi", "Tamil", "Malayalam", "Telugu", "Kannada", "Marathi", "Bengali", "Gujarati", "Punjabi"]

def get_native_pattern(language):
    patterns = {
        "Hindi": r'[\u0900-\u097F]',
        "Marathi": r'[\u0900-\u097F]',
        "Tamil": r'[\u0B80-\u0BFF]',
        "Malayalam": r'[\u0D00-\u0D7F]',
        "Telugu": r'[\u0C00-\u0C7F]',
        "Kannada": r'[\u0C80-\u0CFF]',
        "Bengali": r'[\u0980-\u09FF]',
        "Punjabi": r'[\u0A00-\u0A7F]',
        "Gujarati": r'[\u0A80-\u0AFF]'
    }
    return patterns.get(language, r'.')

def generate_call(prompt):
    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7, "num_predict": 350}
    }
    req = urllib.request.Request(URL, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            res = json.loads(response.read().decode('utf-8'))
            return res.get('response', '')
    except Exception as e:
        print(f"  Request Error: {e}")
    return ""

def main():
    if not os.path.exists("data"): os.makedirs("data")
    
    dataset = []
    if os.path.exists(OUTPUT_PATH):
        try:
            with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
                dataset = json.load(f)
        except: dataset = []

    target_count = 150 # Aim for 150 meaningful synthetic variations
    current_count = len(dataset)
    
    print(f"Starting Synthetic Generation. Target: {target_count}. Current: {current_count}")

    # Generate combinations
    for brand_info in BRANDS:
        for theme in brand_info['themes']:
            for lang in LANGUAGES:
                if current_count >= target_count: break
                
                # Deduplication check
                if any(i['response']['Brand'] == brand_info['brand'] and i['response']['Language'] == lang and i['response']['Theme'] == theme for i in dataset):
                    continue

                print(f"[{current_count+1}/{target_count}] {brand_info['brand']} | {lang} | {theme}")
                
                prompt = f"""Write a 30s ad in {lang}.
Brand: {brand_info['brand']}
Theme: {theme}
Tagline: {brand_info['tagline']}

[CONTEXT]:
[VISUAL]:
[AUDIO/DIALOGUE]: (Strictly {lang} script)
[TAGLINE]:
"""
                content = generate_call(prompt)
                
                # Basic validation
                pattern = get_native_pattern(lang)
                if "[AUDIO/DIALOGUE]" in content and re.search(pattern, content):
                    entry = {
                        "instruction": f"Write an organic advertisement for {brand_info['brand']} in {lang} with theme {theme}.",
                        "response": {
                            "Brand": brand_info['brand'],
                            "Language": lang,
                            "Theme": theme,
                            "Content": content
                        }
                    }
                    dataset.append(entry)
                    current_count += 1
                    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
                        json.dump(dataset, f, indent=2, ensure_ascii=False)
                    print(f"  Success.")
                else:
                    print(f"  Failed validation (Format or Native Script).")
                
                time.sleep(1)
            if current_count >= target_count: break
        if current_count >= target_count: break

    print(f"Finished. Total Synthetic Samples: {len(dataset)}")

if __name__ == "__main__":
    main()
