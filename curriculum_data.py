"""
Curriculum data models and pre-curated courses for LingoCraft AI.
Provides instant offline fallback and high-quality baseline curricula.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import random
import re


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
    suggested_coach_prompts: List[str] = field(default_factory=list)

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

def build_spanish_hacer_pack(native_lang: str = "English") -> Dict[str, TenseFlashcardPack]:
    lang = native_lang.lower()
    is_pt = "portugu" in lang
    is_es = "español" in lang or "spanish" in lang

    if is_pt:
        return {
            'Infinitivo': TenseFlashcardPack(
                tense_name='Infinitivo',
                tense_order=1,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — El Infinitivo (Hacer)',
                    rule='O **infinitivo** é a forma básica não conjugada do verbo terminando em **-er**. Em espanhol, atua como substantivo verbal e é usado diretamente após preposições, verbos modais ou perífrases verbais.',
                    usage_context='Usado quando a ação é descrita em abstrato ou diretamente regida por outro verbo conjugado (ex.: *querer hacer*, *tener que hacer*).',
                    triggers=['tener que + infinitivo', 'querer + infinitivo', 'antes de', 'después de', 'para']
                ),
                card2_example=Card2Example(
                    target_sentence='Tengo que **hacer** la tarea antes de salir con mis amigos.',
                    native_sentence='Tenho que **fazer** a lição de casa antes de sair com meus amigos.',
                    breakdown='Observe que **hacer** permanece no infinitivo porque segue a locução de obrigação **tengo que**.'
                ),
                card3_pronunciation=Card3Pronunciation(
                    word='hacer',
                    phonetic_breakdown='ha-**CER**',
                    stressed_syllables='**CER**',
                    audio_text='Tengo que hacer la tarea antes de salir.',
                    phonetic_tips='Em espanhol, o **H** inicial é sempre completamente mudo. Palavras terminadas em consoantes que não sejam -N ou -S enfatizam a **última sílaba**.'
                ),
                card4_speech=Card4Speech(
                    target_phrase='Tengo que hacer la tarea.',
                    expected_phonetics='[ˈteŋ.ɡo ke aˈseɾ la taˈɾe.a]',
                    key_focus_sounds='H mudo em hacer, som suave do r no final.',
                    practice_tip='Comece diretamente no som da vogal a ao dizer **hacer**; nunca aspire como no inglês hat.'
                ),
                card5_quiz=Card5Quiz(
                    sentence_prompt='Ella quiere _____ una pregunta importante al profesor.',
                    options=['hacer', 'hace', 'haciendo', 'hizo'],
                    correct_index=0,
                    correct_explanation='¡Excelente! Depois de verbos modais de desejo como **quiere** (quer), o espanhol sempre exige o **infinitivo** base (*hacer*).',
                    distractor_explanations={
                        'hace': '**hace** é conjugado na 3ª pessoa do singular do presente. Não podemos empilhar dois verbos conjugados sem conjunção.',
                        'haciendo': '**haciendo** é o gerúndio contínuo (fazendo), inadequado após querer.',
                        'hizo': '**hizo** é o pretérito indefinido (fez), incompatível com o verbo auxiliar auxiliar.'
                    },
                    micro_practice_prompt="Micro-Prática: Complete: 'Voy a _____ café para todos.'",
                    micro_practice_options=['hacer', 'hago', 'hizo', 'hacemos'],
                    micro_practice_correct_index=0,
                    micro_practice_explanation="Correto! 'Ir a' + **infinitivo** (*hacer*) expressa futuro imediato."
                ),
                suggested_coach_prompts=[
                    "Por que o verbo 'hacer' fica no infinitivo após locuções como 'tener que'?",
                    "Quais são as 3 expressões mais comuns com o infinitivo 'hacer' no dia a dia?",
                    "Como pronunciar o 'r' final de 'ha-CER' de forma natural?"
                ]
            ),
            'Gerundio': TenseFlashcardPack(
                tense_name='Gerundio',
                tense_order=2,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — El Gerundio (Haciendo)',
                    rule='O **gerundio** é o particípio contínuo/progressivo. Para verbos regulares em -er, o sufixo é **-iendo**. O radical **hac-** forma **haciendo** (fazendo).',
                    usage_context='Usado com o verbo auxiliar **estar** (*estar + gerundio*) para descrever ações que estão acontecendo exatamente no momento da fala.',
                    triggers=['estar + gerundio', 'ahora mismo', 'en este momento', 'actualmente']
                ),
                card2_example=Card2Example(
                    target_sentence='Ahora mismo estoy **haciendo** un café caliente para el desayuno.',
                    native_sentence='Agora mesmo estou **fazendo** um café quente para o café da manhã.',
                    breakdown='A estrutura **estoy haciendo** combina o auxiliar **estar** com o gerúndio para marcar uma ação contínua.'
                ),
                card3_pronunciation=Card3Pronunciation(
                    word='haciendo',
                    phonetic_breakdown='ha-**CIEN**-do',
                    stressed_syllables='**CIEN**',
                    audio_text='Ahora mismo estoy haciendo un café caliente.',
                    phonetic_tips="A tônica recai na penúltima sílaba **CIEN**. O 'ie' é um ditongo crescente que desliza junto em uma só sílaba."
                ),
                card4_speech=Card4Speech(
                    target_phrase='Estoy haciendo un café.',
                    expected_phonetics='[esˈtoj aˈsjen.do uŋ kaˈfe]',
                    key_focus_sounds="Deslize o ditongo 'ie' com fluidez: ha-**CIEN**-do.",
                    practice_tip="Não separe 'i' e 'e' em duas sílabas. Soe rápido como um bloco único: **CIEN**."
                ),
                card5_quiz=Card5Quiz(
                    sentence_prompt='¿Qué estás _____ tú en la cocina a estas horas?',
                    options=['haciendo', 'haces', 'hacer', 'hecho'],
                    correct_index=0,
                    correct_explanation='¡Perfecto! Após **estás**, a estrutura progressiva exige estritamente o gerúndio **haciendo**.',
                    distractor_explanations={
                        'haces': "**haces** é presente do indicativo. 'Estás haces' causa conflito verbal; 'estar' exige gerúndio.",
                        'hacer': '**hacer** é o infinitivo.',
                        'hecho': '**hecho** é o particípio passado.'
                    },
                    micro_practice_prompt="Micro-Prática: Complete: 'Nosotros estamos _____ planes para viajar.'",
                    micro_practice_options=['haciendo', 'hacemos', 'hicimos', 'hacer'],
                    micro_practice_correct_index=0,
                    micro_practice_explanation="Na mosca! 'Estamos' + **haciendo** marca a ação coletiva em curso."
                ),
                suggested_coach_prompts=[
                    "Por que usamos 'estar haciendo' em vez de 'ser haciendo'?",
                    "Qual é a diferença de sentido entre 'hago ejercicio' e 'estoy haciendo ejercicio'?",
                    "Como pronunciar o ditongo 'ie' em 'ha-CIEN-do' sem travar a língua?"
                ]
            ),
            'Participio': TenseFlashcardPack(
                tense_name='Participio',
                tense_order=3,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — El Participio (Hecho)',
                    rule='O **participio** de *hacer* é totalmente irregular! Enquanto verbos regulares em -er terminam em *-ido*, *hacer* transforma-se em **hecho** (feito). *Hacido* não existe!',
                    usage_context='Combinado com o auxiliar **haber** para formar tempos perfeitos compostos, ou usado como adjetivo modificando substantivos.',
                    triggers=['haber + hecho', 'ya', 'todavía no', 'alguna vez', 'nunca']
                ),
                card2_example=Card2Example(
                    target_sentence='Ya hemos **hecho** todo el trabajo asignado para hoy.',
                    native_sentence='Já temos **feito** todo o trabalho atribuído para hoje.',
                    breakdown='Nos tempos compostos com *haber*, o auxiliar conjuga (**hemos**), enquanto **hecho** permanece invariável.'
                ),
                card3_pronunciation=Card3Pronunciation(
                    word='hecho',
                    phonetic_breakdown='**HE**-cho',
                    stressed_syllables='**HE**',
                    audio_text='Ya hemos hecho todo el trabajo para hoy.',
                    phonetic_tips="A tônica está na primeira sílaba **HE**. O 'ch' do espanhol é nítido e estalado, como em 'tchau'."
                ),
                card4_speech=Card4Speech(
                    target_phrase='Ya hemos hecho el trabalho.',
                    expected_phonetics='[ɟʝa ˈe.mos ˈe.tʃo el tɾaˈβa.xo]',
                    key_focus_sounds="'H' mudo em hemos e hecho; 'ch' bem definido.",
                    practice_tip="Conecte 'hemos' e 'hecho' naturalmente: 'eh-mos eh-tcho'."
                ),
                card5_quiz=Card5Quiz(
                    sentence_prompt='¿Todavía no has _____ la reserva para el restaurante?',
                    options=['hecho', 'hacido', 'hiciste', 'haciendo'],
                    correct_index=0,
                    correct_explanation='¡Exacto! *Hacer* tem particípio totalmente irregular: **hecho**. Nunca use *hacido*!',
                    distractor_explanations={
                        'hacido': 'Erro muito comum de hiper-regularização! Lembre-se: fazer vira **hecho**.',
                        'hiciste': "**hiciste** é o pretérito indefinido simples, incompatível com o auxiliar 'has'.",
                        'haciendo': '**haciendo** é o gerúndio.'
                    },
                    micro_practice_prompt="Micro-Prática: Complete: 'El pastel está recién _____ por mi abuela.'",
                    micro_practice_options=['hecho', 'hacido', 'hace', 'hicieron'],
                    micro_practice_correct_index=0,
                    micro_practice_explanation="Perfeito! Aqui 'hecho' atua como adjetivo (feito), concordando com 'pastel'."
                ),
                suggested_coach_prompts=[
                    "Por que 'hacer' tem particípio irregular 'hecho' em vez de 'hacido'?",
                    "Quando 'hecho' muda para 'hecha/hechos/hechas' e quando fica invariável?",
                    "Qual é a diferença entre 'lo he hecho' e 'lo hice'?"
                ]
            ),
            'Presente de Indicativo': TenseFlashcardPack(
                tense_name='Presente de Indicativo',
                tense_order=4,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — Presente de Indicativo (Yo-Go)',
                    rule='*Hacer* é um clássico verbo irregular **"Yo-Go"**. Na 1ª pessoa do singular (yo), vira **hago** (com "g"). As demais pessoas seguem as terminações regulares de -er: *tú haces, él hace, nosotros hacemos, ellos hacen*.',
                    usage_context='Usado para hábitos diários, verdades universais e expressões de clima (*hace calor*, *hace frío*).',
                    triggers=['siempre', 'todos los días', 'frecuentemente', 'cada mañana', 'hace calor/frío']
                ),
                card2_example=Card2Example(
                    target_sentence='Yo siempre **hago** ejercicio por la mañana antes del trabajo.',
                    native_sentence='Eu sempre **faço** exercícios pela manhã antes do trabalho.',
                    breakdown="Observe a alteração no radical para 'yo': *hacer* torna-se **hago**."
                ),
                card3_pronunciation=Card3Pronunciation(
                    word='hago',
                    phonetic_breakdown='**HA**-go',
                    stressed_syllables='**HA**',
                    audio_text='Yo siempre hago ejercicio por la mañana.',
                    phonetic_tips="A tônica cai em **HA**. O 'g' antes de 'o' soa forte como em 'gato'."
                ),
                card4_speech=Card4Speech(
                    target_phrase='Yo siempre hago ejercicio.',
                    expected_phonetics='[ɟʝo ˈsjem.pɾe ˈa.ɣo e.xeɾˈsi.sjo]',
                    key_focus_sounds='Tônica na primeira sílaba: **HA**-go. H mudo.',
                    practice_tip="Mantenha as vogais abertas e sonoras: 'yo SYEM-pre AH-go'."
                ),
                card5_quiz=Card5Quiz(
                    sentence_prompt='Cada fin de semana, yo _____ una tarta deliciosa para la familia.',
                    options=['hago', 'haco', 'hace', 'hacemos'],
                    correct_index=0,
                    correct_explanation='¡Brillante! A 1ª pessoa singular "yo" no presente é a forma irregular "Yo-Go": **hago**.',
                    distractor_explanations={
                        'haco': 'Tentativa natural de regularização, mas o espanhol histórico insere o velar "g": **hago**.',
                        'hace': "**hace** é 3ª pessoa singular (él/ella), não 'yo'.",
                        'hacemos': "**hacemos** é 1ª pessoa plural (nosotros = nós)."
                    },
                    micro_practice_prompt="Micro-Prática: Complete: '¿Qué _____ tú los sábados por la tarde?'",
                    micro_practice_options=['haces', 'hago', 'hace', 'hacéis'],
                    micro_practice_correct_index=0,
                    micro_practice_explanation="¡Exacto! 'Tú' recebe a terminação padrão de -er: **haces**."
                ),
                suggested_coach_prompts=[
                    "Por que apenas a primeira pessoa 'yo' é irregular ('hago') no presente?",
                    "Por que se diz 'hace calor' em vez de 'está calor' em espanhol?",
                    "Quais outros verbos têm essa irregularidade 'Yo-Go' (como 'tener', 'poner', 'salir')?"
                ]
            ),
            'Pretérito Indefinido': TenseFlashcardPack(
                tense_name='Pretérito Indefinido',
                tense_order=5,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — Pretérito Indefinido (Hic- / Hiz-)',
                    rule='No passado simples (*Pretérito Indefinido*), *hacer* sofre mutação radical para **hic-**: *yo hice, tú hiciste, él **hizo**, nosotros hicimos, ellos hicieron*. Note a troca ortográfica **c para z** na 3ª pessoa para manter o som brando!',
                    usage_context='Usado para descrever ações concluídas em um momento pontual e terminado no passado.',
                    triggers=['ayer', 'anoche', 'la semana pasada', 'el año pasado', 'hace dos días']
                ),
                card2_example=Card2Example(
                    target_sentence='Ayer mi hermano **hizo** una cena increíble para mi cumpleaños.',
                    native_sentence='Ontem meu irmão **fez** um jantar incrível para o meu aniversário.',
                    breakdown="Na 3ª pessoa do singular, *hic-* muda para **hiz-** antes de 'o' (**hizo**) para evitar o som duro de 'k' (*hico*)."
                ),
                card3_pronunciation=Card3Pronunciation(
                    word='hizo',
                    phonetic_breakdown='**HI**-zo',
                    stressed_syllables='**HI**',
                    audio_text='Ayer mi hermano hizo una cena increíble.',
                    phonetic_tips="A tônica fica na primeira sílaba **HI**. Na América Latina soa como 'EE-so'; na Espanha central soa com 'th'."
                ),
                card4_speech=Card4Speech(
                    target_phrase='Ayer mi hermano hizo la cena.',
                    expected_phonetics='[aˈɟʝeɾ mj eɾˈma.no ˈi.so la ˈse.na]',
                    key_focus_sounds='Acento na primeira sílaba: **HI**-zo; nunca acentue o final.',
                    practice_tip='Diga com convicção **HI**-zo, nunca hi-ZO.'
                ),
                card5_quiz=Card5Quiz(
                    sentence_prompt='¿Quién _____ todo este desastre en la sala ayer?',
                    options=['hizo', 'hació', 'hice', 'hicieron'],
                    correct_index=0,
                    correct_explanation="¡Extraordinario! 'Quién' (singular) exige a 3ª pessoa do pretérito com mudança ortográfica: **hizo**.",
                    distractor_explanations={
                        'hació': 'Armadilha clássica! Verbos irregulares com raiz forte não levam acento no final (-ió). Fazer vira **hizo**.',
                        'hice': "**hice** é 1ª pessoa ('yo hice'), não 3ª pessoa.",
                        'hicieron': '**hicieron** é plural (ellos).'
                    },
                    micro_practice_prompt="Micro-Prática: Complete: 'Yo _____ todo lo posible para ayudarte ayer.'",
                    micro_practice_options=['hice', 'hizo', 'hiciste', 'hací'],
                    micro_practice_correct_index=0,
                    micro_practice_explanation="¡Fantástico! 'Yo' + pretérito de hacer é **hice**."
                ),
                suggested_coach_prompts=[
                    "Por que 'hizo' usa 'z' em vez de 'c' como em 'hice'?",
                    "Por que verbos como 'hizo' ou 'pudo' não têm acento gráfico no pretérito?",
                    "Qual é o melhor macete para memorizar 'hice, hiciste, hizo'?"
                ]
            )
        }

    # Default English Explanations
    return {
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
            ),
            suggested_coach_prompts=[
                "Why is 'hacer' unconjugated after modal verbs like 'tener que' or 'querer'?",
                "What are 3 common Spanish idiomatic expressions that use the infinitive 'hacer'?",
                "How do I pronounce the final 'r' in 'ha-CER' with a clean Spanish tap?"
            ]
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
                    'hacer': '**hacer** is the infinitive. "Estás hacer" is ungrammatical.',
                    'hecho': '**hecho** is the past participle.'
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: 'Nosotros estamos _____ planes para viajar.'",
                micro_practice_options=['haciendo', 'hacemos', 'hicimos', 'hacer'],
                micro_practice_correct_index=0,
                micro_practice_explanation="Spot on! 'Estamos' + **haciendo** marks the ongoing collective action."
            ),
            suggested_coach_prompts=[
                "Why do we say 'estoy haciendo' instead of 'soy haciendo'?",
                "What is the difference in nuance between 'hago ejercicio' and 'estoy haciendo ejercicio'?",
                "How do I glide the diphthong 'ie' smoothly in 'ha-CIEN-do' without hesitating?"
            ]
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
                    'hacido': "A very common learner mistake! English speakers often over-regularize -er verbs to *-ido*. Remember: *hacer* becomes **hecho**!",
                    'hiciste': "**hiciste** is the simple past preterite. The auxiliary verb 'has' requires the past participle.",
                    'haciendo': '**haciendo** is the gerund.'
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: 'El pastel está recién _____ por mi abuela.'",
                micro_practice_options=['hecho', 'hacido', 'hace', 'hicieron'],
                micro_practice_correct_index=0,
                micro_practice_explanation="Magnífico! Here 'hecho' acts as an adjective (made / baked), agreeing with 'pastel'."
            ),
            suggested_coach_prompts=[
                "Why is 'hecho' completely irregular instead of 'hacido'?",
                "When does 'hecho' change to 'hecha/hechos/hechas' versus staying invariant?",
                "What is the difference between 'lo he hecho' and 'lo hice'?"
            ]
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
                key_focus_sounds='Initial syllable stress: **HA**-go. Silent h.',
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
            ),
            suggested_coach_prompts=[
                "Why is 'yo' irregular ('hago') while the other persons remain regular ('haces', 'hace')?",
                "Why do Spanish speakers say 'hace calor/frío' instead of 'está calor/frío'?",
                "What other Spanish verbs share this 'Yo-Go' irregularity (like 'tener', 'poner', 'salir')?"
            ]
        ),
        'Pretérito Indefinido': TenseFlashcardPack(
            tense_name='Pretérito Indefinido',
            tense_order=5,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — Pretérito Indefinido (Hic- / Hiz-)',
                rule='In the simple past (*Pretérito Indefinido*), *hacer* undergoes a radical stem mutation to **hic-** with unstressed personal endings: *yo hice, tú hiciste, él **hizo**, nosotros hicimos, ellos hicieron*. Note the spelling change **c to z** in 3rd person to preserve the soft sound!',
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
                    'hació': "Classic beginner trap! Spanish irregular preterites do not take regular accented endings (-ió); they use radical stems with unstressed endings. *Hacer* becomes **hizo**.",
                    'hice': "**hice** is the 1st person singular ('yo hice'), not 3rd person ('quién hizo').",
                    'hicieron': "**hicieron** is 3rd person plural ('ellos hicieron'), whereas 'quién' is singular."
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: 'Yo _____ todo lo posible para ayudarte ayer.'",
                micro_practice_options=['hice', 'hizo', 'hiciste', 'hací'],
                micro_practice_correct_index=0,
                micro_practice_explanation="¡Fantástico! 'Yo' + preterite of hacer is **hice**."
            ),
            suggested_coach_prompts=[
                "Why does 'hizo' use a 'z' instead of a 'c' like 'hice'?",
                "Why do irregular preterite verbs like 'hizo' or 'pudo' lack an accent mark on the last syllable?",
                "Can you give me a trick or mnemonic to easily remember 'yo hice, tú hiciste, él hizo'?"
            ]
        )
    }

def build_spanish_tener_pack(native_lang: str = "English") -> Dict[str, TenseFlashcardPack]:
    lang = native_lang.lower()
    is_pt = "portugu" in lang

    if is_pt:
        return {
            'Infinitivo': TenseFlashcardPack(
                tense_name='Infinitivo',
                tense_order=1,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — El Infinitivo (Tener)',
                    rule="O **infinitivo** é a forma básica não conjugada (*tener*). Em espanhol, é central na perífrase essencial de obrigação e necessidade: **tener que + infinitivo** (ter que fazer algo).",
                    usage_context="Usado após preposições, verbos de desejo (*querer tener*, *esperar tener*) e locuções perifrásticas.",
                    triggers=['tener que + infinitivo', 'querer tener', 'para', 'antes de tener']
                ),
                card2_example=Card2Example(
                    target_sentence='Tengo que **tener** mucha paciencia con esta situación difícil.',
                    native_sentence='Tenho que **ter** muita paciência com esta situação difícil.',
                    breakdown="O verbo principal **tener** permanece no infinitivo após a perífrase de obrigação *tengo que*."
                ),
                card3_pronunciation=Card3Pronunciation(
                    word='tener',
                    phonetic_breakdown='te-**NER**',
                    stressed_syllables='**NER**',
                    audio_text='Tengo que tener mucha paciencia con esta situación.',
                    phonetic_tips="A tonicidade recai na última sílaba **NER**. O 'T' em espanhol é dental (língua encostada nos dentes superiores, sem chiar como em 'tch')."
                ),
                card4_speech=Card4Speech(
                    target_phrase='Tengo que tener paciencia.',
                    expected_phonetics='[ˈteŋ.ɡo ke teˈneɾ paˈsjen.sja]',
                    key_focus_sounds='T dental limpo e r suave final.',
                    practice_tip="Pronuncie o 'te' limpo e claro sem aspirar."
                ),
                card5_quiz=Card5Quiz(
                    sentence_prompt='Ella espera _____ buenas noticias de su familia pronto.',
                    options=['tener', 'tiene', 'teniendo', 'tuvo'],
                    correct_index=0,
                    correct_explanation="¡Correcto! Após o verbo de desejo **espera**, exige-se o **infinitivo** (*tener*).",
                    distractor_explanations={
                        'tiene': "**tiene** é a 3ª pessoa do presente, não pode ser empilhado sem conjunção.",
                        'teniendo': "**teniendo** é o gerúndio contínuo (tendo).",
                        'tuvo': "**tuvo** é o pretérito indefinido (teve)."
                    },
                    micro_practice_prompt="Micro-Prática: Complete: 'Vamos a _____ una fiesta el sábado.'",
                    micro_practice_options=['tener', 'tengo', 'tuvo', 'tenemos'],
                    micro_practice_correct_index=0,
                    micro_practice_explanation="Exato! 'Ir a' exige o infinitivo base **tener**."
                ),
                suggested_coach_prompts=[
                    "Como usar 'tener que' vs 'hay que' em espanhol?",
                    "Por que em espanhol usamos 'tener años' para idade em vez de 'ser'?",
                    "Quais expressões idiomáticas comuns usam o verbo tener?"
                ]
            ),
            'Gerundio': TenseFlashcardPack(
                tense_name='Gerundio',
                tense_order=2,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — El Gerundio (Teniendo)',
                    rule="O **gerúndio** de *tener* é **teniendo** (-iendo). É usado com o auxiliar *estar* para indicar uma experiência ou ação em curso.",
                    usage_context="Utilizado para descrever sensações, experiências ou processos contínuos (*estar teniendo*).",
                    triggers=['ahora mismo', 'en este momento', 'estar + teniendo', 'últimamente']
                ),
                card2_example=Card2Example(
                    target_sentence='Ahora mismo estamos **teniendo** una conversación muy constructiva.',
                    native_sentence='Agora mesmo estamos **tendo** uma conversa muito construtiva.',
                    breakdown="A terminação **-iendo** junta-se ao radical *ten-* formando o ditongo 'ie' com acento tônico em **NIEN**."
                ),
                card3_pronunciation=Card3Pronunciation(
                    word='teniendo',
                    phonetic_breakdown='te-**NIEN**-do',
                    stressed_syllables='**NIEN**',
                    audio_text='Ahora mismo estamos teniendo una conversación constructiva.',
                    phonetic_tips="A sílaba tônica é **NIEN**. O ditongo 'ie' deve ser pronunciado em uma única emissão de voz sem pausa."
                ),
                card4_speech=Card4Speech(
                    target_phrase='Estamos teniendo una buena semana.',
                    expected_phonetics='[esˈta.mos teˈnjen.do ˈu.na ˈbwe.na seˈma.na]',
                    key_focus_sounds='Fluidez no ditongo -nien- de te-nien-do.',
                    practice_tip='Evite separar te-ni-en-do em quatro sílabas; são apenas três sílabas rítmicas.'
                ),
                card5_quiz=Card5Quiz(
                    sentence_prompt='¿Qué tipo de dificultades estás _____ en tu nuevo trabajo?',
                    options=['teniendo', 'tenido', 'tienes', 'tener'],
                    correct_index=0,
                    correct_explanation="¡Excelente! Após **estás** (auxiliar contínuo), exige-se o gerúndio **teniendo**.",
                    distractor_explanations={
                        'tenido': "**tenido** é o particípio passado (tido).",
                        'tienes': "**tienes** é o presente simples do indicativo.",
                        'tener': "**tener** é o infinitivo."
                    },
                    micro_practice_prompt="Micro-Prática: Complete: 'Ellos están _____ mucho éxito.'",
                    micro_practice_options=['teniendo', 'tenido', 'tienen', 'tener'],
                    micro_practice_correct_index=0,
                    micro_practice_explanation="Muito bem! 'Están' + gerúndio = **teniendo**."
                ),
                suggested_coach_prompts=[
                    "Por que dizemos 'estamos teniendo' com ditongo 'ie'?",
                    "Posso usar 'teniendo en cuenta' como 'levando em consideração'?",
                    "Qual a diferença entre 'tengo problemas' e 'estoy teniendo problemas'?"
                ]
            ),
            'Participio': TenseFlashcardPack(
                tense_name='Participio',
                tense_order=3,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — El Participio (Tenido)',
                    rule="O **particípio** de *tener* é regular: **tenido** (-ido). Permanece invariável quando acompanhado do verbo auxiliar **haber** (*he tenido, has tenido, ha tenido*).",
                    usage_context="Expressa experiências ou fatos passados com conexão com o presente.",
                    triggers=['alguna vez', 'nunca', 'siempre', 'este año', 'últimamente', 'ya']
                ),
                card2_example=Card2Example(
                    target_sentence='Siempre he **tenido** mucha suerte con mis compañeros de trabajo.',
                    native_sentence='Sempre **tive** muita sorte com meus colegas de trabalho.',
                    breakdown="Em espanhol, **he tenido** expressa o pretérito perfeito composto com o particípio invariável em -o."
                ),
                card3_pronunciation=Card3Pronunciation(
                    word='tenido',
                    phonetic_breakdown='te-**NI**-do',
                    stressed_syllables='**NI**',
                    audio_text='Siempre he tenido mucha suerte.',
                    phonetic_tips="A ênfase é na penúltima sílaba **NI**. O 'd' entre vogais soa de forma muito suave."
                ),
                card4_speech=Card4Speech(
                    target_phrase='Nunca he tenido problemas.',
                    expected_phonetics='[ˈnuŋ.ka e teˈni.ðo pɾoˈβle.mas]',
                    key_focus_sounds='H mudo em he, d suave em te-ni-do.',
                    practice_tip="Pronuncie 'he tenido' como [e te-NI-do], ligando os sons suavemente."
                ),
                card5_quiz=Card5Quiz(
                    sentence_prompt='Nosotros nunca hemos _____ una oportunidad tan buena.',
                    options=['tenido', 'teniendo', 'tenemos', 'tuve'],
                    correct_index=0,
                    correct_explanation="¡Perfecto! O pretérito perfeito com 'hemos' sempre exige o particípio **tenido**.",
                    distractor_explanations={
                        'teniendo': "**teniendo** é gerúndio.",
                        'tenemos': "**tenemos** é presente do indicativo.",
                        'tuve': "**tuve** é 1ª pessoa do pretérito simples."
                    },
                    micro_practice_prompt="Micro-Prática: Complete: '¿Has _____ tiempo de revisar el informe?'",
                    micro_practice_options=['tenido', 'tener', 'tienes', 'teniendo'],
                    micro_practice_correct_index=0,
                    micro_practice_explanation="Exato! 'Has' + particípio = **tenido**."
                ),
                suggested_coach_prompts=[
                    "Quando usamos 'he tenido' em vez de 'tuve'?",
                    "O particípio 'tenido' muda para feminino ou plural quando usado com haber?",
                    "Quais países preferem 'tuve' a 'he tenido' no dia a dia?"
                ]
            ),
            'Presente de Indicativo': TenseFlashcardPack(
                tense_name='Presente de Indicativo',
                tense_order=4,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — Presente (Tengo, Tienes, Tiene...)',
                    rule="No presente, *tener* apresenta dupla irregularidade: a 1ª pessoa ganha **-go** (**yo tengo**), e as pessoas *tú, él/ella, ellos* sofrem ditongação **e ➔ ie** (**tienes, tiene, tienen**). As formas *nosotros* e *vosotros* permanecem regulares (**tenemos, tenéis**).",
                    usage_context="Usado para expressar idade (*tengo 25 años*), sensações físicas (*tengo hambre/sed*), posse e obrigação.",
                    triggers=['hoy', 'siempre', 'normalmente', 'todos los días', 'ahora']
                ),
                card2_example=Card2Example(
                    target_sentence='Yo **tengo** dos hermanos y vivimos juntos en el centro de Madrid.',
                    native_sentence='Eu **tenho** dois irmãos e moramos juntos no centro de Madri.',
                    breakdown="Observe a terminação irregular de 1ª pessoa **-go**: *yo tengo* (como em *hago*, *pongo*, *vengo*)."
                ),
                card3_pronunciation=Card3Pronunciation(
                    word='tengo',
                    phonetic_breakdown='**TEN**-go',
                    stressed_syllables='**TEN**',
                    audio_text='Yo tengo dos hermanos en Madrid.',
                    phonetic_tips="A tonicidade é na primeira sílaba **TEN**. O 'g' antes de 'o' tem som velar suave [g], como em 'gato'."
                ),
                card4_speech=Card4Speech(
                    target_phrase='Yo tengo una buena idea.',
                    expected_phonetics='[ˈɟʝo ˈteŋ.ɡo ˈu.na ˈbwe.na iˈðe.a]',
                    key_focus_sounds='Acentuação clara em **TEN**-go.',
                    practice_tip="Mantenha o 'yo' breve e enfatize com clareza **TEN**-go."
                ),
                card5_quiz=Card5Quiz(
                    sentence_prompt='Yo _____ mucha prisa porque mi tren sale en diez minutos.',
                    options=['tengo', 'tiene', 'tienes', 'tenemos'],
                    correct_index=0,
                    correct_explanation="¡Magnífico! A 1ª pessoa do singular (yo) do presente de tener é **tengo**.",
                    distractor_explanations={
                        'tiene': "**tiene** é a 3ª pessoa do singular (él/ella).",
                        'tienes': "**tienes** é a 2ª pessoa informal (tú).",
                        'tenemos': "**tenemos** é a 1ª pessoa do plural (nosotros)."
                    },
                    micro_practice_prompt="Micro-Prática: Complete: '¿Cuántos años _____ tú?'",
                    micro_practice_options=['tienes', 'tengo', 'tiene', 'tenéis'],
                    micro_practice_correct_index=0,
                    micro_practice_explanation="Correto! Com 'tú' usa-se a forma ditongada **tienes**."
                ),
                suggested_coach_prompts=[
                    "Por que dizemos 'tengo hambre' e não 'estoy con hambre'?",
                    "Quais outros verbos pertencem à família 'Yo-Go' como tengo e hago?",
                    "Como funciona a ditongação de tener no presente para as outras pessoas?"
                ]
            ),
            'Pretérito Indefinido': TenseFlashcardPack(
                tense_name='Pretérito Indefinido',
                tense_order=5,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — Pretérito Indefinido (Tuve, Tuviste, Tuvo...)',
                    rule="No pretérito indefinido (passado simples), *tener* sofre mutação radical para **tuv-** com desinências atônicas sem acento: *yo **tuve**, tú **tuviste**, él **tuvo**, nosotros **tuvimos**, ellos **tuvieron**.",
                    usage_context="Usado para expressar eventos passados concluídos ou quando algo ocorreu em momento específico (*ayer tuve un examen*).",
                    triggers=['ayer', 'anoche', 'el año pasado', 'la semana pasada', 'en aquel momento']
                ),
                card2_example=Card2Example(
                    target_sentence='Ayer mi amiga **tuvo** una reunión decisiva con el director general.',
                    native_sentence='Ontem minha amiga **teve** uma reunião decisiva com o diretor geral.',
                    breakdown="Observe o radical irregular **tuv-** na 3ª pessoa do singular **tuvo** (sem acento no final)."
                ),
                card3_pronunciation=Card3Pronunciation(
                    word='tuvo',
                    phonetic_breakdown='**TU**-vo',
                    stressed_syllables='**TU**',
                    audio_text='Ayer mi amiga tuvo una reunión decisiva.',
                    phonetic_tips="A tonicidade recai na primeira sílaba: **TU**-vo. Em espanhol, 'b' e 'v' têm o mesmo som bilabial suave [β]."
                ),
                card4_speech=Card4Speech(
                    target_phrase='Ayer tuve mucho trabajo.',
                    expected_phonetics='[aˈʝeɾ ˈtu.βe ˈmu.tʃo tɾaˈβa.xo]',
                    key_focus_sounds='Tônica em **TU**-ve, jota suave como r aspirado em tra-BA-jo.',
                    practice_tip="Enfatize a primeira sílaba: **TU**-ve, nunca tu-VE."
                ),
                card5_quiz=Card5Quiz(
                    sentence_prompt='El mes pasado nosotros _____ que mudarnos a otra ciudad.',
                    options=['tuvimos', 'tenimos', 'tuve', 'tuvieron'],
                    correct_index=0,
                    correct_explanation="¡Excelente! O sujeito 'nosotros' no pretérito irregular de tener é **tuvimos**.",
                    distractor_explanations={
                        'tenimos': "Não existe 'tenimos' em espanhol; o radical irregular é **tuv-**.",
                        'tuve': "**tuve** é a 1ª pessoa do singular (yo).",
                        'tuvieron': "**tuvieron** é a 3ª pessoa do plural (ellos/ellas)."
                    },
                    micro_practice_prompt="Micro-Prática: Complete: '¿_____ tú algún problema ayer?'",
                    micro_practice_options=['Tuviste', 'Tuve', 'Tuvo', 'Tuvimos'],
                    micro_practice_correct_index=0,
                    micro_practice_explanation="Muito bem! 'Tú' no pretérito de tener é **tuviste**."
                ),
                suggested_coach_prompts=[
                    "Por que 'tuve' e 'tuvo' não levam acento gráfico na última letra?",
                    "Qual a diferença de sentido entre 'tuve un perro' e 'tenía un perro'?",
                    "Quais outros verbos usam o radical com -uv- (como estar -> estuve, andar -> anduve)?"
                ]
            )
        }

    # English Native/Support Language
    return {
        'Infinitivo': TenseFlashcardPack(
            tense_name='Infinitivo',
            tense_order=1,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — El Infinitivo (Tener)',
                rule="The **infinitivo** is the basic, unconjugated verb form ending in **-er** (*tener* = to have). It is central to the essential obligation construction: **tener que + infinitive** (to have to do something).",
                usage_context="Used directly after prepositions, modal verbs of desire (*querer tener*), and periphrastic structures.",
                triggers=['tener que + infinitive', 'querer tener', 'para', 'antes de tener']
            ),
            card2_example=Card2Example(
                target_sentence='Tengo que **tener** mucha paciencia con esta situación difícil.',
                native_sentence='I have to **have** a lot of patience with this difficult situation.',
                breakdown="The main verb **tener** stays in the infinitive because it directly follows the obligation construction *tengo que*."
            ),
            card3_pronunciation=Card3Pronunciation(
                word='tener',
                phonetic_breakdown='te-**NER**',
                stressed_syllables='**NER**',
                audio_text='Tengo que tener mucha paciencia con esta situación.',
                phonetic_tips="Stress lands squarely on the final syllable **NER**. The Spanish 'T' is dental (tongue against upper teeth, unvoiced, no puff of air)."
            ),
            card4_speech=Card4Speech(
                target_phrase='Tengo que tener paciencia.',
                expected_phonetics='[ˈteŋ.ɡo ke teˈneɾ paˈsjen.sja]',
                key_focus_sounds='Dental T and clean soft Spanish R on tener.',
                practice_tip="Keep the 'te' syllable crisp and avoid English-style aspiration."
            ),
            card5_quiz=Card5Quiz(
                sentence_prompt='Ella espera _____ buenas noticias de su familia pronto.',
                options=['tener', 'tiene', 'teniendo', 'tuvo'],
                correct_index=0,
                correct_explanation="¡Correcto! After the verb of desire **espera** (hopes/expects), Spanish requires the unconjugated **infinitive** (*tener*).",
                distractor_explanations={
                    'tiene': "**tiene** is 3rd person singular present; you cannot stack two conjugated verbs.",
                    'teniendo': "**teniendo** is the continuous gerund (having).",
                    'tuvo': "**tuvo** is the simple past (had)."
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: 'Vamos a _____ una fiesta el sábado.'",
                micro_practice_options=['tener', 'tengo', 'tuvo', 'tenemos'],
                micro_practice_correct_index=0,
                micro_practice_explanation="Exact! 'Ir a' + infinitive expresses near future: **tener**."
            ),
            suggested_coach_prompts=[
                "How do I choose between 'tener que' and 'hay que' in everyday conversation?",
                "Why do Spanish speakers use 'tener años' instead of 'ser' for age?",
                "What are the top idiomatic expressions using the verb 'tener'?"
            ]
        ),
        'Gerundio': TenseFlashcardPack(
            tense_name='Gerundio',
            tense_order=2,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — El Gerundio (Teniendo)',
                rule="The **gerundio** of *tener* is **teniendo** (-iendo). It pairs with the auxiliary verb *estar* to emphasize experiences, states, or actions occurring right now.",
                usage_context="Used to describe ongoing experiences or conditions in progress (*estar teniendo*).",
                triggers=['ahora mismo', 'en este momento', 'estar + teniendo', 'últimamente']
            ),
            card2_example=Card2Example(
                target_sentence='Ahora mismo estamos **teniendo** una conversación muy constructiva.',
                native_sentence='Right now we are **having** a very constructive conversation.',
                breakdown="The **-iendo** suffix attaches to root *ten-*, forming the diphthong 'ie' with tonic stress on **NIEN**."
            ),
            card3_pronunciation=Card3Pronunciation(
                word='teniendo',
                phonetic_breakdown='te-**NIEN**-do',
                stressed_syllables='**NIEN**',
                audio_text='Ahora mismo estamos teniendo una conversación constructiva.',
                phonetic_tips="The primary stress is on **NIEN**. Pronounce the 'ie' diphthong as one fluid glide without pausing between 'i' and 'e'."
            ),
            card4_speech=Card4Speech(
                target_phrase='Estamos teniendo una buena semana.',
                expected_phonetics='[esˈta.mos teˈnjen.do ˈu.na ˈbwe.na seˈma.na]',
                key_focus_sounds='Fluid diphthong -nien- in te-nien-do.',
                practice_tip='Keep it strictly three syllables: te-nien-do.'
            ),
            card5_quiz=Card5Quiz(
                sentence_prompt='¿Qué tipo de dificultades estás _____ en tu nuevo trabajo?',
                options=['teniendo', 'tenido', 'tienes', 'tener'],
                correct_index=0,
                correct_explanation="¡Excelente! Following **estás** (continuous auxiliary), the gerund **teniendo** is required.",
                distractor_explanations={
                    'tenido': "**tenido** is the past participle (had).",
                    'tienes': "**tienes** is simple present.",
                    'tener': "**tener** is the infinitive."
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: 'Ellos están _____ mucho éxito.'",
                micro_practice_options=['teniendo', 'tenido', 'tienen', 'tener'],
                micro_practice_correct_index=0,
                micro_practice_explanation="Great job! 'Están' + gerund = **teniendo**."
            ),
            suggested_coach_prompts=[
                "Why do we say 'estamos teniendo' with the 'ie' diphthong?",
                "Can I say 'teniendo en cuenta' to mean 'taking into account'?",
                "What is the difference in nuance between 'tengo dudas' and 'estoy teniendo dudas'?"
            ]
        ),
        'Participio': TenseFlashcardPack(
            tense_name='Participio',
            tense_order=3,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — El Participio (Tenido)',
                rule="The **participio** of *tener* is regular: **tenido** (-ido). It is invariable when combined with the auxiliary **haber** (*he tenido, has tenido, ha tenido*).",
                usage_context="Expresses past experiences or occurrences with continuing relevance in the present.",
                triggers=['alguna vez', 'nunca', 'siempre', 'este año', 'últimamente', 'ya']
            ),
            card2_example=Card2Example(
                target_sentence='Siempre he **tenido** mucha suerte con mis compañeros de trabajo.',
                native_sentence='I have always **had** great luck with my coworkers.',
                breakdown="In Spanish, compound perfect tenses keep the participle ending in **-o** regardless of subject gender or number."
            ),
            card3_pronunciation=Card3Pronunciation(
                word='tenido',
                phonetic_breakdown='te-**NI**-do',
                stressed_syllables='**NI**',
                audio_text='Siempre he tenido mucha suerte.',
                phonetic_tips="Stress is on the penultimate syllable **NI**. The intervocalic 'd' is voiced softly, almost like 'th' in the English word 'other'."
            ),
            card4_speech=Card4Speech(
                target_phrase='Nunca he tenido problemas.',
                expected_phonetics='[ˈnuŋ.ka e teˈni.ðo pɾoˈβle.mas]',
                key_focus_sounds='Silent H in he, soft d in te-ni-do.',
                practice_tip="Link 'he tenido' smoothly as [e te-NI-do]."
            ),
            card5_quiz=Card5Quiz(
                sentence_prompt='Nosotros nunca hemos _____ una oportunidad tan buena.',
                options=['tenido', 'teniendo', 'tenemos', 'tuve'],
                correct_index=0,
                correct_explanation="¡Perfecto! Compound past with 'hemos' strictly requires the past participle **tenido**.",
                distractor_explanations={
                    'teniendo': "**teniendo** is the gerund.",
                    'tenemos': "**tenemos** is simple present.",
                    'tuve': "**tuve** is simple preterite 1st person."
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: '¿Has _____ tiempo de revisar el informe?'",
                micro_practice_options=['tenido', 'tener', 'tienes', 'teniendo'],
                micro_practice_correct_index=0,
                micro_practice_explanation="Spot on! 'Has' + participle = **tenido**."
            ),
            suggested_coach_prompts=[
                "When should I choose 'he tenido' vs 'tuve' when talking about my day?",
                "Does 'tenido' ever change to 'tenida' or 'tenidos'?",
                "Which Spanish-speaking regions prefer 'tuve' over 'he tenido'?"
            ]
        ),
        'Presente de Indicativo': TenseFlashcardPack(
            tense_name='Presente de Indicativo',
            tense_order=4,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — Presente (Tengo, Tienes, Tiene...)',
                rule="In the present indicative, *tener* features a double irregularity: 1st person takes **-go** (**yo tengo**), while *tú, él/ella, ellos* stem-change **e ➔ ie** (**tienes, tiene, tienen**). *Nosotros* and *vosotros* remain regular (**tenemos, tenéis**).",
                usage_context="Used for age (*tengo 25 años*), physical sensations (*tengo hambre/sed*), possession, and obligations.",
                triggers=['hoy', 'siempre', 'normalmente', 'todos los días', 'ahora']
            ),
            card2_example=Card2Example(
                target_sentence='Yo **tengo** dos hermanos y vivimos juntos en el centro de Madrid.',
                native_sentence='I **have** two brothers and we live together in central Madrid.',
                breakdown="Notice the irregular 1st-person 'Yo-Go' ending: *yo tengo* (pattern shared by *hago*, *pongo*, *vengo*)."
            ),
            card3_pronunciation=Card3Pronunciation(
                word='tengo',
                phonetic_breakdown='**TEN**-go',
                stressed_syllables='**TEN**',
                audio_text='Yo tengo dos hermanos en Madrid.',
                phonetic_tips="Tonic stress is on **TEN**. The 'g' before 'o' is a smooth velar [g], exactly like 'go' in English."
            ),
            card4_speech=Card4Speech(
                target_phrase='Yo tengo una buena idea.',
                expected_phonetics='[ˈɟʝo ˈteŋ.ɡo ˈu.na ˈbwe.na iˈðe.a]',
                key_focus_sounds='Clear stress on **TEN**-go.',
                practice_tip="Keep 'yo' light and accent **TEN**-go with confidence."
            ),
            card5_quiz=Card5Quiz(
                sentence_prompt='Yo _____ mucha prisa porque mi tren sale en diez minutos.',
                options=['tengo', 'tiene', 'tienes', 'tenemos'],
                correct_index=0,
                correct_explanation="¡Magnífico! The 1st person singular (yo) in the present tense of tener is **tengo**.",
                distractor_explanations={
                    'tiene': "**tiene** is 3rd person singular (él/ella).",
                    'tienes': "**tienes** is 2nd person singular (tú).",
                    'tenemos': "**tenemos** is 1st person plural (nosotros)."
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: '¿Cuántos años _____ tú?'",
                micro_practice_options=['tienes', 'tengo', 'tiene', 'tenéis'],
                micro_practice_correct_index=0,
                micro_practice_explanation="Correct! With 'tú', use the stem-changed form **tienes**."
            ),
            suggested_coach_prompts=[
                "Why do Spanish speakers say 'tengo hambre' instead of 'estoy hambriento'?",
                "What other Spanish verbs belong to the 'Yo-Go' family?",
                "How does the e-to-ie stem change work for 'tú' and 'él' in the present tense?"
            ]
        ),
        'Pretérito Indefinido': TenseFlashcardPack(
            tense_name='Pretérito Indefinido',
            tense_order=5,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — Pretérito Indefinido (Tuve, Tuviste, Tuvo...)',
                rule="In the simple past (*Pretérito Indefinido*), *tener* undergoes a radical stem mutation to **tuv-** with unstressed personal endings: *yo **tuve**, tú **tuviste**, él **tuvo**, nosotros **tuvimos**, ellos **tuvieron**.",
                usage_context="Used for completed past events or specific moments (*ayer tuve un examen*).",
                triggers=['ayer', 'anoche', 'el año pasado', 'la semana pasada', 'en aquel momento']
            ),
            card2_example=Card2Example(
                target_sentence='Ayer mi amiga **tuvo** una reunión decisiva con el director general.',
                native_sentence='Yesterday my friend **had** a decisive meeting with the managing director.',
                breakdown="Observe the irregular **tuv-** radical in the 3rd person singular **tuvo** (unaccented on the final syllable)."
            ),
            card3_pronunciation=Card3Pronunciation(
                word='tuvo',
                phonetic_breakdown='**TU**-vo',
                stressed_syllables='**TU**',
                audio_text='Ayer mi amiga tuvo una reunión decisiva.',
                phonetic_tips="Tonic stress is on **TU**-vo. In Spanish, 'b' and 'v' share the exact same soft bilabial sound [β]."
            ),
            card4_speech=Card4Speech(
                target_phrase='Ayer tuve mucho trabajo.',
                expected_phonetics='[aˈʝeɾ ˈtu.βe ˈmu.tʃo tɾaˈβa.xo]',
                key_focus_sounds='Tonic on **TU**-ve, soft jota in tra-BA-jo.',
                practice_tip="Stress the first syllable: **TU**-ve, never tu-VE."
            ),
            card5_quiz=Card5Quiz(
                sentence_prompt='El mes pasado nosotros _____ que mudarnos a otra ciudad.',
                options=['tuvimos', 'tenimos', 'tuve', 'tuvieron'],
                correct_index=0,
                correct_explanation="¡Excelente! The subject 'nosotros' in the irregular preterite of tener is **tuvimos**.",
                distractor_explanations={
                    'tenimos': "'tenimos' does not exist; the irregular preterite stem is **tuv-**.",
                    'tuve': "**tuve** is 1st person singular (yo).",
                    'tuvieron': "**tuvieron** is 3rd person plural (ellos/ellas)."
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: '¿_____ tú algún problema ayer?'",
                micro_practice_options=['Tuviste', 'Tuve', 'Tuvo', 'Tuvimos'],
                micro_practice_correct_index=0,
                micro_practice_explanation="Great job! 'Tú' in the preterite of tener is **tuviste**."
            ),
            suggested_coach_prompts=[
                "Why don't irregular preterites like 'tuve' and 'tuvo' take accent marks?",
                "What is the difference between 'tuve un problema' and 'tenía un problema'?",
                "What other Spanish verbs share this -uv- preterite stem (like estar -> estuve, andar -> anduve)?"
            ]
        )
    }

SPANISH_HACER_CURRICULUM = CurriculumCourse(
    topic_id='spanish_hacer',
    title='Spanish: Irregular Verbs — Verbo "Hacer"',
    target_language='Spanish',
    target_language_code='es',
    native_language='English',
    native_language_code='en',
    description="Master the essential Spanish irregular verb 'hacer' (to do / to make) across all core grammatical tenses.",
    tenses_roadmap=['Infinitivo', 'Gerundio', 'Participio', 'Presente de Indicativo', 'Pretérito Indefinido'],
    cards_by_tense=build_spanish_hacer_pack(native_lang='English')
)

SPANISH_TENER_CURRICULUM = CurriculumCourse(
    topic_id='spanish_tener',
    title='Spanish: Irregular Verbs — Verbo "Tener"',
    target_language='Spanish',
    target_language_code='es',
    native_language='English',
    native_language_code='en',
    description="Master the essential Spanish irregular verb 'tener' (to have / to possess) across all core grammatical tenses.",
    tenses_roadmap=['Infinitivo', 'Gerundio', 'Participio', 'Presente de Indicativo', 'Pretérito Indefinido'],
    cards_by_tense=build_spanish_tener_pack(native_lang='English')
)

CURATED_CURRICULA = {
    'spanish_hacer': SPANISH_HACER_CURRICULUM,
    'spanish_tener': SPANISH_TENER_CURRICULUM,
}

COMMON_TOPIC_CATALOG = {
    "Spanish": [
        {
            "verb": "tener",
            "topic": "Spanish: Irregular Verbs — Verbo 'Tener'",
            "meaning": "to have / to hold",
            "category": "Irregular Stem & Yo-Go Verb",
            "pedagogical_hook": "Master essential expressions of necessity ('tener que'), age, and irregular preterite stem 'tuv-'."
        },
        {
            "verb": "ir",
            "topic": "Spanish: Irregular Verbs — Verbo 'Ir'",
            "meaning": "to go",
            "category": "High-Frequency Radical Irregular",
            "pedagogical_hook": "Crucial for everyday travel and near-future phrasing ('ir a + infinitivo')."
        },
        {
            "verb": "ser vs estar",
            "topic": "Spanish: 'Ser' vs 'Estar' (Essentials)",
            "meaning": "to be (essence vs state)",
            "category": "Foundational Verb Pair",
            "pedagogical_hook": "Unlock natural conversational fluency by mastering permanent identity vs transient conditions."
        },
        {
            "verb": "poner",
            "topic": "Spanish: Irregular Verbs — Verbo 'Poner'",
            "meaning": "to put / to place",
            "category": "Yo-Go & Radical Preterite",
            "pedagogical_hook": "Directly related to 'hacer', sharing the 'yo pongo' pattern and preterite stem 'pus-'."
        },
        {
            "verb": "decir",
            "topic": "Spanish: Irregular Verbs — Verbo 'Decir'",
            "meaning": "to say / to tell",
            "category": "E-to-I Stem Changer & Yo-Go",
            "pedagogical_hook": "Indispensable for reporting speech, conversations, and preterite stem 'dij-'."
        },
        {
            "verb": "poder",
            "topic": "Spanish: Irregular Verbs — Verbo 'Poder'",
            "meaning": "to be able to / can",
            "category": "O-to-UE Stem Changer & Modal",
            "pedagogical_hook": "Essential modal verb for expressing possibility, requests, and polite permissions."
        },
        {
            "verb": "querer",
            "topic": "Spanish: Irregular Verbs — Verbo 'Querer'",
            "meaning": "to want / to love",
            "category": "E-to-IE Stem Changer",
            "pedagogical_hook": "Central for expressing desires, intentions, and affection."
        },
        {
            "verb": "saber",
            "topic": "Spanish: Irregular Verbs — Verbo 'Saber'",
            "meaning": "to know facts / skills",
            "category": "Irregular 1st Person & Preterite",
            "pedagogical_hook": "Learn 'yo sé', how to express know-how, and the past meaning change ('found out')."
        },
        {
            "verb": "venir",
            "topic": "Spanish: Irregular Verbs — Verbo 'Venir'",
            "meaning": "to come",
            "category": "Yo-Go & E-to-IE Verb",
            "pedagogical_hook": "Combines Yo-Go with stem changes and radical preterite 'vin-'."
        },
        {
            "verb": "pretérito vs imperfecto",
            "topic": "Spanish: Pretérito Indefinido vs Imperfecto",
            "meaning": "past completed vs past ongoing",
            "category": "Narrative Mastery",
            "pedagogical_hook": "Master the art of storytelling in Spanish: background setting vs completed milestone actions."
        }
    ],
    "Portuguese": [
        {
            "verb": "ter",
            "topic": "Portuguese: Verbo Irregular — 'Ter'",
            "meaning": "to have",
            "category": "Verbo Irregular Essencial",
            "pedagogical_hook": "Fundamental para expressar posse, idade e obrigação ('ter que')."
        },
        {
            "verb": "ir",
            "topic": "Portuguese: Verbo Irregular — 'Ir'",
            "meaning": "to go",
            "category": "Verbo Irregular de Movimento",
            "pedagogical_hook": "Indispensável para expressar deslocamento e o futuro composto ('vou fazer')."
        },
        {
            "verb": "ser vs estar",
            "topic": "Portuguese: 'Ser' vs 'Estar' (Fundamentos)",
            "meaning": "to be (essência vs estado)",
            "category": "Par Verbal Fundamental",
            "pedagogical_hook": "Domine a distinção entre características permanentes e estados temporários."
        },
        {
            "verb": "pôr",
            "topic": "Portuguese: Verbo Irregular — 'Pôr'",
            "meaning": "to put / to place",
            "category": "Verbo Especial da 2ª Conjugação",
            "pedagogical_hook": "Verbo único com radicais irregulares em quase todos os tempos verbais."
        },
        {
            "verb": "dizer",
            "topic": "Portuguese: Verbo Irregular — 'Dizer'",
            "meaning": "to say / to tell",
            "category": "Verbo de Comunicação",
            "pedagogical_hook": "Essencial para relatar diálogos e conversas cotidianas."
        },
        {
            "verb": "poder",
            "topic": "Portuguese: Verbo Irregular — 'Poder'",
            "meaning": "to be able to / can",
            "category": "Verbo Modal",
            "pedagogical_hook": "Permite formular pedidos, expressar capacidade e permissão de forma natural."
        },
        {
            "verb": "vir",
            "topic": "Portuguese: Verbo Irregular — 'Vir'",
            "meaning": "to come",
            "category": "Verbo de Movimento",
            "pedagogical_hook": "Aprenda a diferença entre 'ir' e 'vir' e domine as formas 'venho' e 'vim'."
        },
        {
            "verb": "perfeito vs imperfeito",
            "topic": "Portuguese: Pretérito Perfeito vs Imperfeito",
            "meaning": "passado pontual vs habitual",
            "category": "Narrativa no Passado",
            "pedagogical_hook": "Aprenda a contar histórias com riqueza de detalhes distinguindo ações concluídas e hábitos."
        }
    ],
    "English": [
        {
            "verb": "to be",
            "topic": "English: Irregular Verbs — 'To Be'",
            "meaning": "am / is / are / was / were",
            "category": "Foundational Copular Verb",
            "pedagogical_hook": "The most fundamental irregular verb in English across all persons and tenses."
        },
        {
            "verb": "to have",
            "topic": "English: Irregular Verbs — 'To Have'",
            "meaning": "have / has / had",
            "category": "Possession & Auxiliary Verb",
            "pedagogical_hook": "Essential for everyday possession and forming all perfect tenses (e.g., 'have done')."
        },
        {
            "verb": "to go",
            "topic": "English: Irregular Verbs — 'To Go'",
            "meaning": "go / went / gone",
            "category": "Radical Movement Verb",
            "pedagogical_hook": "Master 'went' vs 'gone' and common idiomatic phrasal verbs."
        },
        {
            "verb": "to see",
            "topic": "English: Irregular Verbs — 'To See'",
            "meaning": "see / saw / seen",
            "category": "Perception Verb",
            "pedagogical_hook": "Crucial for everyday conversation and perfect tense usage."
        },
        {
            "verb": "to take",
            "topic": "English: Irregular Verbs — 'To Take'",
            "meaning": "take / took / taken",
            "category": "High-Frequency Transitive",
            "pedagogical_hook": "Key building block for dozens of common phrasal verbs (take off, take up, take on)."
        }
    ]
}

def get_recommended_next_topics(
    target_lang: str,
    current_topic: str,
    studied_topics: List[str],
    count: int = 3,
    shuffle: bool = False,
    seed: Optional[int] = None,
) -> List[Dict[str, str]]:
    """
    Selects recommended next topics for the given target language that have not yet been studied.
    Excludes the current topic and any topic previously recorded as studied.
    Supports optional shuffling for variety.
    """
    catalog = COMMON_TOPIC_CATALOG.get(target_lang, COMMON_TOPIC_CATALOG.get("Spanish", []))
    studied_lower = [t.lower().strip() for t in (studied_topics or [])]
    current_lower = current_topic.lower().strip()

    def _matches_topic(verb: str, topic_title: str, text: str) -> bool:
        if not text:
            return False
        if topic_title.lower().strip() == text:
            return True
        words = re.findall(r'\w+', verb.lower())
        if not words:
            return False
        return all(re.search(r'\b' + re.escape(w) + r'\b', text, re.IGNORECASE) for w in words)

    unstudied = []
    for item in catalog:
        item_topic = item["topic"]
        item_verb = item["verb"]
        if _matches_topic(item_verb, item_topic, current_lower):
            continue
        if any(_matches_topic(item_verb, item_topic, s) for s in studied_lower):
            continue
        unstudied.append(dict(item))

    if not unstudied:
        unstudied = [
            dict(item) for item in catalog
            if not _matches_topic(item["verb"], item["topic"], current_lower)
        ]

    if shuffle:
        rng = random.Random(seed)
        rng.shuffle(unstudied)

    return unstudied[:count]



def get_curriculum_or_fallback(topic_query: str = '', *args, **kwargs) -> CurriculumCourse:
    target_lang = kwargs.get('target_lang', 'Spanish')
    native_lang = kwargs.get('native_lang', 'English')
    if len(args) == 1:
        val = str(args[0]).strip()
        if 'portugu' in val.lower() or 'english' in val.lower():
            native_lang = val
        else:
            target_lang = val
    elif len(args) >= 2:
        target_lang = str(args[0]).strip()
        native_lang = str(args[1]).strip()

    t_lower = (topic_query or '').lower()

    if "tener" in t_lower:
        cards = build_spanish_tener_pack(native_lang=native_lang)
        desc = "Domine o verbo irregular 'tener' (ter) em espanhol passo a passo." if 'portugu' in native_lang.lower() else "Master the essential Spanish irregular verb 'tener' (to have / to possess) across all core grammatical tenses."
        return CurriculumCourse(
            topic_id='spanish_tener',
            title='Spanish: Irregular Verbs — Verbo "Tener"',
            target_language=target_lang or 'Spanish',
            target_language_code='es',
            native_language=native_lang,
            native_language_code='pt' if 'portugu' in native_lang.lower() else 'en',
            description=desc,
            tenses_roadmap=['Infinitivo', 'Gerundio', 'Participio', 'Presente de Indicativo', 'Pretérito Indefinido'],
            cards_by_tense=cards
        )

    cards = build_spanish_hacer_pack(native_lang=native_lang)
    desc = f"Domine o verbo irregular 'hacer' (fazer) em espanhol passo a passo." if 'portugu' in native_lang.lower() else f"Master the essential Spanish irregular verb 'hacer' (to do / to make) across all core grammatical tenses."
    return CurriculumCourse(
        topic_id='spanish_hacer',
        title='Spanish: Irregular Verbs — Verbo "Hacer"',
        target_language=target_lang or 'Spanish',
        target_language_code='es',
        native_language=native_lang,
        native_language_code='pt' if 'portugu' in native_lang.lower() else 'en',
        description=desc,
        tenses_roadmap=['Infinitivo', 'Gerundio', 'Participio', 'Presente de Indicativo', 'Pretérito Indefinido'],
        cards_by_tense=cards
    )

