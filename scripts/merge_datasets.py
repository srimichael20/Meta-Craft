import json
import os

ORGANIC_FILE = "data/organic_ads_dataset.json"
SCRAPED_FILE = "data/scraped_dataset.json"
FINAL_FILE = "data/final_ads_dataset_50.json"

def merge():
    final_data = []
    seen_urls = set()

    # 1. Load Organic Data (always high quality)
    if os.path.exists(ORGANIC_FILE):
        with open(ORGANIC_FILE, "r", encoding="utf-8") as f:
            organic = json.load(f)
            final_data.extend(organic)
            print(f"Loaded {len(organic)} organic entries.")

    # 2. Load Scraped Data
    if os.path.exists(SCRAPED_FILE):
        with open(SCRAPED_FILE, "r", encoding="utf-8") as f:
            scraped = json.load(f)
            count = 0
            for entry in scraped:
                # Basic quality filter
                content = entry.get("response", {}).get("Content", "")
                if "..." in content or not content:
                    continue
                
                url = entry.get("source_url")
                if url and url in seen_urls:
                    continue
                
                final_data.append(entry)
                if url: seen_urls.add(url)
                count += 1
            print(f"Merged {count} unique, high-quality scraped entries.")

    # 3. Save Final
    with open(FINAL_FILE, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    
    print(f"DONE. Final dataset size: {len(final_data)}")
    print(f"Path: {FINAL_FILE}")

if __name__ == "__main__":
    merge()
