#!/usr/bin/env python3
"""🚀 MINI PROJEKTY — Jednoduché projekty na 1-2 hodiny s používáním OOP, souborů a API."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify


def projekt_kalkulacka_oop():
    """🎯 VÝZVA 1: Architektura Objektově Orientované Kalkulačky
    
    Navrhněte strukturu OOP kalkulačky s následujícími prvky:
    - Třídy pro jednotlivé operace
    - Systém undo/redo
    - Podpora pro vlastní operace
    - Logování výpočtů
    
    Vaše řešení by mělo navrhnout plnou architekturu včetně UML diagramu (jako text).
    """
    # TODO: ↓ Vrátit dict s architekturou kalkulačky
    pass


def projekt_organizator_souboru():
    """🎯 VÝZVA 2: Automatický Organizátor Souborů v Robotickém Projektu
    
    Pro robotický projekt s tisíci fotkami z kamer, logy a konfigurací:
    - Organizace podle data, typu souboru, robota
    - Automatické čistění duplikátů
    - Backup strategie
    - Práce se symlinky a archivy
    
    Navrhněte dataclass strukturu projektu s modulární architekturou.
    """
    # TODO: ↓ Vrátit dict s architekturou organizátoru
    pass


def projekt_generator_hesel():
    """🎯 VÝZVA 3: Bezpečnostní Generátor Hesel pro Robotické Systémy
    
    Bezpečné heslo pro SSH přístup na roboty, API klíče, databáze:
    - Různé úrovně bezpečnosti
    - Podpora pro custom pravidla (bez speciálních znaků pro embedded systémy)
    - Offline generace s entropy check
    - Export v různých formátech (JSON, CSV, password manager)
    
    Navrhněte celkovou architekturu s bezpečnostními best practices.
    """
    # TODO: ↓ Vrátit dict s architekturou generátoru
    pass


def projekt_analyzer_csv():
    """🎯 VÝZVA 4: Analyzer CSV Dat z Robotických Senzorů
    
    Analýza CSV souborů s telemetrií robota (teplota, vibrací, napětí):
    - Automatická detekce sloupců
    - Detekce anomálií a outlieru
    - Statistické shrnutí
    - Export reportů s grafy
    - Predikce selhání na základě trendů
    
    Navrhněte plugin-based architekturu pro rozšiřitelnost.
    """
    # TODO: ↓ Vrátit dict s architekturou analyzeru
    pass


def projekt_chatbot_jednoduchy():
    """🎯 VÝZVA 5: Jednoduchý Chatbot pro Diagnostiku Robotů
    
    Interaktivní nástroj pro troubleshooting robotických problémů:
    - Předdefinované How-To a FAQ
    - Stromová logika rozhodování (decision tree)
    - Logování problémů a řešení
    - Lokalizace do více jazyků
    - Export diagnostického reportu
    
    Navrhněte architekturu odpovídajícího systému s možností pozdějšího přidání NLP.
    """
    # TODO: ↓ Vrátit dict s architekturou chatbota
    pass


challenges = [
    Challenge(
        title="Kalkulačka s OOP",
        theory="""
ARCHITEKTURA JEDNODUCHÝCH PROJEKTŮ

Při navrhování mini-projektů se zaměřte na:

1. **Struktura a Moduly**
   - Jasné dělení odpovědnosti (SRP)
   - Jednoduché API pro ostatní části
   - Snadno testovatelné komponenty
   
2. **Git Workflow pro Mini Projekty**
   - feature/kalkulacka větev
   - Commit alespoň na začátku, uprostřed, na konci
   - Descriptivní commit messages
   - Pull request se self-review

3. **Dokumentace**
   - README s příklady použití
   - Docstrings pro veřejné API
   - Diagram v ASCII či Markdown
   - requirements.txt (i když prázdný)

4. **Testing Strategie**
   - Unit testy pro kritické funkce
   - Fixture pro setup
   - Test coverage minimálně 70%

5. **OOP Best Practices**
   - Polymorfismus místo kopírování kódu
   - Dataclasses pro jednoduché objekty
   - Type hints všude

6. **Portfolio Prezentace**
   - Screenshot funcionalit
   - Performance metrics
   - Lessons Learned sekce
   - Link na GitHub s open source licencí
        """,
        task="""Navrhněte plnou architekturu objektově orientované kalkulačky.

Vrátit DICT s těmito POVINNÝMI klíči:
- 'jmeno_projektu': str
- 'popis': str (2-3 věty)
- 'tridy': list of str (názvy všech tříd)
- 'hlavni_moduly': list of str
- 'tech_stack': list of str (jazyky, knihovny)
- 'databaze': str nebo 'ne'
- 'undo_redo_strategie': str (popis jak implementovat)
- 'testing_strategie': str (jaké testy psát)
- 'estimated_lines_of_code': int
- 'portfolio_prezentace': dict (kde se bude prezentovat, jaké features)
        """,
        difficulty=1,
        points=10,
        hints=[
            "Použijte abstraktní bází třídu pro operace",
            "Pattern: Strategy pro různé kalkulátor módy",
            "Uvažujte o Command pattern pro undo/redo",
            "dataclass pro operace s@property gettery"
        ],
        tests=[
            lambda result: verify(isinstance(result, dict), "Musí vracet dict"),
            lambda result: verify("jmeno_projektu" in result, "Chybí jmeno_projektu"),
            lambda result: verify("tridy" in result and isinstance(result["tridy"], list), "tridy musí být list"),
            lambda result: verify(len(result["tridy"]) >= 3, "Minimálně 3 třídy"),
            lambda result: verify("testing_strategie" in result, "Chybí testing_strategie"),
        ]
    ),
    Challenge(
        title="Organizátor Souborů",
        theory="""
PRÁCE SE SOUBORY A MODULÁRNÍ DESIGN

1. **Organizace Souborů pro Robotiku**
   - Standardní struktura: data/, logs/, config/, output/
   - Pojmenování s verzí a datem
   - Symlinky pro aktuální verzi
   
2. **Design Patterns pro Mini Projekty**
   - Observer: notifikace o změní
   - Factory: vytváření organizátorů
   - Decorator: přidávání funkcí
   
3. **Modulární Architektura**
   ```
   organizer/
   ├── core.py (hlavní logika)
   ├── strategies.py (různé způsoby třídění)
   ├── validators.py (kontrola souborů)
   └── backup.py (zálohování)
   ```
   
4. **Error Handling**
   - Custom výjimky pro různé situace
   - Graceful degradation pokud soubor chybí
   - Rollback při chybě
   
5. **Performance**
   - Lazy loading pro velké složky
   - Caching struktury
   - Async pro pomalé operace

6. **Git Best Practices Pro Mini Projekty**
   - `.gitignore` pro config s hesly
   - `tests/` složka na stejné úrovni
   - `ARCHITECTURE.md` popisující design
        """,
        task="""Navrhněte systém pro automatické organizování souborů robotického projektu.

Vrátit DICT s těmito POVINNÝMI klíči:
- 'jmeno_projektu': str
- 'organizacni_strategie': str (jak budou soubory tříděny)
- 'podporovane_typy_souboru': list
- 'moduly': list of str
- 'dataclasses': dict {název: popis}
- 'backup_strategie': str
- 'estimovane_pamet': str (kolik GB musí zvládnout)
- 'klicove_funkce': list of str (top 5)
- 'testovatelne_komponenty': list of str
- 'dokumentace': dict (co se bude dokumentovat)
        """,
        difficulty=1,
        points=10,
        hints=[
            "Použijte pathlib místo os.path",
            "Dataclass pro metadata souborů",
            "Strategy pattern pro různé organizace",
            "Vraťte dict s klíči specifickými pro robotiku"
        ],
        tests=[
            lambda result: verify(isinstance(result, dict), "Musí vracet dict"),
            lambda result: verify("organizacni_strategie" in result, "Chybí organizacni_strategie"),
            lambda result: verify("moduly" in result and len(result["moduly"]) >= 3, "Minimálně 3 moduly"),
            lambda result: verify("backup_strategie" in result, "Chybí backup_strategie"),
            lambda result: verify("klicove_funkce" in result and len(result["klicove_funkce"]) >= 5, "5 klíčových funkcí"),
        ]
    ),
    Challenge(
        title="Generátor Hesel",
        theory="""
BEZPEČNOST V ROBOTICKÝCH PROJEKTECH

1. **Bezpečné Generování Hesel**
   - Entropy: os.urandom() místo random
   - Požadavky: délka, znaky, složitost
   - Offline režim bez internetu
   - Validace na NIST standards
   
2. **Architektura pro Bezpečnost**
   - Strategie pro různé systémy (SSH, DB, API)
   - Konfigurabilní pravidla
   - Audit trail (co bylo vygenerováno)
   - Smazání z paměti po použití
   
3. **Integrace s Robotikou**
   - Speciální pravidla pro embedded systémy
   - Kompatibilita s firmware
   - IPv6 adresy (bez / v heslech)
   
4. **Export Formáty**
   - JSON: strukturovaný pro automatizaci
   - CSV: pro tabulky
   - Plain Text: pro copy-paste
   - Password Manager kompatibilita
   
5. **Best Practices**
   - Nikdy tisknout heslo přímo
   - Cleartext hesla jen v temp souboru
   - Šifrování na disku
   - Bezpečné smazání starých hesel

6. **Testing Bezpečnosti**
   - Distribution testu (homogenita entropie)
   - Kolize testu (žádné duplikáty)
   - Compliance testu (dodržení pravidel)
        """,
        task="""Navrhněte bezpečný generátor hesel pro robotické systémy.

Vrátit DICT s těmito POVINNÝMI klíči:
- 'jmeno_projektu': str
- 'algoritmus': str (jak se bude generovat)
- 'strategie': list of str (jaké strategie pro různé systémy)
- 'export_formaty': list
- 'bezpecnostni_pravidla': dict (minimální délka, znaky, atd.)
- 'embedded_kompatibilita': str (jak se bude řešit kompatibilita)
- 'audit_logging': str (co se bude logovat)
- 'testovani_entropie': list of str
- 'moduly_a_dependencies': list
- 'implementacni_casy': dict (kolik minut na která část)
        """,
        difficulty=2,
        points=15,
        hints=[
            "Zákaz použití random, jen os.urandom()",
            "Factory pattern pro různé strategie",
            "Custom výjimka pro slabá hesla",
            "Mock entropy test místo reálného generování"
        ],
        tests=[
            lambda result: verify(isinstance(result, dict), "Musí vracet dict"),
            lambda result: verify("algoritmus" in result, "Chybí algoritmus"),
            lambda result: verify("strategie" in result and len(result["strategie"]) >= 3, "Minimálně 3 strategie"),
            lambda result: verify("export_formaty" in result and len(result["export_formaty"]) >= 3, "Minimálně 3 export formáty"),
            lambda result: verify("testovani_entropie" in result, "Chybí testovani_entropie"),
        ]
    ),
    Challenge(
        title="Analyzer CSV",
        theory="""
DATOVÁ ANALÝZA PRO ROBOTIKU

1. **Telemetrické Údaje z Robotů**
   - Senzory: teplota, vibrace, síla, napětí, proud
   - Vysoká frekvence: 100+ Hz
   - Dlouhé doby: hodiny až dny měření
   - Outliers a šum
   
2. **Plugin-Based Architektura**
   ```python
   class AnalyzerPlugin(ABC):
       @abstractmethod
       def analyze(self, data: pd.DataFrame) -> dict: pass
   
   class TemperaturePlugin(AnalyzerPlugin): ...
   class VibrationPlugin(AnalyzerPlugin): ...
   ```
   
3. **Detekce Anomálií**
   - Z-score: outliers se 3σ
   - IQR metoda
   - Change point detection
   - Prediktivní failure detection
   
4. **Report Generation**
   - HTML se grafy
   - PDF pro archiv
   - JSON pro další processing
   - Alerting na kritické hodnoty
   
5. **Performance pro Velké Soubory**
   - Chunking namísto load-all
   - NumPy operace místo loops
   - Caching computed values
   
6. **Git Workflow**
   - `feature/csv-anomaly` větev
   - Test data v `tests/fixtures/`
   - Dokumentace s příklady CSV
        """,
        task="""Navrhněte systém pro analýzu CSV dat z robotických senzorů.

Vrátit DICT s těmito POVINNÝMI klíči:
- 'jmeno_projektu': str
- 'podporovane_senzory': list (teplota, vibrace, atd.)
- 'analyzer_pluginy': list (jaké pluginy)
- 'anomaly_detection_metody': list
- 'report_formaty': list
- 'predikce_selhani': str (jak se bude implementovat)
- 'performance_optimization': str (co se bude optimalizovat)
- 'data_struktura': dict (jaká kolumna, datový typ)
- 'minimalni_python_version': str
- 'dependencies': list (pandas, numpy, matplotlib, atd.)
        """,
        difficulty=2,
        points=15,
        hints=[
            "Pandas pro tabulkové operace",
            "matplotlib pro basic grafy",
            "Abstract class pro plugin interface",
            "Dataclass pro výsledky analýzy"
        ],
        tests=[
            lambda result: verify(isinstance(result, dict), "Musí vracet dict"),
            lambda result: verify("podporovane_senzory" in result, "Chybí podporovane_senzory"),
            lambda result: verify("analyzer_pluginy" in result and len(result["analyzer_pluginy"]) >= 3, "Minimálně 3 pluginy"),
            lambda result: verify("anomaly_detection_metody" in result, "Chybí anomaly_detection_metody"),
            lambda result: verify("report_formaty" in result and len(result["report_formaty"]) >= 2, "Minimálně 2 formáty"),
        ]
    ),
    Challenge(
        title="Chatbot Diagnostika",
        theory="""
INTERAKTIVNÍ SYSTÉMY A STROMOVITÁ LOGIKA

1. **Decision Tree Architektura**
   ```
   Problem?
   ├─ Robot se hýbe?
   │  ├─ Ano → Check motory
   │  └─ Ne → Check napájení
   └─ Komunikace?
      ├─ ROS2 offline
      └─ Timeout na topics
   ```
   
2. **State Machine Design**
   - Stavy: welcome, asking, diagnosing, solved, feedback
   - Transitions: user input → next state
   - Persistance: uložit stav pro resume
   
3. **Knowledge Base**
   - YAML/JSON soubory s FAQ
   - Versionování odpovědí
   - Multilingual support
   - Zápisem nových problémů
   
4. **Lokalizace**
   - i18n pro Czech, English, German
   - Pluralizace a formátování
   - Timezones pro timestamps
   
5. **Diagnostika Robotů**
   - Checklist pro každý problém
   - Příkazy k spuštění (ros2 topic echo)
   - Interpretace výstupů
   
6. **Logging a Audit**
   - JSON logy všech konverzací
   - Anonymizace senzitivních dat
   - Agregace pro trend analýzu
        """,
        task="""Navrhněte jednoduchý chatbot pro robotickou diagnostiku.

Vrátit DICT s těmito POVINNÝMI klíči:
- 'jmeno_projektu': str
- 'cil': str (jaké problémy řeší)
- 'stavenice_stavy': list (welcome, asking, atd.)
- 'knowledge_base_format': str (YAML, JSON, atd.)
- 'podporovane_jazyky': list
- 'decision_tree_uzly': int (odhadem)
- 'lokalizacni_strategie': dict
- 'diagnosticke_otazky': list (alespoň 5 příkladů)
- 'export_diagnostiky': list (formáty reportu)
- 'future_nlp_plan': str (jak přidat NLP později)
        """,
        difficulty=2,
        points=15,
        hints=[
            "Dataclass pro state a transitions",
            "Enum pro stavy",
            "Nested dict pro decision tree",
            "i18n knihovna pro lokalizaci"
        ],
        tests=[
            lambda result: verify(isinstance(result, dict), "Musí vracet dict"),
            lambda result: verify("cil" in result, "Chybí cil"),
            lambda result: verify("stavenice_stavy" in result and len(result["stavenice_stavy"]) >= 3, "Minimálně 3 stavy"),
            lambda result: verify("diagnosticke_otazky" in result and len(result["diagnosticke_otazky"]) >= 5, "Minimálně 5 otázek"),
            lambda result: verify("future_nlp_plan" in result, "Chybí future_nlp_plan"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Mini Projekty", "14_01")
