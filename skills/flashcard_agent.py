"""
5-Stage Flashcard Generator Agent for LingoCraft AI.
Produces structured 5-card packs for a specific tense/grammatical form.
"""
import json
from typing import Dict, Any, Optional
from google.adk.agents import Agent
from google import genai
from curriculum_data import TenseFlashcardPack, Card1Concept, Card2Example, Card3Pronunciation, Card4Speech, Card5Quiz

FLASHCARD_SYSTEM_PROMPT = """
You are LingoCraft AI's 5-Stage Flashcard Generator Agent.
Your pedagogical mission is to craft a strict 5-stage flashcard deck for ONE specific tense/form within the user's chosen topic.

Tone & Style Requirements:
- Encouraging, clear, concise, and empathetic.
- Highlight key grammatical words in **bold**.
- Highlight phonetic stress in **UPPERCASE** (e.g., ha-**CIEN**-do).
- Present one tense at a time.

Return ONLY a JSON object matching this schema:
{
  "tense_name": "Name of the tense (e.g., Gerundio)",
  "tense_order": 1,
  "card1_concept": {
    "title": "Card 1: Concept & Rule",
    "rule": "Concise grammatical rule with key words in **bold**.",
    "usage_context": "Real-world communicative usage context.",
    "triggers": ["trigger 1", "trigger 2"]
  },
  "card2_example": {
    "target_sentence": "High-utility target sentence with key conjugated verb in **bold**.",
    "native_sentence": "Natural translation in native language.",
    "breakdown": "Grammatical nuance explaining the structure."
  },
  "card3_pronunciation": {
    "word": "Key conjugated verb or phrase",
    "phonetic_breakdown": "Syllables with stressed syllable in **UPPERCASE** and **bold** (e.g., ha-**CIEN**-do)",
    "stressed_syllables": "**STRESSED_PART**",
    "audio_text": "Clear phrase for text-to-speech",
    "phonetic_tips": "Actionable vocalization tips (e.g., vowel clarity, silent letters)."
  },
  "card4_speech": {
    "target_phrase": "Sentence for the user to speak aloud",
    "expected_phonetics": "IPA or phonetic representation",
    "key_focus_sounds": "Specific sounds to watch out for",
    "practice_tip": "Helpful encouragement for vocal practice."
  },
  "card5_quiz": {
    "sentence_prompt": "Contextual sentence with blank _____ for the verb.",
    "options": ["Correct Option", "Distractor 1", "Distractor 2", "Distractor 3"],
    "correct_index": 0,
    "correct_explanation": "Clear praise explaining why it is correct.",
    "distractor_explanations": {
      "Distractor 1": "Why learners commonly choose this mistake and what it actually means.",
      "Distractor 2": "Why this is incorrect.",
      "Distractor 3": "Why this is incorrect."
    },
    "micro_practice_prompt": "Immediate micro-drill if incorrect: 'Complete: _____ '",
    "micro_practice_options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "micro_practice_correct_index": 0,
    "micro_practice_explanation": "Explanation for the micro-drill."
  }
}
"""

def create_flashcard_agent() -> Agent:
    """Creates an ADK Agent instance for 5-stage flashcard generation."""
    return Agent(
        name="flashcard_generator",
        model="gemini-2.5-flash",
        instruction=FLASHCARD_SYSTEM_PROMPT,
        output_key="flashcard_pack"
    )

def generate_tense_flashcards(
    topic: str,
    tense_name: str,
    tense_order: int,
    target_lang: str,
    native_lang: str,
    api_key: str = ""
) -> TenseFlashcardPack:
    """Generates or loads the 5-card pack for a specific tense."""
    # First check if pre-curated data exists
    from curriculum_data import SPANISH_HACER_CURRICULUM
    if "hacer" in topic.lower() and tense_name in SPANISH_HACER_CURRICULUM.cards_by_tense:
        return SPANISH_HACER_CURRICULUM.cards_by_tense[tense_name]

    if api_key and api_key.strip():
        try:
            client = genai.Client(api_key=api_key.strip())
            prompt = f"""
Topic: {topic}
Target Tense/Form: {tense_name} (Tense index #{tense_order})
Target Language: {target_lang}
Native/Support Language: {native_lang}

Generate the 5-stage flashcard pack. Ensure phonetics have stressed syllables in **UPPERCASE** and bold (e.g. ha-**CIEN**-do). Return strict JSON.
"""
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    system_instruction=FLASHCARD_SYSTEM_PROMPT,
                    response_mime_type="application/json"
                )
            )
            data = json.loads(response.text)
            return TenseFlashcardPack(
                tense_name=data["tense_name"],
                tense_order=data.get("tense_order", tense_order),
                card1_concept=Card1Concept(**data["card1_concept"]),
                card2_example=Card2Example(**data["card2_example"]),
                card3_pronunciation=Card3Pronunciation(**data["card3_pronunciation"]),
                card4_speech=Card4Speech(**data["card4_speech"]),
                card5_quiz=Card5Quiz(**data["card5_quiz"])
            )
        except Exception as e:
            print(f"Flashcard generation fallback: {e}")

    # Fallback to Spanish Hacer pack if tense matches, or generate sensible default
    if tense_name in SPANISH_HACER_CURRICULUM.cards_by_tense:
        return SPANISH_HACER_CURRICULUM.cards_by_tense[tense_name]

    return list(SPANISH_HACER_CURRICULUM.cards_by_tense.values())[0]
