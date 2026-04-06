import json
import os
import urllib.request
import subprocess
import re

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"
OUTPUT_FILE = "data/scraped_dataset.json"

# Verified IDs and Search Queries
SOURCES = [
    "yKxfJ-lBBEA", "UvGwIFVUK7M", "yni_ZJhxVSc", "bffSW7obMiY", "wHQcuVnmi58", 
    "3_GYnVrve0c", "vu2mOLbFn7c", "UPv5XPTL0uU", "npZIAKoDtTA", "W4n3A0OLBtU",
    "ytsearch:Zomato Diwali ad 2024 official", "ytsearch:Zepto Soan Papdi ad 2024",
    "ytsearch:Swiggy Juhi Chawla ad 2024", "ytsearch:Cadbury 5Star MAMA ad",
    "ytsearch:CRED Rahul Dravid Indiranagar ad", "ytsearch:Google India Diwali ad 2024",
    "ytsearch:Apple India ad 2024", "ytsearch:Nike India ad da da ding",
    "ytsearch:Fevikwik fish ad", "ytsearch:Amul classic ad",
    "ytsearch:Surf Excel Lalitaji ad", "ytsearch:Tanishq wedding ad 2024",
    "ytsearch:Vim black bar ad", "ytsearch:Zomato world cup ad",
    "ytsearch:Blinkit Valentine ad", "ytsearch:Lifebuoy Bund se Bund ad",
    "ytsearch:Nirma washing powder ad classic", "ytsearch:Bajaj Hamara Bajaj ad classic",
    "ytsearch:Cadbury cricket ad 2021", "ytsearch:Happydent light ad",
    "ytsearch:Mentos dimag ki batti ad", "ytsearch:Coca Cola India ad Aamir Khan",
    "ytsearch:Pepsi India ad Dhoni", "ytsearch:Bournvita Tayyari Jeet Ki ad",
    "ytsearch:Horlicks commercial India", "ytsearch:Maggi commercial India",
    "ytsearch:Dairymilk Silk ad", "ytsearch:Oreo India ad Dhoni", "ytsearch:Ariel Share The Load ad",
    "ytsearch:Vim black bar ad official", "ytsearch:Lux soap India ad", "ytsearch:Ponds face wash ad India",
    "ytsearch:Colgate Vedshakti ad", "ytsearch:Pepsodent Golu ad", "ytsearch:Dettol soap ad India",
    "ytsearch:Savlon handwash ad 2024", "ytsearch:Lizol cleaner ad", "ytsearch:Harpic bathroom cleaner ad",
    "ytsearch:Good Knight coil ad", "ytsearch:All Out mosquito ad", "ytsearch:Mortein spray ad",
    "ytsearch:Hit spray ad", "ytsearch:Godrej aer spray ad", "ytsearch:Comfort fabric conditioner ad",
    "ytsearch:Tide Plus chauk gaye ad", "ytsearch:Wheel washing powder ad", "ytsearch:Rin bar chamak ad",
    "ytsearch:Mountain Dew Darr Ke Aage Jeet Hai ad", "ytsearch:Thums Up Aaj Kuch Toofani Karte Hain ad",
    "ytsearch:Maaza mango ad", "ytsearch:Frooti ad", "ytsearch:7Up Fido Dido ad",
    "ytsearch:Mirinda ad", "ytsearch:Kurkure ad Juhi Chawla", "ytsearch:Lays ad Ranbir Kapoor",
    "ytsearch:Bikaji Amitabh Bachchan ad", "ytsearch:Haldiram ad"
]

def clean_vtt(vtt_text):
    if not vtt_text: return ""
    # Remove XML-style tags like <00:00:02.639> or <c>
    vtt_text = re.sub(r'<[^>]+>', '', vtt_text)
    lines = vtt_text.split('\n')
    cleaned = []
    for line in lines:
        if '-->' in line or line.strip().isdigit() or not line.strip() or 'WEBVTT' in line or 'Kind:' in line or 'Language:' in line:
            continue
        cleaned.append(line.strip())
    text = " ".join(cleaned)
    text = re.sub(r'\[.*?\]', '', text) 
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_yt_data(source):
    url = f"https://www.youtube.com/watch?v={source}" if not source.startswith("ytsearch:") else source
    try:
        cmd_meta = ["python", "-m", "yt_dlp", "--dump-json", "--skip-download", "--flat-playlist", url]
        result = subprocess.run(cmd_meta, capture_output=True, text=True, encoding='utf-8')
        if result.returncode != 0: return None
        
        meta_lines = result.stdout.strip().split('\n')
        meta = json.loads(meta_lines[0])
        
        video_id = meta.get("id")
        brand = meta.get("uploader", "Unknown Brand").replace("- Topic", "").strip()
        title = meta.get("title", "Unknown Ad")
        actual_url = f"https://www.youtube.com/watch?v={video_id}"

        cmd_subs = ["python", "-m", "yt_dlp", "--write-auto-subs", "--write-subs", "--sub-lang", "hi,en,ta,te", "--skip-download", "--output", f"tmp_{video_id}", actual_url]
        subprocess.run(cmd_subs, capture_output=True)
        
        transcript_text = ""
        lang_found = "English"
        for lang in ['hi', 'ta', 'te', 'en']:
            vtt_file = f"tmp_{video_id}.{lang}.vtt"
            if os.path.exists(vtt_file):
                with open(vtt_file, "r", encoding="utf-8") as f:
                    transcript_text = clean_vtt(f.read())[:2500] 
                lang_found = lang
                os.remove(vtt_file)
                break
        return {"brand": brand, "title": title, "transcript": transcript_text, "language": lang_found, "video_id": video_id}
    except Exception as e:
        print(f"Error fetching {source}: {e}")
        return None

def process_with_llm(data_pkg):
    lang_map = {"hi": "Hindi", "ta": "Tamil", "te": "Telugu", "en": "Hindi"}
    language = lang_map.get(data_pkg['language'], "Hindi")
    
    prompt = f"""
Act as a professional Indian creative copywriter.
Take this YouTube metadata and WRITE A COMPLETE HIGH-QUALITY ADVERTISEMENT SCRIPT.

Brand: {data_pkg['brand']}
Title: {data_pkg['title']}
Transcript: {data_pkg['transcript'] if data_pkg['transcript'] else data_pkg['title']}

STRICT RULES:
1. NO PLACEHOLDERS like "...", "Production cues", "Detail setting", or "Scene description".
2. ACTUALLY WRITE the creative context and visual actions.
3. WRITE THE REAL DIALOGUE in ONLY the NATIVE SCRIPT of {language} (e.g. Devanagari for Hindi).
4. If you output "...", you have failed.
5. Provide a REAL tagline in {language} and English.

OUTPUT ONLY THIS JSON:
{{
  "Brand": "{data_pkg['brand']}",
  "Language": "{language}",
  "Theme": "Storytelling",
  "Content": "[CONTEXT]: (Detailed scene setting)\\n[VISUAL]: (Detailed visual actions)\\n[AUDIO/DIALOGUE]: (Actual {language} words in native script)\\n[MUSIC]: (Music mood/style)\\n[TAGLINE]: (Slogan in {language} + English translation)"
}}
"""
    payload = json.dumps({"model": MODEL, "prompt": prompt, "stream": False, "format": "json"}).encode("utf-8")
    try:
        req = urllib.request.Request(OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as f:
            res = json.loads(f.read().decode("utf-8"))
            out = json.loads(res.get("response", "{}"))
            # Final validation
            if "..." in str(out): return None
            return out
    except: return None

def main():
    if not os.path.exists("data"): os.makedirs("data")
    
    # Load existing to resume
    dataset = []
    processed_ids = set()
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                dataset = json.load(f)
                for entry in dataset:
                    # Extract ID from source_url
                    vid_id = entry.get("source_url", "").split("v=")[-1]
                    if vid_id: processed_ids.add(vid_id)
            print(f"Resuming with {len(dataset)} existing entries.")
        except:
            print("Could not load existing dataset, starting fresh.")
            dataset = []

    print(f"Starting/Resuming FINAL master scrape for {len(SOURCES)} sources...")
    
    for src in SOURCES:
        try:
            # Skip if already processed (only for direct IDs)
            if not src.startswith("ytsearch:") and src in processed_ids:
                print(f"Skipping already processed ID: {src}")
                continue
                
            print(f"Processing {src}...")
            data_pkg = get_yt_data(src)
            
            if not data_pkg:
                print(f"Failed to fetch metadata/subs for {src}")
                continue
                
            # Skip search results if we already have this ID
            if data_pkg.get("video_id") in processed_ids:
                print(f"Skipping duplicate video ID from search: {data_pkg['video_id']}")
                continue

            structured_data = process_with_llm(data_pkg)
            
            if structured_data:
                entry = {
                    "instruction": f"Write an advertisement for {structured_data.get('Brand')} in {structured_data.get('Language')} with theme {structured_data.get('Theme')}.",
                    "response": structured_data,
                    "source_url": f"https://youtube.com/watch?v={data_pkg.get('video_id')}",
                    "is_organic": True
                }
                dataset.append(entry)
                processed_ids.add(data_pkg.get("video_id"))
                
                print(f"Success: {structured_data.get('Brand')} ({data_pkg['video_id']})")
                
                # Immediate save after each success
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    json.dump(dataset, f, ensure_ascii=False, indent=2)
            else: 
                print(f"Failed LLM quality check or generation for {src}")
                
        except Exception as e:
            print(f"CRITICAL ERROR processing {src}: {e}")
            import traceback
            traceback.print_exc()

    print(f"DONE. Total entries in {OUTPUT_FILE}: {len(dataset)}")

if __name__ == "__main__":
    main()
