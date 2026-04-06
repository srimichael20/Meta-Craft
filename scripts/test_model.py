import subprocess
import json

TEST_CASES = [
    {
        "brand": "Tata Salt",
        "language": "Hindi",
        "theme": "Honesty, purity, nation",
        "instruction": "Write a 60-second TV ad script for Tata Salt in Hindi with the theme 'Desh Ka Namak' (Honesty and Purity)."
    },
    {
        "brand": "Sabyasachi",
        "language": "Bengali",
        "theme": "Heritage, luxury, bridal",
        "instruction": "Write a cinematic social reel script for Sabyasachi in Bengali focusing on heritage and the artistry of a bridal lehenga."
    },
    {
        "brand": "Spotify India",
        "language": "Tamil",
        "theme": "Music, travel, mood",
        "instruction": "Write an OTT pre-roll ad for Spotify India in Tamil with the theme 'Mood and Music for long drives'."
    }
]

def run_test(case):
    print(f"\n{'='*50}")
    print(f"Testing for Brand: {case['brand']} ({case['language']})")
    print(f"{'='*50}")
    
    prompt = case['instruction']
    
    try:
        # Running the command through subprocess to call the local ollama model
        result = subprocess.run(
            ["ollama", "run", "metacraft-ads", prompt],
            capture_output=True,
            text=True,
            encoding='utf-8',
            check=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running model for {case['brand']}: {e.stderr}")
    except FileNotFoundError:
        print("Error: 'ollama' command not found. Please ensure Ollama is installed and running.")

if __name__ == "__main__":
    print("MetaCraft AI: Model Evaluation Script")
    print("Note: This script requires 'metacraft-ads' to be created in Ollama first.")
    
    # Prompt user for confirmation if they've setup the model
    # (Since this is a local script, we'll just run it)
    for case in TEST_CASES:
        run_test(case)
