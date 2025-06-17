# Aethero Introspective Parser Audit (Phase1–5)

## 1. Architektonický prehľad

Moduly introspektívneho parsera sú rozdelené do piatich fáz. Orchestráciu zabezpečuje trieda `ParserRunner`. Každá fáza je implementovaná ako samostatný modul a využíva Pydantic dátové modely pre zdieľanie dát. 

- **Phase1LinguisticAnalyzer** – spracúva surový text pomocou spaCy a vytvára `LinguisticBlock`【F:ae_mind/src/introspective_parser/phase1_linguistic_analyzer.py†L16-L70】.
- **Phase2PsychologicalIntrospector** – z `LinguisticBlock` odvádza MBTI typy a emócie a vracia `PsychologicalBlock`【F:ae_mind/src/introspective_parser/phase2_psychological_introspector.py†L39-L120】.
- **Phase3SpeakerSynthesizer** – spája výstupy pre jednotlivých rečníkov do `SpeakerProfile`【F:ae_mind/src/introspective_parser/phase3_speaker_synthesizer.py†L13-L73】.
- **Phase4BehavioralAuditor** – hodnotí manipulatívne rétorické techniky a tvorí `BehavioralAuditBlock`【F:ae_mind/src/introspective_parser/phase4_behavioral_auditor.py†L13-L57】.
- **Phase5Ethics** – agreguje lexikálne skeny, hodnotové vektory a koherenciu do `EthicalVectorBlock`【F:ae_mind/src/introspective_parser/phase5_ethics.py†L15-L63】.

Moduly spolu komunikujú prostredníctvom `IntrospectiveInput`, `PsychologicalBlock` a `SpeakerProfile`. Kód je navrhnutý modulárne, pričom jednotlivé fázy sa dajú voliteľne spustiť samostatne.

## 2. Funkčný rozsah

- **Phase1** využíva spaCy na tokenizáciu, lemmatizáciu a dependency parsing. Výstup je serializovaný do Parquet a JSONL.
- **Phase2** obsahuje heuristický MBTI klasifikátor, detektor emócií a CSJoseph inferencer. Výstupom je `PsychologicalBlock` s metadátami o verziách modelov.
- **Phase3** zhromažďuje psychologické a jazykové bloky podľa `speaker_id` a vytvára longitudinálne profily.
- **Phase4** pomocou regexov zisťuje manipulatívne prvky (polarizačné rámovanie, rétorické otázky) a skóruje demagógiu či populizmus.
- **Phase5** kombinuje pravidlový lexikálny skener, heuristický etický model a tracker koherencie. Hodnotí ľudské práva, udržateľnosť, inkluzivitu a ďalšie kategórie.

Použité modely: spaCy (`sk_core_news_sm`), heuristiky pre MBTI a emócie, vlastné vektorové modely založené na jednoduchých kľúčových slovách.

## 3. Dátové štruktúry a IO

Dátové modely sú definované v `models.py` a zahŕňajú `Token`, `Sentence`, `LinguisticBlock`, `PsychologicalBlock`, `BehavioralAuditBlock`, `SpeakerProfile`, `IntrospectiveInput` a `EthicalVectorBlock`【F:ae_mind/src/introspective_parser/models.py†L1-L79】. 

Výstupy sa ukladajú do Parquet a JSONL súborov prostredníctvom metód `persist` v jednotlivých fázach【F:ae_mind/src/introspective_parser/phase1_linguistic_analyzer.py†L87-L118】【F:ae_mind/src/introspective_parser/phase2_psychological_introspector.py†L142-L156】【F:ae_mind/src/introspective_parser/phase3_speaker_synthesizer.py†L67-L92】.

## 4. Pipeline & runner

`ParserRunner` inicializuje všetky fázy a spúšťa ich v pevne danom poradí【F:ae_mind/src/introspective_parser/parser_runner.py†L4-L42】. Pre Phase5 sú vstupy komponované z predošlých blokov pomocou `IntrospectiveInput`. Pipeline je momentálne synchronná a nevyužíva lazy evaluation ani asynchrónne spracovanie.

## 5. Zložitosť & štruktúra kódu

- Počet modulov (Python súborov) v `introspective_parser`: 15.
- Celkový počet riadkov kódu v týchto moduloch: 1054.
- Testovacích prípadov: 5 súborov so 154 riadkami.
- Triedy: 12 hlavných tried (jedna pre každú fázu + dátové modely).
- Kód je priebežne dokumentovaný komentármi `# AETH:` a v pamäťových logoch.

Najrobustnejšie sú fázy 1 a 2, ktoré majú najviac testov a pokrývajú základné spracovanie textu. Phase5 je zatiaľ experimentálny modul.

## 6. Export & vizualizácia

`exporter.py` umožňuje exportovať všetky bloky do YAML s frontmatterom, Markdown a JSON formátu【F:ae_mind/src/introspective_parser/exporter.py†L1-L35】. Modul `run_pipeline.py` produkuje Parquet alebo JSONL výstupy vhodné pre ďalšie spracovanie. Vizualizácia v Streamlit zatiaľ nie je implementovaná, ale výstupy možno načítať do externých dashboardov.

## 7. Testovanie

V repozitári sa nachádza päť unit testov, ktoré overujú základnú funkčnosť každej fázy a celkovej pipeline【F:ae_mind/tests/test_parser.py†L1-L32】【F:ae_mind/tests/test_phase1.py†L1-L12】【F:ae_mind/tests/test_phase3.py†L1-L24】【F:ae_mind/tests/test_phase4.py†L1-L24】【F:ae_mind/tests/test_phase5.py†L1-L29】. Testy používajú jednoduché textové vstupy a kontrolujú konzistenciu dĺžok tokenov či prítomnosť etických vektorov.

## 8. Reflexia a odporúčania

Najstabilnejšie pôsobí Phase1LinguisticAnalyzer, ktorý už podporuje chunking, caching a validáciu dát. Phase5Ethics je zatiaľ heuristický a vyžaduje prepracovanie na základe robustnejších etických modelov. Do budúcnosti by sa mohla pipeline rozšíriť o asynchrónne spracovanie a automatizovaný export do Notion alebo Streamlit. Pre Phase6 sa odporúča nadviazať na existujúci `CoherenceTracker` a rozšíriť ho o semantické metriky.

