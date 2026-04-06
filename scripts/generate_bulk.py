import json
import urllib.request
import re

URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:1b"

def generate_bulk():
    prompt = """Write 10 short ad scripts for different Indian brands (Amul, Maggi, Zomato, etc.) in a mix of Hindi and Tamil.
Each ad must follow this format EXACTLY:
---
[BRAND]: Name
[LANG]: Language
[CONTENT]: 
[CONTEXT]: ...
[VISUAL]: ...
[AUDIO/DIALOGUE]: ... (Strictly in the language script)
[TAGLINE]: ...
---

Write 10 now."""

    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.8, "num_predict": 1000}
    }
    
    print("Calling Ollama for 10 samples...")
    req = urllib.request.Request(URL, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            res = json.loads(response.read().decode('utf-8'))
            text = res.get('response', '')
            print("Received response.")
            
            # Simple parsing
            blocks = text.split("---")
            dataset = []
            for b in blocks:
                if "[BRAND]" in b and "[AUDIO/DIALOGUE]" in b:
                    brand = re.search(r'\[BRAND\]:\s*(.*)', b)
                    lang = re.search(r'\[LANG\]:\s*(.*)', b)
                    
                    if brand and lang:
                        dataset.append({
                            "instruction": f"Write an ad for {brand.group(1).strip()} in {lang.group(1).strip()}.",
                            "response": {
                                "Brand": brand.group(1).strip(),
                                "Language": lang.group(1).strip(),
                                "Content": b.strip()
                            }
                        })
            
            with open("data/bulk_synthetic.json", "w", encoding="utf-8") as f:
                json.dump(dataset, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(dataset)} samples to data/bulk_synthetic.json")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_bulk()
