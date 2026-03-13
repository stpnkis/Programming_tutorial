#!/usr/bin/env python3
"""🔧 ROS2 Instalace a Setup — Workspace, packages, colcon."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def ros2_prehled():
    """
    🎯 VÝZVA 1: Co je ROS2?
    Vrať dict:
    {
        "název": "Robot Operating System 2",
        "co_je": "middleware framework pro robotiku (NE operační systém)",
        "vlastnosti": ["distribuovaný systém", "real-time capable", "multi-platformový", "DDS komunikace"],
        "vs_ros1": {
            "komunikace": "DDS (ROS2) vs vlastní TCP (ROS1)",
            "real_time": "ano (ROS2) vs ne (ROS1)",
            "lifecycle": "managed nodes (ROS2) vs ne (ROS1)",
            "python": "rclpy (ROS2) vs rospy (ROS1)"
        },
        "distribuce": ["Humble (LTS 2027)", "Iron", "Jazzy"]
    }
    """
    # TODO: ↓
    pass


def workspace_setup():
    """
    🎯 VÝZVA 2: Vytvoření ROS2 workspace.
    Vrať dict s příkazy:
    {
        "vytvoření": [
            "mkdir -p ~/ros2_ws/src",
            "cd ~/ros2_ws",
            "colcon build",
            "source install/setup.bash"
        ],
        "nový_package_python": "ros2 pkg create --build-type ament_python my_pkg --dependencies rclpy",
        "nový_package_cpp": "ros2 pkg create --build-type ament_cmake my_pkg --dependencies rclcpp",
        "build": "colcon build --packages-select my_pkg",
        "source": "source install/setup.bash"
    }
    """
    # TODO: ↓
    pass


def ros2_cli():
    """
    🎯 VÝZVA 3: ROS2 CLI příkazy.
    Vrať dict:
    {
        "node_list": "ros2 node list",
        "topic_list": "ros2 topic list",
        "topic_echo": "ros2 topic echo /topic_name",
        "topic_info": "ros2 topic info /topic_name",
        "topic_pub": "ros2 topic pub /topic_name std_msgs/String '{data: hello}'",
        "service_list": "ros2 service list",
        "service_call": "ros2 service call /srv_name std_srvs/SetBool '{data: true}'",
        "param_list": "ros2 param list",
        "run": "ros2 run package_name node_name",
        "launch": "ros2 launch package_name launch_file.py"
    }
    """
    # TODO: ↓
    pass


def package_struktura():
    """
    🎯 VÝZVA 4: Struktura Python ROS2 balíčku.
    Vrať dict:
    {
        "adresáře": {
            "my_pkg/": "zdrojový kód (Python moduly)",
            "my_pkg/__init__.py": "init",
            "resource/my_pkg": "marker soubor",
            "test/": "testy"
        },
        "soubory": {
            "package.xml": "metadata, závislosti (XML)",
            "setup.py": "Python instalace + entry_points",
            "setup.cfg": "konfigurace pro ros2 run"
        },
        "entry_point": "console_scripts: ['node_name = my_pkg.module:main']"
    }
    """
    # TODO: ↓
    pass


def sourcing_a_env():
    """
    🎯 VÝZVA 5: Environment a sourcing.
    Vrať dict:
    {
        "underlay": "source /opt/ros/humble/setup.bash  # ROS2 instalace",
        "overlay": "source ~/ros2_ws/install/setup.bash  # tvůj workspace",
        "pořadí": "vždy nejdřív underlay, pak overlay",
        "bashrc": "přidej do ~/.bashrc pro automatické načtení",
        "domain_id": "export ROS_DOMAIN_ID=42  # izolace komunikace",
        "localhost": "export ROS_LOCALHOST_ONLY=1  # jen lokální"
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Co je ROS2?",
        theory="""ROS2 (Robot Operating System 2):
  - Middleware pro robotiku
  - Založeno na DDS (Data Distribution Service)
  - Podporuje real-time, multi-robot, embedded
  - Python (rclpy) a C++ (rclcpp)

  ≠ Operační systém!
  = Framework pro komunikaci mezi částmi robota""",
        task="Popiš ROS2 a porovnej s ROS1.",
        difficulty=1, points=15,
        hints=["DDS, real-time, rclpy, managed nodes"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "vs_ros1" in r and len(r.get("vlastnosti", [])) >= 3,
                    "ROS2 overview ✓"
                )
            )(ros2_prehled()),
        ]
    ),
    Challenge(
        title="Workspace Setup",
        task="Popiš vytvoření ROS2 workspace a balíčku.",
        difficulty=1, points=15,
        hints=["mkdir, colcon build, source, ros2 pkg create"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r.get("vytvoření", [])) >= 4 and "colcon" in r.get("build", ""),
                    "Workspace ✓"
                )
            )(workspace_setup()),
        ]
    ),
    Challenge(
        title="ROS2 CLI",
        task="Vyjmenuj nejdůležitější ros2 příkazy.",
        difficulty=1, points=15,
        hints=["ros2 node/topic/service list, echo, pub, call, run, launch"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "topic_echo" in r and "run" in r and "launch" in r,
                    "CLI příkazy ✓"
                )
            )(ros2_cli()),
        ]
    ),
    Challenge(
        title="Struktura balíčku",
        task="Popiš strukturu Python ROS2 balíčku.",
        difficulty=2, points=20,
        hints=["package.xml, setup.py, setup.cfg, entry_points"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "soubory" in r and "package.xml" in r["soubory"],
                    "Package struktura ✓"
                )
            )(package_struktura()),
        ]
    ),
    Challenge(
        title="Environment",
        task="Popiš sourcing a environment variables.",
        difficulty=1, points=10,
        hints=["underlay, overlay, DOMAIN_ID, LOCALHOST_ONLY"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "underlay" in r and "overlay" in r and "domain_id" in r,
                    "Environment ✓"
                )
            )(sourcing_a_env()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "ROS2 Instalace & Setup", "10_01")
