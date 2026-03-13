#!/usr/bin/env python3
"""🤖 STŘEDNÍ PROJEKTY — Projekty na několik dní s API, CV a data processing."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify


def projekt_api_roboticke_flotily():
    """🎯 VÝZVA 1: Architektura REST API pro Management Robotické Flotily
    
    Centralizovaný API pro kontrolu a monitoring více robotů:
    - CRUD operace pro roboty (registrace, update, delete)
    - Real-time status a telemetrie
    - Scheduling a task assignment
    - Autentizace a autorizace (JWT)
    - Rate limiting a caching
    - Webhooks pro notifikace
    
    Navrhněte celkový design s databází, middleware, error handling.
    """
    # TODO: ↓ Vrátit dict s architekturou API
    pass


def projekt_cv_pocitac_objektu():
    """🎯 VÝZVA 2: Computer Vision Systém pro Počítání Objektů
    
    Aplikace pro počítání položek na pásu, robotů v místnosti, součástek:
    - Detekce objektů pomocí YOLO/OpenCV
    - Tracking objektů mezi snímky
    - Statistika a reporting
    - Web UI pro real-time preview
    - Export dat (CSV, JSON)
    - Optimizace pro Jetson Nano (nižší výkon)
    
    Navrhněte architekturu s pipelinem inference → tracking → reporting.
    """
    # TODO: ↓ Vrátit dict s architekturou CV systému
    pass


def projekt_data_pipeline_etl():
    """🎯 VÝZVA 3: Data Pipeline ETL pro Robotickou Telemetrii
    
    Automatizovaný systém pro Extract-Transform-Load telemetrických dat:
    - Extract: data z více robotů (MQTT, REST, CSV)
    - Transform: čištění, normalizace, feature engineering
    - Load: do PostgreSQL, data warehouse
    - Schedulování a orchestrace (Airflow-like)
    - Data quality checks
    - Audit trail a recovery
    
    Navrhněte modulární pipeline s error handling a resilience.
    """
    # TODO: ↓ Vrátit dict s architekturou ETL pipeline
    pass


def projekt_framework_testovani():
    """🎯 VÝZVA 4: Vlastní Framework pro Automatizované Testování Robotů
    
    Testing framework specificky pro robotiku:
    - Test runner s parallelizací
    - Fixture pro setup/teardown robotů
    - Assertions pro robotické veličiny (toleranční pásy)
    - Integration s CI/CD (GitHub Actions, GitLab CI)
    - Coverage tracking
    - HTML reporty s fotkami
    - Mocking hardwaru
    
    Navrhněte framework analogický pytest s robot-specifickými features.
    """
    # TODO: ↓ Vrátit dict s architekturou testing frameworku
    pass


def projekt_cli_tool_argparse():
    """🎯 VÝZVA 5: CLI Tool s Click Framework pro Robotickou Konfiguraci
    
    Příkazový řádek pro jednoduchou konfiguraci a management robotů:
    - Příkazy: init-robot, deploy-firmware, monitor, calibrate
    - Subcommands: robot config set / get / list
    - Interaktivní mód pro složité operace
    - Config file support (.yaml)
    - Múdra auto-complete
    - Help s příklady
    - Logging na zařízení
    
    Navrhněte CLI s dobrou UX, ergonomií a dokumentací.
    """
    # TODO: ↓ Vrátit dict s architekturou CLI toolu
    pass


challenges = [
    Challenge(
        title="REST API Flotila Robotů",
        theory="""
DESIGN STŘEDNĚJŠÍCH PROJEKTŮ: API A BACKEND

1. **REST API Best Practices**
   - RESTful URL: /api/v1/robots/{id}
   - HTTP metody: GET, POST, PUT, DELETE
   - Status codes: 200, 201, 400, 401, 404, 500
   - Versioning pro kompatibilitu
   - Dokumentace: OpenAPI/Swagger
   
2. **Databázový Design**
   - Entity: Robot, Task, Status, Log
   - Relationships: Robot 1:N Tasks, Task N:M Robots
   - Normalizace: až 3NF
   - Indexy na query-heavy sloupce
   - Migration strategy (alembic)
   
3. **Authentication & Authorization**
   - JWT tokens namíste sessionů
   - Refresh tokens pro dlouhodobost
   - Role-based access control (admin, operator, viewer)
   - Rate limiting: 100 req/min na user
   
4. **Architektura**
   ```
   fastapi/flask/django
   ├── routes/ (API endpoints)
   ├── models/ (dataclasses, ORM)
   ├── services/ (business logic)
   ├── db/ (database access)
   ├── middleware/ (auth, logging)
   └── tests/
   ```
   
5. **Error Handling**
   - Custom exceptions třídy
   - Centrální error handler
   - Structured logging (JSON)
   - Error tracking (Sentry)
   
6. **Deployment**
   - Docker container
   - docker-compose pro dev stack
   - Kubernetes manifest pro prod
   - Health check endpoint
   - Graceful shutdown
   
7. **Git Workflow**
   - `develop` a `main` branch
   - PR ze `feature/*` do `develop`
   - Tag pro release `v1.2.3`
   - CHANGELOG.md s verzemi
        """,
        task="""Navrhněte REST API pro management robotické flotily.

Vrátit DICT s těmito POVINNÝMI klíči:
- 'jmeno_projektu': str
- 'framework': str (FastAPI, Flask, FastAPI, atd.)
- 'endpoints': list of dict (method, path, description)
- 'databaze': str (PostgreSQL, MongoDB, atd.)
- 'db_entity': list (Robot, Task, Status, atd.)
- 'authentication': str (JWT, OAuth2, atd.)
- 'authorization': dict (role definition)
- 'caching_strategie': str
- 'rate_limiting': str
- 'deployment': dict (Docker, K8s, atd.)
- 'monitoring': list (metrics k měření)
- 'tech_stack': list
- 'estimated_endpoints': int
- 'database_relationships': dict (cardinality)
        """,
        difficulty=3,
        points=20,
        hints=[
            "Minimálně 10 endpoints",
            "2 role: admin a operator",
            "Dataclass pro request/response DTOs",
            "PostgreSQL s SQLAlchemy ORM",
            "JWT s expirací"
        ],
        tests=[
            lambda result: verify(isinstance(result, dict), "Musí vracet dict"),
            lambda result: verify("framework" in result, "Chybí framework"),
            lambda result: verify("endpoints" in result and len(result["endpoints"]) >= 10, "Minimálně 10 endpoints"),
            lambda result: verify("databaze" in result, "Chybí databaze"),
            lambda result: verify("authentication" in result, "Chybí authentication"),
            lambda result: verify("db_entity" in result and len(result["db_entity"]) >= 3, "Minimálně 3 entity"),
        ]
    ),
    Challenge(
        title="Computer Vision Počítač",
        theory="""
COMPUTER VISION PRO PRŮMYSLOVOU AUTOMATIZACI

1. **Object Detection Pipeline**
   - YOLO v8: Real-time, vysoký accuracy
   - OpenCV: Basic image processing
   - Preprocessing: resize, normalize, augmentation
   - Inference: quantization pro embedded
   - Postprocessing: NMS, confidence thresholding
   
2. **Multi-Object Tracking**
   - Kalman filter pro predikci
   - Hungarian algorithm pro asociaci
   - Track ID generování
   - Track persistence (ztracení a nálezení)
   - Centrování objektů v 3D (pokud stereo kamera)
   
3. **Performance Optimization**
   - Quantization: FP32 → INT8
   - Pruning: zmenšení modelu
   - Batch processing
   - Jetson Nano specifika (CUDA, TensorRT)
   - Framesize trade-off
   
4. **Architektura Aplikace**
   ```
   cv_app/
   ├── inference/
   │  ├── detector.py (YOLO wrapper)
   │  └── tracker.py (Kalman + asociace)
   ├── metrics/
   │  ├── counter.py (počítadlo)
   │  └── reporter.py (statistika)
   ├── ui/
   │  └── web.py (Flask/FastAPI)
   └── storage/
      └── save_videos.py
   ```
   
5. **Deployment na Hardware**
   - Docker image pro Jetson
   - NVIDIA base image
   - CUDA libraries
   - Health monitoring
   
6. **Testing**
   - Unit test na detector
   - Mock YOLO model
   - Benchmark FPS
   - Accuracy na reference dataset
        """,
        task="""Navrhněte Computer Vision systém pro počítání objektů.

Vrátit DICT s těmito POVINNÝMI klíči:
- 'jmeno_projektu': str
- 'detection_model': str (YOLO, RetinaNet, atd.)
- 'tracking_algoritmus': str (Kalman, DeepSORT, atd.)
- 'supported_objects': list (co se bude detekovat)
- 'hardware_target': str (CPU, GPU, Jetson, atd.)
- 'fps_target': int
- 'accuracy_metric': str (mAP, precision, recall)
- 'deployment': dict (Docker, Kubernetes)
- 'ui_framework': str (Flask, FastAPI, WebSocket, atd.)
- 'export_formaty': list (CSV, JSON, Video, atd.)
- 'performance_optimization': list
- 'testing_strategie': dict
- 'modely_pro_trening': dict (dataset, epochs, atd.)
        """,
        difficulty=3,
        points=20,
        hints=[
            "Stáhněte existující YOLO model (v8s nebo menší)",
            "OpenCV pro video capture a display",
            "Flask se SocketIO pro real-time stream",
            "CSV export s timestampy",
            "Mock detection pro unit testy"
        ],
        tests=[
            lambda result: verify(isinstance(result, dict), "Musí vracet dict"),
            lambda result: verify("detection_model" in result, "Chybí detection_model"),
            lambda result: verify("tracking_algoritmus" in result, "Chybí tracking_algoritmus"),
            lambda result: verify("supported_objects" in result and len(result["supported_objects"]) >= 2, "Minimálně 2 objekty"),
            lambda result: verify("fps_target" in result and result["fps_target"] > 0, "FPS musí být > 0"),
        ]
    ),
    Challenge(
        title="ETL Data Pipeline",
        theory="""
ORCHESTRACE A ETL PROCESY PRO ROBOTIKU

1. **Data Sources v Robotice**
   - MQTT: Real-time topics (sensor/temperature/robot_1)
   - REST API: Polling robotických senzorů
   - CSV/Parquet: Batch files
   - Databáze: PostgreSQL live feeds
   - Log files: Parsování syslog
   
2. **Extract Fáze**
   - Connectors: adapter pattern pro různé zdroje
   - Incremental: delta loading (poslední 1 hod)
   - Error handling: reconnection policy
   - Caching: avoiding duplicates
   
3. **Transform Fáze**
   - Data cleansing: null hodnoty, duplicates
   - Type casting: raw string → float s jednotkami
   - Feature engineering: derived columns
   - Aggregations: rolling averages
   - Validation: schema checks
   
4. **Load Fáze**
   - Batch vs Stream: architektura
   - Transactions: ACID properties
   - Idempotency: safe retry
   - Partitioning: rok/měsíc/robot
   
5. **Orchestrace (Airflow-like)**
   - DAG: Directed Acyclic Graph
   - Tasks: extract, transform, load
   - Dependencies: task A → task B
   - Scheduling: CRON expressions
   - Retry logic: exponential backoff
   - Monitoring: task status, SLA
   
6. **Architektura**
   ```
   etl_pipeline/
   ├── extractors/
   │  ├── mqtt_extractor.py
   │  ├── api_extractor.py
   │  └── csv_extractor.py
   ├── transformers/
   │  ├── cleaner.py
   │  ├── validator.py
   │  └── aggregator.py
   ├── loaders/
   │  ├── postgres_loader.py
   │  └── s3_loader.py
   ├── scheduler/
   │  ├── dag_runner.py
   │  └── orchestrator.py
   └── monitoring/
      └── metrics.py
   ```
        """,
        task="""Navrhněte ETL pipeline pro robotickou telemetrii.

Vrátit DICT s těmito POVINNÝMI klíči:
- 'jmeno_projektu': str
- 'data_zdroje': list (MQTT, REST, CSV, atd.)
- 'extract_strategie': dict (incremental, batch, stream)
- 'transform_operace': list (cleansing, feature eng, atd.)
- 'target_database': str (PostgreSQL, Redshift, BigQuery)
- 'dag_tasks': list (task names v pořadí)
- 'scheduling': str (cron expression, frekvence)
- 'error_handling': dict (retry policy, alerting)
- 'monitoring': list (metrics k měření)
- 'estimated_volume': str (GB/den, records/sec)
- 'tech_stack': list (Airflow, Luigi, Python, atd.)
- 'data_quality_checks': list
- 'disaster_recovery': str (backup, rollback strategie)
        """,
        difficulty=3,
        points=20,
        hints=[
            "Dataclass pro pipeline config",
            "Abstract ExtractorBase třídu",
            "Scheduled.every().hour.do() pattern",
            "PostgreSQL s partitioningem",
            "JSON logy pro auditování"
        ],
        tests=[
            lambda result: verify(isinstance(result, dict), "Musí vracet dict"),
            lambda result: verify("data_zdroje" in result and len(result["data_zdroje"]) >= 2, "Minimálně 2 zdroje"),
            lambda result: verify("dag_tasks" in result and len(result["dag_tasks"]) >= 3, "Minimálně 3 tasky"),
            lambda result: verify("target_database" in result, "Chybí target_database"),
            lambda result: verify("scheduling" in result, "Chybí scheduling"),
        ]
    ),
    Challenge(
        title="Testing Framework pro Roboty",
        theory="""
TESTING FRAMEWORK DESIGN VZORŮ

1. **Pytest Architektura**
   - Fixtures: setup/teardown s auto-use
   - Parametrize: běh stejného testu s různými daty
   - Markers: @pytest.mark.slow, @pytest.mark.integration
   - Plugins: custom hooks a reports
   - Conftest.py: sdílená konfigurace
   
2. **Robot-Specific Testing**
   - Hardware mocking: Mock ROS2 nodes
   - Tolerance testu: float aproximace
   - Timeout handling: dlouhé operace
   - Integration testy: skutečný hardware
   - Performance testy: benchmark
   
3. **Fixture Strategy**
   ```python
   @pytest.fixture(scope="session")
   def robot_config():
       return load_config("test_config.yaml")
   
   @pytest.fixture
   def mock_robot(robot_config):
       return MockRobot(robot_config)
   
   def test_move_forward(mock_robot):
       # Test zde
   ```
   
4. **CI/CD Integration**
   - GitHub Actions: .github/workflows/test.yml
   - Triggers: push do develop, PR
   - Jobs: lint, unit, integration, coverage
   - Artifacts: test reports, coverage
   
5. **Coverage & Quality**
   - Coverage minimálně 80%
   - Coverage report HTML
   - Sonarqube integrace
   - Code quality checks (ruff, mypy)
   
6. **Parallel Testing**
   - pytest-xdist pro paralelizaci
   - Shared resources: database pooling
   - Flaky test detection
   
7. **Reporting**
   - JUnit XML pro CI/CD
   - HTML report s screenshoty
   - Performance profiling
   - Test execution time trending
        """,
        task="""Navrhněte testing framework pro robotické testy.

Vrátit DICT s těmito POVINNÝMI klíči:
- 'jmeno_projektu': str
- 'zaklada_se_na': str (pytest, unittest, own)
- 'fixture_typy': dict (session, module, function scopes)
- 'mock_objekty': list (MockRobot, MockSensor, atd.)
- 'test_kategorie': list (unit, integration, performance)
- 'tolerance_testu': dict (float precision, timeout, atd.)
- 'ci_cd_integration': str (GitHub Actions, GitLab CI, atd.)
- 'coverage_minimalně': int (procenta)
- 'paralelizace': str (xdist, thread, process)
- 'reporting_formaty': list (JUnit, HTML, atd.)
- 'test_parallelizace': bool
- 'tech_stack': list
- 'architektura': dict (jak se bude strukturovat)
        """,
        difficulty=3,
        points=20,
        hints=[
            "pytest s fixtures a parametrize",
            "Dataclass pro test config",
            "Mock třídy pro hardware",
            "pytest-cov pro coverage",
            "@pytest.fixture s autouse"
        ],
        tests=[
            lambda result: verify(isinstance(result, dict), "Musí vracet dict"),
            lambda result: verify("fixture_typy" in result, "Chybí fixture_typy"),
            lambda result: verify("mock_objekty" in result and len(result["mock_objekty"]) >= 3, "Minimálně 3 mock objekty"),
            lambda result: verify("test_kategorie" in result and "integration" in result["test_kategorie"], "Musí být integration testy"),
            lambda result: verify("coverage_minimalně" in result and result["coverage_minimalně"] >= 70, "Min 70% coverage"),
        ]
    ),
    Challenge(
        title="CLI Tool s Click Framework",
        theory="""
DESIGN COMMAND-LINE NÁSTROJŮ

1. **Click Framework Architektura**
   ```python
   @click.group()
   def cli(): pass
   
   @cli.command()
   @click.option('--robot-id', required=True)
   @click.option('--config', default='config.yaml')
   def deploy(robot_id, config):
       '''Deploy firmware na robota.'''
       pass
   
   @cli.group()
   def config(): pass
   
   @config.command()
   def list():
       '''Vypsat všechny konfigurace.'''
       pass
   ```
   
2. **UX Best Practices**
   - Jasné command names (deploy, calibrate)
   - Intuitivní flags (--verbose, --dry-run)
   - Help text s příklady
   - Confirmation pro destructivní akce
   - Progress bar pro dlouhé operace
   
3. **Configuration Management**
   - Config file: ~/.robotrc nebo ./robot.yaml
   - Environment variables backup
   - Priority: CLI args > env > config file
   - Validation: schema checking
   
4. **Interactive Mode**
   - click.prompt() pro vstupy
   - click.confirm() pro yes/no
   - Autocomplete: custom completer
   - History: readline
   
5. **Deployment & Distribution**
   - Setuptools entry points
   - Binary: PyInstaller
   - Shell completion: bash/zsh
   - Man pages: auto-generated
   
6. **Architektura**
   ```
   robot_cli/
   ├── cli/
   │  ├── __main__.py (entry point)
   │  ├── commands/
   │  │  ├── deploy.py
   │  │  ├── monitor.py
   │  │  └── config.py
   │  └── utils/
   │     ├── formatters.py
   │     └── validators.py
   ├── config/
   │  └── defaults.yaml
   └── tests/
      └── test_cli.py (s CliRunner)
   ```
   
7. **Testing CLI**
   - CliRunner z click.testing
   - Mock subprocessy
   - Capture output
   - Simulate user input
        """,
        task="""Navrhněte CLI tool pro robotickou konfiguraci.

Vrátit DICT s těmito POVINNÝMI klíči:
- 'jmeno_projektu': str
- 'commands': list (deploy, monitor, calibrate, atd.)
- 'hlavni_příkazy': list (top-level commands)
- 'subcommands': dict (groupů subcommands)
- 'globalni_flags': list (--verbose, --dry-run, atd.)
- 'config_file': str (cesta)
- 'interactive_tasks': list (které operace budou interaktivní)
- 'autocompletion': str (bash, zsh, both)
- 'help_system': dict (help text strategie)
- 'error_handling': list (jak se budou zobrazovat chyby)
- 'tech_stack': list (Click, Typer, atd.)
- 'deployment': str (pip, executable, Docker)
        """,
        difficulty=3,
        points=20,
        hints=[
            "Minimálně 8 commandů",
            "click.group() pro subcommands",
            "click.option pro flags",
            "click.prompt pro vstupy",
            "CliRunner pro testy"
        ],
        tests=[
            lambda result: verify(isinstance(result, dict), "Musí vracet dict"),
            lambda result: verify("commands" in result and len(result["commands"]) >= 8, "Minimálně 8 commandů"),
            lambda result: verify("subcommands" in result, "Chybí subcommands"),
            lambda result: verify("globalni_flags" in result and len(result["globalni_flags"]) >= 2, "Minimálně 2 global flags"),
            lambda result: verify("interactive_tasks" in result, "Chybí interactive_tasks"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Střední Projekty", "14_02")
