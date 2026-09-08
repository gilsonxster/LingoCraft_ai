"""
Unit and integration test script for LingoCraft AI.
Verifies all 5-stage flashcard steps, audio generation, and agent evaluation loops.
"""
import os
import sys

# Ensure local dir in path
sys.path.insert(0, '/usr/local/google/home/gilsonsoares/LingoCraft_ai')

from lingocraft_agent import LingoCraftOrchestrator
from curriculum_data import SPANISH_HACER_CURRICULUM
from audio_utils import generate_tts_audio, evaluate_spoken_accuracy

def test_lingocraft_system():
    print("==================================================")
    print("Starting LingoCraft AI System Tests...")
    print("==================================================")
    
    orchestrator = LingoCraftOrchestrator(api_key="")
    
    # 1. Test Curriculum Roadmap
    print("[1] Testing Curriculum Initializer Agent...")
    plan = orchestrator.initialize_curriculum(
        topic="Irregular Verbs: Verbo 'Hacer'",
        target_lang="Spanish",
        native_lang="English"
    )
    assert "tenses_roadmap" in plan, "Plan missing tenses_roadmap!"
    assert len(plan["tenses_roadmap"]) >= 5, "Expected at least 5 tenses in roadmap!"
    print(f"    Roadmap verified: {plan['tenses_roadmap']}")
    
    # 2. Test 5-Stage Flashcard Pack per Tense
    print("[2] Testing 5-Stage Flashcard Generator Agent...")
    for idx, tense in enumerate(plan["tenses_roadmap"][:3]):
        pack = orchestrator.load_tense_card_pack(
            topic="Irregular Verbs: Verbo 'Hacer'",
            tense_name=tense,
            tense_order=idx + 1,
            target_lang="Spanish",
            native_lang="English"
        )
        assert pack.card1_concept is not None, f"Missing Card 1 for {tense}"
        assert pack.card2_example is not None, f"Missing Card 2 for {tense}"
        assert pack.card3_pronunciation is not None, f"Missing Card 3 for {tense}"
        assert pack.card4_speech is not None, f"Missing Card 4 for {tense}"
        assert pack.card5_quiz is not None, f"Missing Card 5 for {tense}"
        print(f"    Tense '{tense}' 5-Card Pack loaded:")
        print(f"      - Card 1 Rule: {pack.card1_concept.title}")
        print(f"      - Card 2 Example: {pack.card2_example.target_sentence}")
        print(f"      - Card 3 Pronunciation: {pack.card3_pronunciation.phonetic_breakdown}")
        print(f"      - Card 4 Speech Target: {pack.card4_speech.target_phrase}")
        print(f"      - Card 5 Quiz: {pack.card5_quiz.sentence_prompt}")
        
    # 3. Test Audio Generation (Card 3)
    print("[3] Testing TTS Audio Generation (Card 3)... ")
    audio = generate_tts_audio("ha-CIEN-do", lang="es")
    assert len(audio) > 1000, f"Audio generation failed, byte length: {len(audio)}"
    print(f"    Native MP3 audio generated successfully ({len(audio)} bytes)!")
    
    # 4. Test Speech Validation (Card 4)
    print("[4] Testing Speech Validation Agent (Card 4)... ")
    speech_good = orchestrator.validate_speech(
        spoken_text="estoy haciendo un cafe",
        target_phrase="Estoy haciendo un café.",
        target_lang="Spanish",
        native_lang="English"
    )
    assert speech_good["accuracy_score"] >= 80, "High score expected for exact match!"
    print(f"    Speech match score: {speech_good['accuracy_score']}% ({speech_good['feedback_title']})")
    
    speech_bad = orchestrator.validate_speech(
        spoken_text="estoy asiendo algo",
        target_phrase="Estoy haciendo un café caliente.",
        target_lang="Spanish",
        native_lang="English"
    )
    assert speech_bad.get("requires_micro_practice") is True, "Expected micro practice for low score!"
    print(f"    Speech mispronunciation handled: {speech_bad['feedback_title']}")
    print(f"    Micro-practice: {speech_bad.get('micro_practice_drill')}")
    
    # 5. Test Conjugation Quiz (Card 5)
    print("[5] Testing Conjugation Quiz Evaluator Agent (Card 5)... ")
    quiz_data = SPANISH_HACER_CURRICULUM.cards_by_tense["Gerundio"].card5_quiz
    
    # Correct option
    correct_eval = orchestrator.evaluate_quiz(
        quiz_data=quiz_data,
        selected_option="haciendo",
        target_lang="Spanish",
        native_lang="English"
    )
    assert correct_eval["is_correct"] is True, "Expected correct evaluation!"
    print(f"    Correct answer praise: {correct_eval['headline']}")
    
    # Incorrect option with constructive feedback & micro-practice
    incorrect_eval = orchestrator.evaluate_quiz(
        quiz_data=quiz_data,
        selected_option="haces",
        target_lang="Spanish",
        native_lang="English"
    )
    assert incorrect_eval["is_correct"] is False, "Expected incorrect evaluation!"
    assert len(incorrect_eval["why_common_mistake"]) > 0, "Expected explanation of common mistake!"
    assert len(incorrect_eval["micro_practice_prompt"]) > 0, "Expected micro-practice prompt!"
    print(f"    Constructive feedback: {incorrect_eval['headline']}")
    print(f"    Why common: {incorrect_eval['why_common_mistake']}")
    print(f"    Micro-practice prompt: {incorrect_eval['micro_practice_prompt']}")
    
    # 6. Test Interactive Coach Chat
    print("[6] Testing Ask Coach LingoCraft...")
    coach_reply = orchestrator.ask_coach(
        question="Why do Spanish speakers say hace calor instead of es calor?",
        current_topic="Irregular Verbs: Verbo 'Hacer'",
        current_tense="Presente de Indicativo",
        target_lang="Spanish",
        native_lang="English"
    )
    assert len(coach_reply) > 20, "Coach reply was empty!"
    print(f"    Coach answer sample: {coach_reply[:120]}...")
    
    print("==================================================")
    print("ALL LINGOCRAFT AI AGENT TESTS PASSED SUCCESSFULLY!")
    print("==================================================")

if __name__ == '__main__':
    test_lingocraft_system()
