#!/usr/bin/env python3
"""🏆 ROS2 Projekt — Návrh kompletního robotického systému od A do Z."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def architektura_projektu():
    """
    🎯 VÝZVA 1: Architektura robotického projektu.
    Vrať dict:
    {
        "název": "Autonomní mobilní robot pro indoor navigaci",
        "balíčky": {
            "my_robot_description": "URDF/Xacro model robota",
            "my_robot_bringup": "launch soubory pro start systému",
            "my_robot_navigation": "konfigurace Nav2 a mapy",
            "my_robot_perception": "zpracování senzorových dat",
            "my_robot_interfaces": "custom messages a services",
            "my_robot_behavior": "vysokoúrovňová logika a state machine"
        },
        "workspace_struktura": '''ros2_ws/src/
├── my_robot_description/
│   ├── urdf/
│   ├── meshes/
│   ├── rviz/
│   └── launch/
├── my_robot_bringup/
│   ├── launch/
│   ├── config/
│   └── maps/
├── my_robot_perception/
│   ├── my_robot_perception/
│   └── launch/
├── my_robot_navigation/
│   ├── config/
│   ├── launch/
│   └── maps/
├── my_robot_interfaces/
│   ├── msg/
│   ├── srv/
│   └── action/
└── my_robot_behavior/
    ├── my_robot_behavior/
    └── launch/''',
        "princip": "každý balíček má jednu zodpovědnost (Single Responsibility)"
    }
    """
    # TODO: ↓
    pass


def bringup_a_konfigurace():
    """
    🎯 VÝZVA 2: Bringup — spuštění celého robota.
    Vrať dict:
    {
        "hlavní_launch": '''import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, GroupAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_desc = get_package_share_directory('my_robot_description')
    pkg_nav = get_package_share_directory('my_robot_navigation')
    pkg_perc = get_package_share_directory('my_robot_perception')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim', default_value='true'),
        DeclareLaunchArgument('map', default_value=os.path.join(pkg_nav, 'maps', 'office.yaml')),

        # Robot model + TF
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_desc, 'launch', 'robot_state.launch.py'))),

        # Navigace
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_nav, 'launch', 'navigation.launch.py')),
            launch_arguments={'map': LaunchConfiguration('map')}.items()),

        # Percepce
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_perc, 'launch', 'perception.launch.py'))),
    ])''',
        "params_yaml": '''my_robot:
  ros__parameters:
    robot_name: "kubo"
    max_linear_speed: 0.5
    max_angular_speed: 1.0
    sensor_update_rate: 30.0
    safety_distance: 0.3
    battery_low_threshold: 20.0''',
        "spuštění": {
            "simulace": "ros2 launch my_robot_bringup robot.launch.py use_sim:=true",
            "reálný_robot": "ros2 launch my_robot_bringup robot.launch.py use_sim:=false",
            "jen_nav": "ros2 launch my_robot_navigation navigation.launch.py map:=/path/to/map.yaml"
        }
    }
    """
    # TODO: ↓
    pass


def state_machine():
    """
    🎯 VÝZVA 3: Stavový automat — řízení chování robota.
    Vrať dict:
    {
        "co_je": "vysokoúrovňová logika robota — co dělat a kdy",
        "stavy": {
            "IDLE": "čeká na úkol",
            "NAVIGATING": "jede k cíli",
            "EXPLORING": "prozkoumává neznámé prostředí",
            "DOCKING": "parkuje u nabíjecí stanice",
            "ERROR": "chyba — zastaví se a čeká na pomoc",
            "LOW_BATTERY": "nízká baterie — jede k nabíječce"
        },
        "přechody": {
            "IDLE → NAVIGATING": "přijat nový cíl",
            "NAVIGATING → IDLE": "cíl dosažen",
            "NAVIGATING → ERROR": "navigace selhala",
            "* → LOW_BATTERY": "baterie pod 20%",
            "LOW_BATTERY → DOCKING": "nabíječka nalezena",
            "DOCKING → IDLE": "nabití dokončeno"
        },
        "implementace": '''from enum import Enum, auto

class RobotState(Enum):
    IDLE = auto()
    NAVIGATING = auto()
    EXPLORING = auto()
    DOCKING = auto()
    ERROR = auto()
    LOW_BATTERY = auto()

class StateMachine(Node):
    def __init__(self):
        super().__init__('state_machine')
        self.state = RobotState.IDLE
        self.timer = self.create_timer(0.1, self.tick)
        self.nav = BasicNavigator()

    def tick(self):
        if self.state == RobotState.IDLE:
            self.handle_idle()
        elif self.state == RobotState.NAVIGATING:
            self.handle_navigating()
        elif self.state == RobotState.LOW_BATTERY:
            self.handle_low_battery()

    def handle_idle(self):
        if self.battery < 20.0:
            self.transition(RobotState.LOW_BATTERY)
        elif self.has_goal():
            self.nav.goToPose(self.current_goal)
            self.transition(RobotState.NAVIGATING)

    def transition(self, new_state):
        self.get_logger().info(f'{self.state.name} → {new_state.name}')
        self.state = new_state''',
        "alternativy": ["BehaviorTree.CPP (Nav2 styl)", "SMACH (ROS1)", "FlexBE", "vlastní"]
    }
    """
    # TODO: ↓
    pass


def testovani_a_simulace():
    """
    🎯 VÝZVA 4: Testování a simulace ROS2 projektu.
    Vrať dict:
    {
        "unit_testy": {
            "framework": "pytest + launch_testing",
            "příklad": '''import pytest
from my_robot_perception.obstacle_detector import detect_obstacles

def test_no_obstacles():
    ranges = [10.0] * 360  # žádné překážky
    obstacles = detect_obstacles(ranges)
    assert len(obstacles) == 0

def test_single_obstacle():
    ranges = [10.0] * 360
    ranges[170:190] = [0.5] * 20  # překážka vpředu
    obstacles = detect_obstacles(ranges)
    assert len(obstacles) == 1'''
        },
        "integration_testy": {
            "popis": "launch_testing — spuštění nodů a kontrola chování",
            "příklad": '''import launch_testing
import pytest
import rclpy
from std_msgs.msg import String

@pytest.mark.launch_test
def generate_test_description():
    return LaunchDescription([
        Node(package='my_robot', executable='publisher'),
        launch_testing.actions.ReadyToTest()
    ])

class TestNode(unittest.TestCase):
    def test_message_received(self, proc_output):
        rclpy.init()
        node = rclpy.create_node('test_node')
        received = []
        node.create_subscription(String, '/topic',
            lambda msg: received.append(msg.data), 10)
        # Spin a čekej na zprávu
        assert len(received) > 0'''
        },
        "simulace": {
            "gazebo": "ros2 launch gazebo_ros gazebo.launch.py world:=my_world.world",
            "gazebo_spawn": '''Node(
    package='gazebo_ros',
    executable='spawn_entity.py',
    arguments=['-entity', 'my_robot', '-topic', 'robot_description'])''',
            "alternativy": ["Gazebo Classic", "Ignition Gazebo", "Webots", "Isaac Sim"]
        },
        "colcon_test": "colcon test --packages-select my_robot_perception && colcon test-result"
    }
    """
    # TODO: ↓
    pass


def dokumentace_a_deploy():
    """
    🎯 VÝZVA 5: Dokumentace, CI/CD a nasazení.
    Vrať dict:
    {
        "dokumentace": {
            "README": "popis projektu, instalace, spuštění, architektura",
            "topics_services": '''# Publikuje
/cmd_vel (geometry_msgs/Twist)       — příkazy pro řízení
/robot_status (my_interfaces/RobotStatus) — stav robota

# Odebírá
/scan (sensor_msgs/LaserScan)       — data z lidaru
/odom (nav_msgs/Odometry)           — odometrie

# Services
/get_robot_info (my_interfaces/GetRobotInfo)
/set_speed (my_interfaces/SetSpeed)''',
            "parametry": "tabulka všech parametrů s defaults a popisem",
            "diagram": "architektura jako rqt_graph nebo Mermaid"
        },
        "ci_cd": {
            "github_actions": '''name: ROS2 CI
on: [push, pull_request]
jobs:
  build-and-test:
    runs-on: ubuntu-22.04
    container: ros:humble
    steps:
      - uses: actions/checkout@v3
      - name: Install deps
        run: |
          apt-get update
          rosdep install --from-paths src -y --ignore-src
      - name: Build
        run: colcon build --symlink-install
      - name: Test
        run: colcon test && colcon test-result --verbose''',
            "docker": '''FROM ros:humble
COPY src/ /ros2_ws/src/
WORKDIR /ros2_ws
RUN apt-get update && rosdep install --from-paths src -y --ignore-src
RUN colcon build --symlink-install
CMD ["ros2", "launch", "my_robot_bringup", "robot.launch.py"]'''
        },
        "deploy_checklist": [
            "Všechny testy prochází",
            "Dokumentace aktuální",
            "Parametry konfigurovatelné (ne hardcoded)",
            "Logování na správných úrovních",
            "Graceful shutdown (cleanup)",
            "udev rules pro senzory",
            "Systemd service pro autostart"
        ],
        "systemd": '''[Unit]
Description=My Robot ROS2
After=network.target

[Service]
Type=simple
User=robot
ExecStart=/bin/bash -c "source /opt/ros/humble/setup.bash && source /home/robot/ros2_ws/install/setup.bash && ros2 launch my_robot_bringup robot.launch.py"
Restart=always

[Install]
WantedBy=multi-user.target'''
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Architektura projektu",
        theory="""Správná struktura = základ úspěchu:
  Každý balíček má jednu zodpovědnost:
  - description: model robota (URDF)
  - bringup: launch soubory, konfigurace
  - navigation: Nav2, mapy
  - perception: zpracování senzorů
  - interfaces: custom messages
  - behavior: logika robota

  Workspace:
  ros2_ws/src/
  ├── my_robot_description/
  ├── my_robot_bringup/
  └── ...  (jeden balíček = jeden účel)""",
        task="Navrhni architekturu robotického projektu s balíčky.",
        difficulty=1, points=15,
        hints=[
            "Odděluj description, bringup, navigation, perception",
            "Single Responsibility Principle i pro ROS2 balíčky"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "balíčky" in r
                    and len(r["balíčky"]) >= 4
                    and "workspace_struktura" in r,
                    "Architektura ✓"
                )
            )(architektura_projektu()),
        ]
    ),
    Challenge(
        title="Bringup a konfigurace",
        theory="""Bringup = hlavní launch pro celý systém:
  Zahrnuje:
  - Robot model (URDF + robot_state_publisher)
  - Navigace (Nav2)
  - Percepce (senzory)
  - Parametry z YAML

  IncludeLaunchDescription pro modularitu:
  Každý subsystém má svůj launch, bringup je spojuje.""",
        task="Navrhni bringup launch soubor s konfigurací.",
        difficulty=2, points=20,
        hints=[
            "IncludeLaunchDescription pro zahrnutí sub-launchů",
            "Parameters z YAML, DeclareLaunchArgument pro CLI"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "hlavní_launch" in r
                    and "params_yaml" in r
                    and "spuštění" in r,
                    "Bringup ✓"
                )
            )(bringup_a_konfigurace()),
        ]
    ),
    Challenge(
        title="Stavový automat",
        theory="""State machine = logika chování:
  IDLE → NAVIGATING → IDLE (úspěch)
  IDLE → NAVIGATING → ERROR (selhání)
  * → LOW_BATTERY → DOCKING → IDLE

  Implementace:
  - Enum pro stavy
  - Timer tick() pro pravidelnou kontrolu
  - Metoda pro každý stav
  - transition() pro přechody s logováním""",
        task="Implementuj stavový automat pro robota.",
        difficulty=3, points=25,
        hints=[
            "Enum pro stavy, tick() v timeru, transition()",
            "handle_idle(), handle_navigating() — metoda per stav"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "stavy" in r
                    and "přechody" in r
                    and "implementace" in r
                    and len(r["stavy"]) >= 4,
                    "State machine ✓"
                )
            )(state_machine()),
        ]
    ),
    Challenge(
        title="Testování a simulace",
        theory="""Testování ROS2 projektů:
  Unit testy: pytest pro čistou logiku
  Integration: launch_testing — spuštění nodů
  Simulace: Gazebo — virtuální svět + fyzika

  colcon test → spustí všechny testy
  colcon test-result → výsledky

  Gazebo:
  - spawn_entity.py pro vložení robota
  - gazebo plugins pro senzory""",
        task="Napiš testy a nastav simulaci.",
        difficulty=3, points=25,
        hints=[
            "pytest pro unit testy, launch_testing pro integrační",
            "Gazebo: spawn_entity.py, world soubory"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "unit_testy" in r
                    and "integration_testy" in r
                    and "simulace" in r,
                    "Testování ✓"
                )
            )(testovani_a_simulace()),
        ]
    ),
    Challenge(
        title="Dokumentace a deploy",
        theory="""Profesionální projekt potřebuje:
  Dokumentace:
  - README s instalací a spuštěním
  - Seznam topiců, services, parametrů
  - Diagram architektury

  CI/CD:
  - GitHub Actions s ROS2 kontejnerem
  - Docker pro reprodukovatelnost

  Deploy:
  - Systemd service pro autostart
  - udev rules pro senzory
  - Čistý shutdown""",
        task="Připrav dokumentaci, CI/CD a deploy.",
        difficulty=2, points=20,
        hints=[
            "README, topics list, CI s colcon build + test",
            "Docker + systemd pro produkční nasazení"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "dokumentace" in r
                    and "ci_cd" in r
                    and "deploy_checklist" in r
                    and len(r["deploy_checklist"]) >= 5,
                    "Dokumentace & deploy ✓"
                )
            )(dokumentace_a_deploy()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "ROS2 Projekt", "10_10")
