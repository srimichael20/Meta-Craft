import json
import urllib.request
import re

URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:1b"

def generate_minimal():
    prompt = """Generate 20 short ad scripts for top Indian brands.
Format for each:
[BRAND]: Name
[LANG]: Language
[CONTENT]: [CONTEXT]: ... [VISUAL]: ... [AUDIO/DIALOGUE]: (Native script) [TAGLINE]: ...
---
(Repeat for 20)"""

    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.9, "num_predict": 1500}
    }
    
    print("Requesting 20 samples...")
    req = urllib.request.Request(URL, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=600) as response:
            res = json.loads(response.read().decode('utf-8'))
            text = res.get('response', '')
            print("Received response.")
            
            blocks = text.split("---")
            dataset = []
            for b in blocks:
                if "[BRAND]" in b and "[AUDIO/DIALOGUE]" in b:
                    brand_match = re.search(r'\[BRAND\]:\s*(.*)', b)
                    lang_match = re.search(r'\[LANG\]:\s*(.*)', b)
                    
                    if brand_match and lang_match:
                        dataset.append({
                            "instruction": f"Write an ad for {brand_match.group(1).strip()} in {lang_match.group(1).strip()}.",
                            "response": {
                                "Brand": brand_match.group(1).strip(),
                                "Language": lang_match.group(1).strip(),
                                "Content": b.strip()
                            }
                        })
            
            # Append to existing
            if os.path.exists("data/bulk_synthetic.json"):
                with open("data/bulk_synthetic.json", "r", encoding="utf-8") as f:
                    existing = json.load(f)
                existing.extend(dataset)
            else:
                existing = dataset

            with open("data/bulk_synthetic.json", "w", encoding="utf-8") as f:
                json.dump(existing, f, indent=2, ensure_ascii=False)
            print(f"Total bulk samples: {len(existing)}")

    except Exception as e:
        print(f"Error: {e}")

import os
if __name__ == "__main__":
    generate_minimal()
