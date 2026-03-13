#!/usr/bin/env python3
"""📦 ROS2 Custom Messages — Vlastní .msg, .srv, .action soubory a package konfigurace."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def msg_zaklady():
    """
    🎯 VÝZVA 1: Definice vlastních .msg souborů.
    Vrať dict:
    {
        "co_je_msg": "definice struktury zprávy pro topic komunikaci",
        "umístění": "my_interfaces/msg/RobotStatus.msg",
        "primitivní_typy": ["bool", "int8", "int32", "int64", "float32", "float64", "string"],
        "příklad_msg": '''# RobotStatus.msg
std_msgs/Header header
string robot_name
float64 battery_level
float64[3] position       # pole pevné délky
float64[] velocities      # pole proměnné délky
bool is_active
int32 error_code''',
        "pole": {
            "pevné": "float64[3] position  # vždy 3 prvky",
            "dynamické": "float64[] data  # libovolný počet",
            "konstanty": "int32 STATUS_OK=0\nint32 STATUS_ERROR=1"
        },
        "vnořené": "geometry_msgs/Point position  # použití jiné msg"
    }
    """
    # TODO: ↓
    pass


def srv_definice():
    """
    🎯 VÝZVA 2: Definice vlastních .srv souborů.
    Vrať dict:
    {
        "co_je_srv": "definice request/response formátu pro service",
        "umístění": "my_interfaces/srv/GetRobotInfo.srv",
        "struktura": "request část\\n---\\nresponse část",
        "příklad_srv": '''# GetRobotInfo.srv
string robot_name
---
float64 battery
float64[3] position
string status
bool success
string message''',
        "příklad_set": '''# SetSpeed.srv
string robot_name
float64 linear_speed
float64 angular_speed
---
bool success
string message''',
        "použití_v_kódu": '''from my_interfaces.srv import GetRobotInfo

# Server
self.srv = self.create_service(GetRobotInfo, 'get_info', self.cb)

# Client
self.cli = self.create_client(GetRobotInfo, 'get_info')'''
    }
    """
    # TODO: ↓
    pass


def action_definice():
    """
    🎯 VÝZVA 3: Definice vlastních .action souborů.
    Vrať dict:
    {
        "co_je_action": "definice goal/result/feedback pro dlouhé úkoly",
        "umístění": "my_interfaces/action/Navigate.action",
        "struktura": "goal\\n---\\nresult\\n---\\nfeedback",
        "příklad_action": '''# Navigate.action
# Goal
geometry_msgs/PoseStamped target_pose
float64 max_speed
---
# Result
bool success
float64 total_distance
float64 total_time
---
# Feedback
geometry_msgs/PoseStamped current_pose
float64 distance_remaining
float64 estimated_time''',
        "pomocné_typy": "geometry_msgs/PoseStamped, std_msgs/Header — vnořené zprávy",
        "použití_v_kódu": '''from my_interfaces.action import Navigate
from rclpy.action import ActionServer, ActionClient'''
    }
    """
    # TODO: ↓
    pass


def cmake_a_package():
    """
    🎯 VÝZVA 4: CMakeLists.txt a package.xml pro custom messages.
    Vrať dict:
    {
        "package_typ": "ament_cmake — custom messages vyžadují CMake i pro Python balíčky",
        "package_xml": '''<?xml version="1.0"?>
<package format="3">
  <name>my_interfaces</name>
  <version>0.0.1</version>
  <description>Custom message definitions</description>
  <maintainer email="dev@robot.cz">Developer</maintainer>
  <license>MIT</license>

  <buildtool_depend>ament_cmake</buildtool_depend>
  <buildtool_depend>rosidl_default_generators</buildtool_depend>

  <depend>geometry_msgs</depend>
  <depend>std_msgs</depend>

  <exec_depend>rosidl_default_runtime</exec_depend>
  <member_of_group>rosidl_interface_packages</member_of_group>
</package>''',
        "cmakelists": '''cmake_minimum_required(VERSION 3.8)
project(my_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/RobotStatus.msg"
  "srv/GetRobotInfo.srv"
  "action/Navigate.action"
  DEPENDENCIES geometry_msgs std_msgs
)

ament_package()''',
        "build": "colcon build --packages-select my_interfaces",
        "klíčové_závislosti": ["rosidl_default_generators", "rosidl_default_runtime", "rosidl_interface_packages"]
    }
    """
    # TODO: ↓
    pass


def pouziti_custom_msg():
    """
    🎯 VÝZVA 5: Použití custom messages v jiném balíčku.
    Vrať dict:
    {
        "závislost_package_xml": "<depend>my_interfaces</depend>",
        "závislost_setup_py": "install_requires=['my_interfaces']  # není vždy nutné",
        "import_msg": "from my_interfaces.msg import RobotStatus",
        "import_srv": "from my_interfaces.srv import GetRobotInfo",
        "import_action": "from my_interfaces.action import Navigate",
        "publisher_příklad": '''from my_interfaces.msg import RobotStatus

msg = RobotStatus()
msg.robot_name = 'kubo'
msg.battery_level = 87.5
msg.position = [1.0, 2.0, 0.0]
msg.is_active = True
msg.error_code = 0
self.pub.publish(msg)''',
        "inspekce": {
            "zobrazit_msg": "ros2 interface show my_interfaces/msg/RobotStatus",
            "seznam": "ros2 interface list | grep my_interfaces",
            "balíčky": "ros2 interface packages"
        }
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Vlastní .msg soubory",
        theory="""Message soubor definuje strukturu dat:
  # RobotStatus.msg
  string robot_name
  float64 battery_level
  bool is_active

  Typy: bool, int32, float64, string, pole[]
  Vnořené: geometry_msgs/Point position
  Konstanty: int32 MAX_SPEED=10

  Umístění: my_interfaces/msg/RobotStatus.msg""",
        task="Navrhni .msg soubor pro stav robota.",
        difficulty=1, points=15,
        hints=[
            "Primitivní typy + pole + vnořené zprávy",
            "float64[3] pro pevné pole, float64[] pro dynamické"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "příklad_msg" in r
                    and "primitivní_typy" in r
                    and len(r["primitivní_typy"]) >= 5,
                    "MSG soubory ✓"
                )
            )(msg_zaklady()),
        ]
    ),
    Challenge(
        title="Vlastní .srv soubory",
        theory=""".srv soubor = request + response oddělené ---:
  # GetRobotInfo.srv
  string robot_name     # request
  ---
  float64 battery       # response
  bool success

  Server přijme request, odpoví response.
  create_service(GetRobotInfo, 'name', callback)""",
        task="Navrhni .srv soubor pro dotaz na stav robota.",
        difficulty=1, points=15,
        hints=[
            "Oddělení request/response pomocí ---",
            "Response typicky obsahuje bool success + string message"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "příklad_srv" in r and "---" in r["příklad_srv"],
                    "SRV soubory ✓"
                )
            )(srv_definice()),
        ]
    ),
    Challenge(
        title="Vlastní .action soubory",
        theory=""".action soubor = goal + result + feedback:
  # Navigate.action
  PoseStamped target     # Goal
  ---
  bool success            # Result
  ---
  PoseStamped current     # Feedback

  Feedback se posílá průběžně během vykonávání.""",
        task="Navrhni .action soubor pro navigaci.",
        difficulty=2, points=20,
        hints=[
            "Tři části oddělené --- (goal, result, feedback)",
            "Feedback = průběžná informace (pozice, vzdálenost)"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "příklad_action" in r
                    and r["příklad_action"].count("---") >= 2,
                    "ACTION soubory ✓"
                )
            )(action_definice()),
        ]
    ),
    Challenge(
        title="CMakeLists a package.xml",
        theory="""Custom messages vyžadují CMake build:
  package.xml:
    rosidl_default_generators (buildtool)
    rosidl_default_runtime (exec)
    member_of_group: rosidl_interface_packages

  CMakeLists.txt:
    rosidl_generate_interfaces(${PROJECT_NAME}
      "msg/RobotStatus.msg"
      DEPENDENCIES std_msgs
    )

  DŮLEŽITÉ: interface balíček = jen definice zpráv!""",
        task="Nakonfiguruj CMakeLists.txt a package.xml.",
        difficulty=2, points=20,
        hints=[
            "rosidl_default_generators + rosidl_default_runtime",
            "rosidl_generate_interfaces() v CMakeLists.txt"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "cmakelists" in r
                    and "package_xml" in r
                    and "rosidl" in r["cmakelists"],
                    "CMake konfigurace ✓"
                )
            )(cmake_a_package()),
        ]
    ),
    Challenge(
        title="Použití custom messages",
        theory="""V jiném balíčku:
  1. package.xml: <depend>my_interfaces</depend>
  2. Import: from my_interfaces.msg import RobotStatus
  3. Vytvoření: msg = RobotStatus()
  4. Vyplnění: msg.robot_name = 'kubo'
  5. Publish: self.pub.publish(msg)

  Inspekce: ros2 interface show my_interfaces/msg/RobotStatus""",
        task="Ukaž jak importovat a použít custom messages.",
        difficulty=2, points=20,
        hints=[
            "from my_interfaces.msg import RobotStatus",
            "ros2 interface show/list pro inspekci"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "import_msg" in r
                    and "publisher_příklad" in r
                    and "inspekce" in r,
                    "Použití custom msg ✓"
                )
            )(pouziti_custom_msg()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "ROS2 Custom Messages", "10_05")
