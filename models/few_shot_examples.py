"""
Few-Shot Examples for Indian Language Script Generation.
Strictly follows the [CONTEXT], [VISUAL], [AUDIO/DIALOGUE], [TAGLINE] format.
"""

FEW_SHOT_EXAMPLES = {
    "hindi": [
        {
            "input": "Brand: Amul | Format: TV Ad 30 sec | Theme: Mother's Love",
            "output": """[CONTEXT]: 
एक मध्यमवर्गीय भारतीय रसोई। सुबह का समय है।

[VISUAL]: 
माँ ताज़ा पराठा बना रही है। उस पर अमूल बटर का एक टुकड़ा पिघल रहा है। बच्चा बड़ी बेसब्री से इंतज़ार कर रहा है।

[AUDIO/DIALOGUE]: 
माँ (मुस्कुराते हुए): "बिना मक्खन के पराठा? नामुमकिन!"
बच्चा: "माँ, थोड़ा और अमूल!"
VO: "पीढ़ियों का स्वाद, भारत का अपना अमूल।"

[TAGLINE]: 
Amul - The Taste of India."""
        }
    ],
    "tamil": [
        {
            "input": "Brand: Pothys | Format: TV Ad 60 sec | Theme: Wedding Silk",
            "output": """[CONTEXT]: 
ஜொலிக்கும் பட்டுச் சேலைகள் நிறைந்த ஒரு பிரம்மாண்டமான ஷோரூம்.

[VISUAL]: 
மணப்பெண் ஒரு அழகான காஞ்சிபுரம் பட்டுச் சேலையை அணிந்து கண்ணாடியில் பார்க்கிறாள். அவளது கண்கள் மகிழ்ச்சியில் பிரகாசிக்கின்றன.

[AUDIO/DIALOGUE]: 
பெண்: "இந்த கல்யாணத்துக்கு ஏத்த பட்டு, போத்தீஸ்-ல மட்டும் தான் கிடைக்கும்!"
தாய்: "பாரம்பரியமும் அழகும் இணைந்த இடம் இது."

[TAGLINE]: 
Pothys - Aalayam of Silks."""
        }
    ],
    "malayalam": [
        {
            "input": "Brand: Kalyan Jewellers | Format: TV Ad 30 sec | Theme: Wedding Trust",
            "output": """[CONTEXT]: 
കേരളത്തിലെ ഒരു പരമ്പരാഗത വിവാഹ മണ്ഡപം.

[VISUAL]: 
അച്ഛൻ മകൾക്ക് സ്വർണ്ണാഭരണങ്ങൾ അണിയിക്കുന്നു. ആഭരണങ്ങളുടെ തിളക്കം മകളുടെ മുഖത്ത് പ്രതിഫലിക്കുന്നു.

[AUDIO/DIALOGUE]: 
അച്ഛൻ: "മോളെ, ഈ സ്വർണ്ണം നിന്റെ ഐശ്വര്യമാണ്. കല്യാണ് നൽകുന്ന ഈ വിശ്വാസം നമ്മുടെ കരുത്താണ്."

[TAGLINE]: 
Kalyan Jewellers — Trust is Everything."""
        }
    ]
}

def get_examples_for_language(language: str, count: int = 1) -> list:
    return FEW_SHOT_EXAMPLES.get(language.lower(), FEW_SHOT_EXAMPLES["hindi"])[:count]


def format_few_shot_block(examples):
    formatted = ""
    for ex in examples:
        formatted += f"Input: {ex['input']}\nOutput: {ex['output']}\n\n"
    return formatted