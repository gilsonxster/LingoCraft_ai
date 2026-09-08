"""
Conjugation Quiz Evaluator Agent for LingoCraft AI.
Analyzes quiz submissions, explains common pitfalls, and generates micro-practice drills.
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
4. Always bold key grammatical terms (**bold**).

Return ONLY a JSON object:
{
  "is_correct": true/false,
  "headline": "¡Brillante!" or "¡Casi! Comprendamos este detalle:",
  "feedback": "Detailed explanation with **bold** highlights.",
  "why_common_mistake": "Why learners often make this slip...",
  "micro_practice_prompt": "Try this micro-practice: 'El chef _____ la comida ayer.'",
  "micro_practice_options": ["hizo", "hace", "hicieron", "hacer"],
  "micro_practice_correct_index": 0,
  "micro_practice_explanation": "Explanation for the micro-practice."
}
"""

def create_quiz_agent() -> Agent:
    """Creates an ADK Agent instance for quiz evaluation."""
    return Agent(
        name="quiz_evaluator",
        model="gemini-2.5-flash",
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
    """Evaluates quiz selection with constructive feedback loop."""
    correct_option = quiz_data.options[quiz_data.correct_index]
    is_correct = (selected_option.strip() == correct_option.strip())

    if is_correct:
        return {
            "is_correct": True,
            "headline": "¡Excelente trabajo! 🎯",
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
        f"Choosing '**{selected_option}**' is a common misstep because it resembles other standard conjugations."
    )

    if api_key and api_key.strip():
        try:
            client = genai.Client(api_key=api_key.strip())
            prompt = f"""
Sentence Prompt: {quiz_data.sentence_prompt}
Options: {quiz_data.options}
Correct Option: {correct_option}
Learner Selected: {selected_option}
Pre-identified pitfall: {distractor_reason}

Explain why this mistake is common and provide an immediate micro-practice drill. Return strict JSON.
"""
            response = client.models.generate_content(
                model="gemini-2.5-flash",
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

    # Offline constructive feedback
    return {
        "is_correct": False,
        "headline": "¡No pasa nada, es un error muy común! 💡",
        "feedback": f"You chose '**{selected_option}**', but the correct form here is '**{correct_option}**'.",
        "why_common_mistake": distractor_reason,
        "micro_practice_prompt": quiz_data.micro_practice_prompt,
        "micro_practice_options": quiz_data.micro_practice_options,
        "micro_practice_correct_index": quiz_data.micro_practice_correct_index,
        "micro_practice_explanation": quiz_data.micro_practice_explanation
    }
