import io
import difflib
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

def generate_tts_audio(text: str, lang: str = 'es') -> bytes:
    code = resolve_lang_code(lang)
    try:
        tts = gTTS(text=text, lang=code, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.getvalue()
    except Exception:
        try:
            tts = gTTS(text=text, lang='en', slow=False)
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

def evaluate_spoken_accuracy(spoken_text: str, target_phrase: str) -> dict:
    clean_spoken = ''.join(c for c in spoken_text.lower() if c.isalnum() or c.isspace()).strip()
    clean_target = ''.join(c for c in target_phrase.lower() if c.isalnum() or c.isspace()).strip()

    if not clean_spoken:
        return {
            'score': 0,
            'status': 'empty',
            'similarity': 0.0,
            'feedback': 'No speech detected. Please try recording again or type what you said.'
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
        'spoken': spoken_text,
        'target': target_phrase
    }
