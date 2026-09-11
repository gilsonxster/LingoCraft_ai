"""
Persistent Session Manager for LingoCraft AI.
Stores study progress, active tenses, flashcard status, and coach conversations in SQLite
to allow students to pause their studies and seamlessly resume later.
"""

import json
import os
import sqlite3
import time
import uuid
from typing import Any, Dict, List, Optional

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DB_PATH = os.path.join(DB_DIR, "lingocraft_sessions.db")


def init_db(db_path: str = DB_PATH) -> None:
    """Initializes the SQLite database and creates the sessions table if needed."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS study_sessions (
                session_id TEXT PRIMARY KEY,
                topic TEXT NOT NULL,
                target_language TEXT NOT NULL,
                native_language TEXT NOT NULL,
                active_tense_index INTEGER NOT NULL DEFAULT 0,
                active_card_step INTEGER NOT NULL DEFAULT 1,
                completed_tenses_json TEXT NOT NULL DEFAULT '[]',
                completed_card_steps_json TEXT NOT NULL DEFAULT '[]',
                current_curriculum_json TEXT NOT NULL,
                chat_history_json TEXT NOT NULL DEFAULT '[]',
                needs_review_tenses_json TEXT NOT NULL DEFAULT '[]',
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            )
        """)
        cursor.execute("PRAGMA table_info(study_sessions)")
        cols = [c[1] for c in cursor.fetchall()]
        if "needs_review_tenses_json" not in cols:
            cursor.execute("ALTER TABLE study_sessions ADD COLUMN needs_review_tenses_json TEXT NOT NULL DEFAULT '[]'")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sessions_updated_at ON study_sessions(updated_at DESC)
        """)
        conn.commit()


def generate_session_id() -> str:
    """Generates a memorable and compact unique session code, e.g. lingo-a7c3e1."""
    return f"lingo-{uuid.uuid4().hex[:6]}"


def save_session(session_id: str, state_dict: Dict[str, Any], db_path: str = DB_PATH) -> bool:
    """Saves or updates the session snapshot in SQLite."""
    try:
        init_db(db_path)
        curriculum = state_dict.get("current_curriculum", {})
        topic = curriculum.get("topic", "General Language Study")
        target_lang = curriculum.get("target_language", "Spanish")
        native_lang = curriculum.get("native_language", "English")
        active_tense_idx = int(state_dict.get("active_tense_index", 0))
        active_card_step = int(state_dict.get("active_card_step", 1))

        completed_tenses = list(state_dict.get("completed_tenses", []))
        completed_card_steps = list(state_dict.get("completed_card_steps", []))
        needs_review_tenses = list(state_dict.get("needs_review_tenses", []))
        chat_history = state_dict.get("chat_history", [])

        now = time.time()

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO study_sessions (
                    session_id, topic, target_language, native_language,
                    active_tense_index, active_card_step,
                    completed_tenses_json, completed_card_steps_json,
                    current_curriculum_json, chat_history_json,
                    needs_review_tenses_json,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET
                    topic = excluded.topic,
                    target_language = excluded.target_language,
                    native_language = excluded.native_language,
                    active_tense_index = excluded.active_tense_index,
                    active_card_step = excluded.active_card_step,
                    completed_tenses_json = excluded.completed_tenses_json,
                    completed_card_steps_json = excluded.completed_card_steps_json,
                    current_curriculum_json = excluded.current_curriculum_json,
                    chat_history_json = excluded.chat_history_json,
                    needs_review_tenses_json = excluded.needs_review_tenses_json,
                    updated_at = excluded.updated_at
            """, (
                session_id,
                topic,
                target_lang,
                native_lang,
                active_tense_idx,
                active_card_step,
                json.dumps(completed_tenses),
                json.dumps(completed_card_steps),
                json.dumps(curriculum),
                json.dumps(chat_history),
                json.dumps(needs_review_tenses),
                now,
                now
            ))
            conn.commit()
        return True
    except Exception as e:
        print(f"Error saving session {session_id}: {e}")
        return False


def load_session(session_id: str, db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    """Loads a study session by session_id from SQLite. Returns None if not found."""
    try:
        init_db(db_path)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    session_id, topic, target_language, native_language,
                    active_tense_index, active_card_step,
                    completed_tenses_json, completed_card_steps_json,
                    current_curriculum_json, chat_history_json,
                    needs_review_tenses_json,
                    created_at, updated_at
                FROM study_sessions
                WHERE session_id = ?
            """, (session_id,))
            row = cursor.fetchone()
            if not row:
                return None

            needs_rev = set()
            if len(row) > 10 and row[10]:
                try:
                    needs_rev = set(json.loads(row[10]))
                except Exception:
                    needs_rev = set()

            return {
                "session_id": row[0],
                "topic": row[1],
                "target_language": row[2],
                "native_language": row[3],
                "active_tense_index": row[4],
                "active_card_step": row[5],
                "completed_tenses": set(json.loads(row[6])),
                "completed_card_steps": set(json.loads(row[7])),
                "current_curriculum": json.loads(row[8]),
                "chat_history": json.loads(row[9]),
                "needs_review_tenses": needs_rev,
                "created_at": row[11],
                "updated_at": row[12],
            }
    except Exception as e:
        print(f"Error loading session {session_id}: {e}")
        return None


def list_recent_sessions(limit: int = 5, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Lists the most recently updated study sessions."""
    try:
        init_db(db_path)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    session_id, topic, target_language, native_language,
                    active_tense_index, active_card_step,
                    completed_tenses_json, current_curriculum_json,
                    needs_review_tenses_json,
                    updated_at
                FROM study_sessions
                ORDER BY updated_at DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            results = []
            for r in rows:
                try:
                    curriculum = json.loads(r[7])
                    roadmap = curriculum.get("tenses_roadmap", [])
                    total_tenses = len(roadmap)
                    completed_tenses = json.loads(r[6])
                    needs_review = json.loads(r[8]) if len(r) > 8 and r[8] else []
                except Exception:
                    total_tenses = 5
                    completed_tenses = []
                    needs_review = []

                results.append({
                    "session_id": r[0],
                    "topic": r[1],
                    "target_language": r[2],
                    "native_language": r[3],
                    "active_tense_index": r[4],
                    "active_card_step": r[5],
                    "completed_count": len(completed_tenses),
                    "needs_review_count": len(needs_review),
                    "total_tenses": total_tenses,
                    "updated_at": r[9]
                })
            return results
    except Exception as e:
        print(f"Error listing recent sessions: {e}")
        return []



def delete_session(session_id: str, db_path: str = DB_PATH) -> bool:
    """Deletes a session from the SQLite database."""
    try:
        init_db(db_path)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM study_sessions WHERE session_id = ?", (session_id,))
            conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting session {session_id}: {e}")
        return False
