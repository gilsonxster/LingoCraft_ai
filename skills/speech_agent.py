"""
Speech Validation Agent for LingoCraft AI.
Evaluates transcription and phonetic accuracy, provides actionable tips and immediate micro-practice.
"""
import json
from typing import Dict, Any
from google.adk.agents import Agent
from google import genai
from audio_utils import evaluate_spoken_accuracy

SPEECH_SYSTEM_PROMPT = """
You are LingoCraft AI's Speech Validation Agent.
Your pedagogical purpose:
1. Evaluate the user's spoken audio transcription against the target phrase.
2. Determine phonetic accuracy and identify pronunciation stumbling blocks (vowels, stressed syllables, silent letters, rolling consonants).
3. If pronunciation is good/excellent: celebrate their vocal effort warmly.
4. If pronunciation needs improvement: empathetically explain WHY this sound or stress pattern is tricky for non-native speakers, provide actionable vocal adjustments, and offer a quick micro-practice sentence or word to isolate the sound.
5. Highlight phonetic stress in **UPPERCASE** and **bold** (e.g., ha-**CIEN**-do).

Return ONLY a JSON object:
{
  "accuracy_score": 85,
  "feedback_title": "¡Casi perfecto!",
  "evaluation_message": "Your vocal cadence was very natural. Focus on keeping the stress on **CIEN**.",
  "phonetic_breakdown": "ha-**CIEN**-do",
  "actionable_tip": "Make sure the initial 'h' is silent and glide the 'ie' smoothly.",
  "requires_micro_practice": false,
  "micro_practice_drill": "Say 3 times: ha-**CIEN**-do café."
}
"""

def create_speech_agent() -> Agent:
    """Creates an ADK Agent instance for speech evaluation."""
    return Agent(
        name="speech_validator",
        model="gemini-2.5-flash",
        instruction=SPEECH_SYSTEM_PROMPT,
        output_key="speech_evaluation"
    )

def evaluate_speech_submission(
    spoken_text: str,
    target_phrase: str,
    target_lang: str,
    native_lang: str,
    api_key: str = ""
) -> Dict[str, Any]:
    """Evaluates spoken transcription using algorithmic comparison or Gemini."""
    algo_result = evaluate_spoken_accuracy(spoken_text, target_phrase)
    score = algo_result["score"]

    if api_key and api_key.strip():
        try:
            client = genai.Client(api_key=api_key.strip())
            prompt = f"""
Target Language: {target_lang}
Native Language: {native_lang}
Target Phrase: "{target_phrase}"
User Spoken Transcription: "{spoken_text}"
Algorithmic Text Similarity Score: {score}%

Provide an empathetic, constructive speech validation report. Return strict JSON.
"""
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    system_instruction=SPEECH_SYSTEM_PROMPT,
                    response_mime_type="application/json"
                )
            )
            data = json.loads(response.text)
            data["accuracy_score"] = max(score, data.get("accuracy_score", score))
            return data
        except Exception as e:
            print(f"Speech evaluation fallback: {e}")

    # Offline algorithmic evaluation
    if score >= 80:
        return {
            "accuracy_score": score,
            "feedback_title": "¡Excelente Pronunciación! 🌟",
            "evaluation_message": f"Great vocalization! You matched '{target_phrase}' clearly and confidently.",
            "phonetic_breakdown": "Well stressed and clear vowels",
            "actionable_tip": "Keep this exact rhythm when speaking in real conversations!",
            "requires_micro_practice": False,
            "micro_practice_drill": ""
        }
    elif score >= 50:
        return {
            "accuracy_score": score,
            "feedback_title": "¡Buen Intento! Moving in the right direction 👍",
            "evaluation_message": f"You transcribed '{spoken_text}' compared to '{target_phrase}'.",
            "phonetic_breakdown": "Pay attention to vowel precision",
            "actionable_tip": "Be mindful of silent letters and ensure the primary syllable receives emphatic stress.",
            "requires_micro_practice": True,
            "micro_practice_drill": f"Try repeating slowly: '{target_phrase}' focusing on the main verb."
        }
    else:
        return {
            "accuracy_score": score,
            "feedback_title": "Let's Refine That! Don't worry, pronunciation takes muscle memory 💪",
            "evaluation_message": f"We detected '{spoken_text}', but the target was '{target_phrase}'.",
            "phonetic_breakdown": "Break down each syllable independently",
            "actionable_tip": "Speak slowly and clearly into the microphone. Practice individual words first!",
            "requires_micro_practice": True,
            "micro_practice_drill": f"Repeat 3 times: '{target_phrase}'"
        }
