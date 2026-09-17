import re
import sys

# Define all 4 extra pack blocks

HACER_PT_EXTRA = ''',
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
            )'''

HACER_EN_EXTRA = ''',
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
        )'''

TENER_PT_EXTRA = ''',
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
        )'''

TENER_EN_EXTRA = ''',
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
        )'''

print("All extra packs compiled in script.")
