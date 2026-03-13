#!/usr/bin/env python3
"""🚀 ROS2 Launch Files — Python launch, argumenty, skupiny nodů, podmínky."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def launch_zaklady():
    """
    🎯 VÝZVA 1: Základy launch souborů.
    Vrať dict:
    {
        "co_je_launch": "soubor pro spuštění více nodů najednou s konfigurací",
        "formáty": {
            "python": ".launch.py — nejflexibilnější, doporučený",
            "xml": ".launch.xml — jednodušší syntaxe",
            "yaml": ".launch.yaml — kompaktní"
        },
        "umístění": "my_pkg/launch/my_launch.launch.py",
        "spuštění": "ros2 launch my_pkg my_launch.launch.py",
        "minimální_příklad": '''from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='demo_nodes_cpp',
            executable='talker',
            name='my_talker',
            output='screen'
        ),
        Node(
            package='demo_nodes_cpp',
            executable='listener',
            name='my_listener',
            output='screen'
        ),
    ])''',
        "setup_py": "('share/' + package_name + '/launch', glob('launch/*.launch.py'))"
    }
    """
    # TODO: ↓
    pass


def launch_argumenty():
    """
    🎯 VÝZVA 2: Launch argumenty a parametry.
    Vrať dict:
    {
        "deklarace": '''from launch.actions import DeclareLaunchArgument
DeclareLaunchArgument('use_sim', default_value='true', description='Použít simulaci')''',
        "použití": '''from launch.substitutions import LaunchConfiguration
use_sim = LaunchConfiguration('use_sim')''',
        "cli_override": "ros2 launch my_pkg launch.py use_sim:=false",
        "parametry_nodu": '''Node(
    package='my_pkg',
    executable='my_node',
    parameters=[{
        'robot_name': 'kubo',
        'max_speed': 1.5,
        'use_sim': LaunchConfiguration('use_sim')
    }]
)''',
        "yaml_config": '''Node(
    package='my_pkg',
    executable='my_node',
    parameters=[os.path.join(pkg_share, 'config', 'params.yaml')]
)''',
        "remapping": '''Node(
    package='my_pkg',
    executable='my_node',
    remappings=[('/cmd_vel', '/robot1/cmd_vel')]
)'''
    }
    """
    # TODO: ↓
    pass


def launch_skupiny():
    """
    🎯 VÝZVA 3: Skupiny nodů a namespaces.
    Vrať dict:
    {
        "group": '''from launch_ros.actions import PushRosNamespace
from launch.actions import GroupAction

robot1_group = GroupAction([
    PushRosNamespace('robot1'),
    Node(package='my_pkg', executable='driver'),
    Node(package='my_pkg', executable='sensor'),
])''',
        "namespace_efekt": {
            "bez_ns": "/cmd_vel, /odom",
            "s_ns_robot1": "/robot1/cmd_vel, /robot1/odom"
        },
        "composable_nodes": '''from launch_ros.actions import ComposableNodeContainer, LoadComposableNode
ComposableNodeContainer(
    name='my_container',
    namespace='',
    package='rclcpp_components',
    executable='component_container',
    composable_node_descriptions=[
        ComposableNode(package='my_pkg', plugin='my_pkg::MyNode')
    ]
)''',
        "multi_robot": "Namespace pro každého robota → izolace topiců"
    }
    """
    # TODO: ↓
    pass


def launch_podminky():
    """
    🎯 VÝZVA 4: Podmínky a events v launch souborech.
    Vrať dict:
    {
        "if_condition": '''from launch.conditions import IfCondition
Node(
    package='my_pkg',
    executable='rviz2',
    condition=IfCondition(LaunchConfiguration('gui'))
)''',
        "unless_condition": '''from launch.conditions import UnlessCondition
Node(
    package='my_pkg',
    executable='headless_node',
    condition=UnlessCondition(LaunchConfiguration('gui'))
)''',
        "events": {
            "on_exit": "akce při ukončení nodu",
            "on_process_start": "akce při spuštění procesu",
            "on_shutdown": "akce při shutdown launch souboru"
        },
        "include_launch": '''from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
        os.path.join(pkg_share, 'launch', 'other.launch.py')
    ),
    launch_arguments={'use_sim': 'true'}.items()
)''',
        "timed_action": '''from launch.actions import TimerAction
TimerAction(period=5.0, actions=[
    Node(package='my_pkg', executable='delayed_node')
])'''
    }
    """
    # TODO: ↓
    pass


def launch_kompletni():
    """
    🎯 VÝZVA 5: Kompletní launch soubor pro robota.
    Vrať dict:
    {
        "popis": "Launch soubor pro simulaci robota s parametry",
        "soubor": '''import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, GroupAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, PushRosNamespace

def generate_launch_description():
    pkg_share = get_package_share_directory('my_robot')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim', default_value='true'),
        DeclareLaunchArgument('robot_name', default_value='kubo'),
        DeclareLaunchArgument('gui', default_value='true'),

        GroupAction([
            PushRosNamespace(LaunchConfiguration('robot_name')),
            Node(
                package='my_robot', executable='driver',
                parameters=[os.path.join(pkg_share, 'config', 'params.yaml')],
                output='screen'),
            Node(
                package='my_robot', executable='sensor_fusion',
                output='screen'),
        ]),

        Node(
            package='rviz2', executable='rviz2',
            condition=IfCondition(LaunchConfiguration('gui')),
            arguments=['-d', os.path.join(pkg_share, 'rviz', 'config.rviz')]),
    ])''',
        "spuštění": "ros2 launch my_robot robot.launch.py use_sim:=true gui:=false robot_name:=kubo"
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Launch soubory — základy",
        theory="""Launch soubor = spuštění více nodů najednou:
  ros2 launch my_pkg launch.py

  Python launch soubor:
  def generate_launch_description():
      return LaunchDescription([
          Node(package='pkg', executable='node'),
      ])

  Výhody: parametrizace, podmínky, skupiny, events""",
        task="Vytvoř minimální launch soubor se dvěma nody.",
        difficulty=1, points=15,
        hints=[
            "LaunchDescription([Node(...), Node(...)])",
            "generate_launch_description() musí vrátit LaunchDescription"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "minimální_příklad" in r
                    and "generate_launch_description" in r["minimální_příklad"],
                    "Launch základy ✓"
                )
            )(launch_zaklady()),
        ]
    ),
    Challenge(
        title="Launch argumenty a parametry",
        theory="""Argumenty pro konfiguraci z příkazové řádky:
  DeclareLaunchArgument('use_sim', default_value='true')
  LaunchConfiguration('use_sim')

  Parametry nodu:
  Node(..., parameters=[{'key': 'value'}])

  Z CLI:
  ros2 launch pkg launch.py use_sim:=false""",
        task="Přidej argumenty, parametry a remapping do launch.",
        difficulty=2, points=20,
        hints=[
            "DeclareLaunchArgument + LaunchConfiguration",
            "parameters=[dict] nebo parameters=[cesta_k_yaml]"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "deklarace" in r
                    and "parametry_nodu" in r
                    and "remapping" in r,
                    "Argumenty ✓"
                )
            )(launch_argumenty()),
        ]
    ),
    Challenge(
        title="Skupiny nodů a namespaces",
        theory="""GroupAction + PushRosNamespace:
  → všechny nody ve skupině dostanou prefix

  /cmd_vel → /robot1/cmd_vel

  Ideální pro multi-robot systémy:
  - Každý robot má svůj namespace
  - Nody i topicy jsou izolované""",
        task="Vytvoř skupinu nodů s namespace pro multi-robot.",
        difficulty=2, points=20,
        hints=[
            "GroupAction([PushRosNamespace('ns'), Node(...)])",
            "ComposableNodeContainer pro sdílení paměti"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "group" in r
                    and "namespace_efekt" in r
                    and "multi_robot" in r,
                    "Skupiny ✓"
                )
            )(launch_skupiny()),
        ]
    ),
    Challenge(
        title="Podmínky a events",
        theory="""Podmíněné spuštění nodů:
  IfCondition(LaunchConfiguration('gui'))
  UnlessCondition(LaunchConfiguration('gui'))

  Zahrnutí jiného launch souboru:
  IncludeLaunchDescription(
      PythonLaunchDescriptionSource(path),
      launch_arguments={...}.items()
  )""",
        task="Přidej podmínky, include a timed actions.",
        difficulty=3, points=25,
        hints=[
            "IfCondition/UnlessCondition pro podmíněné spuštění",
            "IncludeLaunchDescription pro zahrnutí jiného launch"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "if_condition" in r
                    and "include_launch" in r
                    and "events" in r,
                    "Podmínky ✓"
                )
            )(launch_podminky()),
        ]
    ),
    Challenge(
        title="Kompletní robot launch",
        theory="""Reálný launch soubor kombinuje vše:
  1. DeclareLaunchArgument — vstupní parametry
  2. GroupAction + Namespace — organizace
  3. IfCondition — volitelné nody (GUI, sim)
  4. IncludeLaunchDescription — modulární launch
  5. Parametry z YAML — konfigurace

  Konvence: launch/ adresář v balíčku""",
        task="Navrhni kompletní launch soubor pro robota.",
        difficulty=3, points=25,
        hints=[
            "Argumenty → Namespace → Nody → Podmíněné GUI",
            "get_package_share_directory pro cesty k souborům"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "soubor" in r
                    and "generate_launch_description" in r["soubor"]
                    and "spuštění" in r,
                    "Kompletní launch ✓"
                )
            )(launch_kompletni()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "ROS2 Launch Files", "10_04")
