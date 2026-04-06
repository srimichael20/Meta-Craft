import json
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"

def test_prompt():
    brand = "Clinic Plus"
    title = "Beti Bann ke Aana - Inspiring Indian Ad"
    transcript = "A mother talking to her daughter about strength and hair. The daughter says I will be strong like you. The mother smiles."
    language = "Hindi"

    prompt = f"""
Act as a professional Indian creative copywriter.
Take this metadata and WRITE A FULL SCRIPT.

Brand: {brand}
Title: {title}
Transcript: {transcript}

RULES:
1. DO NOT use the words 'Strictly in', 'native script', '...' or 'placeholder'.
2. WRITE THE REAL DIALOGUE in Devanagari (Hindi script).
3. WRITE REAL PRODUCTION CUES for context and visuals.
4. If you fail to write real dialogue, you have failed the task.

OUTPUT FORMAT:
{{
  "Brand": "{brand}",
  "Language": "{language}",
  "Theme": "Emotion",
  "Content": "[CONTEXT]: (Write real scene setting here)\\n[VISUAL]: (Write real visual actions here)\\n[AUDIO/DIALOGUE]: (Write the ACTUAL dialogue in Hindi here)\\n[MUSIC]: (Describe the music)\\n[TAGLINE]: (Write the slogan in Hindi then English)"
}}
"""
    
    payload = json.dumps({"model": MODEL, "prompt": prompt, "stream": False, "format": "json"}).encode("utf-8")
    
    try:
        req = urllib.request.Request(OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as f:
            res = json.loads(f.read().decode("utf-8"))
            print(res.get("response", ""))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_prompt()
