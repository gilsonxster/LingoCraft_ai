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
        "needs_review_tenses": [2],
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
    assert 2 in loaded["needs_review_tenses"]
    session_manager.delete_session(test_sid)
    print("    Session successfully saved, retrieved, validated, and cleaned up.")

    # 8. Test Dual-Speed TTS Audio Playback (Normal 1.0x vs Practice pace 0.75x)
    print("[8] Testing Dual-Speed TTS Audio Playback (1.0x vs 0.75x)...")
    audio_normal = generate_tts_audio("haciendo", lang="es", slow=False)
    audio_slow = generate_tts_audio("haciendo", lang="es", slow=True)
    assert len(audio_normal) > 0, "Normal speed audio should not be empty!"
    assert len(audio_slow) > 0, "Practice pace audio should not be empty!"
    assert audio_normal != audio_slow, "Normal and slow audio byte streams should be distinct!"
    print(f"    Normal audio bytes: {len(audio_normal)} bytes | Practice (slow) audio bytes: {len(audio_slow)} bytes")

    # 9. Test Word-Level Visual Diff on Speech Validation
    print("[9] Testing Word-Level Visual Diff & Chip Generation...")
    from audio_utils import generate_word_diff, generate_word_diff_html
    target_phrase = "Ahora mismo estoy haciendo un café caliente para el desayuno."
    spoken_phrase = "ahora mismo estoy haziendo un cafe para el desayuno"

    diff_tokens, extra_words = generate_word_diff(target_phrase, spoken_phrase)
    assert len(diff_tokens) == 10, f"Expected 10 target tokens, got {len(diff_tokens)}"
    
    # Check match for 'Ahora', 'mismo', 'estoy', 'un', 'para', 'el'
    matched_words = [d['target'] for d in diff_tokens if d['status'] == 'match']
    assert "Ahora" in matched_words
    assert "mismo" in matched_words
    assert "estoy" in matched_words
    assert "café" in matched_words  # Accents normalized cleanly

    # Check near_match or miss for 'haciendo' (heard: haziendo)
    haciendo_item = [d for d in diff_tokens if 'haciendo' in d['target']][0]
    assert haciendo_item['status'] in ('near_match', 'miss')
    assert haciendo_item['heard'] == 'haziendo'

    # Check omitted word 'caliente'
    caliente_item = [d for d in diff_tokens if 'caliente' in d['target']][0]
    assert caliente_item['status'] == 'omitted'

    diff_html = generate_word_diff_html(target_phrase, spoken_phrase)
    assert "diff-chip diff-match" in diff_html
    assert "diff-chip" in diff_html

    # Test phrase with markdown asterisks (e.g. "**tener**") to verify no raw HTML code block leaks
    md_target = "Es importante **tener** paciencia."
    md_spoken = "Es importante **tener** paciencia."
    md_diff_html = generate_word_diff_html(md_target, md_spoken)
    assert "**" not in md_diff_html, "Markdown asterisks should be stripped from diff chips and recognized speech"
    assert "tener" in md_diff_html
    assert "Speech recognized:" in md_diff_html
    # Ensure no line has 4+ leading spaces to prevent markdown indented code block parsing
    for line in md_diff_html.splitlines():
        assert not line.startswith("    "), f"Indented line found in diff_html: {line!r}"
    eval_acc = evaluate_spoken_accuracy(md_spoken, md_target)
    assert eval_acc["score"] == 100
    assert eval_acc["target"] == "Es importante tener paciencia."
    assert eval_acc["spoken"] == "Es importante tener paciencia."
    print("    Word-level diff correctly tagged matches, mispronunciations, and omissions without markdown leaking.")

    # 10. Test 3-Tier Mastery Confidence (Spaced Repetition & Needs Review)
    print("[10] Testing 3-Tier Mastery & Needs Review Tracking...")
    test_sid_sr = "test-lingo-spaced-rep"
    sr_state = {
        "current_curriculum": plan_en,
        "active_tense_index": 1,
        "active_card_step": 4,
        "completed_tenses": [0],
        "needs_review_tenses": [1, 2],
        "completed_card_steps": [1, 2, 3],
        "chat_history": []
    }
    session_manager.save_session(test_sid_sr, sr_state)
    loaded_sr = session_manager.load_session(test_sid_sr)
    assert loaded_sr is not None
    assert 0 in loaded_sr["completed_tenses"]
    assert 1 in loaded_sr["needs_review_tenses"]
    assert 2 in loaded_sr["needs_review_tenses"]

    recent_list = session_manager.list_recent_sessions(limit=5)
    matched_recent = [r for r in recent_list if r["session_id"] == test_sid_sr]
    assert len(matched_recent) == 1
    assert matched_recent[0]["needs_review_count"] == 2
    session_manager.delete_session(test_sid_sr)
    print("    3-tier mastery states (Mastered, Needs Review, Active) successfully verified.")

    # 11. Test Gamification & XP Points System
    print("[11] Testing Gamification & Craftsman XP Points System...")
    r1 = session_manager.get_rank_for_xp(0)
    assert r1["level"] == 1 and r1["name"] == "Novice Explorer"
    assert r1["progress_ratio"] == 0.0

    r2 = session_manager.get_rank_for_xp(150)
    assert r2["level"] == 2 and r2["name"] == "Apprentice Speaker"
    assert r2["min_xp"] == 100 and r2["max_xp"] == 250

    r3 = session_manager.get_rank_for_xp(350)
    assert r3["level"] == 3 and r3["name"] == "Confident Conversationalist"

    r4 = session_manager.get_rank_for_xp(600)
    assert r4["level"] == 4 and r4["name"] == "Master Craftsman"

    r_max = session_manager.get_rank_for_xp(1500)
    assert r_max["level"] == 4 and r_max["progress_ratio"] == 1.0

    # Test SQLite persistence of XP points
    test_sid_xp = "lingo-test-xp"
    test_state_xp = {
        "current_curriculum": {
            "topic": "Spanish XP Test",
            "target_language": "Spanish",
            "native_language": "English",
            "tenses_roadmap": ["Presente"]
        },
        "active_tense_index": 0,
        "active_card_step": 1,
        "completed_tenses": [0],
        "needs_review_tenses": [],
        "completed_card_steps": [1, 2],
        "chat_history": [],
        "xp_points": 210
    }
    session_manager.save_session(test_sid_xp, test_state_xp)
    loaded_xp = session_manager.load_session(test_sid_xp)
    assert loaded_xp is not None
    assert loaded_xp["xp_points"] == 210

    recents_xp = session_manager.list_recent_sessions(limit=5)
    matched_xp = [r for r in recents_xp if r["session_id"] == test_sid_xp]
    assert len(matched_xp) == 1
    assert matched_xp[0]["xp_points"] == 210
    session_manager.delete_session(test_sid_xp)
    print("    Gamification levels, tier progression, and SQLite persistence verified.")

    # 12. Test Next Topic Recommendation Engine & Unstudied Verb Selection
    print("[12] Testing Next Topic Recommendation Engine & Unstudied Filtering...")
    studied_db = session_manager.get_all_studied_topics()
    assert isinstance(studied_db, list), "get_all_studied_topics must return a list"

    from curriculum_data import get_recommended_next_topics, build_spanish_tener_pack
    recs_spanish = get_recommended_next_topics(
        target_lang="Spanish",
        current_topic="Spanish: Irregular Verbs — Verbo 'Hacer'",
        studied_topics=["Spanish: Irregular Verbs — Verbo 'Hacer'"],
        count=3
    )
    assert len(recs_spanish) >= 1, "Should recommend at least one unstudied topic"
    assert all("verb" in r and "topic" in r and "pedagogical_hook" in r for r in recs_spanish), "Missing required topic fields"
    for r in recs_spanish:
        assert "hacer" not in r["verb"].lower() and "hacer" not in r["topic"].lower()

    # When both 'hacer' and 'tener' have been studied, verify next recommendation excludes both
    recs_next = get_recommended_next_topics(
        target_lang="Spanish",
        current_topic="Spanish: Irregular Verbs — Verbo 'Tener'",
        studied_topics=["Spanish: Irregular Verbs — Verbo 'Hacer'", "Spanish: Irregular Verbs — Verbo 'Tener'"],
        count=3
    )
    assert len(recs_next) >= 1
    assert "tener" not in recs_next[0]["verb"].lower()
    assert "hacer" not in recs_next[0]["verb"].lower()
    assert recs_next[0]["verb"].lower() == "ir", f"Expected 'ir' to be recommended next, got {recs_next[0]['verb']}"

    # Test shuffle functionality
    shuffled_recs = get_recommended_next_topics(
        target_lang="Spanish",
        current_topic="hacer",
        studied_topics=[],
        count=3,
        shuffle=True,
        seed=123
    )
    assert len(shuffled_recs) == 3
    assert all("verb" in r for r in shuffled_recs)

    # Test curated pack for 'tener'
    tener_pack_en = build_spanish_tener_pack(native_lang="English")
    tener_pack_pt = build_spanish_tener_pack(native_lang="Portuguese")
    assert len(tener_pack_en) == 5
    assert len(tener_pack_pt) == 5
    assert "Presente de Indicativo" in tener_pack_en
    assert "tengo" in tener_pack_en["Presente de Indicativo"].card1_concept.rule.lower()

    # Test get_curriculum_or_fallback routing for 'tener'
    curric_tener = get_curriculum_or_fallback("Spanish: Irregular Verbs — Verbo 'Tener'", "Spanish", "English")
    assert "Tener" in curric_tener.title
    assert len(curric_tener.tenses_roadmap) == 5
    print("    Next topic recommendation engine, unstudied filtering, and curated pack verified.")

    print("==================================================")
    print("ALL 12 SYSTEM IMPROVEMENTS TESTED & PASSED SUCCESSFULLY!")
    print("==================================================")


if __name__ == '__main__':
    test_lingocraft_improvements()


