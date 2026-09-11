"""
Conjugation Quiz Evaluator Agent for LingoCraft AI.
Analyzes quiz submissions, explains common pitfalls, and generates micro-practice drills in the learner's native language.
"""
import json
from typing import Dict, Any, List
from google.adk.agents import Agent
from google import genai
from curriculum_data import Card5Quiz

QUIZ_SYSTEM_PROMPT = """
You are LingoCraft AI's Quiz Evaluator Agent.
Your pedagogical purpose:
1. Evaluate user's selected quiz option against the correct answer.
2. If CORRECT: Praise the learner warmly, explain WHY this specific conjugation fits the grammatical context (subject pronoun, tense marker, trigger words).
3. If INCORRECT:
   - Provide empathetic, constructive feedback.
   - Crucially explain WHY this mistake is very common among learners (e.g., false analogies with regular verbs, confusion between 1st and 3rd person singular, mixing up preterite vs imperfect).
   - Offer an IMMEDIATE micro-practice drill (a single sentence challenge with multiple choices) to cement the rule right now before moving forward.
4. CRITICAL LANGUAGE DIRECTIVE: Write the 'headline', 'feedback', 'why_common_mistake', and 'micro_practice_explanation' in the learner's native/support language ({native_lang}).
5. Always bold key grammatical terms (**bold**).

Return ONLY a JSON object:
{
  "is_correct": true/false,
  "headline": "¡Brillante!" or "Almost! Let's understand this detail:",
  "feedback": "Detailed explanation written in native language with **bold** highlights.",
  "why_common_mistake": "Why learners often make this slip in native language...",
  "micro_practice_prompt": "Try this micro-practice in native language: 'El chef _____ la comida ayer.'",
  "micro_practice_options": ["hizo", "hace", "hicieron", "hacer"],
  "micro_practice_correct_index": 0,
  "micro_practice_explanation": "Explanation for the micro-practice in native language."
}
"""

def create_quiz_agent() -> Agent:
    """Creates an ADK Agent instance for quiz evaluation."""
    return Agent(
        name="quiz_evaluator",
        model="gemini-3.1-flash-lite",
        instruction=QUIZ_SYSTEM_PROMPT,
        output_key="quiz_feedback"
    )

def evaluate_quiz_submission(
    quiz_data: Card5Quiz,
    selected_option: str,
    target_lang: str = "Spanish",
    native_lang: str = "English",
    api_key: str = ""
) -> Dict[str, Any]:
    """Evaluates quiz selection with constructive feedback loop in native language."""
    correct_option = quiz_data.options[quiz_data.correct_index]
    is_correct = (selected_option.strip() == correct_option.strip())

    is_pt = "portugu" in native_lang.lower()

    if is_correct:
        headline = "¡Excelente trabalho! 🎯" if is_pt else "¡Excelente trabajo! 🎯"
        return {
            "is_correct": True,
            "headline": headline,
            "feedback": quiz_data.correct_explanation,
            "why_common_mistake": "",
            "micro_practice_prompt": "",
            "micro_practice_options": [],
            "micro_practice_correct_index": 0,
            "micro_practice_explanation": ""
        }

    # Selected incorrect option: get distractor reason
    distractor_reason = quiz_data.distractor_explanations.get(
        selected_option,
        f"Escolher '**{selected_option}**' é um desvio comum porque se assemelha a outras formas conhecidas." if is_pt else f"Choosing '**{selected_option}**' is a common misstep because it resembles other standard conjugations."
    )

    if api_key and api_key.strip():
        try:
            client = genai.Client(api_key=api_key.strip())
            prompt = f"""
Target Language: {target_lang}
Native/Support Language: {native_lang}
Sentence Prompt: {quiz_data.sentence_prompt}
Options: {quiz_data.options}
Correct Option: {correct_option}
Learner Selected: {selected_option}
Pre-identified pitfall: {distractor_reason}

CRITICAL: Explain why this mistake is common and provide an immediate micro-practice drill, WRITTEN ENTIRELY IN {native_lang}. Return strict JSON.
"""
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    system_instruction=QUIZ_SYSTEM_PROMPT,
                    response_mime_type="application/json"
                )
            )
            data = json.loads(response.text)
            data["is_correct"] = False
            return data
        except Exception as e:
            print(f"Quiz evaluation fallback: {e}")

    # Localized offline constructive feedback
    headline = "Sem problemas, é um erro muito comum! 💡" if is_pt else "¡No pasa nada, es un error muy común! 💡"
    feedback_text = (
        f"Você escolheu '**{selected_option}**', mas a forma correta aqui é '**{correct_option}**'."
        if is_pt else
        f"You chose '**{selected_option}**', but the correct form here is '**{correct_option}**'."
    )
    return {
        "is_correct": False,
        "headline": headline,
        "feedback": feedback_text,
        "why_common_mistake": distractor_reason,
        "micro_practice_prompt": quiz_data.micro_practice_prompt,
        "micro_practice_options": quiz_data.micro_practice_options,
        "micro_practice_correct_index": quiz_data.micro_practice_correct_index,
        "micro_practice_explanation": quiz_data.micro_practice_explanation
    }
