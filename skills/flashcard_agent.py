"""
5-Stage Flashcard Generator Agent for LingoCraft AI.
Produces structured 5-card packs for a specific tense/grammatical form.
"""
import json
from typing import Dict, Any, Optional
from google.adk.agents import Agent
from google import genai
from curriculum_data import TenseFlashcardPack, Card1Concept, Card2Example, Card3Pronunciation, Card4Speech, Card5Quiz, get_curriculum_or_fallback

FLASHCARD_SYSTEM_PROMPT = """
You are LingoCraft AI's 5-Stage Flashcard Generator Agent.
Your pedagogical mission is to craft a strict 5-stage flashcard deck for ONE specific tense/form within the user's chosen topic.

CRITICAL LANGUAGE DIRECTIVE:
- Target Language: {target_lang}. Target phrases, conjugated verbs, and examples MUST be in {target_lang}.
- Native/Support Language: {native_lang}. ALL explanatory text, grammatical rules, usage contexts, comparative breakdowns, pronunciation tips, vocal focus tips, quiz feedback, distractor explanations, micro-practice prompts, and suggested coach prompts MUST be written in {native_lang} (or in {target_lang} if native_lang is identical to target_lang).

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
    "rule": "Concise grammatical rule written in the native language with key words in **bold**.",
    "usage_context": "Real-world communicative usage context written in native language.",
    "triggers": ["trigger 1", "trigger 2"]
  },
  "card2_example": {
    "target_sentence": "High-utility target sentence with key conjugated verb in **bold**.",
    "native_sentence": "Natural translation in native language.",
    "breakdown": "Grammatical nuance explaining the structure written in native language."
  },
  "card3_pronunciation": {
    "word": "Key conjugated verb or phrase",
    "phonetic_breakdown": "Syllables with stressed syllable in **UPPERCASE** and **bold** (e.g., ha-**CIEN**-do)",
    "stressed_syllables": "**STRESSED_PART**",
    "audio_text": "Clear phrase for text-to-speech",
    "phonetic_tips": "Actionable vocalization tips in native language (e.g., vowel clarity, silent letters)."
  },
  "card4_speech": {
    "target_phrase": "Sentence for the user to speak aloud in target language",
    "expected_phonetics": "IPA or phonetic representation",
    "key_focus_sounds": "Specific sounds to watch out for, explained in native language",
    "practice_tip": "Helpful encouragement for vocal practice written in native language."
  },
  "card5_quiz": {
    "sentence_prompt": "Contextual sentence with blank _____ for the verb.",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_index": 0,
    "correct_explanation": "Clear praise explaining why it is correct in native language.",
    "distractor_explanations": {
      "Option B": "Why learners commonly make this mistake written in native language.",
      "Option C": "Why this is incorrect in native language.",
      "Option D": "Why this is incorrect in native language."
    },
    "micro_practice_prompt": "Immediate micro-drill if incorrect: 'Complete: _____ '",
    "micro_practice_options": ["Opt 1", "Opt 2", "Opt 3", "Opt 4"],
    "micro_practice_correct_index": 0,
    "micro_practice_explanation": "Explanation for the micro-drill in native language."
  },
  "suggested_coach_prompts": [
    "Smart follow-up question 1 about the trickiest/most complex aspect of this tense?",
    "Smart follow-up question 2 on false friends or common traps?",
    "Smart follow-up question 3 requesting real-life practice examples?"
  ]
}
"""

def create_flashcard_agent() -> Agent:
    """Creates an ADK Agent instance for 5-stage flashcard generation."""
    return Agent(
        name="flashcard_generator",
        model="gemini-3.1-flash-lite",
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
    """Generates or loads the 5-card pack for a specific tense with native language explanations."""
    # First check if pre-curated localized data exists (Hacer, Tener, etc.)
    curriculum = get_curriculum_or_fallback(topic, target_lang, native_lang)
    if tense_name in curriculum.cards_by_tense and (
        "hacer" in topic.lower() or "tener" in topic.lower() or not (api_key and api_key.strip())
    ):
        pack = curriculum.cards_by_tense[tense_name]
        pack.tense_name = tense_name
        return pack

    if api_key and api_key.strip():
        try:
            client = genai.Client(api_key=api_key.strip())
            prompt = f"""
Topic: {topic}
Target Tense/Form: {tense_name} (Tense index #{tense_order})
Target Language: {target_lang}
Native/Support Language: {native_lang}

Generate the 5-stage flashcard pack.
CRITICAL: All explanations, rules, breakdowns, tips, quiz explanations, and 3 suggested_coach_prompts MUST be in {native_lang}.
Ensure phonetics have stressed syllables in **UPPERCASE** and bold (e.g. ha-**CIEN**-do).
Return strict JSON.
"""
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    system_instruction=FLASHCARD_SYSTEM_PROMPT,
                    response_mime_type="application/json"
                )
            )
            data = json.loads(response.text)
            return TenseFlashcardPack(
                tense_name=tense_name,
                tense_order=data.get("tense_order", tense_order),
                card1_concept=Card1Concept(**data["card1_concept"]),
                card2_example=Card2Example(**data["card2_example"]),
                card3_pronunciation=Card3Pronunciation(**data["card3_pronunciation"]),
                card4_speech=Card4Speech(**data["card4_speech"]),
                card5_quiz=Card5Quiz(**data["card5_quiz"]),
                suggested_coach_prompts=data.get("suggested_coach_prompts", [])
            )
        except Exception as e:
            print(f"Flashcard generation fallback: {e}")

    # Localized fallback
    if tense_name in curriculum.cards_by_tense:
        pack = curriculum.cards_by_tense[tense_name]
        pack.tense_name = tense_name
        return pack

    pack = list(curriculum.cards_by_tense.values())[0]
    pack.tense_name = tense_name
    return pack
