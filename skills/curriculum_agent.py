"""
Curriculum Initialization Agent for LingoCraft AI.
Analyzes user selected topic and language pair to construct a structured tense-by-tense roadmap.
"""
import json
from typing import Dict, Any, List
from google.adk.agents import Agent
from google import genai

CURRICULUM_SYSTEM_PROMPT = """
You are LingoCraft AI's Curriculum Initialization Agent.
Your pedagogical role:
1. Detect or verify the target language and native/support language.
2. For the selected topic (e.g., Irregular Verbs: Verbo 'Hacer'), create a pedagogical roadmap of tenses/grammatical forms to be mastered sequentially.
3. Order the roadmap from foundational forms (e.g., Infinitivo, Gerundio, Participio) to core communicative tenses (e.g., Presente, Pretérito Indefinido, Imperfecto, Futuro, Subjuntivo).
4. CRITICAL LANGUAGE DIRECTIVE: Write the 'description' and any overview notes in the learner's specified Native/Support Language ({native_lang}), while keeping tense names standard.

Return ONLY a JSON object with this structure:
{
  "topic": "Topic Title",
  "target_language": "Spanish",
  "target_language_code": "es",
  "native_language": "English",
  "native_language_code": "en",
  "description": "A concise pedagogical summary in the learner's native/support language explaining what this curriculum covers.",
  "tenses_roadmap": ["Infinitivo", "Gerundio", "Participio", "Presente de Indicativo", "Pretérito Indefinido"]
}
"""

def create_curriculum_agent() -> Agent:
    """Creates an ADK Agent instance for curriculum planning."""
    return Agent(
        name="curriculum_initializer",
        model="gemini-2.5-flash",
        instruction=CURRICULUM_SYSTEM_PROMPT,
        output_key="curriculum_plan"
    )

def generate_curriculum_plan(topic: str, target_lang: str, native_lang: str, api_key: str = "") -> Dict[str, Any]:
    """Generates a curriculum roadmap using Gemini or localized fallback rules."""
    if api_key and api_key.strip():
        try:
            client = genai.Client(api_key=api_key.strip())
            prompt = f"""
User Topic: {topic}
Target Language: {target_lang}
Native/Support Language: {native_lang}

Generate the pedagogical curriculum roadmap. Write all descriptions in {native_lang}. Return strict JSON.
"""
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    system_instruction=CURRICULUM_SYSTEM_PROMPT,
                    response_mime_type="application/json"
                )
            )
            data = json.loads(response.text)
            return data
        except Exception as e:
            print(f"Curriculum generation fallback: {e}")

    # Offline / localized curated fallback
    from curriculum_data import get_curriculum_or_fallback
    curriculum = get_curriculum_or_fallback(topic, target_lang, native_lang)
    return {
        "topic": topic or curriculum.title,
        "target_language": target_lang or curriculum.target_language,
        "target_language_code": curriculum.target_language_code,
        "native_language": native_lang or curriculum.native_language,
        "native_language_code": curriculum.native_language_code,
        "description": curriculum.description,
        "tenses_roadmap": curriculum.tenses_roadmap
    }
