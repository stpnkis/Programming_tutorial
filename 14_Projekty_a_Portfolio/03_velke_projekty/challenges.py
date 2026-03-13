#!/usr/bin/env python3
"""🏆 VELKÉ PROJEKTY — Capstone projekty na týdny s komplexní architekturou a nasazením."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify


def projekt_autonomni_navigace():
    """🎯 VÝZVA 1: Autonomní Systém pro Navigaci Robota v Neznámém Prostředí
    
    Komplexní systém pro navigaci mobilního robota bez mapy:
    - SLAM (Simultaneous Localization and Mapping)
    - ROS2 integration (nodes, topics, services)
    - Sensor fusion: lidar, camera, IMU
    - Path planning algoritmy (RRT, A*)
    - Obstacle avoidance: local planning
    - Multi-robot coordination
    - Simulation v Gazebo
    - Real hardware testing
    
    Capstone projekt s 6-8 týdny vývoje, integrací multiple komponent.
    """
    # TODO: ↓ Vrátit dict s úplným plánem systému
    pass


def projekt_ml_inspekce_kvality():
    """🎯 VÝZVA 2: ML-Powered Systém pro Kontrolu Kvality Výroby
    
    Plný ML pipeline od sběru dat až k produkci modelu:
    - Data collection: fotky součástek z kamer
    - Annotation: labeling defektů
    - Model training: CNN pro klasifikaci
    - Evaluation: metriky, confusion matrix
    - Deployment: inference on edge device (Jetson)
    - A/B testing: porovnání modelů v produkci
    - Feedback loop: kontinuální vylepšování
    
    Komplexní ML project s DevOps komponentami.
    """
    # TODO: ↓ Vrátit dict s ML pipeline architekturou
    pass


def projekt_ros2_aplikace():
    """🎯 VÝZVA 3: Komplexní ROS2 Robotická Aplikace
    
    Plná robotická aplikace s více subsystémy:
    - Manipulátor arm control (inverse kinematics)
    - Gripper control s feedback
    - Vision system: object detection a picking
    - Safety systems: collision detection, E-stop
    - Task execution engine
    - Teleoperation UI
    - Hardware abstraction layer
    - Diagnostika a error recovery
    
    ROS2-based projekt s konfigurací v URDF, YAML, launch files.
    """
    # TODO: ↓ Vrátit dict s ROS2 architekturou
    pass


def projekt_iot_sensor_dashboard():
    """🎯 VÝZVA 4: IoT Sensorová Síť s Real-Time Dashboardem
    
    Distribuovaný systém IoT senzorů s centrálním dashboardem:
    - Senzorové uzly: ESP32 s WiFi
    - Gateway: komunikace s cloudem
    - Backend: API a databáze
    - Frontend: Real-time dashboard s WebSockets
    - Analytics: agregace a trend analýza
    - Alerting: notifikace při anomáliích
    - Data storage: time-series database
    - Historické reporting
    
    Multi-layer systém s hardware, firmware, backend, frontend.
    """
    # TODO: ↓ Vrátit dict s IoT architektury
    pass


def projekt_cicd_robotika():
    """🎯 VÝZVA 5: Kompletní CI/CD Pipeline pro Robotický Projekt
    
    DevOps infrastruktura pro robotické aplikace:
    - Source control: Git workflow
    - Build: kompilace, static analysis
    - Test: unit, integration, hardware-in-the-loop
    - Artifact management: binární balíčky
    - Staging environment: pre-production
    - Deployment: na roboty, cloudové servery
    - Monitoring: metrics, logs, tracing
    - Rollback strategie
    
    Kompletní DevOps pipeline od commitů k produkci.
    """
    # TODO: ↓ Vrátit dict s CI/CD pipeline plánem
    pass


challenges = [
    Challenge(
        title="Autonomní Navigace Robota",
        theory="""
CAPSTONE PROJEKTY: KOMPLEXNÍ ROBOTICKÉ SYSTÉMY

1. **Autonomní Navigace Architektura**
   - SLAM: Gmapping, Cartographer (ROS2)
   - Sensor Fusion: Kalman filter pro odometrii
   - Path Planning: global (A*, Dijkstra) + local (DWA)
   - Obstacle Detection: lidar point clouds
   - Multi-sensor Integration: lidar + camera + IMU
   
2. **ROS2 Architecture Design**
   ```
   Navigation Stack
   ├── SLAM Node: /slam/map topic
   ├── Localization: /amcl/pose
   ├── Path Planning: /move_base_simple/goal srv
   ├── Trajectory Control
   └── Motor Command
   
   Sensor Nodes
   ├── /lidar/scan
   ├── /camera/image_raw
   └── /imu/data
   ```
   
3. **Simulation & Testing**
   - Gazebo: physical simulation
   - World files: virtuální prostředí
   - MoveIt: motion planning
   - Hardware-in-the-Loop: real sensors
   - Benchmark: performance metrics
   
4. **Real Hardware Consideration**
   - Computation: resource constraints
   - Latency: real-time requirements
   - Power: battery management
   - Safety: E-stop, zones awareness
   - Calibration: extrinsic camera params
   
5. **Multi-Robot Coordination**
   - Centralized: leader-follower
   - Distributed: consensus algorithm
   - Communication: ROS2 bridges
   - Collision avoidance: velocity obstacles
   
6. **Project Management**
   - Milestones: month 1 SLAM, month 2 planning
   - Risk: sensor drift, computational load
   - Integration: nightly builds
   - Documentation: API, tutorials, videos
   
7. **Portfolio Presentation**
   - Video demo: autonomní jízda a mapování
   - GitHub: open-source s MIT license
   - Blog post: technical deep-dive
   - Comparison: s konkurenčními řešeními
   - Performance metrics: accuracy, speed
        """,
        task="""Navrhněte kompletní systém autonomní navigace.

Vrátit DICT s těmito POVINNÝMI klíči:
- 'jmeno_projektu': str
- 'duration_weky': int (min 6)
- 'cil': str (co bude umět)
- 'slam_algoritmus': str (Gmapping, Cartographer, atd.)
- 'path_planning': dict (global, local algoritmy)
- 'sensory': list (lidar, camera, IMU, atd.)
- 'ros2_nodes': list (jména a funkce uzlů)
- 'topics': dict (topic names, message types)
- 'services': list (srv endpoints)
- 'gazebo_simulation': bool
- 'real_hardware': str (robot model)
- 'multi_robot_support': bool
- 'safety_features': list
- 'testing_strategie': dict (simulation, real world)
- 'deployment': str (Docker, systemd, atd.)
- 'team_role': dict (developer roles)
- 'risk_mitigation': list
        """,
        difficulty=5,
        points=50,
        hints=[
            "ROS2 foxy nebo novější",
            "Nav2 stack pro path planning",
            "MoveIt pro manipulation",
            "Gazebo se URDF robota",
            "pytest jako testing framework"
        ],
        tests=[
            lambda result: verify(isinstance(result, dict), "Musí vracet dict"),
            lambda result: verify("slam_algoritmus" in result, "Chybí slam_algoritmus"),
            lambda result: verify("ros2_nodes" in result and len(result["ros2_nodes"]) >= 5, "Minimálně 5 ROS2 nodes"),
            lambda result: verify("duration_weky" in result and result["duration_weky"] >= 6, "Minimálně 6 týdnů"),
            lambda result: verify("testing_strategie" in result, "Chybí testing_strategie"),
        ]
    ),
    Challenge(
        title="ML Systém Inspekce Kvality",
        theory="""
MACHINE LEARNING PIPELINE DESIGN

1. **Data Collection Phase**
   - Setup: industrial camera mount
   - Lighting: standardizované podmínky
   - Acquisition: fotky normálních + defektních
   - Storage: S3, local SSD
   - Versioning: DVC (Data Version Control)
   
2. **Data Annotation**
   - Tool: CVAT, Labelbox
   - Labels: OK, defekt_A, defekt_B
   - Human review: QA kontrola
   - Workflow: train (80%) + val (10%) + test (10%)
   
3. **Model Training**
   - Framework: PyTorch, TensorFlow
   - Architecture: ResNet50, EfficientNet, ViT
   - Transfer learning: pre-trained ImageNet
   - Hyperparams: batch size 32, lr 0.001
   - Augmentation: rotation, brightness, blur
   
4. **Model Evaluation**
   - Metrics: accuracy, precision, recall, F1
   - Confusion matrix: detekce chyb
   - ROC curve: threshold selection
   - Edge cases: těžké vzorky
   
5. **Deployment Strategy**
   - Quantization: FP32 → INT8 (30% rychleji)
   - Model compression: pruning
   - Framework: ONNX pro interoperability
   - Edge device: Jetson Nano, Coral TPU
   - Inference latency: < 100ms
   
6. **Continuous Improvement**
   - A/B testing: starý vs nový model
   - Feedback loop: sbírání failure cases
   - Model retraining: monthly
   - Metrics tracking: MLflow, Weights & Biases
   - Version management: model registry
   
7. **CI/CD for ML**
   - Automatic testing: accuracy > 95%
   - Data validation: schema checks
   - Model validation: test set evaluation
   - Deployment: gradual rollout (10% → 100%)
   - Monitoring: prediction drift detection
        """,
        task="""Navrhněte kompletní ML pipeline pro inspekci kvality.

Vrátit DICT s těmito POVINNÝMI klíči:
- 'jmeno_projektu': str
- 'duration_weky': int (min 8)
- 'cast_kvality': str (co se kontroluje)
- 'data_collection': dict (camera, osvětlení, počet fotek)
- 'annotation_tool': str (CVAT, Labelbox, atd.)
- 'defekt_typy': list (jaké defekty detekovat)
- 'model_architektura': str (ResNet, EfficientNet, ViT)
- 'framework': str (PyTorch, TensorFlow)
- 'transfer_learning': bool
- 'target_accuracy': int (procenta)
- 'quantization': bool
- 'edge_device': str (Jetson, TPU, CPU)
- 'inference_latency_ms': int
- 'anotace_procesy': dict (labeling workflow)
- 'ab_testing_strategie': str
- 'monitoring': list (metriky k sledování)
- 'retraining_frekvence': str (weekly, monthly)
        """,
        difficulty=5,
        points=50,
        hints=[
            "PyTorch s torchvision pro transfer learning",
            "Albumentations pro augmentation",
            "scikit-learn pro metriky",
            "Ray Tune pro hyperparameter tuning",
            "ONNX pro model export"
        ],
        tests=[
            lambda result: verify(isinstance(result, dict), "Musí vracet dict"),
            lambda result: verify("defekt_typy" in result and len(result["defekt_typy"]) >= 2, "Minimálně 2 typy defektů"),
            lambda result: verify("model_architektura" in result, "Chybí model_architektura"),
            lambda result: verify("target_accuracy" in result and result["target_accuracy"] >= 85, "Min 85% accuracy"),
            lambda result: verify("duration_weky" in result and result["duration_weky"] >= 8, "Minimálně 8 týdnů"),
        ]
    ),
    Challenge(
        title="ROS2 Robotická Aplikace",
        theory="""
ROS2 SYSTÉMOVÝ DESIGN PRO KOMPLEXNÍ ROBOTY

1. **Hardware Architecture**
   - Main computer: PC, Jetson, mini-PC
   - Real-time OS: nie (kontrola motorů za 10ms)
   - Communication: ROS2 DDS middleware
   - I/O: GPIO, serial, CAN bus
   
2. **ROS2 Node Structure**
   ```
   application_layer/
   ├── task_executor (state machine)
   ├── perception (vision, sensors)
   ├── planning (IK, trajectory)
   └── control (motor commands)
   
   driver_layer/
   ├── arm_driver (URDF, kinematics)
   ├── gripper_driver (sensors)
   ├── camera_driver (ROS2 wrapper)
   └── safety_monitor (E-stop, zones)
   ```
   
3. **Configuration Management**
   - URDF: robot kinematic chain
   - YAML: params, gains, limits
   - Launch files: node composition
   - Namespacing: multiple instances
   
4. **Real-Time Capabilities**
   - Real-time kernel: PREEMPT_RT patch
   - Thread priorities: SCHED_FIFO
   - Lock-free data structures
   - Message priorities: QoS policies
   
5. **Safety Mechanisms**
   - E-stop circuit: hardwired cutoff
   - Monitored stop: software verification
   - Joint limits: enforcement
   - Collision detection: force feedback
   - Health monitoring: sensor checks
   
6. **Teleoperation Interface**
   - ROS2 web UI: roslibjs
   - Joystick: /joy topic
   - Keyboard control: rqt plugin
   - First-person view: video stream
   
7. **Diagnostika a Debugging**
   - rqt: visual debugging
   - rosbag2: record/playback
   - tf2 tree: frame debugging
   - Parameter introspection
   
8. **Project Management**
   - Scrum: weekly sprints
   - Integration: nightly builds
   - Staging: pre-production robot
   - Deployment: over-the-air updates
        """,
        task="""Navrhněte kompletní ROS2 robotickou aplikaci.

Vrátit DICT s těmito POVINNÝMI klíči:
- 'jmeno_projektu': str
- 'robot_typ': str (manipulator, mobile, humanoid, atd.)
- 'dof': int (degrees of freedom)
- 'hardware': dict (PC spec, Jetson, atd.)
- 'ros2_distribuci': str (Foxy, Humble, Iron)
- 'application_nodes': list (task_executor, perception, atd.)
- 'driver_nodes': list
- 'urdf_struktury': list (links, joints)
- 'launch_files': list (hlavní launchfile a sub-launchfiles)
- 'yaml_parameters': dict
- 'real_time_requirements': dict (latency, frequency)
- 'safety_features': list
- 'teleoperation_interface': str (web, joystick, hmi, atd.)
- 'diagnostika_nastroje': list (rqt, rosbag2, atd.)
- 'middleware': str (DDS implementace)
- 'qos_policy': dict (reliability, durability)
- 'hardware_abstraction': str (jak se abstrahuje hardware)
        """,
        difficulty=5,
        points=50,
        hints=[
            "ROS2 navigation stack",
            "MoveIt2 pro arm planning",
            "URDF s collision meshes",
            "Launch files s composable nodes",
            "lifecycle nodes pro graceful startup"
        ],
        tests=[
            lambda result: verify(isinstance(result, dict), "Musí vracet dict"),
            lambda result: verify("robot_typ" in result, "Chybí robot_typ"),
            lambda result: verify("application_nodes" in result and len(result["application_nodes"]) >= 3, "Minimálně 3 application nodes"),
            lambda result: verify("safety_features" in result and len(result["safety_features"]) >= 3, "Minimálně 3 safety features"),
            lambda result: verify("real_time_requirements" in result, "Chybí real_time_requirements"),
        ]
    ),
    Challenge(
        title="IoT Sensorová Síť",
        theory="""
IOT SYSTÉM DESIGN S EDGE-TO-CLOUD ARCHITEKTUROU

1. **Hardware Layer**
   - Endpoints: ESP32 s WiFi, LoRaWAN
   - Sensors: temperature, humidity, pressure
   - Power: battery + solar panel
   - Storage: local SD card
   
2. **Node Software**
   - Firmware: MicroPython, Arduino
   - Communication: MQTT, CoAP
   - Local processing: threshold alerting
   - Power management: sleep modes
   
3. **Gateway Architecture**
   - MQTT broker: Mosquitto, AWS IoT Core
   - Message routing: topic subscriptions
   - Data transformation: payload parsing
   - Buffering: offline data queue
   
4. **Backend Services**
   - API: REST/GraphQL
   - Database: InfluxDB (time-series)
   - Cache: Redis (recent values)
   - Message queue: Kafka (event stream)
   
5. **Frontend Dashboard**
   - Real-time updates: WebSocket
   - Visualizations: line charts, gauges
   - Alerts: push notifications
   - Histor report: date range queries
   - Export: CSV, PDF
   
6. **Analytics & ML**
   - Aggregations: hourly, daily averages
   - Anomaly detection: statistical
   - Forecasting: time-series prediction
   - Correlation analysis: between sensors
   
7. **Deployment Topology**
   - Cloud: AWS, GCP, Azure
   - Edge: on-premise server
   - Hybrid: cloud + local backup
   - Redundancy: multi-broker failover
   
8. **DevOps & Monitoring**
   - Docker: containerized services
   - Kubernetes: orchestration
   - Prometheus: metrics
   - ELK: logging (Elasticsearch, Logstash, Kibana)
        """,
        task="""Navrhněte kompletní IoT sensorovou síť.

Vrátit DICT s těmito POVINNÝMI klíči:
- 'jmeno_projektu': str
- 'pocet_uzlu': int (odhadem)
- 'senzor_typy': list (teplota, vlhkost, atd.)
- 'hardware_endpoints': str (ESP32, Arduino, atd.)
- 'komunikacni_protokol': str (MQTT, CoAP, atd.)
- 'gateway': str (Mosquitto, AWS IoT, atd.)
- 'backend_framework': str (FastAPI, Django, atd.)
- 'timeseries_db': str (InfluxDB, Prometheus, atd.)
- 'frontend_framework': str (React, Vue, atd.)
- 'realtime_tech': str (WebSocket, SSE, atd.)
- 'analytics': list (co se bude analytizovat)
- 'deployment': str (AWS, on-premise, hybrid)
- 'redundance': str (failover strategie)
- 'skalabilita': str (kolik uzlů se bude podporovat)
- 'monitoring': list (Prometheus, Grafana, atd.)
- 'alerting_rules': dict (thresholds)
- 'data_retention': str (kolik mesiecu)
        """,
        difficulty=5,
        points=50,
        hints=[
            "MQTT pro lightweight communication",
            "InfluxDB pro time-series storage",
            "FastAPI + SQLAlchemy pro backend",
            "React nebo Vue pro frontend",
            "Docker Compose pro dev environment"
        ],
        tests=[
            lambda result: verify(isinstance(result, dict), "Musí vracet dict"),
            lambda result: verify("senzor_typy" in result and len(result["senzor_typy"]) >= 3, "Minimálně 3 typy senzorů"),
            lambda result: verify("komunikacni_protokol" in result, "Chybí komunikacni_protokol"),
            lambda result: verify("frontend_framework" in result, "Chybí frontend_framework"),
            lambda result: verify("analytics" in result and len(result["analytics"]) >= 2, "Minimálně 2 analytics"),
        ]
    ),
    Challenge(
        title="CI/CD Pipeline Robotika",
        theory="""
DEVOPS & CI/CD PRO ROBOTICKÉ PROJEKTY

1. **Source Control Workflow**
   - Branches: main, develop, feature/*, hotfix/*
   - Commits: conventional commits (feat:, fix:, etc.)
   - PRs: code review, tests, linting
   - Merge strategy: squash pro features
   
2. **Build Pipeline**
   - Compilation: C/C++ robot firmware
   - Static analysis: ruff, mypy, clang-tidy
   - Security scan: bandit, OWASP dependency check
   - Artifact generation: binaries, Docker images
   
3. **Testing Stages**
   - Unit tests: pytest, gtest
   - Integration tests: ROS2 node interaction
   - Manual test: hardware validation
   - Performance tests: benchmark suite
   - Hardware-in-the-loop: real hardware
   
4. **CI/CD Platform**
   - GitHub Actions, GitLab CI, Jenkins
   - Trigger: on push/PR
   - Parallel jobs: reduce build time
   - Caching: dependencies, Docker layers
   - Status badges: build, coverage
   
5. **Artifact Management**
   - Binary repository: Artifactory, Nexus
   - Container registry: Docker Hub, ECR
   - Version tagging: semantic versioning
   - Release notes: automated changelog
   
6. **Deployment Strategy**
   - Staging: pre-production environment
   - Blue-green: zero-downtime deployment
   - Canary: gradual rollout (10% → 50% → 100%)
   - Rollback: previous version recovery
   
7. **Monitoring & Observability**
   - Metrics: Prometheus, Datadog
   - Logging: ELK, CloudWatch
   - Tracing: Jaeger, Zipkin
   - Alerting: PagerDuty, Slack
   - Dashboard: Grafana
   
8. **Documentation**
   - README: setup, usage, troubleshooting
   - API docs: OpenAPI/Swagger
   - Architecture: diagrams, decision records
   - Runbooks: operational procedures
   - Troubleshooting guides
   
9. **Team Structure**
   - Tech lead: architecture decisions
   - DevOps engineer: infrastructure
   - QA engineer: test strategy
   - Release manager: deployment coordination
        """,
        task="""Navrhněte kompletní CI/CD pipeline pro robotickou aplikaci.

Vrátit DICT s těmito POVINNÝMI klíči:
- 'jmeno_projektu': str
- 'repository_platform': str (GitHub, GitLab, Gitea)
- 'branch_strategie': str (git flow, trunk-based, atd.)
- 'ci_cd_platform': str (GitHub Actions, GitLab CI, Jenkins)
- 'build_stages': list (compile, lint, test, package)
- 'testing_frameworky': list (pytest, gtest, atd.)
- 'test_stages': list (unit, integration, hardware)
- 'static_analysis_tools': list (ruff, mypy, clang-tidy, atd.)
- 'artifact_repository': str (Artifactory, ECR, atd.)
- 'container_registry': str (Docker Hub, ECR, atd.)
- 'deployment_strategy': str (blue-green, canary, atd.)
- 'deployment_targets': list (robot hardware, cloud, atd.)
- 'monitoring_metrics': list
- 'alerting_channels': list (Slack, PagerDuty, atd.)
- 'rollback_strategie': str
- 'security_controls': list (SAST, dependency check, atd.)
- 'documentation_coverage': str (API docs, runbooks, atd.)
- 'success_metrics': dict (deployment frequency, lead time, atd.)
        """,
        difficulty=5,
        points=50,
        hints=[
            "GitHub Actions s YAML workflows",
            "Docker pro standardizované environments",
            "pytest s coverage reporting",
            "Semantic versioning pro releases",
            "Slack notifications pro status"
        ],
        tests=[
            lambda result: verify(isinstance(result, dict), "Musí vracet dict"),
            lambda result: verify("ci_cd_platform" in result, "Chybí ci_cd_platform"),
            lambda result: verify("build_stages" in result and len(result["build_stages"]) >= 4, "Minimálně 4 build stages"),
            lambda result: verify("test_stages" in result and len(result["test_stages"]) >= 3, "Minimálně 3 test stages"),
            lambda result: verify("monitoring_metrics" in result and len(result["monitoring_metrics"]) >= 3, "Minimálně 3 monitoring metriky"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Velké Projekty", "14_03")
