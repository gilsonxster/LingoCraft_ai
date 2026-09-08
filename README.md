# 🎓 LingoCraft AI — Language Learning Coach

**LingoCraft AI** is an interactive, empathetic, and highly structured language learning coach built with **Google ADK (Agent Development Kit)**, **Google GenAI (Gemini)**, and **Streamlit**.

Guided by research-backed pedagogy, LingoCraft AI guides foreign language learners through topic-focused, tense-by-tense mastery using an enhanced **5-stage flashcard system**.

---

## 🌟 Pedagogical Workflow

For any user-selected topic (e.g., *Irregular Verbs: Verbo "Hacer"*) and target language pair:

### 1. Curriculum Initialization
* **Language Detection:** Detects the target language and native/support language.
* **Tense Roadmap:** Outlines the roadmap of tenses/modes to be mastered sequentially:
  `Infinitivo` ➔ `Gerundio` ➔ `Participio` ➔ `Presente de Indicativo` ➔ `Pretérito Indefinido`
* **Focused Progression:** Proceeds **one tense/card pack at a time** to avoid cognitive overload.

---

### 2. Enhanced 5-Stage Flashcard Structure (Per Tense/Form)

For each tense/grammatical form within the topic, the student experiences a structured sequential delivery:

| Step | Card Name | Purpose & Content |
|---|---|---|
| **Card 1** | **Concept & Rule** | Concise grammatical explanation, usage context, and common triggers/keywords. |
| **Card 2** | **Bilingual Example** | High-utility real-world phrase comparing the target language structure with the learner's native language. |
| **Card 3** | **Pronunciation Guide** | Phonetic breakdown, stressed syllables marked (e.g., *ha-**CIEN**-do*), and instant audio-ready spoken text via TTS. |
| **Card 4** | **Speech Validation** | Prompts the user to record/speak the phrase. Evaluates transcription/phonetics, highlights target sounds, and provides actionable tips. |
| **Card 5** | **Conjugation Quiz** | Multiple-choice challenge (4 options) testing correct conjugation in a contextual sentence. |

---

## 🔄 Constructive Feedback Loop & Interaction Guidelines

1. **Step-by-Step Delivery:**
   * Presents **one card at a time**. After each card, pauses and prompts the learner to confirm understanding, submit spoken audio, or answer the quiz before revealing the next stage.
2. **Constructive Feedback Loop:**
   * If the learner answers Card 5 incorrectly or mispronounces in Card 4, LingoCraft AI explains **why** the mistake is common (e.g., regularization traps, subject pronoun mismatch, false analogies) and generates an **immediate micro-practice drill** right on the card before advancing to the next tense.
3. **Tone & Style:**
   * Encouraging, empathetic, clear, concise, and pedagogical.
   * Highlights key grammatical terms in **bold** and phonetic stress in **UPPERCASE** (e.g., *ha-**CIEN**-do*).

---

## 🏛️ Multi-Agent Architecture (Google ADK)

Similar to the multi-agent pipeline design in `bufet_agent`, LingoCraft AI coordinates specialized pedagogical agents:

- **1. Curriculum Initialization Agent (`skills/curriculum_agent.py`):** Formulates the tense-by-tense roadmap.
- **2. 5-Stage Flashcard Generator Agent (`skills/flashcard_agent.py`):** Formats Card 1 to Card 5 with structured schemas.
- **3. Speech Validation Agent (`skills/speech_agent.py`):** Analyzes spoken transcription, vowel clarity, and provides vocal tips.
- **4. Conjugation Quiz Evaluator Agent (`skills/quiz_agent.py`):** Evaluates quiz responses, explains common distractors, and provides instant micro-drills.
- **5. Empathetic Conversational Coach (`skills/coach_chat_agent.py`):** Answers real-time questions in the "Ask Coach LingoCraft" chat tab.

---

## 🚀 Quickstart & Setup

### 1. Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)
Create a `.env` file or set your Gemini API key:
```bash
cp .env.example .env
# Edit .env and insert GEMINI_API_KEY=your_key_here
```
*(Note: LingoCraft AI includes rich pre-curated offline mastery packs for instant zero-configuration practice even without an API key!)*

### 3. Run the Streamlit Application
```bash
streamlit run app.py --server.port 8501
```

### 4. Run the Test Suite
```bash
python test_lingocraft.py
```
