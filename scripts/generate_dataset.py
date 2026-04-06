import json
import os
import random
import sys
import time
import urllib.request

# Ensure we can import from models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from models.few_shot_examples import get_examples_for_language
except ImportError:
    # Fallback for different execution contexts
    pass

# Optimization: Use Ollama to generate high-quality ad scripts based on iconic seeds
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "metacraft"

# Organic Seeds gathered from web research
SEEDS = [
    {"brand": "Amul", "tagline": "The Taste of India", "theme": "Dairy, Nation, Happiness", "language": "Hindi"},
    {"brand": "Surf Excel", "tagline": "Daag Acche Hain", "theme": "Good deeds, washing, stains", "language": "Hindi"},
    {"brand": "Cadbury", "tagline": "Kuch Meetha Ho Jaye", "theme": "Celebration, desert, bond", "language": "Hindi"},
    {"brand": "Fevikwik", "tagline": "Chutki mein chipkaye", "theme": "Humor, fixing things, instant", "language": "Hindi"},
    {"brand": "Zomato", "tagline": "Har Craving ka Cure", "theme": "Late night food, delivery", "language": "Hindi"},
    {"brand": "Jio", "tagline": "Digital India", "theme": "Connectivity, family, technology", "language": "Hindi"},
    {"brand": "Tanishq", "tagline": "Tradition with a Twist", "theme": "Wedding, gold, modern culture", "language": "Tamil"},
    {"brand": "OnePlus", "tagline": "Never Settle", "theme": "Speed, photography, technology", "language": "Malayalam"},
    {"brand": "Tata Tea", "tagline": "Jaago Re", "theme": "Social awareness, morning, tea", "language": "Bengali"},
    {"brand": "Pepsi", "tagline": "Yeh Dil Maange More", "theme": "Youth, thirst, cricket", "language": "Telugu"},
    {"brand": "Mahindra", "tagline": "Rise", "theme": "Rural strength, empowerment", "language": "Marathi"},
    {"brand": "Wagh Bakri", "tagline": "Hamesha Rishto Ki Garmahat", "theme": "Family tea time, bonding", "language": "Gujarati"},
    {"brand": "Nandini Milk", "tagline": "Pure and Fresh", "theme": "Local pride, health", "language": "Kannada"},
    {"brand": "Verka", "tagline": "Taste of Punjab", "theme": "Lassi, tradition, energy", "language": "Punjabi"},
    {"brand": "Ariel", "tagline": "Share The Load", "theme": "Equality, household chores", "language": "Hindi", "format": "OTT Pre-roll"},
    {"brand": "BigBasket", "tagline": "Free Delivery", "theme": "Convenience, grocery", "language": "Hindi", "format": "Radio Spot"},
    {"brand": "HDFC Bank", "tagline": "Understand Your World", "theme": "Banking, security", "language": "Hindi", "format": "TV Ad 60 sec"},
    
    # Marathi Expansion
    {"brand": "Lifebuoy", "tagline": "Swasthya Rakshak", "theme": "Hygiene, health, family", "language": "Marathi", "format": "Radio Spot"},
    {"brand": "Asian Paints", "tagline": "Har Ghar Kuch Kehta Hai", "theme": "Home, colors, emotional", "language": "Marathi", "format": "OTT Pre-roll"},
    {"brand": "Maharashtra Tourism", "tagline": "Unlimited", "theme": "Travel, heritage, pride", "language": "Marathi", "format": "TV Ad 60 sec"},
    
    # Gujarati Expansion
    {"brand": "Astral Pipes", "tagline": "Strong and Durable", "theme": "Strength, trust", "language": "Gujarati", "format": "Radio Spot"},
    {"brand": "Fortune Oil", "tagline": "Ghar ka Khana", "theme": "Health, taste, Gujarati snacks", "language": "Gujarati", "format": "OTT Pre-roll"},
    {"brand": "Amul Ice Cream", "tagline": "Real Milk. Real Ice Cream.", "theme": "Summer, happiness, family", "language": "Gujarati", "format": "TV Ad 60 sec"},
    
    # Kannada Expansion
    {"brand": "Mysore Sandal Soap", "tagline": "The Fragrance of Tradition", "theme": "Heritage, fragrance, beauty", "language": "Kannada", "format": "TV Ad 60 sec"},
    {"brand": "Zepto", "tagline": "Groceries in 10 mins", "theme": "Quick delivery, city life", "language": "Kannada", "format": "Radio Spot"},
    {"brand": "Karnataka Tourism", "tagline": "One State, Many Worlds", "theme": "Nature, history, adventure", "language": "Kannada", "format": "OTT Pre-roll"},
    
    # Punjabi Expansion
    {"brand": "Hershey's India", "tagline": "Moments of Happiness", "theme": "Chocolate, love, celebration", "language": "Punjabi", "format": "OTT Pre-roll"},
    {"brand": "Ambuja Cement", "tagline": "Giant Compressive Strength", "theme": "Strength, home building", "language": "Punjabi", "format": "Radio Spot"},
    {"brand": "Hero MotoCorp", "tagline": "Hum Mein Hai Hero — पंजाबिया दी शान", "theme": "Pride, riding, friendship", "language": "Punjabi", "format": "TV Ad 60 sec"},

    # Malayalam & Others
    {"brand": "Muthoot Finance", "tagline": "Trust the Gold", "theme": "Security, gold loan", "language": "Malayalam", "format": "Radio Spot"},
    {"brand": "Kalyan Jewellers", "tagline": "Trust is Everything", "theme": "Wedding, luxury", "language": "Malayalam", "format": "TV Ad 60 sec"},
    {"brand": "Horlicks", "tagline": "Taller, Stronger, Sharper", "theme": "Child health, growth", "language": "Bengali", "format": "OTT Pre-roll"},
    {"brand": "Senco Gold", "tagline": "Expression of Love", "theme": "Artistry, Bengali culture", "language": "Bengali", "format": "Radio Spot"},

    # --- Massive Expansion Phase ---
    {"brand": "Swiggy", "tagline": "Why Step Out?", "theme": "Cravings, rain, indulgence", "language": "Hindi", "format": "Social Reel"},
    {"brand": "Nykaa", "tagline": "Your Beauty, Our Passion", "theme": "Self-love, makeup, confidence", "language": "Hindi", "format": "Social Reel"},
    {"brand": "Blinkit", "tagline": "Everything in 10 minutes", "theme": "Last minute, kitchen essentials", "language": "Hindi", "format": "Social Reel"},
    {"brand": "PhonePe", "tagline": "Karte Ja. Badhte Ja.", "theme": "Universal payment, trust", "language": "Hindi", "format": "TV Ad 30 sec"},
    {"brand": "Cred", "tagline": "Not for Everyone", "theme": "Exclusivity, rewards, irony", "language": "Hindi", "format": "TV Ad 30 sec"},
    {"brand": "Maruti Suzuki", "tagline": "Kitna Deti Hai?", "theme": "Mileage, common man, middle class", "language": "Hindi", "format": "TV Ad 60 sec"},
    {"brand": "Royal Enfield", "tagline": "Made Like a Gun", "theme": "Vibration, road trip, masculinity", "language": "Hindi", "format": "Social Reel"},
    {"brand": "FabIndia", "tagline": "Celebrate India", "theme": "Ethic wear, culture, Diwali", "language": "Hindi", "format": "TV Ad 60 sec"},
    {"brand": "Google Pay", "tagline": "Simple, Secure, Fast", "theme": "Split bill, street food, ease", "language": "Tamil", "format": "Social Reel"},
    {"brand": "Myntra", "tagline": "Be Extraordinary", "theme": "Fashion, Gen Z, trends", "language": "Telugu", "format": "Social Reel"},
    {"brand": "Ajio", "tagline": "Doubt is Out", "theme": "Styles, bold colors, street fashion", "language": "Kannada", "format": "Social Reel"},
    {"brand": "Parle-G", "tagline": "G Maane Genius", "theme": "Childhood memory, chai-biscuit", "language": "Marathi", "format": "TV Ad 30 sec"},
    {"brand": "Thums Up", "tagline": "Taste the Thunder", "theme": "Action, thirst, daring", "language": "Telugu", "format": "TV Ad 30 sec"},
    {"brand": "Maggi", "tagline": "2-Minute Noodles", "theme": "Hostel life, late night, mom's touch", "language": "Hindi", "format": "OTT Pre-roll"},
    {"brand": "Coca-Cola", "tagline": "Open Happiness", "theme": "Family meal, sharing, joy", "language": "Hindi", "format": "TV Ad 30 sec"},
    {"brand": "LIC", "tagline": "Zindagi ke Saath Bhi", "theme": "Security, future, retirement", "language": "Hindi", "format": "TV Ad 60 sec"},
    {"brand": "SBI", "tagline": "The Banker to Every Indian", "theme": "Trust, nation building", "language": "Hindi", "format": "Radio Spot"},
    {"brand": "Groww", "tagline": "Investing made easy", "theme": "Stocks, SIP, youth, wealth", "language": "Hindi", "format": "Social Reel"},
    {"brand": "Unacademy", "tagline": "Crack It", "theme": "Exams, hard work, success", "language": "Hindi", "format": "TV Ad 30 sec"},
    {"brand": "Spotify India", "tagline": "There's a playlist for that", "theme": "Moods, travel, breakout hits", "language": "Punjabi", "format": "Social Reel"},
    {"brand": "Flipkart", "tagline": "India ka Fashion Capital", "theme": "Shopping, small town big dreams", "language": "Bengali", "format": "Social Reel"},
    {"brand": "Acko", "tagline": "Welcome to Change", "theme": "Insurance, no paperwork, fast", "language": "Hindi", "format": "OTT Pre-roll"},
    {"brand": "Mountain Dew", "tagline": "Darr ke Aage Jeet Hai", "theme": "Extreme sports, courage", "language": "English", "format": "TV Ad 30 sec"},
    {"brand": "Red Label", "tagline": "Swad Apnepan Ka", "theme": "Neighbors, breaking barriers, tea", "language": "Hindi", "format": "TV Ad 60 sec"},
    {"brand": "Bournvita", "tagline": "Tayyari Jeet Ki", "theme": "Sports, practice, parenting", "language": "Hindi", "format": "TV Ad 60 sec"},
    {"brand": "Center Fresh", "tagline": "Zuban pe lagaam", "theme": "Humor, awkward moments", "language": "Hindi", "format": "TV Ad 30 sec"},
    {"brand": "PolicyBazaar", "tagline": "Ullu Mat Bano", "theme": "Smart choices, comparison", "language": "Hindi", "format": "Radio Spot"},
    {"brand": "Jar", "tagline": "Save in Gold", "theme": "Micro-savings, daily habits", "language": "Hindi", "format": "Social Reel"},
    {"brand": "Lenskart", "tagline": "Specs for Everyone", "theme": "Style, reading, clarity", "language": "Hindi", "format": "OTT Pre-roll"},
    {"brand": "Boat", "tagline": "Plug into Nirvana", "theme": "Music, sweat, lifestyle", "language": "Hindi", "format": "Social Reel"},
    
    # --- Phase 2: Tech, Finance & Lifestyle ---
    {"brand": "Zerodha", "tagline": "The Variable", "theme": "Transparency, trading, wealth", "language": "Hindi", "format": "OTT Pre-roll"},
    {"brand": "BharatPe", "tagline": "Dhandhe ka Sahi Partner", "theme": "Small business, empowerment", "language": "Hindi", "format": "Radio Spot"},
    {"brand": "Paytm", "tagline": "Paytm Karo", "theme": "Everyday ease, scanner, soundbox", "language": "Hindi", "format": "TV Ad 30 sec"},
    {"brand": "Ola", "tagline": "Move to Future", "theme": "EV, green energy, city cab", "language": "Hindi", "format": "Social Reel"},
    {"brand": "Uber India", "tagline": "Bas Uber Karo", "theme": "Punctuality, office commute", "language": "Hindi", "format": "Social Reel"},
    {"brand": "Limca", "tagline": "Limca Freshness", "theme": "Extreme thirst, lemon, ice", "language": "Hindi", "format": "TV Ad 30 sec"},
    {"brand": "Frooti", "tagline": "Fresh and Juicy", "theme": "Mango, fun, kids", "language": "Hindi", "format": "OTT Pre-roll"},
    {"brand": "Maaza", "tagline": "Dildaar Mango", "theme": "Sharing, indulgence, pulp", "language": "Hindi", "format": "TV Ad 60 sec"},
    {"brand": "Bisleri", "tagline": "Understand the Difference", "theme": "Purity, camel humor, trust", "language": "Hindi", "format": "TV Ad 30 sec"},
    {"brand": "Nykaa Fashion", "tagline": "Stay Stylish", "theme": "Curation, labels, runway", "language": "Hindi", "format": "Social Reel"},
    {"brand": "Ajio", "tagline": "Doubt is Out", "theme": "Boldness, street style", "language": "Hindi", "format": "Social Reel"},
    {"brand": "Practo", "tagline": "Your Home for Health", "theme": "Doctor consult, safety", "language": "Hindi", "format": "OTT Pre-roll"},
    {"brand": "Pharmeasy", "tagline": "Take It Easy", "theme": "Medicine delivery, savings", "language": "Hindi", "format": "TV Ad 30 sec"},
    {"brand": "Vedantu", "tagline": "Understand Better", "theme": "Live learning, interactive", "language": "Hindi", "format": "TV Ad 60 sec"},
    {"brand": "Physics Wallah", "tagline": "Padhai Kahi se bhi", "theme": "Dedication, affordable, exams", "language": "Hindi", "format": "Social Reel"},
    {"brand": "Netflix India", "tagline": "Sabka Prime Time", "theme": "Binge watching, culture, popcorn", "language": "Hindi", "format": "Social Reel"},
    {"brand": "Amazon Prime Video", "tagline": "Entertainment is Here", "theme": "Originals, family drama", "language": "Hindi", "format": "OTT Pre-roll"},
    {"brand": "Hotstar", "tagline": "Home of Cricket", "theme": "T20, excitement, dugout", "language": "Hindi", "format": "TV Ad 30 sec"},
    {"brand": "UltraTech Cement", "tagline": "The Engineer's Choice", "theme": "Construction, strength, future", "language": "Hindi", "format": "TV Ad 60 sec"},
    {"brand": "Asian Paints (Regional)", "tagline": "Har Ghar Kuch Kehta Hai", "theme": "Home, pride", "language": "Odia", "format": "TV Ad 60 sec"},
    {"brand": "Gold Winner", "tagline": "Health and Happiness", "theme": "Cooking, family health", "language": "Tamil", "format": "TV Ad 30 sec"},
    {"brand": "Aachi Masala", "tagline": "Mother's Love", "theme": "Authentic taste, south indian", "language": "Tamil", "format": "Radio Spot"},
    {"brand": "GRT Jewellers", "tagline": "Shimmers of Gold", "theme": "Wedding, celebration", "language": "Tamil", "format": "TV Ad 60 sec"},
    {"brand": "Freedom Oil", "tagline": "Eat Healthy", "theme": "Fitness, cooking", "language": "Telugu", "format": "TV Ad 30 sec"},
    {"brand": "Heritage Milk", "tagline": "Trust the Freshness", "theme": "Dairy, morning habit", "language": "Telugu", "format": "Radio Spot"},
    {"brand": "Malabar Gold", "tagline": "Celebrate the Beauty", "theme": "Luxury, craftsmanship", "language": "Malayalam", "format": "TV Ad 60 sec"},
    {"brand": "Milma", "tagline": "The Taste of Kerala", "theme": "Purity, local pride", "language": "Malayalam", "format": "Radio Spot"},
    {"brand": "MTR", "tagline": "Authentic Indian Food", "theme": "Quick breakfast, tradition", "language": "Kannada", "format": "OTT Pre-roll"},
    {"brand": "Sunfeast Mom's Magic", "tagline": "Just like mom", "theme": "Cookies, emotional, warmth", "language": "Hindi", "format": "TV Ad 30 sec"},
    {"brand": "Bingo!", "tagline": "No confusion, great combination", "theme": "Snacking, humor, youth", "language": "Hindi", "format": "Social Reel"},
    {"brand": "Yippee Noodles", "tagline": "It's Better", "theme": "Kids, lunchbox, long noodles", "language": "Hindi", "format": "TV Ad 30 sec"},
    {"brand": "Kurkure", "tagline": "Tedha Hai Par Mera Hai", "theme": "Family madness, quirky, snack", "language": "Hindi", "format": "TV Ad 30 sec"},
    # --- Phase 3: Regional Powerhouse (Tamil, Malayalam, Hindi) ---
    {"brand": "Pothys", "tagline": "Collections for everyone", "theme": "Wedding, family, silk", "language": "Tamil", "format": "TV Ad 60 sec"},
    {"brand": "Saravana Stores", "tagline": "Low price, high quality", "theme": "Shopping, crowd, variety", "language": "Tamil", "format": "Radio Spot"},
    {"brand": "Aravind Eye Care", "tagline": "Vision for all", "theme": "Healthcare, compassion, service", "language": "Tamil", "format": "OTT Pre-roll"},
    {"brand": "Tamil Nadu Tourism", "tagline": "Enchanting Tamil Nadu", "theme": "Heritage, temples, culture", "language": "Tamil", "format": "TV Ad 60 sec"},
    {"brand": "Chennai Super Kings", "tagline": "Whistle Podu", "theme": "Sports, fans, yellow pride", "language": "Tamil", "format": "Social Reel"},
    {"brand": "Sakthi Masala", "tagline": "The taste of home", "theme": "Cooking, spices, mom's kitchen", "language": "Tamil", "format": "Radio Spot"},
    {"brand": "Butterfly Appliances", "tagline": "Good for home", "theme": "Kitchen, safety, efficiency", "language": "Tamil", "format": "TV Ad 30 sec"},
    {"brand": "Ramraj Cotton", "tagline": "Spirit of tradition", "theme": "Dhotis, men's pride, white", "language": "Tamil", "format": "Social Reel"},
    {"brand": "Jos Alukkas", "tagline": "Gold for generations", "theme": "Jewellery, trust, inheritance", "language": "Malayalam", "format": "TV Ad 60 sec"},
    {"brand": "Federal Bank", "tagline": "Your perfect banking partner", "theme": "Finance, trust, digital", "language": "Malayalam", "format": "TV Ad 30 sec"},
    {"brand": "Kerala Tourism", "tagline": "God's Own Country", "theme": "Nature, backwaters, peace", "language": "Malayalam", "format": "OTT Pre-roll"},
    {"brand": "Asianet", "tagline": "The heart of Kerala", "theme": "Media, news, entertainment", "language": "Malayalam", "format": "Radio Spot"},
    {"brand": "Kalyan Silks", "tagline": "Tradition in every thread", "theme": "Saree, wedding, festive", "language": "Malayalam", "format": "TV Ad 60 sec"},
    {"brand": "Nirapara", "tagline": "Purity in every grain", "theme": "Food, rice, spices", "language": "Malayalam", "format": "Social Reel"},
    {"brand": "Haldiram's", "tagline": "Always tasty", "theme": "Snacks, hospitality, guests", "language": "Hindi", "format": "TV Ad 30 sec"},
    {"brand": "Patanjali", "tagline": "Prakriti ka Aashirwad", "theme": "Health, ayurveda, swadeshi", "language": "Hindi", "format": "OTT Pre-roll"},
    {"brand": "Indigo Airlines", "tagline": "On-time performance", "theme": "Travel, professionalism, speed", "language": "Hindi", "format": "Social Reel"},
    {"brand": "WhatsApp India", "tagline": "Safety first", "theme": "Connectivity, private messaging", "language": "Hindi", "format": "Social Reel"},
    {"brand": "Tata Salt", "tagline": "Desh ka Namak", "theme": "Nation, trust, health", "language": "Hindi", "format": "TV Ad 30 sec"},
]


def generate_script(seed):
    ad_format = seed.get('format', 'TV Ad 30 sec')
    language = seed['language']
    brand = seed['brand']
    
    # Fetch curated few-shot examples for this language
    few_shot_block = ""
    try:
        from models.few_shot_examples import get_examples_for_language
        examples = get_examples_for_language(language, count=3)
        for ex in examples:
            few_shot_block += f"Input: {ex['input']}\nOutput:\n{ex['output']}\n\n"
    except Exception:
        few_shot_block = "No examples available. Use cinematic time-block format."

    prompt = f"""
You are a master Indian creative Copywriter specializing in {language} advertising.
Your task: Write a cinematically vivid script for {brand}.

--- REFERENCE STYLE ---
{few_shot_block}
--- END REFERENCE ---

Brand: {brand}
Format: {ad_format}
Tagline: {seed['tagline']}
Theme: {seed['theme']}
Language: {language}

STRICT REQUIREMENTS:
1. NATIVE SCRIPT: All dialogue MUST be in {language} script (No Romanized/English letters for dialogue).
2. BRAND LOCK: The script MUST be specifically about {brand}. Do NOT mention other brands.
3. FORMAT:
   [CONTEXT]: ...
   [VISUAL]: ...
   [AUDIO/DIALOGUE]: ...
   [TAGLINE]: {seed['tagline']}
4. MINIMUM 3 SCENES.
"""
    
    max_retries = 3
    for attempt in range(max_retries):
        data = json.dumps({
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7, "num_predict": 500}
        }).encode("utf-8")
        
        try:
            req = urllib.request.Request(OLLAMA_URL, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req) as f:
                response = json.loads(f.read().decode("utf-8"))
                script_text = response.get("response", "")
                
                # Validation: Check if the brand name is present and format is followed
                if brand.lower() in script_text.lower() and "[AUDIO/DIALOGUE]" in script_text:
                    return script_text
                else:
                    print(f"[Attempt {attempt+1}] Validation failed (Brand mismatch or bad format). Retrying...")
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2)
            
    return None

def main():
    print(f"Starting dataset generation using {MODEL} with Brand-Lock Validation...")
    output_path = os.path.join("data", "organic_ads_dataset.json")
    
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            dataset = json.load(f)
    else:
        dataset = []
    
    existing_keys = [f"{item['response']['Brand']}_{item['response']['Language']}" for item in dataset]
    
    for i, seed in enumerate(SEEDS):
        key = f"{seed['brand']}_{seed['language']}"
        if key in existing_keys:
            continue
            
        print(f"[{i+1}/{len(SEEDS)}] Generating: {seed['brand']} ({seed['language']})...")
        script_text = generate_script(seed)
        
        if script_text:
            entry = {
                "instruction": f"Write an organic advertisement for {seed['brand']} in {seed['language']} with theme {seed['theme']}.",
                "response": {
                    "Brand": seed['brand'],
                    "Language": seed['language'],
                    "Theme": seed['theme'],
                    "Content": script_text
                }
            }
            dataset.append(entry)
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(dataset, f, indent=2, ensure_ascii=False)
            
            print(f"Successfully saved {seed['brand']}")
            time.sleep(1)
        else:
            print(f"Failed to generate valid script for {seed['brand']} after retries.")
        
    print(f"Done! Dataset size: {len(dataset)}")

if __name__ == "__main__":
    main()
