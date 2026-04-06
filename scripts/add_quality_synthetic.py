import json
import os

NEW_ADS = [
    {
        "instruction": "Write an organic advertisement for Maggi in Marathi with theme Quick Snack, Childhood, Rain.",
        "response": {
            "Brand": "Maggi",
            "Language": "Marathi",
            "Theme": "Quick Snack, Childhood, Rain",
            "Content": "[CONTEXT]: पावसाळी संध्याकाळ. खिडकीबाहेर पाऊस पडत आहे.\n\n[VISUAL]: एक मुलगा खिडकीपाशी बसून पाऊस बघतोय. आई किचनमधून गरम मॅगीची वाडगी घेऊन येते. मॅगीमधून वाफा निघत आहेत.\n\n[AUDIO/DIALOGUE]: \nमुलगा: \"आई, मॅगी? येस!\"\nआई: \"दोन मिनिटात तयार, तुझ्या आवडीची.\"\nVO: \"प्रत्येक पावसाळी आठवणीत, मॅगीची चव. मॅगी - खुशाल जगा!\"\n\n[TAGLINE]: Maggi - 2-Minute Noodles"
        }
    },
    {
        "instruction": "Write an organic advertisement for Amazon India in Telugu with theme Fast Delivery, E-commerce.",
        "response": {
            "Brand": "Amazon India",
            "Language": "Telugu",
            "Theme": "Fast Delivery, E-commerce",
            "Content": "[CONTEXT]: ఒక మధ్యతరగతి ఇల్లు. పండగ తాలూకు సందడి.\n\n[VISUAL]: ఒక తండ్రి తన కూతురికి సర్ప్రైజ్ గిఫ్ట్ ఇవ్వాలని అనుకుంటాడు. వెంటనే అమెజాన్ యాప్ లో బుక్ చేస్తాడు. మరుసటి రోజు ఉదయమే ప్యాకేజీ వస్తుంది.\n\n[AUDIO/DIALOGUE]: \nకూతురు: \"నా గిఫ్ట్ వచ్చేసిందా? థాంక్యూ నాన్న!\"\nతండ్రి: \"అమెజాన్ ఉంటే మన పండగలు ఇంకా స్పెషల్!\"\nVO: \"వేగవంతమైన డెలివరీ, మీ ఇంటి వరకు. అమెజాన్!\"\n\n[TAGLINE]: Amazon - Aapki Apni Dukaan"
        }
    },
    {
        "instruction": "Write an organic advertisement for Wagh Bakri in Gujarati with theme Family Bonding, Tea.",
        "response": {
            "Brand": "Wagh Bakri",
            "Language": "Gujarati",
            "Theme": "Family Bonding, Tea",
            "Content": "[CONTEXT]: રવિવારની સવાર. આખું કુટુંબ ગાર્ડનમાં બેઠું છે.\n\n[VISUAL]: દાદાજી અને દાદી ચાની ચૂસકી લેતા જૂની વાતો કરે છે. વહુ ગરમાગરમ વાઘ બકરી ચા પીરસે છે.\n\n[AUDIO/DIALOGUE]: \nદાદા: \"આ ચામાં તો સબંધોની મીઠાશ છે.\"\nVO: \"વાઘ બકરી ચા - હમેશા રિશ્તો કી ગરમાહટ.\"\n\n[TAGLINE]: Wagh Bakri - Hamesha Rishto Ki Garmahat"
        }
    },
    {
        "instruction": "Write an organic advertisement for Nandini in Kannada with theme Purity, Freshness, Farm.",
        "response": {
            "Brand": "Nandini",
            "Language": "Kannada",
            "Theme": "Purity, Freshness, Farm",
            "Content": "[CONTEXT]: ಹಸಿರು ಗದ್ದೆಗಳು, ಮುಂಜಾನೆಯ ಸಮಯ.\n\n[VISUAL]: ಹಸುಗಳು ಕಾಡಿನಲ್ಲಿ ಮೇಯುತ್ತಿವೆ. ರೈತರು ತಾಜಾ ಹಾಲನ್ನು ಸಂಗ್ರಹಿಸುತ್ತಿದ್ದಾರೆ. ಮನೆಯಲ್ಲಿ ಅಜ್ಜಿ ಮೊಮ್ಮಗನಿಗೆ ಒಂದು ಲೋಟ ನಂದಿನಿ ಹಾಲು ಕೊಡುತ್ತಿದ್ದಾರೆ.\n\n[AUDIO/DIALOGUE]: \nಮೊಮ್ಮಗ: \"ಅಜ್ಜಿ, ಈ ಹಾಲು ತುಂಬಾ ರುಚಿಯಾಗಿದೆ!\"\nVO: \"ಶುದ್ಧತೆ ಮತ್ತು ನಂಬಿಕೆಯ ಸಂಕೇತ. ನಂದಿನಿ ಹಾಲು - ಕರ್ನಾಟಕದ ಹೆಮ್ಮೆ.\"\n\n[TAGLINE]: Nandini - Purity in every drop"
        }
    },
    {
        "instruction": "Write an organic advertisement for Senco Gold in Bengali with theme Artistry, Wedding, Tradition.",
        "response": {
            "Brand": "Senco Gold",
            "Language": "Bengali",
            "Theme": "Artistry, Wedding, Tradition",
            "Content": "[CONTEXT]: একটি রাজকীয় বিয়ের মণ্ডপ। প্রদীপের আলোয় চারপাশ উজ্জ্বল।\n\n[VISUAL]: কনে আয়নার সামনে দাঁড়িয়ে নিজেকে দেখছেন। তিনি সেনকো গোল্ডের একটি ভারী নেকলেস পরে আছেন। অলঙ্কারের সূক্ষ্ম কাজ ফুটে উঠছে।\n\n[AUDIO/DIALOGUE]: \nমা: \"তুই যেন আমার লক্ষ্মী মা। সেনকোর এই গয়না তোকে পূর্ণতা দিল।\"\nVO: \"শিল্পকলা আর আভিজাত্যের মিলন। সেনকো গোল্ড - ঐতিহ্যের ছোঁয়ায়।\"\n\n[TAGLINE]: Senco Gold - Artistry of Bengal"
        }
    },
    {
        "instruction": "Write an organic advertisement for Thums Up in Hindi with theme Summer, Toofani, Bravery.",
        "response": {
            "Brand": "Thums Up",
            "Language": "Hindi",
            "Theme": "Summer, Toofani, Bravery",
            "Content": "[CONTEXT]: तपती धूप, एक रेगिस्तान का दृश्य।\n\n[VISUAL]: एक साहसी नायक (Hero) अपनी जीप से रेत के टीलों को पार कर रहा है। वह थम्स अप की बोतल खोलता है, फिज़ की आवाज़ गूँजती है।\n\n[AUDIO/DIALOGUE]: \nVO: \"डर के आगे जीत है? नहीं, डर के ऊपर तूफ़ान है!\"\nनायक: \"आज कुछ तूफ़ानी करते हैं!\"\nVO: \"थम्स अप - स्वाद तूफ़ान का।\"\n\n[TAGLINE]: Thums Up - Taste the Thunder"
        }
    }
]

def add_synthetic():
    path = "data/organic_ads_dataset.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            dataset = json.load(f)
    else:
        dataset = []

    # Filter out duplicates
    existing_instructions = {item['instruction'] for item in dataset}
    added = 0
    for ad in NEW_ADS:
        if ad['instruction'] not in existing_instructions:
            dataset.append(ad)
            added += 1
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    print(f"Added {added} high-quality synthetic samples to {path}.")

if __name__ == "__main__":
    add_synthetic()
