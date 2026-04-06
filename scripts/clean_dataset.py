import json
import os

def clean_dataset(filename):
    if not os.path.exists(filename):
        return
        
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    cleaned_data = []
    removed_count = 0
    
    for item in data:
        brand = item['response']['Brand'].lower()
        content = item['response']['Content'].lower()
        
        # Heuristic: If content mentions other major brands but it shouldn't
        other_brands = ["amul", "blinkit", "zomato", "swiggy"]
        if brand not in other_brands:
            hallucinated = False
            for b in other_brands:
                if b in content:
                    hallucinated = True
                    break
            if hallucinated:
                removed_count += 1
                continue
        
        # Check if native script is missing for Hindi/Tamil/Malayalam
        lang = item['response']['Language']
        if lang == "Hindi" and not any('\u0900' <= c <= '\u097f' for c in item['response']['Content']):
            removed_count += 1
            continue
        if lang == "Tamil" and not any('\u0b80' <= c <= '\u0bff' for c in item['response']['Content']):
            removed_count += 1
            continue
        if lang == "Malayalam" and not any('\u0d00' <= c <= '\u0d7f' for c in item['response']['Content']):
            removed_count += 1
            continue

        cleaned_data.append(item)
        
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
        
    print(f"Cleaned {filename}: Removed {removed_count} hallucinated/bad samples. Remaining: {len(cleaned_data)}")

if __name__ == "__main__":
    clean_dataset("data/organic_ads_dataset.json")
