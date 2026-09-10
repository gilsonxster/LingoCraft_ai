"""
Interactive Empathetic Language Coach Agent for LingoCraft AI.
Answers learners' questions with warm pedagogy, bold keywords, and UPPERCASE phonetics in their native language.
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
- CRITICAL LANGUAGE DIRECTIVE: Speak to the learner in their selected Native/Support Language ({native_lang}), while using {target_lang} for vocabulary, examples, and conjugations.
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
    """Generates a response from Coach LingoCraft in the learner's native language."""
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
- Target Language to Learn: {target_lang}
- Learner's Native/Support Language: {native_lang}

Recent Conversation:
{history_text}

Learner's Question: "{question}"

Provide an empathetic, encouraging, and pedagogically clear response written in {native_lang}. Remember to bold key terms and put phonetic stress in **UPPERCASE**.
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

    # Offline empathetic coach responses (localized)
    q_lower = question.lower()
    is_pt = "portugu" in native_lang.lower()

    if "calor" in q_lower or "weather" in q_lower or "tempo" in q_lower or "clima" in q_lower:
        if is_pt:
            return "Excelente pergunta! Em espanhol, fenômenos climáticos e sensações térmicas usam o verbo **hacer** (*hace calor*, *hace frío*), e não *ser* ou *estar*. Pense que a atmosfera 'faz' calor: pronuncie **HA**-ce ca-**LOR**!"
        return "Great question! In Spanish, weather states like heat or cold use the verb **hacer** (*hace calor*, *hace frío*) rather than *ser* or *estar*. We describe the atmospheric condition as something the weather 'makes' (**hace**)! Pronounce it: **HA**-ce ca-**LOR**."

    elif "difference" in q_lower or "diferença" in q_lower or "hice" in q_lower or "hizo" in q_lower or "z" in q_lower:
        if is_pt:
            return "No Pretérito Indefinido (passado simples), o radical é **hic-**: **yo hice** (eu fiz) usa 'c' brando, mas **él/ella hizo** (ele/ela fez) troca a grafia para 'z' antes da vogal 'o' (**HI**-zo) para manter o som brando e evitar que soe como 'hico'!"
        return "In the Pretérito Indefinido (simple past), remember the radical stem is **hic-**: **yo hice** (I did/made) has a soft 'c', whereas **él/ella hizo** (he/she did/made) changes spelling to 'z' before the letter 'o' (**HI**-zo) to keep the pronunciation soft!"

    elif "estar" in q_lower or "haber" in q_lower or "progress" in q_lower or "gerund" in q_lower:
        if is_pt:
            return "O **gerundio** (*haciendo*) combina-se exclusivamente com **estar** (*estoy haciendo*) para indicar uma ação ocorrendo exatamente no presente! Já o verbo **haber** só se combina com o **participio** (*he hecho* = fiz / tenho feito). Pronuncie a tônica: ha-**CIEN**-do!"
        return "The **gerundio** (*haciendo*) pairs with **estar** (*estoy haciendo*) to describe an action happening right now! In contrast, **haber** only pairs with the past participle (*he hecho* = I have done). Pronounce the stress clearly: ha-**CIEN**-do!"

    else:
        if is_pt:
            return f"Olá! Como seu coach **LingoCraft AI**, estou aqui para ajudar você a dominar **{current_tense}** para **{current_topic}**. A chave do aprendizado de idiomas é o treino constante e a fala em voz alta. Concentre-se nas sílabas tônicas como ha-**CIEN**-do. Que outro exemplo você gostaria de praticar juntos?"
        return f"¡Hola! As your **LingoCraft AI** coach, I am thrilled to help you master **{current_tense}** for **{current_topic}**. Remember: regular practice builds muscle memory. Keep your focus on stressed syllables like ha-**CIEN**-do and do not hesitate to practice out loud! What other sentence would you like us to break down together?"
