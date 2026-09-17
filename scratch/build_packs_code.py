import sys

# Define code for extra tenses for Hacer (PT)
HACER_PT_EXTRA = '''            'Pretérito Imperfecto': TenseFlashcardPack(
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
                    sentence_prompt='Si tuviéramos más presupuesto, nós _____ un viaje inolvidable.',
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
'''

print("Code defined successfully.")
