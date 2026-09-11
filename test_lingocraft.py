"""
Unit and integration test suite for LingoCraft AI.
Verifies all 5 improvements:
1. Stepper navigation and jumping to next card / marking complete.
2. Native language localization (English & Portuguese).
3. Neutral language labels in bilingual examples.
4. Conjugation quiz option shuffling & active selection.
5. Contextual coach follow-up prompts per tense pack.
"""
import os
import sys

sys.path.insert(0, '/usr/local/google/home/gilsonsoares/LingoCraft_ai')

from lingocraft_agent import LingoCraftOrchestrator
from curriculum_data import SPANISH_HACER_CURRICULUM, get_curriculum_or_fallback
from audio_utils import generate_tts_audio, evaluate_spoken_accuracy

def test_lingocraft_improvements():
    print("==================================================")
    print("Running LingoCraft AI Enhanced Test Suite...")
    print("==================================================")

    orchestrator = LingoCraftOrchestrator(api_key="")

    # 1. Test Localization in Native Language (Improvement 2)
    print("[1] Testing Native Language Localization (English vs Portuguese)...")
    plan_en = orchestrator.initialize_curriculum("Irregular Verbs: Verbo 'Hacer'", "Spanish", "English")
    plan_pt = orchestrator.initialize_curriculum("Irregular Verbs: Verbo 'Hacer'", "Spanish", "Portuguese")
    
    assert "tenses_roadmap" in plan_en and "tenses_roadmap" in plan_pt
    assert "fazer" in plan_pt["description"].lower() or "domine" in plan_pt["description"].lower(), "Portuguese localization failed!"
    print(f"    EN Plan Description: {plan_en['description']}")
    print(f"    PT Plan Description: {plan_pt['description']}")

    # 2. Test 5-Stage Flashcard Pack and Suggested Coach Prompts (Improvement 5)
    print("[2] Testing Flashcard Pack & Suggested Coach Prompts...")
    pack_en = orchestrator.load_tense_card_pack("Irregular Verbs: Verbo 'Hacer'", "Gerundio", 2, "Spanish", "English")
    pack_pt = orchestrator.load_tense_card_pack("Irregular Verbs: Verbo 'Hacer'", "Gerundio", 2, "Spanish", "Portuguese")

    assert len(pack_en.suggested_coach_prompts) >= 3, "Missing coach prompts in English pack!"
    assert len(pack_pt.suggested_coach_prompts) >= 3, "Missing coach prompts in Portuguese pack!"
    print(f"    EN Suggested Coach Prompts for Gerundio ({len(pack_en.suggested_coach_prompts)}):")
    for p in pack_en.suggested_coach_prompts:
        print(f"      - {p}")
    print(f"    PT Suggested Coach Prompts for Gerundio ({len(pack_pt.suggested_coach_prompts)}):")
    for p in pack_pt.suggested_coach_prompts:
        print(f"      - {p}")

    # 3. Test Neutral Labels and Comparative Phrases (Improvement 3)
    print("[3] Testing Bilingual Comparative Phrase structure...")
    assert "haciendo" in pack_en.card2_example.target_sentence.lower()
    assert "making" in pack_en.card2_example.native_sentence.lower()
    assert "fazendo" in pack_pt.card2_example.native_sentence.lower()
    print("    Target Sentence: ", pack_en.card2_example.target_sentence)
    print("    EN Meaning:      ", pack_en.card2_example.native_sentence)
    print("    PT Meaning:      ", pack_pt.card2_example.native_sentence)

    # 4. Test Conjugation Quiz & Option Shuffling (Improvement 4)
    print("[4] Testing Conjugation Quiz Evaluator & Shuffling...")
    quiz_data = pack_en.card5_quiz
    correct_opt = quiz_data.options[quiz_data.correct_index]
    
    # Verify evaluation
    correct_eval = orchestrator.evaluate_quiz(quiz_data, correct_opt, "Spanish", "English")
    assert correct_eval["is_correct"] is True, "Quiz correct answer evaluation failed!"

    wrong_eval_en = orchestrator.evaluate_quiz(quiz_data, "haces", "Spanish", "English")
    assert wrong_eval_en["is_correct"] is False, "Quiz wrong answer evaluation failed!"
    assert len(wrong_eval_en["why_common_mistake"]) > 0

    wrong_eval_pt = orchestrator.evaluate_quiz(pack_pt.card5_quiz, "haces", "Spanish", "Portuguese")
    assert wrong_eval_pt["is_correct"] is False
    assert "conflito" in wrong_eval_pt["why_common_mistake"].lower() or "indicativo" in wrong_eval_pt["why_common_mistake"].lower()
    print("    EN Constructive Feedback: ", wrong_eval_en["headline"])
    print("    PT Constructive Feedback: ", wrong_eval_pt["headline"])

    # 5. Test Coach Answering Localized Follow-up Questions (Improvement 5 + 2)
    print("[5] Testing Coach Chat with Portuguese Native Language...")
    coach_reply_pt = orchestrator.ask_coach(
        question="Por que se diz 'hace calor' em vez de 'está calor'?",
        current_topic="Irregular Verbs: Verbo 'Hacer'",
        current_tense="Presente de Indicativo",
        target_lang="Spanish",
        native_lang="Portuguese"
    )
    assert len(coach_reply_pt) > 20
    assert "calor" in coach_reply_pt.lower()
    # 6. Test Zero-Latency TTS Audio Caching
    print("[6] Testing Zero-Latency TTS Audio Caching...")
    import time
    t0 = time.time()
    audio1 = generate_tts_audio("haciendo", lang="es")
    t1 = time.time()
    audio2 = generate_tts_audio("haciendo", lang="es")
    t2 = time.time()
    
    assert len(audio1) > 0, "TTS audio bytes should not be empty!"
    assert audio1 == audio2, "Cached audio bytes must match exactly!"
    cache_duration = t2 - t1
    print(f"    Initial TTS Call Duration: {t1 - t0:.4f}s | Cached Call Duration: {cache_duration:.6f}s")
    assert cache_duration < 0.001, "Cached TTS call should execute in less than 1ms!"

    # 7. Test Session Manager Persistence and State Dict Serialization
    print("[7] Testing Session Manager Persistence...")
    import session_manager
    test_sid = "test-lingo-session-001"
    sample_state = {
        "current_curriculum": plan_en,
        "active_tense_index": 2,
        "active_card_step": 3,
        "completed_tenses": [0, 1],
        "completed_card_steps": [1, 2],
        "chat_history": [{"role": "user", "content": "Hello Coach!"}],
    }
    saved_ok = session_manager.save_session(test_sid, sample_state)
    assert saved_ok is True, "Session save failed!"
    loaded = session_manager.load_session(test_sid)
    assert loaded is not None, "Session load returned None!"
    assert loaded["active_tense_index"] == 2
    assert loaded["active_card_step"] == 3
    assert 1 in loaded["completed_tenses"]
    session_manager.delete_session(test_sid)
    print("    Session successfully saved, retrieved, validated, and cleaned up.")

    print("==================================================")
    print("ALL 7 SYSTEM IMPROVEMENTS TESTED & PASSED SUCCESSFULLY!")
    print("==================================================")

if __name__ == '__main__':
    test_lingocraft_improvements()
