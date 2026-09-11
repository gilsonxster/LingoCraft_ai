import io
import re
import difflib
import functools
from gtts import gTTS
import speech_recognition as sr

LANG_CODE_MAP = {
    'spanish': 'es',
    'español': 'es',
    'french': 'fr',
    'français': 'fr',
    'german': 'de',
    'deutsch': 'de',
    'italian': 'it',
    'italiano': 'it',
    'portuguese': 'pt',
    'português': 'pt',
    'japanese': 'ja',
    'nihongo': 'ja',
    'english': 'en',
    'chinese': 'zh-cn',
    'russian': 'ru',
    'arabic': 'ar',
}

def resolve_lang_code(lang_name: str) -> str:
    cleaned = lang_name.strip().lower()
    for name, code in LANG_CODE_MAP.items():
        if name in cleaned:
            return code
    if len(cleaned) == 2:
        return cleaned
    return 'es'

import html
import unicodedata

def strip_markdown(text: str) -> str:
    """Strips markdown formatting characters like bold (** or __), italics (* or _), backticks, etc."""
    if not text:
        return ""
    cleaned = re.sub(r'[*_~`]', '', text)
    return ' '.join(cleaned.split())

def strip_accents(text: str) -> str:
    """Removes diacritical marks/accents for robust phonetic and lexical matching."""
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

def clean_word_for_matching(word: str) -> str:
    """Normalizes a word by removing accents, non-alphanumeric chars, and lowering case."""
    return strip_accents(''.join(c for c in word.lower() if c.isalnum()))

@functools.lru_cache(maxsize=256)
def generate_tts_audio(text: str, lang: str = 'es', slow: bool = False) -> bytes:
    """Generates zero-latency cached TTS audio bytes with normal (1.0x) or practice (0.75x) speeds."""
    code = resolve_lang_code(lang)
    try:
        tts = gTTS(text=text, lang=code, slow=slow)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.getvalue()
    except Exception:
        try:
            tts = gTTS(text=text, lang='en', slow=slow)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp.getvalue()
        except Exception:
            return b''

def transcribe_audio_bytes(audio_bytes: bytes, lang: str = 'es') -> str:
    if not audio_bytes:
        return ''
    code = resolve_lang_code(lang)
    recognizer = sr.Recognizer()
    try:
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language=code)
            return text.strip()
    except Exception:
        return ''

def generate_word_diff(target_phrase: str, spoken_text: str):
    """
    Compares target words with spoken words to identify matches, mispronunciations, and omissions.
    Returns (diff_results, extra_words).
    """
    clean_target = strip_markdown(target_phrase)
    clean_spoken = strip_markdown(spoken_text) if spoken_text else ""

    t_words = clean_target.split()
    s_words = clean_spoken.split() if clean_spoken else []

    norm_t = [clean_word_for_matching(w) for w in t_words]
    norm_s = [clean_word_for_matching(w) for w in s_words]

    matcher = difflib.SequenceMatcher(None, norm_t, norm_s)
    diff_results = []
    extra_words = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            for idx in range(i1, i2):
                j_idx = j1 + (idx - i1)
                diff_results.append({
                    'target': t_words[idx],
                    'status': 'match',
                    'heard': s_words[j_idx] if j_idx < len(s_words) else None,
                    'similarity': 1.0
                })
        elif tag == 'replace':
            t_slice = t_words[i1:i2]
            s_slice = s_words[j1:j2]
            for offset in range(max(len(t_slice), len(s_slice))):
                if offset < len(t_slice) and offset < len(s_slice):
                    tw = t_slice[offset]
                    sw = s_slice[offset]
                    ctw = clean_word_for_matching(tw)
                    csw = clean_word_for_matching(sw)
                    sim = difflib.SequenceMatcher(None, ctw, csw).ratio()
                    if ctw == csw or sim >= 0.88:
                        status = 'match'
                    elif sim >= 0.70:
                        status = 'near_match'
                    else:
                        status = 'miss'
                    diff_results.append({
                        'target': tw,
                        'status': status,
                        'heard': sw,
                        'similarity': sim
                    })
                elif offset < len(t_slice):
                    diff_results.append({
                        'target': t_slice[offset],
                        'status': 'omitted',
                        'heard': None,
                        'similarity': 0.0
                    })
                elif offset < len(s_slice):
                    extra_words.append(s_slice[offset])
        elif tag == 'delete':
            for idx in range(i1, i2):
                diff_results.append({
                    'target': t_words[idx],
                    'status': 'omitted',
                    'heard': None,
                    'similarity': 0.0
                })
        elif tag == 'insert':
            for idx in range(j1, j2):
                extra_words.append(s_words[idx])

    return diff_results, extra_words

def generate_word_diff_html(target_phrase: str, spoken_text: str) -> str:
    """Renders accessible Google Material 3 HTML chips showing word-level accuracy."""
    clean_target = strip_markdown(target_phrase)
    clean_spoken = strip_markdown(spoken_text) if spoken_text else ""
    diff_results, extra_words = generate_word_diff(clean_target, clean_spoken)
    chips_html = []

    for item in diff_results:
        t_word = html.escape(item['target'])
        status = item['status']
        heard = html.escape(item.get('heard') or '')

        if status == 'match':
            chips_html.append(
                f'<span class="diff-chip diff-match" title="Matched accurately: \'{t_word}\'">'
                f'<strong>{t_word}</strong> <span class="diff-icon">✓</span></span>'
            )
        elif status == 'near_match':
            chips_html.append(
                f'<span class="diff-chip diff-near" title="Close pronunciation: heard \'{heard}\'">'
                f'<strong>{t_word}</strong> <span class="diff-heard">({heard})</span> <span class="diff-icon">≈</span></span>'
            )
        elif status == 'miss':
            chips_html.append(
                f'<span class="diff-chip diff-miss" title="Mispronounced: heard \'{heard}\' instead of \'{t_word}\'">'
                f'<strong>{t_word}</strong> <span class="diff-heard">({heard})</span> <span class="diff-icon">⚠️</span></span>'
            )
        elif status == 'omitted':
            chips_html.append(
                f'<span class="diff-chip diff-omitted" title="Word omitted in speech">'
                f'<strong>{t_word}</strong> <span class="diff-icon">❌</span></span>'
            )

    extra_html = ""
    if extra_words:
        esc_extra = html.escape(', '.join(extra_words))
        extra_html = f'<div style="font-size: 0.8125rem; color: #B06000; margin-top: 8px;">➕ <em>Extra words spoken: {esc_extra}</em></div>'

    esc_spoken = html.escape(clean_spoken) if clean_spoken else "<em>(No speech detected)</em>"
    chips_str = " ".join(chips_html)

    # Note: Do not indent lines with 4+ spaces or insert blank lines inside this block,
    # as CommonMark/Markdown parsers in Streamlit will interpret indented lines as code blocks.
    html_parts = [
        '<div class="diff-breakdown-card">',
        '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">',
        '<span style="font-weight: 600; font-size: 0.8125rem; color: var(--gmat-sys-color-text-secondary); text-transform: uppercase; letter-spacing: 0.03rem;">🔍 Word-by-word pronunciation accuracy</span>',
        '<span style="font-size: 0.75rem; color: var(--gmat-sys-color-text-secondary);">✓ Match &nbsp; ≈ Near &nbsp; ⚠️ Mispronounced &nbsp; ❌ Omitted</span>',
        '</div>',
        f'<div style="display: flex; flex-wrap: wrap; gap: 6px; align-items: center; line-height: 1.8;">{chips_str}</div>',
    ]
    if extra_html:
        html_parts.append(extra_html)
    html_parts.extend([
        f'<div style="font-size: 0.8125rem; color: var(--gmat-sys-color-text-secondary); margin-top: 10px; padding-top: 8px; border-top: 1px solid var(--gmat-sys-color-outline);"><strong>Speech recognized:</strong> "{esc_spoken}"</div>',
        '</div>'
    ])
    return "\n".join(html_parts)

def evaluate_spoken_accuracy(spoken_text: str, target_phrase: str) -> dict:
    clean_target_phrase = strip_markdown(target_phrase)
    clean_spoken_text = strip_markdown(spoken_text) if spoken_text else ""

    clean_spoken = ''.join(c for c in clean_spoken_text.lower() if c.isalnum() or c.isspace()).strip()
    clean_target = ''.join(c for c in clean_target_phrase.lower() if c.isalnum() or c.isspace()).strip()

    diff_results, extra_words = generate_word_diff(clean_target_phrase, clean_spoken_text)
    diff_html = generate_word_diff_html(clean_target_phrase, clean_spoken_text)

    if not clean_spoken:
        return {
            'score': 0,
            'status': 'empty',
            'similarity': 0.0,
            'feedback': 'No speech detected. Please try recording again or type what you said.',
            'word_diff': diff_results,
            'extra_words': extra_words,
            'diff_html': diff_html,
        }

    matcher = difflib.SequenceMatcher(None, clean_spoken, clean_target)
    similarity = matcher.ratio()
    score = int(similarity * 100)

    if score >= 85:
        status = 'excellent'
    elif score >= 65:
        status = 'good'
    else:
        status = 'needs_practice'

    return {
        'score': score,
        'similarity': similarity,
        'status': status,
        'spoken': clean_spoken_text,
        'target': clean_target_phrase,
        'word_diff': diff_results,
        'extra_words': extra_words,
        'diff_html': diff_html,
    }


