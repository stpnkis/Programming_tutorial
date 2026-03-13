#!/usr/bin/env python3
"""🤖 URDF & Robot Model — Links, joints, Xacro makra a vizualizace v RViz."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def urdf_zaklady():
    """
    🎯 VÝZVA 1: Základy URDF — co je a k čemu slouží.
    Vrať dict:
    {
        "co_je_urdf": "Unified Robot Description Format — XML popis robota",
        "účel": ["vizualizace v RViz", "simulace v Gazebo", "plánování pohybu", "TF strom"],
        "základní_elementy": {
            "link": "fyzická část robota (tělo, kolo, rameno)",
            "joint": "spojení mezi dvěma linky (rotace, posuv)"
        },
        "minimální_urdf": '''<?xml version="1.0"?>
<robot name="my_robot">
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.3 0.1"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
    </visual>
  </link>
</robot>''',
        "soubor_umístění": "my_robot/urdf/robot.urdf",
        "zobrazení": "ros2 launch my_robot display.launch.py"
    }
    """
    # TODO: ↓
    pass


def links_a_geometrie():
    """
    🎯 VÝZVA 2: Links — vizuál, kolize, setrvačnost.
    Vrať dict:
    {
        "visual": {
            "popis": "jak link vypadá (pro vizualizaci)",
            "geometrie": ["box", "cylinder", "sphere", "mesh"],
            "příklad": '''<visual>
  <origin xyz="0 0 0.05" rpy="0 0 0"/>
  <geometry>
    <cylinder radius="0.1" length="0.1"/>
  </geometry>
  <material name="red">
    <color rgba="0.8 0 0 1"/>
  </material>
</visual>'''
        },
        "collision": {
            "popis": "tvar pro detekci kolizí (často zjednodušený)",
            "příklad": '''<collision>
  <geometry>
    <cylinder radius="0.1" length="0.1"/>
  </geometry>
</collision>'''
        },
        "inertial": {
            "popis": "hmotnost a setrvačnost pro fyzikální simulaci",
            "příklad": '''<inertial>
  <mass value="1.0"/>
  <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/>
</inertial>'''
        },
        "mesh": '''<geometry>
  <mesh filename="package://my_robot/meshes/body.stl" scale="0.001 0.001 0.001"/>
</geometry>''',
        "origin": "origin xyz='x y z' rpy='roll pitch yaw' — posunutí a rotace geometrie"
    }
    """
    # TODO: ↓
    pass


def joints():
    """
    🎯 VÝZVA 3: Joints — typy spojení mezi linky.
    Vrať dict:
    {
        "typy": {
            "fixed": "pevné spojení, žádný pohyb (senzor na těle)",
            "revolute": "rotace kolem osy s limity (kloub ramena)",
            "continuous": "rotace bez limitů (kolo)",
            "prismatic": "lineární posuv s limity (výtah)",
            "floating": "6 DOF — volný pohyb (nepoužívá se moc)",
            "planar": "pohyb v rovině (2 DOF)"
        },
        "příklad_revolute": '''<joint name="arm_joint" type="revolute">
  <parent link="base_link"/>
  <child link="arm_link"/>
  <origin xyz="0.1 0 0.15" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-1.57" upper="1.57" effort="10" velocity="1.0"/>
</joint>''',
        "příklad_continuous": '''<joint name="left_wheel_joint" type="continuous">
  <parent link="base_link"/>
  <child link="left_wheel"/>
  <origin xyz="0 0.15 0" rpy="-1.5708 0 0"/>
  <axis xyz="0 0 1"/>
</joint>''',
        "příklad_fixed": '''<joint name="laser_joint" type="fixed">
  <parent link="base_link"/>
  <child link="laser_frame"/>
  <origin xyz="0.2 0 0.1" rpy="0 0 0"/>
</joint>''',
        "elementy": {
            "parent": "rodičovský link",
            "child": "potomkový link",
            "origin": "pozice a orientace jointu",
            "axis": "osa rotace/posuvu",
            "limit": "limity pohybu (lower, upper, effort, velocity)"
        }
    }
    """
    # TODO: ↓
    pass


def xacro():
    """
    🎯 VÝZVA 4: Xacro — makra a parametrizace URDF.
    Vrať dict:
    {
        "co_je": "XML makro jazyk pro URDF — parametrizace, modularita, DRY",
        "výhody": ["proměnné", "makra (funkce)", "include", "podmínky", "matematika"],
        "proměnné": '''<xacro:property name="wheel_radius" value="0.05"/>
<xacro:property name="wheel_width" value="0.02"/>
<xacro:property name="base_length" value="0.3"/>''',
        "makro": '''<xacro:macro name="wheel" params="prefix reflect">
  <link name="${prefix}_wheel">
    <visual>
      <geometry>
        <cylinder radius="${wheel_radius}" length="${wheel_width}"/>
      </geometry>
    </visual>
  </link>
  <joint name="${prefix}_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="${prefix}_wheel"/>
    <origin xyz="0 ${reflect * 0.15} 0" rpy="-1.5708 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>
</xacro:macro>

<xacro:wheel prefix="left" reflect="1"/>
<xacro:wheel prefix="right" reflect="-1"/>''',
        "include": '''<xacro:include filename="$(find my_robot)/urdf/wheels.xacro"/>''',
        "matematika": "${base_length / 2 + wheel_radius}",
        "podmínky": '''<xacro:if value="${use_camera}">
  <xacro:include filename="camera.xacro"/>
</xacro:if>''',
        "kompilace": "xacro robot.urdf.xacro > robot.urdf",
        "launch_integrace": '''import xacro
robot_description = xacro.process_file(urdf_path).toxml()'''
    }
    """
    # TODO: ↓
    pass


def rviz_vizualizace():
    """
    🎯 VÝZVA 5: Vizualizace robota v RViz.
    Vrať dict:
    {
        "robot_state_publisher": {
            "co_dělá": "čte URDF a publikuje TF transformace + /robot_description",
            "launch": '''Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    parameters=[{'robot_description': robot_description}]
)'''
        },
        "joint_state_publisher": {
            "co_dělá": "publikuje stavy kloubů na /joint_states",
            "gui_verze": "joint_state_publisher_gui — sliders pro manuální ovládání",
            "launch": '''Node(
    package='joint_state_publisher_gui',
    executable='joint_state_publisher_gui'
)'''
        },
        "rviz": {
            "co_dělá": "3D vizualizace — zobrazí model, TF, senzory",
            "launch": '''Node(
    package='rviz2',
    executable='rviz2',
    arguments=['-d', os.path.join(pkg_share, 'rviz', 'config.rviz')]
)''',
            "displays": ["RobotModel", "TF", "LaserScan", "PointCloud2", "Image", "Path", "Map"]
        },
        "kompletní_launch": '''def generate_launch_description():
    pkg = get_package_share_directory('my_robot')
    urdf = os.path.join(pkg, 'urdf', 'robot.urdf.xacro')
    robot_desc = xacro.process_file(urdf).toxml()

    return LaunchDescription([
        Node(package='robot_state_publisher',
             executable='robot_state_publisher',
             parameters=[{'robot_description': robot_desc}]),
        Node(package='joint_state_publisher_gui',
             executable='joint_state_publisher_gui'),
        Node(package='rviz2', executable='rviz2',
             arguments=['-d', os.path.join(pkg, 'rviz', 'display.rviz')]),
    ])''',
        "závislosti": ["robot_state_publisher", "joint_state_publisher_gui", "rviz2", "xacro"]
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="URDF — základy",
        theory="""URDF = Unified Robot Description Format:
  XML soubor popisující robota:
  - Links: fyzické části (tělo, kola, ramena)
  - Joints: spojení mezi links (rotace, posuv)

  <robot name="my_robot">
    <link name="base_link">
      <visual><geometry><box size="0.5 0.3 0.1"/></geometry></visual>
    </link>
  </robot>

  Účel: vizualizace, simulace, plánování, TF""",
        task="Popiš URDF formát a vytvoř minimální model.",
        difficulty=1, points=15,
        hints=[
            "Robot = links + joints v XML formátu",
            "<robot>, <link>, <joint> — hlavní elementy"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "minimální_urdf" in r
                    and "základní_elementy" in r
                    and len(r.get("účel", [])) >= 3,
                    "URDF základy ✓"
                )
            )(urdf_zaklady()),
        ]
    ),
    Challenge(
        title="Links — vizuál, kolize, setrvačnost",
        theory="""Link má tři části:
  <visual>: jak vypadá (pro zobrazení)
  <collision>: tvar pro kolize (zjednodušený)
  <inertial>: hmotnost + setrvačnost (simulace)

  Geometrie: box, cylinder, sphere, mesh
  Origin: posunutí/rotace geometrie

  Pro Gazebo MUSÍ mít collision i inertial!""",
        task="Popiš visual, collision a inertial elementy.",
        difficulty=2, points=20,
        hints=[
            "visual (box/cylinder/sphere/mesh), collision, inertial",
            "origin xyz='...' rpy='...' pro pozicování"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "visual" in r
                    and "collision" in r
                    and "inertial" in r
                    and "mesh" in r,
                    "Links ✓"
                )
            )(links_a_geometrie()),
        ]
    ),
    Challenge(
        title="Joints — typy spojení",
        theory="""Joint spojuje parent → child link:
  fixed:      pevný (senzor na těle)
  revolute:   rotace s limity (kloub)
  continuous:  rotace bez limitů (kolo)
  prismatic:  lineární posuv (výtah)

  <joint name="j1" type="revolute">
    <parent link="base"/>
    <child link="arm"/>
    <axis xyz="0 1 0"/>        ← osa rotace
    <limit lower="-1.57" upper="1.57"/>
  </joint>""",
        task="Popiš typy jointů a jejich elementy.",
        difficulty=2, points=20,
        hints=[
            "fixed, revolute, continuous, prismatic — hlavní typy",
            "parent, child, origin, axis, limit — elementy jointu"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "typy" in r
                    and len(r["typy"]) >= 4
                    and "elementy" in r,
                    "Joints ✓"
                )
            )(joints()),
        ]
    ),
    Challenge(
        title="Xacro — makra pro URDF",
        theory="""Xacro = XML macro pro URDF:
  Proměnné:  <xacro:property name="r" value="0.05"/>
  Makra:     <xacro:macro name="wheel" params="side"/>
  Include:   <xacro:include filename="wheels.xacro"/>
  Matika:    ${base_length / 2}
  Podmínky:  <xacro:if value="${use_cam}"/>

  DRY princip: definuj jednou, použij vícekrát""",
        task="Vytvoř Xacro makra pro parametrizovaný model.",
        difficulty=3, points=25,
        hints=[
            "xacro:property pro proměnné, xacro:macro pro makra",
            "${výraz} pro substituci, include pro modularitu"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "proměnné" in r
                    and "makro" in r
                    and "include" in r
                    and "matematika" in r,
                    "Xacro ✓"
                )
            )(xacro()),
        ]
    ),
    Challenge(
        title="Vizualizace v RViz",
        theory="""Pro zobrazení robota potřebuješ:
  1. robot_state_publisher — čte URDF, publikuje TF
  2. joint_state_publisher — publikuje stavy kloubů
  3. rviz2 — 3D vizualizace

  robot_state_publisher:
  - /robot_description (URDF string)
  - TF transformace pro všechny linky

  joint_state_publisher_gui:
  - /joint_states → sliders pro klouby""",
        task="Navrhni kompletní launch pro vizualizaci robota.",
        difficulty=2, points=20,
        hints=[
            "robot_state_publisher + joint_state_publisher + rviz2",
            "xacro.process_file(path).toxml() pro načtení Xacro"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "robot_state_publisher" in r
                    and "joint_state_publisher" in r
                    and "kompletní_launch" in r,
                    "RViz vizualizace ✓"
                )
            )(rviz_vizualizace()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "URDF & Robot Model", "10_07")
