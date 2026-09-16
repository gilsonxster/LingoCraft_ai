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
    conjugation_header: Optional[str] = None
    conjugations: List[str] = field(default_factory=list)

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

    def __post_init__(self):
        if self.target_phrase:
            self.target_phrase = re.sub(r'[*_~`]', '', self.target_phrase).strip()

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

def _add_pack_aliases(packs: Dict[str, TenseFlashcardPack]) -> Dict[str, TenseFlashcardPack]:
    """Expands tense pack dictionary with common canonical aliases."""
    alias_map = {
        'Condicional Simple': ['Condicional', 'Condicional Simple de Indicativo', 'Condicional de Indicativo'],
        'Pretérito Imperfecto': ['Pretérito Imperfecto de Indicativo', 'Imperfecto', 'Copretérito'],
        'Futuro Simple': ['Futuro', 'Futuro Simple de Indicativo'],
        'Futuro Próximo': ['Futuro Inmediato', 'Ir a + Infinitivo', 'Futuro Proximo'],
        'Presente de Subjuntivo': ['Presente Subjuntivo', 'Subjuntivo'],
        'Presente de Indicativo': ['Presente', 'Presente Indicativo'],
        'Pretérito Indefinido': ['Pretérito', 'Pretérito Indefinido de Indicativo', 'Indefinido', 'Pasado Simple']
    }
    result = dict(packs)
    for canonical_name, aliases in alias_map.items():
        if canonical_name in packs:
            for al in aliases:
                if al not in result:
                    result[al] = packs[canonical_name]
    return result

def build_spanish_hacer_pack(native_lang: str = "English") -> Dict[str, TenseFlashcardPack]:
    lang = native_lang.lower()
    is_pt = "portugu" in lang
    is_es = "español" in lang or "spanish" in lang

    if is_pt:
        return _add_pack_aliases({
            'Infinitivo': TenseFlashcardPack(
                tense_name='Infinitivo',
                tense_order=1,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — El Infinitivo (Hacer)',
                    rule='O **infinitivo** é a forma básica não conjugada do verbo terminando em **-er**. Em espanhol, atua como substantivo verbal e é usado diretamente após preposições, verbos modais ou perífrases verbais.',
                    usage_context='Usado quando a ação é descrita em abstrato ou diretamente regida por outro verbo conjugado (ex.: *querer hacer*, *tener que hacer*).',
                    triggers=['tener que + infinitivo', 'querer + infinitivo', 'antes de', 'después de', 'para'],
                    conjugation_header='Estruturas essenciais com o infinitivo (perífrases verbais):',
                    conjugations=[
                        'tener que + hacer (ter que fazer / obrigação)',
                        'ir a + hacer (ir fazer / futuro imediato)',
                        'querer + hacer (querer fazer / intenção e desejo)',
                        'poder + hacer (poder fazer / capacidade e permissão)',
                        'antes de + hacer (antes de fazer / sequência temporal)',
                        'para + hacer (para fazer / finalidade e propósito)'
                    ]

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
                    triggers=['estar + gerundio', 'ahora mismo', 'en este momento', 'actualmente'],
                    conjugation_header='A conjugação contínua é muito comum (estar + gerundio):',
                    conjugations=[
                        'yo estoy haciendo (eu estou fazendo)',
                        'tú estás haciendo (tu estás fazendo / você está fazendo)',
                        'él/ella/usted está haciendo (ele/ela/você está fazendo)',
                        'nosotros/as estamos haciendo (nós estamos fazendo)',
                        'vosotros/as estáis haciendo (vós estais fazendo)',
                        'ellos/ellas/ustedes están haciendo (eles/elas/vocês estão fazendo)'
                    ]
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
                    "Qual é a diferença de sentido entre 'hago ejercicio' e 'estoy haciendo exercício'?",
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
                    triggers=['haber + hecho', 'ya', 'todavía no', 'alguna vez', 'nunca'],
                    conjugation_header='A conjugação composta perfeita (haber + participio):',
                    conjugations=[
                        'yo he hecho (eu fiz / tenho feito)',
                        'tú has hecho (tu fizeste / você fez)',
                        'él/ella/usted ha hecho (ele/ela/você fez)',
                        'nosotros/as hemos hecho (nós fizemos / temos feito)',
                        'vosotros/as habéis hecho (vós fizestes)',
                        'ellos/ellas/ustedes han hecho (eles/elas/vocês fizeram)'
                    ]
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
                    triggers=['siempre', 'todos los días', 'frecuentemente', 'cada mañana', 'hace calor/frío'],
                    conjugation_header='A conjugação é bastante irregular, mas muito comum:',
                    conjugations=[
                        'yo hago (eu faço)',
                        'tú haces (tu fazes / você faz)',
                        'él/ella/usted hace (ele/ela/você faz)',
                        'nosotros/as hacemos (nós fazemos)',
                        'vosotros/as hacéis (vós fazeis)',
                        'ellos/ellas/ustedes hacen (eles/elas/vocês fazem)'
                    ]
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
                    triggers=['ayer', 'anoche', 'la semana pasada', 'el año pasado', 'hace dos días'],
                    conjugation_header='A conjugação no pretérito simples muda para o radical hic- / hiz-:',
                    conjugations=[
                        'yo hice (eu fiz)',
                        'tú hiciste (tu fizeste / você fez)',
                        'él/ella/usted hizo (ele/ela/você fez)',
                        'nosotros/as hicimos (nós fizemos)',
                        'vosotros/as hicisteis (vós fizestes)',
                        'ellos/ellas/ustedes hicieron (eles/elas/vocês fizeram)'
                    ]
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
            ),
            'Pretérito Imperfecto': TenseFlashcardPack(
                tense_name='Pretérito Imperfecto',
                tense_order=6,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — Pretérito Imperfecto (Hacía, Hacías...)',
                    rule='No **Pretérito Imperfeito**, *hacer* mantém o radical regular **hac-** e recebe as desinências regulares de verbos em -er com acento gráfico obrigatório no **í**: *-ía, -ías, -ía, -íamos, -íais, -ían*.',
                    usage_context='Usado para hábitos no passado, ações repetidas ou contínuas e para expressar condições meteorológicas no passado (*hacía frío, hacía sol*).',
                    triggers=['cuando era niño/a', 'antes', 'siempre', 'hacía frío/calor', 'todos los días', 'mientras'],
                    conjugation_header='A conjugação no pretérito imperfeito é regular sobre o radical hac-:',
                    conjugations=[
                        'yo hacía (eu fazia)',
                        'tú hacías (tu fazias / você fazia)',
                        'él/ella/usted hacía (ele/ela/você fazia)',
                        'nosotros/as hacíamos (nós fazíamos)',
                        'vosotros/as hacíais (vós fazíeis)',
                        'ellos/ellas/ustedes hacían (eles/elas/vocês faziam)'
                    ]
                ),
                card2_example=Card2Example(
                    target_sentence='En aquella época, yo **hacía** deporte todas las tardes después de la escuela.',
                    native_sentence='Naquela época, eu **fazia** esportes todas as tardes depois da escola.',
                    breakdown='O verbo **hacía** expressa uma rotina habitual que se estendia no passado sem marcar início nem fim pontual.'
                ),
                card3_pronunciation=Card3Pronunciation(
                    word='hacía',
                    phonetic_breakdown='ha-**CÍ**-a',
                    stressed_syllables='**CÍ**',
                    audio_text='En aquella época yo hacía deporte todas las tardes.',
                    phonetic_tips='O H inicial é completamente mudo. O acento no í quebra o encontro vocálico: ha-CÍ-a.'
                ),
                card4_speech=Card4Speech(
                    target_phrase='Yo hacía deporte todas las tardes.',
                    expected_phonetics='[ɟʝo aˈsi.a ðeˈpoɾ.te ˈto.ðas las ˈtaɾ.ðes]',
                    key_focus_sounds='H mudo em hacía, tônica no CÍ.',
                    practice_tip='Pronuncie três sílabas claras: ha-CÍ-a.'
                ),
                card5_quiz=Card5Quiz(
                    sentence_prompt='Ayer mientras caminábamos por la montaña, _____ mucho frío y viento.',
                    options=['hacía', 'hizo', 'hace', 'haría'],
                    correct_index=0,
                    correct_explanation='¡Perfecto! Para descrever o cenário climático contínuo no passado (*mientras caminábamos*), usa-se o imperfeito: **hacía**.',
                    distractor_explanations={
                        'hizo': 'hizo marca uma ação pontual delimitada no tempo.',
                        'hace': 'hace é o presente do indicativo.',
                        'haría': 'haría é o condicional simples.'
                    },
                    micro_practice_prompt="Micro-Prática: Complete: 'Nosotros _____ los deberes juntos todos los veranos.'",
                    micro_practice_options=['hacíamos', 'hicimos', 'hacemos', 'hagamos'],
                    micro_practice_correct_index=0,
                    micro_practice_explanation="Exato! Nós no imperfeito é **hacíamos**."
                ),
                suggested_coach_prompts=[
                    "Por que se diz 'hacía frío' no passado em vez de 'estaba frío'?",
                    "Qual a diferença de sentido entre 'ayer hice una tarta' e 'antes hacía tartas'?",
                    "Por que todas as pessoas do pretérito imperfeito em -er levam acento no 'í'?"
                ]
            ),
            'Futuro Próximo': TenseFlashcardPack(
                tense_name='Futuro Próximo',
                tense_order=7,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — Futuro Próximo (Voy a hacer...)',
                    rule='O **Futuro Próximo** é construído com a perífrase **ir (no presente) + a + infinitivo (hacer)**. É a estrutura mais espontânea e frequente no espanhol falado para ações planejadas.',
                    usage_context='Usado para intenções imediatas, planos próximos e previsões baseadas em acontecimentos presentes.',
                    triggers=['mañana', 'esta tarde', 'este fin de semana', 'pronto', 'voy a'],
                    conjugation_header='A conjugação no futuro próximo (ir a + hacer):',
                    conjugations=[
                        'yo voy a hacer (eu vou fazer)',
                        'tú vas a hacer (tu vais fazer / você vai fazer)',
                        'él/ella/usted va a hacer (ele/ela/você vai fazer)',
                        'nosotros/as vamos a hacer (nós vamos fazer)',
                        'vosotros/as vais a hacer (vós ides fazer)',
                        'ellos/ellas/ustedes van a hacer (eles/elas/vocês vão fazer)'
                    ]
                ),
                card2_example=Card2Example(
                    target_sentence='Esta noche **voy a hacer** una cena especial para mis amigos.',
                    native_sentence='Esta noite **vou fazer** um jantar especial para os meus amigos.',
                    breakdown='Apenas o auxiliar ir conjuga (**voy**), seguido da preposição obrigatória **a** e do infinitivo base (**hacer**).'
                ),
                card3_pronunciation=Card3Pronunciation(
                    word='voy a hacer',
                    phonetic_breakdown='voy a ha-**CER**',
                    stressed_syllables='**CER**',
                    audio_text='Esta noche voy a hacer una cena especial.',
                    phonetic_tips='Ligue as palavras em um fluxo contínuo: [bo-ja-a-SER].'
                ),
                card4_speech=Card4Speech(
                    target_phrase='Esta noche voy a hacer la cena.',
                    expected_phonetics='[ˈes.ta ˈno.tʃe ˈβoj a aˈseɾ la ˈse.na]',
                    key_focus_sounds='Fusão vogal voy a a-ser, r suave final.',
                    practice_tip='Conecte voy a hacer sem hesitação.'
                ),
                card5_quiz=Card5Quiz(
                    sentence_prompt='¿Qué _____ tú mañana por la tarde?',
                    options=['vas a hacer', 'va a hacer', 'vais hacer', 'voy a hacer'],
                    correct_index=0,
                    correct_explanation='¡Excelente! Com o pronome tú, a fórmula de futuro próximo exige: **vas a hacer**.',
                    distractor_explanations={
                        'va a hacer': 'va a hacer corresponde a él/ella/usted.',
                        'vais hacer': 'Falta a preposição obrigatória a.',
                        'voy a hacer': 'voy corresponde a yo.'
                    },
                    micro_practice_prompt="Micro-Prática: Complete: 'Nosotros _____ las maletas ahora mismo.'",
                    micro_practice_options=['vamos a hacer', 'van a hacer', 'vamos hacer', 'vamos a hacíamos'],
                    micro_practice_correct_index=0,
                    micro_practice_explanation="Correto! Com nosotros usa-se **vamos a hacer**."
                ),
                suggested_coach_prompts=[
                    "Por que nunca se pode omitir a preposição 'a' em 'ir a + infinitivo'?",
                    "Quando usar 'voy a hacer' em vez de 'haré' na conversação real?",
                    "Como pronunciar 'voy a hacer' rápido com ritmo natural?"
                ]
            ),
            'Futuro Simple': TenseFlashcardPack(
                tense_name='Futuro Simple',
                tense_order=8,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — Futuro Simple (Haré, Harás...)',
                    rule='No **Futuro Simples**, *hacer* sofre contração sincopada irregular: o radical reduz-se a **har-** (perde o som -ce-). As desinências recebem acento gráfico: *-é, -ás, -á, -emos, -éis, -án*.',
                    usage_context='Usado para planos a longo prazo, promessas formais e expressar probabilidade/suposição no presente (*¿Dónde está María? Hará las compras*).',
                    triggers=['el año que viene', 'en el futuro', 'algún día', 'seguramente', 'probablemente', 'mañana'],
                    conjugation_header='A conjugação no futuro simples sofre síncope para o radical har-:',
                    conjugations=[
                        'yo haré (eu farei)',
                        'tú harás (tu farás / você fará)',
                        'él/ella/usted hará (ele/ela/você fará)',
                        'nosotros/as haremos (nós faremos)',
                        'vosotros/as haréis (vós fareis)',
                        'ellos/ellas/ustedes harán (eles/elas/vocês farão)'
                    ]
                ),
                card2_example=Card2Example(
                    target_sentence='Te prometo que mañana **haré** todo lo posible para ayudarte.',
                    native_sentence='Te prometo que amanhã **farei** todo o possível para te ajudar.',
                    breakdown='Observe a raiz contraída **har-** com terminação oxítona acentuada **-é** (**haré**).'
                ),
                card3_pronunciation=Card3Pronunciation(
                    word='haré',
                    phonetic_breakdown='ha-**RÉ**',
                    stressed_syllables='**RÉ**',
                    audio_text='Te prometo que mañana haré todo lo posible.',
                    phonetic_tips='H mudo e tônica forte na última sílaba: ha-RÉ.'
                ),
                card4_speech=Card4Speech(
                    target_phrase='Mañana haré todo lo posible.',
                    expected_phonetics='[maˈɲa.na aˈɾe ˈto.ðo lo poˈsi.βle]',
                    key_focus_sounds='Tônica em ha-RÉ, r brando.',
                    practice_tip='Diga com convicção na última sílaba: ha-RÉ.'
                ),
                card5_quiz=Card5Quiz(
                    sentence_prompt='El próximo mes el nuevo director _____ cambios importantes en la empresa.',
                    options=['hará', 'hacerá', 'hace', 'haría'],
                    correct_index=0,
                    correct_explanation='¡Brillante! A 3ª pessoa do singular no futuro simples com raiz sincopada har- é **hará**.',
                    distractor_explanations={
                        'hacerá': 'Não existe hacerá! O verbo fazer sofre síncope radical: hará.',
                        'hace': 'hace é o presente do indicativo.',
                        'haría': 'haría é o condicional simples.'
                    },
                    micro_practice_prompt="Micro-Prática: Complete: '¿Qué _____ vosotros cuando lleguéis a Madrid?'",
                    micro_practice_options=['haréis', 'haceréis', 'harán', 'hacéis'],
                    micro_practice_correct_index=0,
                    micro_practice_explanation="Perfeito! Vosotros no futuro simples é **haréis**."
                ),
                suggested_coach_prompts=[
                    "Por que o radical de 'hacer' encolhe para 'har-' no futuro simples?",
                    "Como expressar dúvida no presente usando 'hará' (ex.: ¿qué hora será/hará)?",
                    "Qual a diferença entre prometer com 'haré' vs 'voy a hacer'?"
                ]
            ),
            'Condicional Simple': TenseFlashcardPack(
                tense_name='Condicional Simple',
                tense_order=9,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — El Condicional Simple (Haría, Harías...)',
                    rule='No **Condicional Simples**, *hacer* utiliza o mesmo radical sincopado do futuro (**har-**), seguido das terminações regulares com acento no **í**: *-ía, -ías, -ía, -íamos, -íais, -ían*.',
                    usage_context='Usado para conselhos delicados (*yo en tu lugar haría esto*), hipóteses irreais e pedidos com cortesia e polidez.',
                    triggers=['si pudiera...', 'yo en tu lugar', 'me gustaría', 'probablemente', 'yo que tú', 'por favor'],
                    conjugation_header='A conjugação no condicional simples usa o radical har- e terminações em -ía:',
                    conjugations=[
                        'yo haría (eu faria)',
                        'tú harías (tu farias / você faria)',
                        'él/ella/usted haría (ele/ela/você faria)',
                        'nosotros/as haríamos (nós faríamos)',
                        'vosotros/as haríais (vós faríeis)',
                        'ellos/ellas/ustedes harían (eles/elas/vocês fariam)'
                    ]
                ),
                card2_example=Card2Example(
                    target_sentence='Yo en tu lugar **haría** las cosas de otra manera.',
                    native_sentence='Eu no seu lugar **faria** as coisas de outra maneira.',
                    breakdown='O condicional **haría** atenua conselhos tornando a sugestão educada e ponderada.'
                ),
                card3_pronunciation=Card3Pronunciation(
                    word='haría',
                    phonetic_breakdown='ha-**RÍ**-a',
                    stressed_syllables='**RÍ**',
                    audio_text='Yo en tu lugar haría las cosas de otra manera.',
                    phonetic_tips='H mudo e hiato nítido em ha-RÍ-a.'
                ),
                card4_speech=Card4Speech(
                    target_phrase='Yo en tu lugar haría las cosas bien.',
                    expected_phonetics='[ɟʝo en tu luˈɣaɾ aˈɾi.a las ˈko.sas ˈbjen]',
                    key_focus_sounds='Hiato em ha-RÍ-a, fluidez ao falar.',
                    practice_tip='Separe as sílabas com suavidade: ha-RÍ-a.'
                ),
                card5_quiz=Card5Quiz(
                    sentence_prompt='Si tuviéramos más presupuesto, nosotros _____ un viaje inolvidable.',
                    options=['haríamos', 'hacíamos', 'hicimos', 'haremos'],
                    correct_index=0,
                    correct_explanation='¡Perfecto! Na consequência da oração condicional hipotética (*si tuviéramos...*), usa-se o condicional simples: **haríamos**.',
                    distractor_explanations={
                        'hacíamos': 'hacíamos é o pretérito imperfeito do indicativo.',
                        'hicimos': 'hicimos é o pretérito indefinido.',
                        'haremos': 'haremos é o futuro simples.'
                    },
                    micro_practice_prompt="Micro-Prática: Complete: '¿Nos _____ tú el favor de cerrar la puerta?'",
                    micro_practice_options=['harías', 'hiciste', 'haces', 'hagas'],
                    micro_practice_correct_index=0,
                    micro_practice_explanation="Muito bem! Para pedidos cordiais com tú, usa-se **harías**."
                ),
                suggested_coach_prompts=[
                    "Como usar o condicional simples 'haría' para fazer pedidos com máxima cortesia?",
                    "Qual a diferença entre 'yo hacía' (imperfeito) e 'yo haría' (condicional)?",
                    "Por que 'hacer' e 'tener' compartilham a mesma terminação '-ía' no condicional?"
                ]
            ),
            'Presente de Subjuntivo': TenseFlashcardPack(
                tense_name='Presente de Subjuntivo',
                tense_order=10,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — Presente de Subjuntivo (Haga, Hagas...)',
                    rule='O **Presente de Subjuntivo** de *hacer* é formado a partir do radical irregular da 1ª pessoa do presente do indicativo (**hag-** de *yo hago*), adotando a vogal temática oposta **-a-**: *haga, hagas, haga, hagamos, hagáis, hagan*.',
                    usage_context='Usado após expressões de desejo, conselho, dúvida, necessidade impessoal (*es necesario que hagas esto*) ou orações concessivas.',
                    triggers=['ojalá que', 'es necesario que', 'quiero que', 'dudo que', 'para que', 'es mejor que'],
                    conjugation_header='A conjugação no presente do subjuntivo baseia-se no radical hag-:',
                    conjugations=[
                        'que yo haga (que eu faça)',
                        'que tú hagas (que tu faças / você faça)',
                        'que él/ella/usted haga (que ele/ela/você faça)',
                        'nosotros/as hagamos (que nós façamos)',
                        'vosotros/as hagáis (que vós façais)',
                        'ellos/ellas/ustedes hagan (que eles/elas/vocês façam)'
                    ]
                ),
                card2_example=Card2Example(
                    target_sentence='Es muy importante que tú **hagas** la tarea antes de la clase.',
                    native_sentence='É muito importante que você **faça** a lição de casa antes da aula.',
                    breakdown='A oração impessoal valorativa (*es importante que*) governa o modo subjuntivo (**hagas**).'
                ),
                card3_pronunciation=Card3Pronunciation(
                    word='hagas',
                    phonetic_breakdown='**HA**-gas',
                    stressed_syllables='**HA**',
                    audio_text='Es muy importante que tú hagas la tarea.',
                    phonetic_tips='H mudo e g suave antes de a: HA-gas.'
                ),
                card4_speech=Card4Speech(
                    target_phrase='Espero que hagas un buen trabajo.',
                    expected_phonetics='[esˈpe.ɾo ke ˈa.ɣas um bwen tɾaˈβa.xo]',
                    key_focus_sounds='Tônica em **HA**-gas, g suave.',
                    practice_tip='Mantenha as vogais abertas e sonoras.'
                ),
                card5_quiz=Card5Quiz(
                    sentence_prompt='El médico me recomendó que yo _____ ejercicio moderado cada día.',
                    options=['haga', 'hago', 'hace', 'hiciera'],
                    correct_index=0,
                    correct_explanation='¡Extraordinario! Após recomendação (*recomendó que*), o verbo exige o subjuntivo: **haga**.',
                    distractor_explanations={
                        'hago': 'hago é o presente do indicativo, inadequado no contexto subjuntivo.',
                        'hace': 'hace é 3ª pessoa do indicativo.',
                        'hiciera': 'hiciera é o imperfeito do subjuntivo.'
                    },
                    micro_practice_prompt="Micro-Prática: Complete: 'Ojalá que el profesor no nos _____ un examen sorpresa.'",
                    micro_practice_options=['haga', 'hace', 'hizo', 'hará'],
                    micro_practice_correct_index=0,
                    micro_practice_explanation="Correto! Após ojalá que usa-se o presente do subjuntivo: **haga**."
                ),
                suggested_coach_prompts=[
                    "Por que a 'regra do Yo' (yo hago -> hag-) é essencial para o subjuntivo?",
                    "Quais orações com 'que' sempre ativam o subjuntivo 'haga'?",
                    "Como usar 'haga lo que haga' para expressar concessão em espanhol?"
                ]
            )
        })

    # Default English Explanations
    return _add_pack_aliases({
        'Infinitivo': TenseFlashcardPack(
            tense_name='Infinitivo',
            tense_order=1,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — El Infinitivo (Hacer)',
                rule='The **infinitivo** is the unconjugated base dictionary form of the verb ending in **-er**. In Spanish, it acts as a verbal noun and is used directly after prepositions, modal auxiliary verbs, or verbal periphrases.',
                usage_context='Used whenever an action is described in the abstract or directly governed by another conjugated verb (e.g., *querer hacer*, *tener que hacer*).',
                triggers=['tener que + infinitivo', 'querer + infinitivo', 'antes de', 'después de', 'para'],
                conjugation_header='Essential structures with the infinitive (verbal periphrases):',
                conjugations=[
                    'tener que + hacer (have to do / obligation)',
                    'ir a + hacer (going to do / immediate future)',
                    'querer + hacer (want to do / desire)',
                    'poder + hacer (can do / ability)',
                    'antes de + hacer (before doing / sequence)',
                    'para + hacer (in order to do / purpose)'
                ]

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
                triggers=['estar + gerundio', 'ahora mismo', 'en este momento', 'actualmente'],
                conjugation_header='The continuous progressive conjugation (estar + gerund):',
                conjugations=[
                    'yo estoy haciendo (I am doing / making)',
                    'tú estás haciendo (you are doing / making)',
                    'él/ella/usted está haciendo (he/she/you formal is doing / making)',
                    'nosotros/as estamos haciendo (we are doing / making)',
                    'vosotros/as estáis haciendo (you all are doing / making)',
                    'ellos/ellas/ustedes están haciendo (they/you all formal are doing / making)'
                ]
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
                triggers=['haber + hecho', 'ya', 'todavía no', 'alguna vez', 'nunca'],
                conjugation_header='The compound perfect conjugation (haber + participle):',
                conjugations=[
                    'yo he hecho (I have done / made)',
                    'tú has hecho (you have done / made)',
                    'él/ella/usted ha hecho (he/she/you formal has done / made)',
                    'nosotros/as hemos hecho (we have done / made)',
                    'vosotros/as habéis hecho (you all have done / made)',
                    'ellos/ellas/ustedes han hecho (they/you all formal have done / made)'
                ]
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
                triggers=['siempre', 'todos los días', 'frecuentemente', 'cada mañana', 'hace calor/frío'],
                conjugation_header='The conjugation has an irregular 1st person (Yo-Go), essential in daily Spanish:',
                conjugations=[
                    'yo hago (I do / make)',
                    'tú haces (you do / make)',
                    'él/ella/usted hace (he/she/you formal does / makes)',
                    'nosotros/as hacemos (we do / make)',
                    'vosotros/as hacéis (you all do / make)',
                    'ellos/ellas/ustedes hacen (they/you all formal do / make)'
                ]
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
                triggers=['ayer', 'anoche', 'la semana pasada', 'el año pasado', 'hace dos días'],
                conjugation_header='The simple preterite conjugation mutates to the stem hic- / hiz-:',
                conjugations=[
                    'yo hice (I did / made)',
                    'tú hiciste (you did / made)',
                    'él/ella/usted hizo (he/she/you formal did / made)',
                    'nosotros/as hicimos (we did / made)',
                    'vosotros/as hicisteis (you all did / made)',
                    'ellos/ellas/ustedes hicieron (they/you all formal did / made)'
                ]
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
        ),
        'Pretérito Imperfecto': TenseFlashcardPack(
            tense_name='Pretérito Imperfecto',
            tense_order=6,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — Pretérito Imperfecto (Hacía, Hacías...)',
                rule='In the **Pretérito Imperfecto**, *hacer* is regular on the stem **hac-**: all forms take the standard accented endings *-ía, -ías, -ía, -íamos, -íais, -ían*.',
                usage_context='Used for habitual past routines, ongoing background actions, and weather in the past (*hacía frío*, *hacía sol*).',
                triggers=['cuando era niño/a', 'antes', 'siempre', 'hacía frío/calor', 'todos los días', 'mientras'],
                conjugation_header='The imperfect tense uses regular -ía endings on the stem hac-:',
                conjugations=[
                    'yo hacía (I did / was doing / used to do)',
                    'tú hacías (you did / were doing / used to do)',
                    'él/ella/usted hacía (he/she/you formal did / was doing / used to do)',
                    'nosotros/as hacíamos (we did / were doing / used to do)',
                    'vosotros/as hacíais (you all did / were doing / used to do)',
                    'ellos/ellas/ustedes hacían (they/you all formal did / were doing / used to do)'
                ]
            ),
            card2_example=Card2Example(
                target_sentence='En aquella época, yo **hacía** deporte todas las tardes después de la escuela.',
                native_sentence='Back then, I **used to play** sports every afternoon after school.',
                breakdown='The verb **hacía** conveys habitual routine in the past without a defined starting or ending point.'
            ),
            card3_pronunciation=Card3Pronunciation(
                word='hacía',
                phonetic_breakdown='ha-**CÍ**-a',
                stressed_syllables='**CÍ**',
                audio_text='En aquella época yo hacía deporte todas las tardes.',
                phonetic_tips='Silent initial H. Accent mark on í splits the vowels into a hiatus: ha-CÍ-a.'
            ),
            card4_speech=Card4Speech(
                target_phrase='Yo hacía deporte todas las tardes.',
                expected_phonetics='[ɟʝo aˈsi.a ðeˈpoɾ.te ˈto.ðas las ˈtaɾ.ðes]',
                key_focus_sounds='Silent H in hacía, stress on CÍ.',
                practice_tip='Pronounce three distinct syllables: ha-CÍ-a.'
            ),
            card5_quiz=Card5Quiz(
                sentence_prompt='Ayer mientras caminábamos por la montaña, _____ mucho frío y viento.',
                options=['hacía', 'hizo', 'hace', 'haría'],
                correct_index=0,
                correct_explanation='¡Perfecto! To describe ongoing background weather in the past (*mientras caminábamos*), Spanish uses the imperfect: **hacía**.',
                distractor_explanations={
                    'hizo': 'hizo expresses a single completed event in the past.',
                    'hace': 'hace is simple present.',
                    'haría': 'haría is conditional simple.'
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: 'Nosotros _____ los deberes juntos todos los veranos.'",
                micro_practice_options=['hacíamos', 'hicimos', 'hacemos', 'hagamos'],
                micro_practice_correct_index=0,
                micro_practice_explanation="Correct! We in the imperfect is **hacíamos**."
            ),
            suggested_coach_prompts=[
                "Why do Spanish speakers say 'hacía frío' instead of 'estaba frío'?",
                "What is the nuance difference between 'ayer hice' and 'antes hacía'?",
                "Why do all imperfect endings for -er verbs take an accent mark on the 'í'?"
            ]
        ),
        'Futuro Próximo': TenseFlashcardPack(
            tense_name='Futuro Próximo',
            tense_order=7,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — Futuro Próximo (Voy a hacer...)',
                rule='The **Futuro Próximo** combines **ir (present) + a + infinitivo (hacer)**. It is the dominant natural way in daily conversation to discuss immediate upcoming actions.',
                usage_context='Used for immediate intentions, scheduled plans, and predictions grounded in present observation.',
                triggers=['mañana', 'esta tarde', 'este fin de semana', 'pronto', 'voy a'],
                conjugation_header='The near future structure (ir a + hacer):',
                conjugations=[
                    'yo voy a hacer (I am going to do / make)',
                    'tú vas a hacer (you are going to do / make)',
                    'él/ella/usted va a hacer (he/she/you formal is going to do / make)',
                    'nosotros/as vamos a hacer (we are going to do / make)',
                    'vosotros/as vais a hacer (you all are going to do / make)',
                    'ellos/ellas/ustedes van a hacer (they/you all formal are going to do / make)'
                ]
            ),
            card2_example=Card2Example(
                target_sentence='Esta noche **voy a hacer** una cena especial para mis amigos.',
                native_sentence='Tonight I am **going to make** a special dinner for my friends.',
                breakdown='Only auxiliary ir conjugates (**voy**); **hacer** stays in the base infinitive following the preposition **a**.'
            ),
            card3_pronunciation=Card3Pronunciation(
                word='voy a hacer',
                phonetic_breakdown='voy a ha-**CER**',
                stressed_syllables='**CER**',
                audio_text='Esta noche voy a hacer una cena especial.',
                phonetic_tips='Glide smoothly across the words: [bo-ja-a-SER].'
            ),
            card4_speech=Card4Speech(
                target_phrase='Esta noche voy a hacer la cena.',
                expected_phonetics='[ˈes.ta ˈno.tʃe ˈβoj a aˈseɾ la ˈse.na]',
                key_focus_sounds='Vowel linking voy a a-cer, soft tap r.',
                practice_tip='Say voy a hacer in one breath.'
            ),
            card5_quiz=Card5Quiz(
                sentence_prompt='¿Qué _____ tú mañana por la tarde?',
                options=['vas a hacer', 'va a hacer', 'vais hacer', 'voy a hacer'],
                correct_index=0,
                correct_explanation='¡Excelente! With subject tú, the near future requires: **vas a hacer**.',
                distractor_explanations={
                    'va a hacer': 'va matches él/ella/usted.',
                    'vais hacer': 'Missing the mandatory preposition a.',
                    'voy a hacer': 'voy matches yo.'
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: 'Nosotros _____ las maletas ahora mismo.'",
                micro_practice_options=['vamos a hacer', 'van a hacer', 'vamos hacer', 'vamos a hacíamos'],
                micro_practice_correct_index=0,
                micro_practice_explanation="Exact! With nosotros use **vamos a hacer**."
            ),
            suggested_coach_prompts=[
                "Why can you never drop the preposition 'a' in 'ir a + infinitive'?",
                "When do native speakers prefer 'voy a hacer' over 'haré'?",
                "How do I link 'voy a' smoothly like a native speaker?"
            ]
        ),
        'Futuro Simple': TenseFlashcardPack(
            tense_name='Futuro Simple',
            tense_order=8,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — Futuro Simple (Haré, Harás...)',
                rule='In the **Futuro Simple**, *hacer* undergoes an irregular stem contraction to **har-** (losing *-ce-*). Endings are oxytone and accented: *-é, -ás, -á, -emos, -éis, -án*.',
                usage_context='Used for long-range future predictions, solemn promises, and expressing conjecture or probability in the present (*¿Dónde estará? Hará la compra*).',
                triggers=['el año que viene', 'en el futuro', 'algún día', 'seguramente', 'probablemente', 'mañana'],
                conjugation_header='The simple future mutates to the irregular shortened stem har-:',
                conjugations=[
                    'yo haré (I will do / make)',
                    'tú harás (you will do / make)',
                    'él/ella/usted hará (he/she/you formal will do / make)',
                    'nosotros/as haremos (we will do / make)',
                    'vosotros/as haréis (you all will do / make)',
                    'ellos/ellas/ustedes harán (they/you all formal will do / make)'
                ]
            ),
            card2_example=Card2Example(
                target_sentence='Te prometo que mañana **haré** todo lo posible para ayudarte.',
                native_sentence='I promise you that tomorrow I **will do** everything possible to help you.',
                breakdown='Observe the contracted stem **har-** paired with the stressed future ending **-é**.'
            ),
            card3_pronunciation=Card3Pronunciation(
                word='haré',
                phonetic_breakdown='ha-**RÉ**',
                stressed_syllables='**RÉ**',
                audio_text='Te prometo que mañana haré todo lo posible.',
                phonetic_tips='Silent initial H; sharp strong stress on the final syllable: ha-RÉ.'
            ),
            card4_speech=Card4Speech(
                target_phrase='Mañana haré todo lo posible.',
                expected_phonetics='[maˈɲa.na aˈɾe ˈto.ðo lo poˈsi.βle]',
                key_focus_sounds='Final stress in ha-RÉ, soft single r.',
                practice_tip='Land firmly on RÉ.'
            ),
            card5_quiz=Card5Quiz(
                sentence_prompt='El próximo mes el nuevo director _____ cambios importantes en la empresa.',
                options=['hará', 'hacerá', 'hace', 'haría'],
                correct_index=0,
                correct_explanation='¡Brillante! The 3rd person singular future of hacer uses the contracted stem har-: **hará**.',
                distractor_explanations={
                    'hacerá': "'hacerá' does not exist; hacer contracts to har-.",
                    'hace': 'hace is simple present.',
                    'haría': 'haría is conditional.'
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: '¿Qué _____ vosotros cuando lleguéis a Madrid?'",
                micro_practice_options=['haréis', 'haceréis', 'harán', 'hacéis'],
                micro_practice_correct_index=0,
                micro_practice_explanation="Spot on! Vosotros in future simple is **haréis**."
            ),
            suggested_coach_prompts=[
                "Why does 'hacer' shrink to 'har-' in the future tense?",
                "How do I use 'hará' to express probability in the present?",
                "What is the difference in tone between 'haré' and 'voy a hacer'?"
            ]
        ),
        'Condicional Simple': TenseFlashcardPack(
            tense_name='Condicional Simple',
            tense_order=9,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — El Condicional Simple (Haría, Harías...)',
                rule='In the **Condicional Simple**, *hacer* uses the same contracted stem as the future (**har-**), followed by standard conditional endings: *-ía, -ías, -ía, -íamos, -íais, -ían*.',
                usage_context='Used for hypothetical actions, polite requests (*¿harías el favor?*), and giving advice (*yo que tú haría esto*).',
                triggers=['si pudiera...', 'yo en tu lugar', 'me gustaría', 'probablemente', 'yo que tú', 'por favor'],
                conjugation_header='The simple conditional uses the contracted stem har- with -ía endings:',
                conjugations=[
                    'yo haría (I would do / make)',
                    'tú harías (you would do / make)',
                    'él/ella/usted haría (he/she/you formal would do / make)',
                    'nosotros/as haríamos (we would do / make)',
                    'vosotros/as haríais (you all would do / make)',
                    'ellos/ellas/ustedes harían (they/you all formal would do / make)'
                ]
            ),
            card2_example=Card2Example(
                target_sentence='Yo en tu lugar **haría** las cosas de otra manera.',
                native_sentence='In your place, I **would do** things differently.',
                breakdown='The conditional **haría** softens advice and makes suggestions thoughtful and polite.'
            ),
            card3_pronunciation=Card3Pronunciation(
                word='haría',
                phonetic_breakdown='ha-**RÍ**-a',
                stressed_syllables='**RÍ**',
                audio_text='Yo en tu lugar haría las cosas de otra manera.',
                phonetic_tips='Silent H and clear hiatus on ha-RÍ-a.'
            ),
            card4_speech=Card4Speech(
                target_phrase='Yo en tu lugar haría las cosas bien.',
                expected_phonetics='[ɟʝo en tu luˈɣaɾ aˈɾi.a las ˈko.sas ˈbjen]',
                key_focus_sounds='Hiatus in ha-RÍ-a, fluid sentence flow.',
                practice_tip='Keep all 3 syllables distinct: ha-RÍ-a.'
            ),
            card5_quiz=Card5Quiz(
                sentence_prompt='Si tuviéramos más presupuesto, nosotros _____ un viaje inolvidable.',
                options=['haríamos', 'hacíamos', 'hicimos', 'haremos'],
                correct_index=0,
                correct_explanation='¡Perfecto! Following an unreal si-clause (*si tuviéramos...*), the main clause takes the conditional: **haríamos**.',
                distractor_explanations={
                    'hacíamos': 'hacíamos is imperfect indicative.',
                    'hicimos': 'hicimos is preterite.',
                    'haremos': 'haremos is future simple.'
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: '¿Nos _____ tú el favor de cerrar la puerta?'",
                micro_practice_options=['harías', 'hiciste', 'haces', 'hagas'],
                micro_practice_correct_index=0,
                micro_practice_explanation="Great job! For polite requests with tú, use **harías**."
            ),
            suggested_coach_prompts=[
                "How do I use 'haría' to formulate ultra-polite requests?",
                "What is the difference between 'yo hacía' and 'yo haría'?",
                "Why do 'hacer' and 'tener' share the exact same -ía endings in conditional?"
            ]
        ),
        'Presente de Subjuntivo': TenseFlashcardPack(
            tense_name='Presente de Subjuntivo',
            tense_order=10,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — Presente de Subjuntivo (Haga, Hagas...)',
                rule='The **Presente de Subjuntivo** takes the 1st person present indicative stem (**hag-** from *yo hago*) and adds opposite vowel endings (**-a-**): *haga, hagas, haga, hagamos, hagáis, hagan*.',
                usage_context='Used after expressions of desire (*quiero que hagas*), doubt, impersonal necessity (*es necesario que hagas esto*), and hopes (*ojalá que haga sol*).',
                triggers=['ojalá que', 'es necesario que', 'quiero que', 'dudo que', 'para que', 'es mejor que'],
                conjugation_header='The present subjunctive derives from the 1st person yo-go stem hag-:',
                conjugations=[
                    'que yo haga (that I do / make)',
                    'que tú hagas (that you do / make)',
                    'que él/ella/usted haga (that he/she/you formal does / makes)',
                    'nosotros/as hagamos (that we do / make)',
                    'que vosotros/as hagáis (that you all do / make)',
                    'que ellos/ellas/ustedes hagan (that they/you all formal do / make)'
                ]
            ),
            card2_example=Card2Example(
                target_sentence='Es muy importante que tú **hagas** la tarea antes de la clase.',
                native_sentence='It is very important that you **do** the homework before class.',
                breakdown='The impersonal trigger *es muy importante que* governs the subjunctive verb form **hagas**.'
            ),
            card3_pronunciation=Card3Pronunciation(
                word='hagas',
                phonetic_breakdown='**HA**-gas',
                stressed_syllables='**HA**',
                audio_text='Es muy importante que tú hagas la tarea.',
                phonetic_tips='Silent H and soft voiced velar g before a: HA-gas.'
            ),
            card4_speech=Card4Speech(
                target_phrase='Espero que hagas un buen trabajo.',
                expected_phonetics='[esˈpe.ɾo ke ˈa.ɣas um bwen tɾaˈβa.xo]',
                key_focus_sounds='Initial stress **HA**-gas, soft Spanish g.',
                practice_tip='Keep vowels open and bright.'
            ),
            card5_quiz=Card5Quiz(
                sentence_prompt='El médico me recomendó que yo _____ ejercicio moderado cada día.',
                options=['haga', 'hago', 'hace', 'hiciera'],
                correct_index=0,
                correct_explanation='¡Extraordinario! Following recommendation (*recomendó que*), Spanish requires the subjunctive: **haga**.',
                distractor_explanations={
                    'hago': 'hago is present indicative, ungrammatical under subjunctive triggers.',
                    'hace': 'hace is 3rd person indicative.',
                    'hiciera': 'hiciera is past imperfect subjunctive.'
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: 'Ojalá que el profesor no nos _____ un examen sorpresa.'",
                micro_practice_options=['haga', 'hace', 'hizo', 'hará'],
                micro_practice_correct_index=0,
                micro_practice_explanation="Spot on! After ojalá que use the present subjunctive: **haga**."
            ),
            suggested_coach_prompts=[
                "Why is the 'Yo-Rule' (yo hago -> hag-) the key to Spanish subjunctive?",
                "Which common phrases with 'que' always trigger 'haga'?",
                "How do you use 'haga lo que haga' to mean 'no matter what he does'?"
            ]
        )
    })

def build_spanish_tener_pack(native_lang: str = "English") -> Dict[str, TenseFlashcardPack]:
    lang = native_lang.lower()
    is_pt = "portugu" in lang

    if is_pt:
        return _add_pack_aliases({
            'Infinitivo': TenseFlashcardPack(
                tense_name='Infinitivo',
                tense_order=1,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — El Infinitivo (Tener)',
                    rule="O **infinitivo** é a forma básica não conjugada (*tener*). Em espanhol, é central na perífrase essencial de obrigação e necessidade: **tener que + infinitivo** (ter que fazer algo).",
                    usage_context="Usado após preposições, verbos de desejo (*querer tener*, *esperar tener*) e locuções perifrásticas.",
                    triggers=['tener que + infinitivo', 'querer tener', 'para', 'antes de tener'],
                    conjugation_header='Estruturas essenciais com o infinitivo (perífrases verbais):',
                    conjugations=[
                        'tener que + infinitivo (ter que / obrigação e necessidade)',
                        'hay que + tener (é preciso ter / dever impessoal)',
                        'ir a + tener (vai ter / futuro próximo)',
                        'querer + tener (querer ter / desejo)',
                        'antes de + tener (antes de ter / tempo)',
                        'para + tener (para ter / finalidade)'
                    ]
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
                    triggers=['ahora mismo', 'en este momento', 'estar + teniendo', 'últimamente'],
                    conjugation_header='A conjugação contínua é muito comum (estar + gerundio):',
                    conjugations=[
                        'yo estoy teniendo (eu estou tendo)',
                        'tú estás teniendo (tu estás tendo / você está tendo)',
                        'él/ella/usted está teniendo (ele/ela/você está tendo)',
                        'nosotros/as estamos teniendo (nós estamos tendo)',
                        'vosotros/as estáis teniendo (vós estais tendo)',
                        'ellos/ellas/ustedes están teniendo (eles/elas/vocês estão tendo)'
                    ]
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
                    triggers=['alguna vez', 'nunca', 'siempre', 'este año', 'últimamente', 'ya'],
                    conjugation_header='A conjugação composta perfeita (haber + participio):',
                    conjugations=[
                        'yo he tenido (eu tive / tenho tido)',
                        'tú has tenido (tu tiveste / você teve)',
                        'él/ella/usted ha tenido (ele/ela/você teve)',
                        'nosotros/as hemos tenido (nós tivemos / temos tido)',
                        'vosotros/as habéis tenido (vós tivestes)',
                        'ellos/ellas/ustedes han tenido (eles/elas/vocês tiveram)'
                    ]
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
                    triggers=['hoy', 'siempre', 'normalmente', 'todos los días', 'ahora'],
                    conjugation_header='A conjugação é bastante irregular, mas muito comum:',
                    conjugations=[
                        'yo tengo (eu tenho)',
                        'tú tienes (tu tens / você tem)',
                        'él/ella/usted tiene (ele/ela/você tem)',
                        'nosotros/as tenemos (nós temos)',
                        'vosotros/as tenéis (vós tendes)',
                        'ellos/ellas/ustedes tienen (eles/elas/vocês têm)'
                    ]
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
                    triggers=['ayer', 'anoche', 'el año pasado', 'la semana pasada', 'en aquel momento'],
                    conjugation_header='A conjugação no pretérito simples muda para o radical irregular tuv-:',
                    conjugations=[
                        'yo tuve (eu tive)',
                        'tú tuviste (tu tiveste / você teve)',
                        'él/ella/usted tuvo (ele/ela/você teve)',
                        'nosotros/as tuvimos (nós tivemos)',
                        'vosotros/as tuvisteis (vós tivestes)',
                        'ellos/ellas/ustedes tuvieron (eles/elas/vocês tiveram)'
                    ]
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
            ),
            'Pretérito Imperfecto': TenseFlashcardPack(
                tense_name='Pretérito Imperfecto',
                tense_order=6,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — Pretérito Imperfecto (Tenía, Tenías...)',
                    rule='No **Pretérito Imperfeito**, *tener* mantém o radical regular **ten-** e recebe as desinências regulares de verbos em -er com acento gráfico obrigatório no **í**: *-ía, -ías, -ía, -íamos, -íais, -ían*.',
                    usage_context='Usado para descrever situações habituais, estados contínuos no passado, idade (*cuando tenía 10 años*) ou o cenário de fundo de outra ação.',
                    triggers=['cuando era niño/a', 'antes', 'siempre', 'todos los veranos', 'mientras', 'de joven'],
                    conjugation_header='A conjugação no pretérito imperfeito é regular sobre o radical ten-:',
                    conjugations=[
                        'yo tenía (eu tinha)',
                        'tú tenías (tu tinhas / você tinha)',
                        'él/ella/usted tenía (ele/ela/você tinha)',
                        'nosotros/as teníamos (nós tínhamos)',
                        'vosotros/as teníais (vós tínheis)',
                        'ellos/ellas/ustedes tenían (eles/elas/vocês tinham)'
                    ]
                ),
                card2_example=Card2Example(
                    target_sentence='Cuando era niño, yo **tenía** un perro pequeño que me acompañaba siempre.',
                    native_sentence='Quando eu era criança, eu **tinha** um cachorro pequeno que me acompanhava sempre.',
                    breakdown='Usa-se **tenía** para indicar uma situação contínua ou posse habitual no passado, não uma ação pontual isolada.'
                ),
                card3_pronunciation=Card3Pronunciation(
                    word='tenía',
                    phonetic_breakdown='te-**NÍ**-a',
                    stressed_syllables='**NÍ**',
                    audio_text='Cuando era niño, yo tenía un perro pequeño.',
                    phonetic_tips='O acento gráfico no í cria um hiato nítido: te-NÍ-a.'
                ),
                card4_speech=Card4Speech(
                    target_phrase='Yo tenía un perro pequeño.',
                    expected_phonetics='[ɟʝo teˈni.a um ˈpe.ro peˈke.ɲo]',
                    key_focus_sounds='Hiato nítido em te-NÍ-a, r forte vibrante em perro.',
                    practice_tip='Separe claramente a vogal í da vogal a em te-NÍ-a.'
                ),
                card5_quiz=Card5Quiz(
                    sentence_prompt='En aquella época, nosotros _____ muchas dudas sobre el futuro.',
                    options=['teníamos', 'tuvimos', 'tenemos', 'tendríamos'],
                    correct_index=0,
                    correct_explanation='¡Perfecto! Para descrever uma situação contínua ou habitual no passado (*en aquella época*), usa-se o pretérito imperfeito: **teníamos**.',
                    distractor_explanations={
                        'tuvimos': 'tuvimos é o pretérito indefinido pontual.',
                        'tenemos': 'tenemos é o presente do indicativo.',
                        'tendríamos': 'tendríamos é o condicional simples.'
                    },
                    micro_practice_prompt="Micro-Prática: Complete: '¿Cuántos años _____ tú en 2015?'",
                    micro_practice_options=['tenías', 'tuviste', 'tienes', 'tengas'],
                    micro_practice_correct_index=0,
                    micro_practice_explanation="Correto! Para idade habitual no passado, usa-se o imperfeito: **tenías**."
                ),
                suggested_coach_prompts=[
                    "Qual é a diferença de nuance entre 'tuve miedo' e 'tenía miedo'?",
                    "Por que todas as pessoas do pretérito imperfeito de verbos em -er levam acento no 'í'?",
                    "Como expressar hábitos de infância em espanhol usando 'tenía'?"
                ]
            ),
            'Futuro Próximo': TenseFlashcardPack(
                tense_name='Futuro Próximo',
                tense_order=7,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — Futuro Próximo (Voy a tener...)',
                    rule='O **Futuro Próximo** é construído com a perífrase **ir (no presente) + a + infinitivo (tener)**. É a forma mais natural e frequente na conversação cotidiana para falar de planos futuros certos ou imediatos.',
                    usage_context='Usado para intenções imediatas, compromissos agendados e eventos futuros baseados em evidências do presente.',
                    triggers=['mañana', 'esta tarde', 'el próximo fin de semana', 'pronto', 'voy a'],
                    conjugation_header='A conjugação no futuro próximo (ir a + tener):',
                    conjugations=[
                        'yo voy a tener (eu vou ter)',
                        'tú vas a tener (tu vais ter / você vai ter)',
                        'él/ella/usted va a tener (ele/ela/você vai ter)',
                        'nosotros/as vamos a tener (nós vamos ter)',
                        'vosotros/as vais a tener (vós ides ter)',
                        'ellos/ellas/ustedes van a tener (eles/elas/vocês vão ter)'
                    ]
                ),
                card2_example=Card2Example(
                    target_sentence='Mañana **voy a tener** una reunión decisiva con el nuevo equipo.',
                    native_sentence='Amanhã **vou ter** uma reunião decisiva com a nova equipe.',
                    breakdown='Apenas o auxiliar ir conjuga (**voy**), seguido da preposição obrigatória **a** e do infinitivo base (**tener**).'
                ),
                card3_pronunciation=Card3Pronunciation(
                    word='voy a tener',
                    phonetic_breakdown='voy a te-**NER**',
                    stressed_syllables='**NER**',
                    audio_text='Mañana voy a tener una reunión decisiva.',
                    phonetic_tips='Ligue os sons de forma suave: [bo-ja-te-NER].'
                ),
                card4_speech=Card4Speech(
                    target_phrase='Mañana voy a tener una reunión.',
                    expected_phonetics='[maˈɲa.na ˈβoj a teˈneɾ ˈu.na rewˈnjon]',
                    key_focus_sounds='Ligação voy a, r suave no final de tener.',
                    practice_tip='Fale sem pausas entre voy e a: voy-a.'
                ),
                card5_quiz=Card5Quiz(
                    sentence_prompt='Nosotros _____ mucho trabajo la próxima semana.',
                    options=['vamos a tener', 'vamos tener', 'van a tener', 'vamos a tendríamos'],
                    correct_index=0,
                    correct_explanation='¡Excelente! A estrutura perifrástica exige o verbo ir conjugado + a + infinitivo: **vamos a tener**.',
                    distractor_explanations={
                        'vamos tener': 'Erro comum: no espanhol a preposição a é estritamente obrigatória em ir a + infinitivo.',
                        'van a tener': 'van é 3ª pessoa do plural (ellos), não nós.',
                        'vamos a tendríamos': 'Nunca se conjuga o segundo verbo após ir a.'
                    },
                    micro_practice_prompt="Micro-Prática: Complete: '¿Qué _____ tú que hacer mañana?'",
                    micro_practice_options=['vas a tener', 'va a tener', 'voy a tener', 'vais tener'],
                    micro_practice_correct_index=0,
                    micro_practice_explanation="Exato! Com tú usamos **vas a tener**."
                ),
                suggested_coach_prompts=[
                    "Por que nunca se pode omitir a preposição 'a' em 'voy a tener'?",
                    "Quando os hispanofalantes preferem 'voy a tener' em vez de 'tendré'?",
                    "Como conectar os sons de 'voy a' para soar como um falante nativo?"
                ]
            ),
            'Futuro Simple': TenseFlashcardPack(
                tense_name='Futuro Simple',
                tense_order=8,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — Futuro Simple (Tendré, Tendrás...)',
                    rule='No **Futuro Simples**, *tener* sofre síncope no radical: perde a vogal *-e-* e ganha *-d-*, formando o radical irregular **tendr-**. As terminações recebem acento gráfico em quase todas as pessoas: *-é, -ás, -á, -emos, -éis, -án*.',
                    usage_context='Usado para previsões a longo prazo, promessas formais e expressar probabilidade ou suposição no presente (*¿Quién será? Tendrá 20 años*).',
                    triggers=['el año que viene', 'en el futuro', 'algún día', 'seguramente', 'probablemente', 'pronto'],
                    conjugation_header='A conjugação no futuro simples sofre síncope para o radical tendr-:',
                    conjugations=[
                        'yo tendré (eu terei)',
                        'tú tendrás (tu terás / você terá)',
                        'él/ella/usted tendrá (ele/ela/você terá)',
                        'nosotros/as tendremos (nós teremos)',
                        'vosotros/as tendréis (vós tereis)',
                        'ellos/ellas/ustedes tendrán (eles/elas/vocês terão)'
                    ]
                ),
                card2_example=Card2Example(
                    target_sentence='El próximo año **tendré** la oportunidad de vivir en España.',
                    native_sentence='No próximo ano **terei** a oportunidade de viver na Espanha.',
                    breakdown='Observe o radical irregular **tendr-** acompanhado da terminação oxítona acentuada **-é**.'
                ),
                card3_pronunciation=Card3Pronunciation(
                    word='tendré',
                    phonetic_breakdown='ten-**DRÉ**',
                    stressed_syllables='**DRÉ**',
                    audio_text='El próximo año tendré la oportunidad de vivir en España.',
                    phonetic_tips='Palavra aguda com ênfase forte na última sílaba: ten-DRÉ.'
                ),
                card4_speech=Card4Speech(
                    target_phrase='Pronto tendré buenas noticias.',
                    expected_phonetics='[ˈpɾon.to tenˈdɾe ˈβwe.nas noˈti.sjas]',
                    key_focus_sounds='Acento oxítono em ten-DRÉ.',
                    practice_tip='Coloque toda a energia vocal na sílaba DRÉ.'
                ),
                card5_quiz=Card5Quiz(
                    sentence_prompt='Si te esfuerzas cada día, tú _____ grandes resultados.',
                    options=['tendrás', 'tenerás', 'tienes', 'tendrías'],
                    correct_index=0,
                    correct_explanation='¡Brillante! A 2ª pessoa do futuro simples de tener tem radical irregular tendr- e desinência acentuada: **tendrás**.',
                    distractor_explanations={
                        'tenerás': 'Não regularize! O verbo tener sofre síncope e ganha d: tendrás.',
                        'tienes': 'tienes é o presente do indicativo.',
                        'tendrías': 'tendrías é o condicional simples.'
                    },
                    micro_practice_prompt="Micro-Prática: Complete: 'Nosotros _____ una respuesta oficial el viernes.'",
                    micro_practice_options=['tendremos', 'teneremos', 'tuvimos', 'tengamos'],
                    micro_practice_correct_index=0,
                    micro_practice_explanation="Perfeito! Nosotros no futuro simples é **tendremos**."
                ),
                suggested_coach_prompts=[
                    "Por que o radical vira 'tendr-' em vez de 'tener-' no futuro?",
                    "Como usar o futuro simples 'tendrá hambre' para expressar probabilidade no presente?",
                    "Quais outros verbos têm essa mesma mutação 'dr' (como poner -> pondré, salir -> saldré)?"
                ]
            ),
            'Condicional Simple': TenseFlashcardPack(
                tense_name='Condicional Simple',
                tense_order=9,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — El Condicional Simple (Tendría, Tendrías...)',
                    rule='No **Condicional Simples**, *tener* compartilha o radical sincopado do futuro (**tendr-**), mas recebe as terminações com acento gráfico obrigatório no **í**: *-ía, -ías, -ía, -íamos, -íais, -ían*.',
                    usage_context='Usado para hipóteses, conselhos ponderados (*yo en tu lugar tendría cuidado*), situações condicionadas por uma oração com si (*si tuviera dinero, tendría una casa*) e pedidos corteses.',
                    triggers=['si tuviera...', 'yo en tu lugar', 'me gustaría', 'probablemente', 'en ese caso', 'yo que tú'],
                    conjugation_header='A conjugação no condicional simples usa o radical tendr- e terminações em -ía:',
                    conjugations=[
                        'yo tendría (eu teria)',
                        'tú tendrías (tu terias / você teria)',
                        'él/ella/usted tendría (ele/ela/você teria)',
                        'nosotros/as tendríamos (nós teríamos)',
                        'vosotros/as tendríais (vós teríeis)',
                        'ellos/ellas/ustedes tendrían (eles/elas/vocês teriam)'
                    ]
                ),
                card2_example=Card2Example(
                    target_sentence='Yo en tu lugar **tendría** mucho cuidado antes de tomar una decisión.',
                    native_sentence='Eu no seu lugar **teria** muito cuidado antes de tomar uma decisão.',
                    breakdown='O condicional **tendría** expressa uma recomendação atenuada e cordial baseada no radical **tendr-**.'
                ),
                card3_pronunciation=Card3Pronunciation(
                    word='tendría',
                    phonetic_breakdown='ten-**DRÍ**-a',
                    stressed_syllables='**DRÍ**',
                    audio_text='Yo en tu lugar tendría mucho cuidado.',
                    phonetic_tips='O acento agudo no í quebra o encontro vocálico em hiato nítido: ten-DRÍ-a.'
                ),
                card4_speech=Card4Speech(
                    target_phrase='Yo tendría mucho cuidado.',
                    expected_phonetics='[ɟʝo tenˈdɾi.a ˈmu.tʃo kwiˈða.ðo]',
                    key_focus_sounds='Hiato forte em ten-DRÍ-a, d suave em cuidado.',
                    practice_tip='Pronuncie três sílabas rítmicas: ten-drí-a.'
                ),
                card5_quiz=Card5Quiz(
                    sentence_prompt='Si tuviéramos más tiempo libre, nosotros _____ una mascota.',
                    options=['tendríamos', 'teníamos', 'tuvimos', 'tendremos'],
                    correct_index=0,
                    correct_explanation='¡Perfecto! A consequência de uma condição irreal no presente (*si tuviéramos...*), exige o condicional simples: **tendríamos**.',
                    distractor_explanations={
                        'teníamos': 'teníamos é pretérito imperfeito do indicativo.',
                        'tuvimos': 'tuvimos é pretérito indefinido.',
                        'tendremos': 'tendremos é futuro simples.'
                    },
                    micro_practice_prompt="Micro-Prática: Complete: '¿Qué _____ tú si ganaras la lotería?'",
                    micro_practice_options=['tendrías', 'tuviste', 'tienes', 'tengas'],
                    micro_practice_correct_index=0,
                    micro_practice_explanation="Excelente! Com tú a terminação do condicional é **tendrías**."
                ),
                suggested_coach_prompts=[
                    "Como diferenciar na pronúncia e no ouvido 'tendría' de 'tenía'?",
                    "Como formular conselhos educados com 'yo en tu lugar tendría...'?",
                    "Por que a oração com 'si tuviera...' sempre se conecta com 'tendría'?"
                ]
            ),
            'Presente de Subjuntivo': TenseFlashcardPack(
                tense_name='Presente de Subjuntivo',
                tense_order=10,
                card1_concept=Card1Concept(
                    title='Cartão 1: Conceito & Regra — Presente de Subjuntivo (Tenga, Tengas...)',
                    rule='O **Presente de Subjuntivo** de *tener* deriva do radical da 1ª pessoa do presente do indicativo (**teng-** de *yo tengo*), trocando a vogal temática para **-a-**: *tenga, tengas, tenga, tengamos, tengáis, tengan*.',
                    usage_context='Usado após verbos de desejo, dúvida, orações impessoais de necessidade (*es necesario que tengas paciencia*) e expressões com ojalá (*ojalá que tengamos suerte*).',
                    triggers=['ojalá que', 'es necesario que', 'espero que', 'quiero que', 'dudo que', 'para que', 'es importante que'],
                    conjugation_header='A conjugação no presente do subjuntivo baseia-se no radical teng-:',
                    conjugations=[
                        'que yo tenga (que eu tenha)',
                        'que tú tengas (que tu tenhas / você tenha)',
                        'que él/ella/usted tenga (que ele/ela/você tenha)',
                        'nosotros/as tengamos (que nós tenhamos)',
                        'vosotros/as tengáis (que vós tenhais)',
                        'ellos/ellas/ustedes tengan (que eles/elas/vocês tenham)'
                    ]
                ),
                card2_example=Card2Example(
                    target_sentence='Es fundamental que **tengas** paciencia durante este proceso.',
                    native_sentence='É fundamental que você **tenha** paciência durante este processo.',
                    breakdown='A expressão impessoal de avaliação (*es fundamental que*) exige o modo subjuntivo (**tengas**).'
                ),
                card3_pronunciation=Card3Pronunciation(
                word='tengas',
                phonetic_breakdown='**TEN**-gas',
                stressed_syllables='**TEN**',
                audio_text='Es fundamental que tengas paciencia durante este proceso.',
                phonetic_tips='T dental limpo e velar suave em gas.'
            ),
            card4_speech=Card4Speech(
                target_phrase='Espero que tengas un buen día.',
                expected_phonetics='[esˈpe.ɾo ke ˈteŋ.ɡas um bwen ˈdi.a]',
                key_focus_sounds='Tônica em **TEN**-gas, som suave de g.',
                practice_tip='Ligue que e tengas naturalmente.'
            ),
            card5_quiz=Card5Quiz(
                sentence_prompt='Ojalá que nosotros _____ buenas noticias mañana.',
                options=['tengamos', 'tenemos', 'tuvimos', 'tendremos'],
                correct_index=0,
                correct_explanation='¡Extraordinario! Após a partícula de desejo **ojalá que**, exige-se o presente do subjuntivo: **tengamos**.',
                distractor_explanations={
                    'tenemos': 'tenemos é presente do indicativo, inadequado após ojalá que.',
                    'tuvimos': 'tuvimos é pretérito indefinido.',
                    'tendremos': 'tendremos é futuro simples.'
                },
                micro_practice_prompt="Micro-Prática: Complete: 'Quiero que tú _____ mucho éxito.'",
                micro_practice_options=['tengas', 'tienes', 'tuvo', 'tendrás'],
                micro_practice_correct_index=0,
                micro_practice_explanation="Correto! Querer que com sujeitos diferentes exige o subjuntivo: **tengas**."
            ),
            suggested_coach_prompts=[
                "Por que a forma 'yo tengo' é a chave para formar todo o presente do subjuntivo ('tenga, tengas...')?",
                "Quais expressões impessoais em espanhol sempre exigem o subjuntivo?",
                "Qual é a diferença de sentido entre 'sé que tienes tiempo' e 'espero que tengas tiempo'?"
            ]
        )
        })

    # English Native/Support Language
    return _add_pack_aliases({
        'Infinitivo': TenseFlashcardPack(
            tense_name='Infinitivo',
            tense_order=1,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — El Infinitivo (Tener)',
                rule="The **infinitivo** is the basic, unconjugated verb form ending in **-er** (*tener* = to have). It is central to the essential obligation construction: **tener que + infinitive** (to have to do something).",
                usage_context="Used directly after prepositions, modal verbs of desire (*querer tener*), and periphrastic structures.",
                triggers=['tener que + infinitive', 'querer tener', 'para', 'antes de tener'],
                conjugation_header='Essential structures with the infinitive (verbal periphrases):',
                conjugations=[
                    'tener que + infinitive (have to / obligation)',
                    'hay que + tener (one must have / impersonal necessity)',
                    'ir a + tener (going to have / near future)',
                    'querer + tener (want to have / desire)',
                    'antes de + tener (before having / sequence)',
                    'para + tener (in order to have / purpose)'
                ]

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
                triggers=['ahora mismo', 'en este momento', 'estar + teniendo', 'últimamente'],
                conjugation_header='The continuous progressive conjugation (estar + gerund):',
                conjugations=[
                    'yo estoy teniendo (I am having)',
                    'tú estás teniendo (you are having)',
                    'él/ella/usted está teniendo (he/she/you formal is having)',
                    'nosotros/as estamos teniendo (we are having)',
                    'vosotros/as estáis teniendo (you all are having)',
                    'ellos/ellas/ustedes están teniendo (they/you all formal are having)'
                ]
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
                triggers=['alguna vez', 'nunca', 'siempre', 'este año', 'últimamente', 'ya'],
                conjugation_header='The compound perfect conjugation (haber + participle):',
                conjugations=[
                    'yo he tenido (I have had)',
                    'tú has tenido (you have had)',
                    'él/ella/usted ha tenido (he/she/you formal has had)',
                    'nosotros/as hemos tenido (we have had)',
                    'vosotros/as habéis tenido (you all have had)',
                    'ellos/ellas/ustedes han tenido (they/you all formal have had)'
                ]
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
                triggers=['hoy', 'siempre', 'normalmente', 'todos los días', 'ahora'],
                conjugation_header='The present conjugation features an irregular Yo-Go 1st person and stem change:',
                conjugations=[
                    'yo tengo (I have)',
                    'tú tienes (you have)',
                    'él/ella/usted tiene (he/she/you formal has)',
                    'nosotros/as tenemos (we have)',
                    'vosotros/as tenéis (you all have)',
                    'ellos/ellas/ustedes tienen (they/you all formal have)'
                ]
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
                triggers=['ayer', 'anoche', 'el año pasado', 'la semana pasada', 'en aquel momento'],
                conjugation_header='In the simple past (preterite), the stem mutates to irregular tuv-:',
                conjugations=[
                    'yo tuve (I had)',
                    'tú tuviste (you had)',
                    'él/ella/usted tuvo (he/she/you formal had)',
                    'nosotros/as tuvimos (we had)',
                    'vosotros/as tuvisteis (you all had)',
                    'ellos/ellas/ustedes tuvieron (they/you all formal had)'
                ]
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
        ),
        'Pretérito Imperfecto': TenseFlashcardPack(
            tense_name='Pretérito Imperfecto',
            tense_order=6,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — Pretérito Imperfecto (Tenía, Tenías...)',
                rule='In the **Pretérito Imperfecto**, *tener* is regular on stem **ten-** and takes standard -er endings with mandatory accents on the **í**: *-ía, -ías, -ía, -íamos, -íais, -ían*.',
                usage_context='Used for describing ongoing background conditions, habitual past states, and expressing past age (*cuando tenía diez años*).',
                triggers=['cuando era niño/a', 'antes', 'siempre', 'todos los veranos', 'mientras', 'de joven'],
                conjugation_header='The imperfect tense uses regular -ía endings with accent marks on the í:',
                conjugations=[
                    'yo tenía (I had / used to have)',
                    'tú tenías (you had / used to have)',
                    'él/ella/usted tenía (he/she/you formal had / used to have)',
                    'nosotros/as teníamos (we had / used to have)',
                    'vosotros/as teníais (you all had / used to have)',
                    'ellos/ellas/ustedes tenían (they/you all formal had / used to have)'
                ]
            ),
            card2_example=Card2Example(
                target_sentence='Cuando era niño, yo **tenía** un perro pequeño que me acompañaba siempre.',
                native_sentence='When I was a child, I **had** a little dog that always accompanied me.',
                breakdown='Notice the continuous descriptive state conveyed by **tenía**, contrasting with completed events.'
            ),
            card3_pronunciation=Card3Pronunciation(
                word='tenía',
                phonetic_breakdown='te-**NÍ**-a',
                stressed_syllables='**NÍ**',
                audio_text='Cuando era niño, yo tenía un perro pequeño.',
                phonetic_tips='The accent mark on í forms a hiatus: te-NÍ-a.'
            ),
            card4_speech=Card4Speech(
                target_phrase='Yo tenía un perro pequeño.',
                expected_phonetics='[ɟʝo teˈni.a um ˈpe.ro peˈke.ɲo]',
                key_focus_sounds='Clean hiatus te-NÍ-a, trilled Spanish rr in perro.',
                practice_tip='Clearly enunciate the stressed NÍ.'
            ),
            card5_quiz=Card5Quiz(
                sentence_prompt='En aquella época, nosotros _____ muchas dudas sobre el futuro.',
                options=['teníamos', 'tuvimos', 'tenemos', 'tendríamos'],
                correct_index=0,
                correct_explanation='¡Perfecto! To express an ongoing state in the past (*en aquella época*), Spanish uses the imperfect: **teníamos**.',
                distractor_explanations={
                    'tuvimos': 'tuvimos is preterite, for completed punctual events.',
                    'tenemos': 'tenemos is present indicative.',
                    'tendríamos': 'tendríamos is conditional.'
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: '¿Cuántos años _____ tú en 2015?'",
                micro_practice_options=['tenías', 'tuviste', 'tienes', 'tengas'],
                micro_practice_correct_index=0,
                micro_practice_explanation="Spot on! For age in the past, use imperfect: **tenías**."
            ),
            suggested_coach_prompts=[
                "What is the nuance difference between 'tuve miedo' and 'tenía miedo'?",
                "Why do all imperfect endings for -er verbs take an accent mark on the 'í'?",
                "How do I use 'tenía' to talk about childhood habits?"
            ]
        ),
        'Futuro Próximo': TenseFlashcardPack(
            tense_name='Futuro Próximo',
            tense_order=7,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — Futuro Próximo (Voy a tener...)',
                rule='The **Futuro Próximo** is built with **ir (present) + a + infinitivo (tener)**. It is the most common conversational way to express upcoming plans and certain intentions.',
                usage_context='Used for immediate future plans, scheduled events, and predictions grounded in present evidence.',
                triggers=['mañana', 'esta tarde', 'el próximo fin de semana', 'pronto', 'voy a'],
                conjugation_header='The near future structure (ir a + tener):',
                conjugations=[
                    'yo voy a tener (I am going to have)',
                    'tú vas a tener (you are going to have)',
                    'él/ella/usted va a tener (he/she/you formal is going to have)',
                    'nosotros/as vamos a tener (we are going to have)',
                    'vosotros/as vais a tener (you all are going to have)',
                    'ellos/ellas/ustedes van a tener (they/you all formal are going to have)'
                ]
            ),
            card2_example=Card2Example(
                target_sentence='Mañana **voy a tener** una reunión decisiva con el nuevo equipo.',
                native_sentence='Tomorrow I am **going to have** a decisive meeting with the new team.',
                breakdown='Only the auxiliary *ir* conjugates (**voy**); **tener** stays in the base infinitive preceded by **a**.'
            ),
            card3_pronunciation=Card3Pronunciation(
                word='voy a tener',
                phonetic_breakdown='voy a te-**NER**',
                stressed_syllables='**NER**',
                audio_text='Mañana voy a tener una reunión decisiva.',
                phonetic_tips='Glide smoothly across the words: [bo-ja-te-NER].'
            ),
            card4_speech=Card4Speech(
                target_phrase='Mañana voy a tener una reunión.',
                expected_phonetics='[maˈɲa.na ˈβoj a teˈneɾ ˈu.na rewˈnjon]',
                key_focus_sounds='Vowel linking voy a, soft tap r.',
                practice_tip='Say voy a tener smoothly without hesitation.'
            ),
            card5_quiz=Card5Quiz(
                sentence_prompt='Nosotros _____ mucho trabajo la próxima semana.',
                options=['vamos a tener', 'vamos tener', 'van a tener', 'vamos a tendríamos'],
                correct_index=0,
                correct_explanation='¡Excelente! The periphrastic structure requires conjugated ir + a + infinitive: **vamos a tener**.',
                distractor_explanations={
                    'vamos tener': 'Common error: in Spanish the preposition a is strictly required after ir.',
                    'van a tener': 'van matches ellos/ellas/ustedes.',
                    'vamos a tendríamos': 'Never conjugate the second verb after ir a.'
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: '¿Qué _____ tú que hacer mañana?'",
                micro_practice_options=['vas a tener', 'va a tener', 'voy a tener', 'vais tener'],
                micro_practice_correct_index=0,
                micro_practice_explanation="Exact! With tú use **vas a tener**."
            ),
            suggested_coach_prompts=[
                "Why can you never drop the preposition 'a' in 'voy a tener'?",
                "When do native speakers prefer 'voy a tener' over 'tendré'?",
                "How do I link 'voy a' smoothly like a native speaker?"
            ]
        ),
        'Futuro Simple': TenseFlashcardPack(
            tense_name='Futuro Simple',
            tense_order=8,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — Futuro Simple (Tendré, Tendrás...)',
                rule='In the **Futuro Simple**, *tener* undergoes a syncope stem mutation: it drops *-e-* and inserts *-d-*, producing **tendr-**. Personal endings are oxytone and accented on nearly every form: *-é, -ás, -á, -emos, -éis, -án*.',
                usage_context='Used for long-range future predictions, solemn promises, and expressing conjecture or probability in the present (*Tendrá unos 30 años* = He is probably about 30).',
                triggers=['el año que viene', 'en el futuro', 'algún día', 'seguramente', 'probablemente', 'pronto'],
                conjugation_header='The simple future mutates to the irregular stem tendr-:',
                conjugations=[
                    'yo tendré (I will have)',
                    'tú tendrás (you will have)',
                    'él/ella/usted tendrá (he/she/you formal will have)',
                    'nosotros/as tendremos (we will have)',
                    'vosotros/as tendréis (you all will have)',
                    'ellos/ellas/ustedes tendrán (they/you all formal will have)'
                ]
            ),
            card2_example=Card2Example(
                target_sentence='El próximo año **tendré** la oportunidad de vivir en España.',
                native_sentence='Next year I **will have** the opportunity to live in Spain.',
                breakdown='Observe the irregular stem **tendr-** paired with the stressed ending **-é**.'
            ),
            card3_pronunciation=Card3Pronunciation(
                word='tendré',
                phonetic_breakdown='ten-**DRÉ**',
                stressed_syllables='**DRÉ**',
                audio_text='El próximo año tendré la oportunidad de vivir en España.',
                phonetic_tips='Oxytone word with strong final stress: ten-DRÉ.'
            ),
            card4_speech=Card4Speech(
                target_phrase='Pronto tendré buenas noticias.',
                expected_phonetics='[ˈpɾon.to tenˈdɾe ˈβwe.nas noˈti.sjas]',
                key_focus_sounds='Strong final stress in ten-DRÉ.',
                practice_tip='Place clear energy on DRÉ.'
            ),
            card5_quiz=Card5Quiz(
                sentence_prompt='Si te esfuerzas cada día, tú _____ grandes resultados.',
                options=['tendrás', 'tenerás', 'tienes', 'tendrías'],
                correct_index=0,
                correct_explanation='¡Brillante! The 2nd person future simple of tener has irregular stem tendr-: **tendrás**.',
                distractor_explanations={
                    'tenerás': 'Do not regularize! Tener syncopates to tendr-: tendrás.',
                    'tienes': 'tienes is present indicative.',
                    'tendrías': 'tendrías is conditional.'
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: 'Nosotros _____ una respuesta oficial el viernes.'",
                micro_practice_options=['tendremos', 'teneremos', 'tuvimos', 'tengamos'],
                micro_practice_correct_index=0,
                micro_practice_explanation="Perfect! We in simple future is **tendremos**."
            ),
            suggested_coach_prompts=[
                "Why does 'tener' become 'tendr-' instead of 'tener-' in the future?",
                "How do you use 'tendrá calor' to express probability in the present?",
                "Which other verbs follow this -dr- mutation (poner -> pondré, salir -> saldré)?"
            ]
        ),
        'Condicional Simple': TenseFlashcardPack(
            tense_name='Condicional Simple',
            tense_order=9,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — El Condicional Simple (Tendría, Tendrías...)',
                rule='In the **Condicional Simple**, *tener* shares the irregular syncopated stem with the future (**tendr-**), but takes regular conditional endings with accents on the **í**: *-ía, -ías, -ía, -íamos, -íais, -ían*.',
                usage_context='Used for hypothetical statements, polite advice (*yo en tu lugar tendría cuidado* = If I were you I would be careful), and consequences of hypothetical si-clauses (*si tuviera dinero, tendría una casa*).',
                triggers=['si tuviera...', 'yo en tu lugar', 'me gustaría', 'probablemente', 'en ese caso', 'yo que tú'],
                conjugation_header='The simple conditional uses the stem tendr- with accented -ía endings:',
                conjugations=[
                    'yo tendría (I would have)',
                    'tú tendrías (you would have)',
                    'él/ella/usted tendría (he/she/you formal would have)',
                    'nosotros/as tendríamos (we would have)',
                    'vosotros/as tendríais (you all would have)',
                    'ellos/ellas/ustedes tendrían (they/you all formal would have)'
                ]
            ),
            card2_example=Card2Example(
                target_sentence='Yo en tu lugar **tendría** mucho cuidado antes de tomar una decisión.',
                native_sentence='In your place, I **would have** a lot of care before making a decision.',
                breakdown='The conditional **tendría** softens the advice with polite nuance using the stem **tendr-**.'
            ),
            card3_pronunciation=Card3Pronunciation(
                word='tendría',
                phonetic_breakdown='ten-**DRÍ**-a',
                stressed_syllables='**DRÍ**',
                audio_text='Yo en tu lugar tendría mucho cuidado.',
                phonetic_tips='The accent mark on í creates a clean hiatus: ten-DRÍ-a.'
            ),
            card4_speech=Card4Speech(
                target_phrase='Yo tendría mucho cuidado.',
                expected_phonetics='[ɟʝo tenˈdɾi.a ˈmu.tʃo kwiˈða.ðo]',
                key_focus_sounds='Clear hiatus in ten-DRÍ-a, soft d in cuidado.',
                practice_tip='Pronounce all 3 rhythmic syllables: ten-drí-a.'
            ),
            card5_quiz=Card5Quiz(
                sentence_prompt='Si tuviéramos más tiempo libre, nosotros _____ una mascota.',
                options=['tendríamos', 'teníamos', 'tuvimos', 'tendremos'],
                correct_index=0,
                correct_explanation='¡Perfecto! Following an unreal si-clause (*si tuviéramos...*), the result takes conditional: **tendríamos**.',
                distractor_explanations={
                    'teníamos': 'teníamos is imperfect.',
                    'tuvimos': 'tuvimos is preterite.',
                    'tendremos': 'tendremos is future.'
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: '¿Qué _____ tú si ganaras la lotería?'",
                micro_practice_options=['tendrías', 'tuviste', 'tienes', 'tengas'],
                micro_practice_correct_index=0,
                micro_practice_explanation="Excellent! With tú the conditional ending is **tendrías**."
            ),
            suggested_coach_prompts=[
                "How do I distinguish 'tendría' from 'tenía' when listening to spoken Spanish?",
                "How do you give polite advice using 'yo en tu lugar tendría...'?",
                "Why do 'si tuviera...' sentences always link to 'tendría' in the consequence?"
            ]
        ),
        'Presente de Subjuntivo': TenseFlashcardPack(
            tense_name='Presente de Subjuntivo',
            tense_order=10,
            card1_concept=Card1Concept(
                title='Card 1: Concept & Rule — Presente de Subjuntivo (Tenga, Tengas...)',
                rule='The **Presente de Subjuntivo** is formed by taking the 1st person singular present indicative stem (**teng-** from *yo tengo*) and adding opposite vowel endings (**-a-**): *tenga, tengas, tenga, tengamos, tengáis, tengan*.',
                usage_context='Required after expressions of desire (*quiero que tengas*), doubt, impersonal necessity (*es necesario que tengas paciencia*), and hopes (*ojalá que tengamos*).',
                triggers=['ojalá que', 'es necesario que', 'espero que', 'quiero que', 'dudo que', 'para que', 'es importante que'],
                conjugation_header='The present subjunctive derives from the 1st person yo-go stem teng-:',
                conjugations=[
                    'que yo tenga (that I have / that I may have)',
                    'que tú tengas (that you have)',
                    'que él/ella/usted tenga (that he/she/you formal has)',
                    'nosotros/as tengamos (that we have)',
                    'vosotros/as tengáis (that you all have)',
                    'ellos/ellas/ustedes tengan (that they/you all formal have)'
                ]
            ),
            card2_example=Card2Example(
                target_sentence='Es fundamental que **tengas** paciencia durante este proceso.',
                native_sentence='It is essential that you **have** patience during this process.',
                breakdown='The impersonal trigger phrase *es fundamental que* governs the subjunctive verb form **tengas**.'
            ),
            card3_pronunciation=Card3Pronunciation(
                word='tengas',
                phonetic_breakdown='**TEN**-gas',
                stressed_syllables='**TEN**',
                audio_text='Es fundamental que tengas paciencia durante este proceso.',
                phonetic_tips='Clean dental T and soft velar g before a: TEN-gas.'
            ),
            card4_speech=Card4Speech(
                target_phrase='Espero que tengas un buen día.',
                expected_phonetics='[esˈpe.ɾo ke ˈteŋ.ɡas um bwen ˈdi.a]',
                key_focus_sounds='Initial stress in **TEN**-gas, soft g sound.',
                practice_tip='Glide from que to tengas smoothly.'
            ),
            card5_quiz=Card5Quiz(
                sentence_prompt='Ojalá que nosotros _____ buenas noticias mañana.',
                options=['tengamos', 'tenemos', 'tuvimos', 'tendremos'],
                correct_index=0,
                correct_explanation='¡Extraordinario! Following desire particle **ojalá que**, the subjunctive is required: **tengamos**.',
                distractor_explanations={
                    'tenemos': 'tenemos is indicative.',
                    'tuvimos': 'tuvimos is preterite.',
                    'tendremos': 'tendremos is future.'
                },
                micro_practice_prompt="Quick Micro-Practice: Complete: 'Quiero que tú _____ mucho éxito.'",
                micro_practice_options=['tengas', 'tienes', 'tuvo', 'tendrás'],
                micro_practice_correct_index=0,
                micro_practice_explanation="Correct! Desiring another person to act requires subjunctive: **tengas**."
            ),
            suggested_coach_prompts=[
                "Why is the 'Yo-Rule' (yo tengo -> teng-) the key to forming Spanish subjunctive?",
                "Which impersonal phrases in Spanish always require the subjunctive?",
                "What is the difference in meaning between 'sé que tienes tiempo' and 'espero que tengas tiempo'?"
            ]
        )
    })

SPANISH_HACER_CURRICULUM = CurriculumCourse(
    topic_id='spanish_hacer',
    title='Spanish: Irregular Verbs — Verbo "Hacer"',
    target_language='Spanish',
    target_language_code='es',
    native_language='English',
    native_language_code='en',
    description="Master the essential Spanish irregular verb 'hacer' (to do / to make) across all core grammatical tenses.",
    tenses_roadmap=['Infinitivo', 'Gerundio', 'Participio', 'Presente de Indicativo', 'Pretérito Indefinido', 'Pretérito Imperfecto', 'Futuro Próximo', 'Futuro Simple', 'Condicional Simple', 'Presente de Subjuntivo'],
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
    tenses_roadmap=['Infinitivo', 'Gerundio', 'Participio', 'Presente de Indicativo', 'Pretérito Indefinido', 'Pretérito Imperfecto', 'Futuro Próximo', 'Futuro Simple', 'Condicional Simple', 'Presente de Subjuntivo'],
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
            tenses_roadmap=['Infinitivo', 'Gerundio', 'Participio', 'Presente de Indicativo', 'Pretérito Indefinido', 'Pretérito Imperfecto', 'Futuro Próximo', 'Futuro Simple', 'Condicional Simple', 'Presente de Subjuntivo'],
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
        tenses_roadmap=['Infinitivo', 'Gerundio', 'Participio', 'Presente de Indicativo', 'Pretérito Indefinido', 'Pretérito Imperfecto', 'Futuro Próximo', 'Futuro Simple', 'Condicional Simple', 'Presente de Subjuntivo'],
        cards_by_tense=cards
    )

