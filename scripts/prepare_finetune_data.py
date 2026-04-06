import json
import re
import os

def clean_response(text):
    # Remove conversational filler
    # Remove "Okay, here's..." or similar intros
    text = re.sub(r'^(Okay|Sure|Here is|Here’s|Certainly|This is)[^:\n]*:\n*', '', text, flags=re.IGNORECASE)
    
    # Remove final "Let me know if..." or similar outros
    text = re.sub(r'(\n+)?(Let me know|Hope this|I hope|This script|This ad|Feel free)[^\n]*$', '', text, flags=re.IGNORECASE | re.MULTILINE)
    
    # Remove markdown code blocks if any
    text = re.sub(r'```[a-z]*\n?', '', text)
    text = re.sub(r'```', '', text)
    
    return text.strip()

def prepare():
    files = ["data/organic_ads_dataset.json", "data/scraped_dataset.json", "data/final_ads_dataset_50.json", "data/synthetic_ads_dataset.json"]
    train_data = []
    
    seen_content = set() # Avoid duplicates across files
    
    for filename in files:
        if not os.path.exists(filename):
            continue
            
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                instruction = item.get("instruction", "")
                response_obj = item.get("response", {})
                content = response_obj.get("Content", "")
                
                if not content: continue
                
                cleaned_content = clean_response(content)
                
                # Deduplication logic
                content_hash = cleaned_content[:100] # Use first 100 chars as a proxy
                if content_hash in seen_content:
                    continue
                seen_content.add(content_hash)
                
                # Alpaca format is standard for many tuning repos
                train_data.append({
                    "instruction": instruction,
                    "input": "",
                    "output": cleaned_content
                })
                
    # Save as JSONL for training
    with open("data/train_alpaca.jsonl", "w", encoding="utf-8") as f:
        for entry in train_data:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            
    # Also save as JSON for easy viewing
    with open("data/train_alpaca.json", "w", encoding="utf-8") as f:
        json.dump(train_data, f, indent=2, ensure_ascii=False)
        
    print(f"Prepared {len(train_data)} samples for fine-tuning.")
    print("Files created: data/train_alpaca.jsonl and data/train_alpaca.json")

if __name__ == "__main__":
    prepare()
