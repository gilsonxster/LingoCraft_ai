"""
Interactive Empathetic Language Coach Agent for LingoCraft AI.
Answers learners' questions with warm pedagogy, bold keywords, and UPPERCASE phonetics.
"""
from google.adk.agents import Agent
from google import genai

COACH_SYSTEM_PROMPT = """
You are 'LingoCraft AI', an interactive, empathetic, and highly structured language learning coach.
Your primary mission is to guide learners through topic-focused, tense-by-tense mastery of foreign languages using an enhanced 5-stage flashcard system.

Guidelines:
- Tone & Style: Warm, encouraging, clear, concise, and pedagogical.
- Always highlight key words and grammatical terms in **bold**.
- Highlight phonetic stress in **UPPERCASE** (e.g., ha-**CIEN**-do).
- Never overwhelm the user; keep answers structured, actionable, and focused on the current topic/tense.
- Provide practical example sentences comparing the target language structure with the user's native language.
"""

def create_coach_agent() -> Agent:
    """Creates an ADK Agent instance for the chat coach."""
    return Agent(
        name="lingocraft_coach",
        model="gemini-2.5-flash",
        instruction=COACH_SYSTEM_PROMPT,
        output_key="coach_response"
    )

def ask_lingocraft_coach(
    question: str,
    current_topic: str,
    current_tense: str,
    target_lang: str = "Spanish",
    native_lang: str = "English",
    chat_history: list = None,
    api_key: str = ""
) -> str:
    """Generates a response from Coach LingoCraft."""
    if api_key and api_key.strip():
        try:
            client = genai.Client(api_key=api_key.strip())
            history_lines = []
            if chat_history:
                for msg in chat_history[-6:]:
                    role = "Learner" if msg.get("role") == "user" else "Coach LingoCraft"
                    content_str = str(msg.get("content", ""))
                    history_lines.append(role + ": " + content_str)
            history_text = chr(10).join(history_lines)

            prompt = f"""
Current Study Context:
- Topic: {current_topic}
- Current Active Tense/Form: {current_tense}
- Target Language: {target_lang}
- Native Language: {native_lang}

Recent Conversation:
{history_text}

Learner's Question: "{question}"

Provide an empathetic, encouraging, and pedagogically clear response. Remember to bold key terms and put phonetic stress in **UPPERCASE**.
"""
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    system_instruction=COACH_SYSTEM_PROMPT
                )
            )
            return response.text
        except Exception as e:
            print(f"Coach chat fallback: {e}")

    # Offline empathetic coach responses
    q_lower = question.lower()
    if "calor" in q_lower or "weather" in q_lower:
        return "Great question! In Spanish, weather states like heat or cold use the verb **hacer** (*hace calor*, *hace frío*) rather than *ser* or *estar*. We describe the atmospheric condition as something the weather 'makes' (**hace**)! Pronounce it: **HA**-ce ca-**LOR**."
    elif "difference" in q_lower or "hice" in q_lower or "hizo" in q_lower:
        return "In the Pretérito Indefinido (simple past), remember the radical stem is **hic-**: **yo hice** (I did/made) has a soft 'c', whereas **él/ella hizo** (he/she did/made) changes spelling to 'z' before the letter 'o' (**HI**-zo) to keep the pronunciation soft!"
    else:
        return f"¡Hola! As your **LingoCraft AI** coach, I am thrilled to help you master **{current_tense}** for **{current_topic}**. Remember: regular practice builds muscle memory. Keep your focus on stressed syllables like ha-**CIEN**-do and do not hesitate to practice out loud! What other sentence would you like us to break down together?"
