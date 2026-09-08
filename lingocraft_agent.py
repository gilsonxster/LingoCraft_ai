"""
LingoCraft AI Master Agent Pipeline.
Coordinates curriculum planning, 5-stage flashcard delivery, speech evaluation, and quiz feedback.
Built using Google ADK and Google GenAI SDK.
"""
import os
import asyncio
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

from google.adk.agents import SequentialAgent, ParallelAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Import skills
from skills.curriculum_agent import create_curriculum_agent, generate_curriculum_plan
from skills.flashcard_agent import create_flashcard_agent, generate_tense_flashcards
from skills.speech_agent import create_speech_agent, evaluate_speech_submission
from skills.quiz_agent import create_quiz_agent, evaluate_quiz_submission
from skills.coach_chat_agent import create_coach_agent, ask_lingocraft_coach
from curriculum_data import TenseFlashcardPack, CurriculumCourse, Card5Quiz

# Load environment variables
load_dotenv()

# Establish Google ADK Multi-Agent Architecture
lingocraft_pipeline = SequentialAgent(
    name="lingocraft_master_pipeline",
    sub_agents=[
        create_curriculum_agent(),
        create_flashcard_agent(),
        ParallelAgent(
            name="learning_feedback_panel",
            sub_agents=[create_speech_agent(), create_quiz_agent()]
        ),
        create_coach_agent()
    ]
)

class LingoCraftOrchestrator:
    """
    High-level orchestrator interfacing Streamlit session state with LingoCraft AI agents.
    """
    def __init__(self, api_key: str = ""):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")

    def initialize_curriculum(self, topic: str, target_lang: str, native_lang: str) -> Dict[str, Any]:
        """Runs Curriculum Initializer Agent."""
        return generate_curriculum_plan(topic, target_lang, native_lang, self.api_key)

    def load_tense_card_pack(
        self,
        topic: str,
        tense_name: str,
        tense_order: int,
        target_lang: str,
        native_lang: str
    ) -> TenseFlashcardPack:
        """Runs 5-Stage Flashcard Generator Agent."""
        return generate_tense_flashcards(
            topic=topic,
            tense_name=tense_name,
            tense_order=tense_order,
            target_lang=target_lang,
            native_lang=native_lang,
            api_key=self.api_key
        )

    def validate_speech(
        self,
        spoken_text: str,
        target_phrase: str,
        target_lang: str,
        native_lang: str
    ) -> Dict[str, Any]:
        """Runs Speech Validation Agent."""
        return evaluate_speech_submission(
            spoken_text=spoken_text,
            target_phrase=target_phrase,
            target_lang=target_lang,
            native_lang=native_lang,
            api_key=self.api_key
        )

    def evaluate_quiz(
        self,
        quiz_data: Card5Quiz,
        selected_option: str,
        target_lang: str,
        native_lang: str
    ) -> Dict[str, Any]:
        """Runs Conjugation Quiz Evaluator Agent with constructive feedback loop."""
        return evaluate_quiz_submission(
            quiz_data=quiz_data,
            selected_option=selected_option,
            target_lang=target_lang,
            native_lang=native_lang,
            api_key=self.api_key
        )

    def ask_coach(
        self,
        question: str,
        current_topic: str,
        current_tense: str,
        target_lang: str,
        native_lang: str,
        chat_history: list = None
    ) -> str:
        """Runs interactive Empathetic Coach Agent."""
        return ask_lingocraft_coach(
            question=question,
            current_topic=current_topic,
            current_tense=current_tense,
            target_lang=target_lang,
            native_lang=native_lang,
            chat_history=chat_history,
            api_key=self.api_key
        )
