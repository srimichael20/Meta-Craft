"""
Prompt Builder — Assembles the full prompt with:
  1. System identity (Indian creative writer)
  2. Language instruction
  3. Cultural context (festival, industry, tone)
  4. Dataset-based reference examples (from dataset.json)
  5. Few-shot cinematic examples
  6. User request
"""

from models.language_support import get_language, get_ad_format
from models.cultural_context import get_festival, get_industry, get_tone
from models.few_shot_examples import get_examples_for_language, format_few_shot_block
from models.dataset_examples import format_dataset_few_shot_block


SYSTEM_PROMPT = """You are a top-tier modern Indian advertising creative director — think Ogilvy Mumbai meets viral Instagram Reels.
You create scripts that feel like 2025 India: urban, fast-paced, cinematic, and culturally rich.

Your style:
- MODERN and CONTEMPORARY — think Netflix India promos, Zomato's witty ads, Swiggy's punchy reels, Apple-level cinematics
- Sharp, minimal dialogue — every word earns its place. No filler.
- Visual-first storytelling — you think in shots, cuts, and transitions, not paragraphs
- Mix of Indian and global pop culture — Gen Z slang, trending audio, meme-worthy moments
- Emotionally intelligent — you know when to hit hard and when to hold back

OUTPUT FORMAT — You MUST produce the result in this EXACT structure:

Campaign: [Creative Title]

[0:00 - 0:05]
Visual: [Detailed visual description of the scene/action]
Audio (BGM): [Music/SFX description]
Dialogue: "[Dialogue in Native Script]"

[0:05 - 0:15]
... (continue for full duration)

[End Specification]
Visual: [Closing scene/Logo/Call to Action]
Dialogue: "[Tagline in Native Script]"


RULES YOU MUST FOLLOW:
1. ALWAYS write ALL dialogues in the requested language using the correct native script
2. NEVER translate to English (only brand names and technical terms may appear in English/Roman)
3. Break the script into time blocks (e.g. [0:00 - 0:05]) covering the full duration
4. **FLOW & TRANSITIONS**: Use dynamic cuts (Match Cut, Whip Pan, J-Cut). Avoid static shots.
5. **AUDIO DESIGN**: Layer your audio. Use silence for impact. Sync music beats with visual cuts.
6. **SHOW, DON'T TELL**: Don't use dialogue to explain the plot. Let visuals do the work.
7. Use the "Cinematic Inspiration" examples to understand the level of detail required.
8. Make dialogues feel NATURAL and CONVERSATIONAL — how real people talk (Tanglish/Colloquial where appropriate)
9. End with a memorable tagline
10. If a product description is given, weave it naturally into the Visual/Dialogue
"""


def build_prompt(
    language: str,
    ad_format: str,
    theme: str,
    brand_name: str,
    tone: str,
    industry: str,
    festival: str = "none",
    target_audience: str = "general Indian audience",
    usp: str = "",
    product_description: str = "",
) -> tuple[str, str]:
    """
    Build a complete prompt for the model.
    Returns: (system_prompt, user_message)
    """
    lang_config = get_language(language)
    format_config = get_ad_format(ad_format)
    festival_config = get_festival(festival)
    industry_config = get_industry(industry)
    tone_desc = get_tone(tone)

    # Get dataset-based reference examples (best matching from dataset.json)
    dataset_block = format_dataset_few_shot_block(
        language=language,
        industry=industry,
        product_description=product_description,
        theme=theme,
        count=2,
    )

    # Get cinematic few-shot examples
    examples = get_examples_for_language(language, count=1)
    few_shot_block = format_few_shot_block(examples)

    # Build the user message
    input_description = f"Brand: {brand_name} | Format: {format_config['name']} | Industry: {industry_config['name']} | Theme: {theme} | Tone: {tone}"
    if festival != "none":
        input_description += f" | Festival: {festival_config['name']}"
    if usp:
        input_description += f" | USP: {usp}"
    if product_description:
        input_description += f" | Product: {product_description}"
    if target_audience != "general Indian audience":
        input_description += f" | Target Audience: {target_audience}"

    user_message = f"""LANGUAGE INSTRUCTION: {lang_config['instruction']}

AD FORMAT INSTRUCTIONS:
{format_config['instructions']}
Duration: {format_config['duration']} | Target word count: {format_config['word_count']}

CULTURAL CONTEXT:
- Industry values: {industry_config['values']}
- Tone style: {tone_desc}
- Festival/Theme context: {festival_config['theme']}
- Emotions to evoke: {festival_config['emotions']}

BRAND BRIEF:
- Brand Name: {brand_name}
- Industry: {industry_config['name']}
- Key message theme: {theme}
{f"- Product Description: {product_description}" if product_description else ""}
{f"- Unique Selling Point: {usp}" if usp else ""}
{f"- Target Audience: {target_audience}" if target_audience else ""}

HERE ARE REFERENCE EXAMPLES FROM OUR DATABASE (Use them for CULTURAL CONTEXT and TONE only):
{dataset_block}

ADDITIONAL CINEMATIC INSPIRATION:
{few_shot_block}

--- NOW WRITE THE SCRIPT ---
IMPORTANT: Follow the [Time] - Visual - Audio - Dialogue format strictly.
INPUT: {input_description}
OUTPUT:"""

    return SYSTEM_PROMPT, user_message

