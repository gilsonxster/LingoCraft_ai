"""
Curriculum data models and pre-curated courses for LingoCraft AI.
Provides instant offline fallback and high-quality baseline curricula.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

@dataclass
class Card1Concept:
    title: str
    rule: str
    usage_context: str
    triggers: List[str]

@dataclass
class Card2Example:
    target_sentence: str
    native_sentence: str
    breakdown: str

@dataclass
class Card3Pronunciation:
    word: str
    phonetic_breakdown: str
    stressed_syllables: str
    audio_text: str
    phonetic_tips: str

@dataclass
class Card4Speech:
    target_phrase: str
    expected_phonetics: str
    key_focus_sounds: str
    practice_tip: str

@dataclass
class Card5Quiz:
    sentence_prompt: str
    options: List[str]
    correct_index: int
    correct_explanation: str
    distractor_explanations: Dict[str, str]
    micro_practice_prompt: str
    micro_practice_options: List[str]
    micro_practice_correct_index: int
    micro_practice_explanation: str

@dataclass
class TenseFlashcardPack:
    tense_name: str
    tense_order: int
    card1_concept: Card1Concept
    card2_example: Card2Example
    card3_pronunciation: Card3Pronunciation
    card4_speech: Card4Speech
    card5_quiz: Card5Quiz

@dataclass
class CurriculumCourse:
    topic_id: str
    title: str
    target_language: str
    target_language_code: str
    native_language: str
    native_language_code: str
    description: str
    tenses_roadmap: List[str]
    cards_by_tense: Dict[str, TenseFlashcardPack]

# Pre-curated Spanish Course: Irregular Verbs: Verbo "Hacer"
SPANISH_HACER_CURRICULUM = CurriculumCourse(
    topic_id='spanish_hacer',
    title='Irregular Verbs: Verbo "Hacer"',
    target_language='Spanish',
    target_language_code='es',
    native_language='English',
    native_language_code='en',
    description="Master the essential Spanish irregular verb 'hacer' (to do / to make) across all core grammatical tenses.",
    tenses_roadmap=['Infinitivo', 'Gerundio', 'Participio', 'Presente de Indicativo', 'Pretérito Indefinido'],
    cards_by_tense={
        'Infinitivo': TenseFlashcardPack(
            tense_name='Infinitivo',
            tense_order=1,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — El Infinitivo (Hacer)',
                rule='The **infinitivo** is the unconjugated base dictionary form of the verb ending in **-er**. In Spanish, it acts as a verbal noun and is used directly after prepositions, modal auxiliary verbs, or verbal periphrases.',
                usage_context='Used whenever an action is described in the abstract or directly governed by another conjugated verb (e.g., *querer hacer*, *tener que hacer*).',
                triggers=['tener que + infinitivo', 'querer + infinitivo', 'antes de', 'después de', 'para']
            ),
            card2_example=Card2Example(
                target_sentence='Tengo que **hacer** la tarea antes de salir con mis amigos.',
                native_sentence='I have to **do** the homework before going out with my friends.',
                breakdown='Notice that **hacer** remains unconjugated in the infinitive because it immediately follows the modal obligation structure **tengo que**.'
            ),
            card3_pronunciation=Card3Pronunciation(
                word='hacer',
                phonetic_breakdown='ha-**CER**',
                stressed_syllables='**CER**',
                audio_text='Tengo que hacer la tarea antes de salir.',
                phonetic_tips="In Spanish, the initial **H** is always completely silent. Words ending in consonants other than -N or -S naturally stress the **final syllable** (oxytone / palabra aguda)."
            ),
            card4_speech=Card4Speech(
                target_phrase='Tengo que hacer la tarea.',
                expected_phonetics='[ˈteŋ.ɡo ke aˈseɾ la taˈɾe.a]',
                key_focus_sounds="Silent 'h' in 'hacer', soft tap 'r' at the end.",
                practice_tip="Start directly on the vowel sound 'ah' when saying **hacer**; never aspirate like English 'hat'."
            ),
            card5_quiz=Card5Quiz(
                sentence_prompt='Ella quiere _____ una pregunta importante al profesor.',
                options=['hacer', 'hace', 'haciendo', 'hizo'],
                correct_index=0,
                correct_explanation='¡Excelente! After modal verbs expressing desire like **quiere** (wants), Spanish always requires the base **infinitivo** (*hacer*).',
                distractor_explanations={
                    'hace': "**hace** is conjugated 3rd person singular present indicative. We cannot stack two conjugated verbs back-to-back without a conjunction; 'quiere' already carries the conjugation.",
                    'haciendo': "**haciendo** is the continuous gerund. It would mean 'wants doing', which is grammatically ungrammatical after 'querer'.",
                    'hizo': "**hizo** is the simple past (pretérito). It cannot function as an infinitive complement."
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: 'Voy a _____ café para todos.'",
                micro_practice_options=['hacer', 'hago', 'hizo', 'hacemos'],
                micro_practice_correct_index=0,
                micro_practice_explanation="Correct! 'Ir a' + **infinitivo** (*hacer*) expresses immediate future intentions."
            )
        ),
        'Gerundio': TenseFlashcardPack(
            tense_name='Gerundio',
            tense_order=2,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — El Gerundio (Haciendo)',
                rule='The **gerundio** is the continuous/progressive participle. For regular **-er** verbs, the suffix is **-iendo**. The stem **hac-** takes **-iendo** to form **haciendo** (doing / making).',
                usage_context='Used with the auxiliary verb **estar** (*estar + gerundio*) to describe actions that are currently in progress right at the moment of speech.',
                triggers=['estar + gerundio', 'ahora mismo', 'en este momento', 'actualmente']
            ),
            card2_example=Card2Example(
                target_sentence='Ahora mismo estoy **haciendo** un café caliente para el desayuno.',
                native_sentence='Right now I am **making** a hot coffee for breakfast.',
                breakdown='The structure **estoy haciendo** pairs the auxiliary **estar** with the gerund **haciendo** to indicate the action is actively taking place.'
            ),
            card3_pronunciation=Card3Pronunciation(
                word='haciendo',
                phonetic_breakdown='ha-**CIEN**-do',
                stressed_syllables='**CIEN**',
                audio_text='Ahora mismo estoy haciendo un café caliente.',
                phonetic_tips="Stress is firmly on the penultimate syllable **CIEN**. The 'ie' is a rising diphthong that glides smoothly together into one syllable."
            ),
            card4_speech=Card4Speech(
                target_phrase='Estoy haciendo un café.',
                expected_phonetics='[esˈtoj aˈsjen.do uŋ kaˈfe]',
                key_focus_sounds="Blend the diphthong 'ie' smoothly: ha-**CIEN**-do.",
                practice_tip="Do not separate 'i' and 'e' into two syllables. It sounds like 'see-en' blended rapidly: **CIEN**."
            ),
            card5_quiz=Card5Quiz(
                sentence_prompt='¿Qué estás _____ tú en la cocina a estas horas?',
                options=['haciendo', 'haces', 'hacer', 'hecho'],
                correct_index=0,
                correct_explanation='¡Perfecto! Following **estás**, the continuous progressive structure strictly demands the gerund **haciendo**.',
                distractor_explanations={
                    'haces': "**haces** is present indicative. 'Estás haces' creates an impossible double auxiliary conflict; 'estar' requires a gerund.",
                    'hacer': "**hacer** is the infinitive. 'Estás hacer' is grammatically incorrect in Spanish.",
                    'hecho': "**hecho** is the past participle. 'Estás hecho' would describe a passive state rather than an ongoing activity."
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: 'Nosotros estamos _____ planes para viajar.'",
                micro_practice_options=['haciendo', 'hacemos', 'hicimos', 'hacer'],
                micro_practice_correct_index=0,
                micro_practice_explanation="Spot on! 'Estamos' + **haciendo** marks the ongoing collective action."
            )
        ),
        'Participio': TenseFlashcardPack(
            tense_name='Participio',
            tense_order=3,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — El Participio (Hecho)',
                rule='The **participio pasivo** of *hacer* is totally irregular! While regular -er verbs end in *-ido*, *hacer* transforms into **hecho** (done / made). *Hacido* does not exist!',
                usage_context='Coupled with auxiliary **haber** to form all Compound Perfect Tenses (*Pretérito Perfecto Compuesto*), or as an adjective modifying a noun.',
                triggers=['haber + hecho', 'ya', 'todavía no', 'alguna vez', 'nunca']
            ),
            card2_example=Card2Example(
                target_sentence='Ya hemos **hecho** todo el trabajo asignado para hoy.',
                native_sentence='We have already **done** all the work assigned for today.',
                breakdown='In compound tenses, the auxiliary **haber** conjugates (**hemos**), while **hecho** remains completely invariant (invariable).'
            ),
            card3_pronunciation=Card3Pronunciation(
                word='hecho',
                phonetic_breakdown='**HE**-cho',
                stressed_syllables='**HE**',
                audio_text='Ya hemos hecho todo el trabajo para hoy.',
                phonetic_tips="Stress is on the initial syllable **HE**. The Spanish **CH** is crisp, exactly like 'ch' in English 'chocolate' or 'chair'."
            ),
            card4_speech=Card4Speech(
                target_phrase='Ya hemos hecho el trabajo.',
                expected_phonetics='[ɟʝa ˈe.mos ˈe.tʃo el tɾaˈβa.xo]',
                key_focus_sounds="Silent 'h' in both 'hemos' and 'hecho'; crisp 'ch'.",
                practice_tip="Glide from 'hemos' to 'hecho' naturally: 'eh-mos eh-cho'."
            ),
            card5_quiz=Card5Quiz(
                sentence_prompt='¿Todavía no has _____ la reserva para el restaurante?',
                options=['hecho', 'hacido', 'hiciste', 'haciendo'],
                correct_index=0,
                correct_explanation='¡Exacto! *Hacer* has an irregular past participle: **hecho**. Never use *hacido*!',
                distractor_explanations={
                    'hacido': "A very common learner mistake! English speakers and beginners often over-regularize -er verbs to *-ido*. Remember: *hacer* becomes **hecho**!",
                    'hiciste': "**hiciste** is the simple past preterite. The auxiliary verb 'has' (from haber) requires the invariant past participle.",
                    'haciendo': "**haciendo** is the gerund, used with 'estar', not compound 'haber'."
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: 'El pastel está recién _____ por mi abuela.'",
                micro_practice_options=['hecho', 'hacido', 'hace', 'hicieron'],
                micro_practice_correct_index=0,
                micro_practice_explanation="Magnífico! Here 'hecho' acts as an adjective (made / baked), agreeing with 'pastel'."
            )
        ),
        'Presente de Indicativo': TenseFlashcardPack(
            tense_name='Presente de Indicativo',
            tense_order=4,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — Presente de Indicativo (Yo-Go Verbs)',
                rule='*Hacer* is a classic **"Yo-Go"** irregular verb. In the 1st person singular (yo), it forms **hago** (with a "g"). The remaining persons follow standard -er regular endings: *tú haces, él hace, nosotros hacemos, ellos hacen*.',
                usage_context='Used for present habits, current states, general truths, and weather expressions (*hace calor*, *hace frío*).',
                triggers=['siempre', 'todos los días', 'frecuentemente', 'cada mañana', 'hace calor/frío']
            ),
            card2_example=Card2Example(
                target_sentence='Yo siempre **hago** ejercicio por la mañana antes del trabajo.',
                native_sentence='I always **do** exercise in the morning before work.',
                breakdown="Observe the radical stem change for 'yo': *hacer* becomes **hago**, while preserving meaning."
            ),
            card3_pronunciation=Card3Pronunciation(
                word='hago',
                phonetic_breakdown='**HA**-go',
                stressed_syllables='**HA**',
                audio_text='Yo siempre hago ejercicio por la mañana.',
                phonetic_tips="Stress falls on **HA**. The 'g' before 'o' produces a voiced velar plosive [ɡ] sound, like 'go' in English."
            ),
            card4_speech=Card4Speech(
                target_phrase='Yo siempre hago ejercicio.',
                expected_phonetics='[ɟʝo ˈsjem.pɾe ˈa.ɣo e.xeɾˈsi.sjo]',
                key_focus_sounds="Initial syllable stress: **HA**-go. Silent 'h'.",
                practice_tip="Keep vowels crisp and short: 'yo SYEM-preh AH-goh eh-her-SEE-syoh'."
            ),
            card5_quiz=Card5Quiz(
                sentence_prompt='Cada fin de semana, yo _____ una tarta deliciosa para la familia.',
                options=['hago', 'haco', 'hace', 'hacemos'],
                correct_index=0,
                correct_explanation='¡Brillante! The 1st person singular "yo" in the present is the irregular "Yo-Go" form: **hago**.',
                distractor_explanations={
                    'haco': 'A very natural regularization error! Spanish historically phoneticized the 1st person with an inserted velar "g", producing **hago**, not *haco*.',
                    'hace': "**hace** is 3rd person singular (él / ella / usted), but the subject pronoun is 'yo'.",
                    'hacemos': "**hacemos** is 1st person plural (nosotros = we), not 'yo'."
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: '¿Qué _____ tú los sábados por la tarde?'",
                micro_practice_options=['haces', 'hago', 'hace', 'hacéis'],
                micro_practice_correct_index=0,
                micro_practice_explanation="¡Exacto! 'Tú' takes the standard regular -er ending: **haces**."
            )
        ),
        'Pretérito Indefinido': TenseFlashcardPack(
            tense_name='Pretérito Indefinido',
            tense_order=5,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — Pretérito Indefinido (Hic- / Hiz-)',
                rule='In the simple past (*Pretérito Indefinido*), *hacer* undergoes a radical stem mutation to **hic-** with unstressed personal endings: *yo hice, tú hiciste, él **hizo**, nosotros hicimos, ellos hicieron*. Note the spelling change **c ➔ z** in 3rd person to preserve the soft sound!',
                usage_context='Used to describe completed actions that occurred at a specific point or finished timeframe in the past.',
                triggers=['ayer', 'anoche', 'la semana pasada', 'el año pasado', 'hace dos días']
            ),
            card2_example=Card2Example(
                target_sentence='Ayer mi hermano **hizo** una cena increíble para mi cumpleaños.',
                native_sentence='Yesterday my brother **made** an incredible dinner for my birthday.',
                breakdown="In the 3rd person singular, *hic-* shifts to **hiz-** before 'o' (**hizo**) to preserve the soft 's/th' sound instead of a hard 'k' sound (*hico*)."
            ),
            card3_pronunciation=Card3Pronunciation(
                word='hizo',
                phonetic_breakdown='**HI**-zo',
                stressed_syllables='**HI**',
                audio_text='Ayer mi hermano hizo una cena increíble.',
                phonetic_tips="Stress is placed on the first syllable **HI**. In Latin America it sounds like 'EE-so'; in central/northern Spain it has the dental fricative 'EE-tho'."
            ),
            card4_speech=Card4Speech(
                target_phrase='Ayer mi hermano hizo la cena.',
                expected_phonetics='[aˈɟʝeɾ mj eɾˈma.no ˈi.so la ˈse.na]',
                key_focus_sounds='Stress on **HI**-zo; do not stress the last syllable.',
                practice_tip='Avoid stressing the ending: say **HI**-zo, never hi-ZO.'
            ),
            card5_quiz=Card5Quiz(
                sentence_prompt='¿Quién _____ todo este desastre en la sala ayer?',
                options=['hizo', 'hació', 'hice', 'hicieron'],
                correct_index=0,
                correct_explanation="¡Extraordinario! 'Quién' (singular) requires the 3rd person preterite with orthographic change: **hizo**.",
                distractor_explanations={
                    'hació': 'Classic beginner trap! Spanish irregular preterites do not take regular accented endings (-ió); they use radical stems with unstressed endings. *Hacer* becomes **hizo**.',
                    'hice': "**hice** is the 1st person singular ('yo hice'), not 3rd person ('quién hizo').",
                    'hicieron': "**hicieron** is 3rd person plural ('ellos hicieron'), whereas 'quién' is singular."
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: 'Yo _____ todo lo posible para ayudarte ayer.'",
                micro_practice_options=['hice', 'hizo', 'hiciste', 'hací'],
                micro_practice_correct_index=0,
                micro_practice_explanation="¡Fantástico! 'Yo' + preterite of hacer is **hice**."
            )
        )
    }
)

CURATED_CURRICULA = {
    'spanish_hacer': SPANISH_HACER_CURRICULUM
}

def get_curriculum_or_fallback(topic_query: str, target_lang: str = 'Spanish') -> Optional[CurriculumCourse]:
    query = topic_query.lower()
    if 'hacer' in query or 'irregular' in query or 'spanish' in target_lang.lower():
        return SPANISH_HACER_CURRICULUM
    return SPANISH_HACER_CURRICULUM
