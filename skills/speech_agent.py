"""
Speech Validation Agent for LingoCraft AI.
Evaluates transcription and phonetic accuracy, provides actionable tips and immediate micro-practice in the learner's native language.
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
6. CRITICAL LANGUAGE DIRECTIVE: Write the 'feedback_title', 'evaluation_message', 'actionable_tip', and 'micro_practice_drill' in the learner's specified native/support language ({native_lang}).

Return ONLY a JSON object:
{
  "accuracy_score": 85,
  "feedback_title": "Headline in native language (e.g., Quase perfeito!)",
  "evaluation_message": "Your vocal cadence was very natural written in native language.",
  "phonetic_breakdown": "ha-**CIEN**-do",
  "actionable_tip": "Make sure the initial h is silent and glide the ie smoothly written in native language.",
  "requires_micro_practice": false,
  "micro_practice_drill": "Say 3 times: ha-**CIEN**-do café."
}
"""

def create_speech_agent() -> Agent:
    """Creates an ADK Agent instance for speech evaluation."""
    return Agent(
        name="speech_validator",
        model="gemini-3.1-flash-lite",
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
    is_pt = "portugu" in native_lang.lower()

    clean_target = algo_result.get("target", target_phrase)
    clean_spoken = algo_result.get("spoken", spoken_text)

    if api_key and api_key.strip():
        try:
            client = genai.Client(api_key=api_key.strip())
            prompt = f"""
Target Language: {target_lang}
Native/Support Language: {native_lang}
Target Phrase: "{clean_target}"
User Spoken Transcription: "{clean_spoken}"
Algorithmic Text Similarity Score: {score}%

CRITICAL: Provide an empathetic, constructive speech validation report written entirely in {native_lang}. Return strict JSON.
"""
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    system_instruction=SPEECH_SYSTEM_PROMPT,
                    response_mime_type="application/json"
                )
            )
            data = json.loads(response.text)
            data["accuracy_score"] = max(score, data.get("accuracy_score", score))
            data["diff_html"] = algo_result.get("diff_html", "")
            data["word_diff"] = algo_result.get("word_diff", [])
            data["extra_words"] = algo_result.get("extra_words", [])
            return data
        except Exception as e:
            print(f"Speech evaluation fallback: {e}")

    # Localized offline algorithmic evaluation
    diff_html = algo_result.get("diff_html", "")
    word_diff = algo_result.get("word_diff", [])
    extra_words = algo_result.get("extra_words", [])

    if score >= 80:
        return {
            "accuracy_score": score,
            "feedback_title": "Excelente Pronúncia! 🌟" if is_pt else "¡Excelente Pronunciación! 🌟",
            "evaluation_message": f"Ótima vocalização! Você reproduziu '{clean_target}' com muita clareza." if is_pt else f"Great vocalization! You matched '{clean_target}' clearly and confidently.",
            "phonetic_breakdown": "Vogais claras e sílaba tônica bem definida",
            "actionable_tip": "Mantenha esse mesmo ritmo ao falar em conversas reais!" if is_pt else "Keep this exact rhythm when speaking in real conversations!",
            "requires_micro_practice": False,
            "micro_practice_drill": "",
            "diff_html": diff_html,
            "word_diff": word_diff,
            "extra_words": extra_words
        }
    elif score >= 50:
        return {
            "accuracy_score": score,
            "feedback_title": "Bom esforço! No caminho certo 👍" if is_pt else "¡Buen Intento! Moving in the right direction 👍",
            "evaluation_message": f"Você falou '{clean_spoken}', comparado com o modelo '{clean_target}'." if is_pt else f"You transcribed '{clean_spoken}' compared to '{clean_target}'.",
            "phonetic_breakdown": "Atenção à precisão das vogais",
            "actionable_tip": "Fique atento às letras mudas e certifique-se de que a sílaba principal receba a ênfase correta." if is_pt else "Be mindful of silent letters and ensure the primary syllable receives emphatic stress.",
            "requires_micro_practice": True,
            "micro_practice_drill": f"Tente repetir devagar: '{clean_target}' focando no verbo principal." if is_pt else f"Try repeating slowly: '{clean_target}' focusing on the main verb.",
            "diff_html": diff_html,
            "word_diff": word_diff,
            "extra_words": extra_words
        }
    else:
        return {
            "accuracy_score": score,
            "feedback_title": "Vamos lapidar isso! Pronúncia exige memória muscular 💪" if is_pt else "Let's Refine That! Pronunciation takes muscle memory 💪",
            "evaluation_message": f"Detectamos '{clean_spoken}', mas a frase alvo era '{clean_target}'." if is_pt else f"We detected '{clean_spoken}', but the target was '{clean_target}'.",
            "phonetic_breakdown": "Divida cada sílaba pausadamente",
            "actionable_tip": "Fale calmamente perto do microfone, praticando uma palavra por vez." if is_pt else "Speak slowly and clearly into the microphone. Practice individual words first!",
            "requires_micro_practice": True,
            "micro_practice_drill": f"Repita 3 vezes em voz alta: '{clean_target}'" if is_pt else f"Repeat 3 times aloud: '{clean_target}'",
            "diff_html": diff_html,
            "word_diff": word_diff,
            "extra_words": extra_words
        }

