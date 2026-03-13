#!/usr/bin/env python3
"""🗺️ ROS2 Navigation — Nav2, costmaps, plannery, AMCL a autonomní navigace."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def nav2_prehled():
    """
    🎯 VÝZVA 1: Přehled Nav2 stacku.
    Vrať dict:
    {
        "co_je_nav2": "ROS2 navigační stack — autonomní navigace mobilních robotů",
        "komponenty": {
            "planner_server": "globální plánování cesty (A*, NavFn, Theta*)",
            "controller_server": "lokální sledování cesty (DWB, TEB, regulace)",
            "recovery_server": "zotavení z uvíznutí (spin, backup, wait)",
            "bt_navigator": "Behavior Tree orchestrátor — řídí celý navigační cyklus",
            "costmap": "mapa nákladů pro plánování (překážky, inflace)",
            "amcl": "lokalizace na mapě (Adaptive Monte Carlo Localization)"
        },
        "vstupy": {
            "mapa": "/map — OccupancyGrid (ze SLAM nebo uložená)",
            "odom": "/odom — odometrie robota",
            "scan": "/scan — LaserScan pro lokalizaci a costmapy",
            "tf": "map → odom → base_link transformace"
        },
        "výstupy": {
            "cmd_vel": "/cmd_vel — Twist příkazy pro řízení",
            "plan": "/plan — Path plánovaná cesta"
        },
        "spuštění": "ros2 launch nav2_bringup navigation_launch.py"
    }
    """
    # TODO: ↓
    pass


def costmapy():
    """
    🎯 VÝZVA 2: Costmaps — mapy nákladů.
    Vrať dict:
    {
        "co_je_costmap": "2D mřížka kde každá buňka má 'cenu' průchodu",
        "typy": {
            "global_costmap": "celá známá mapa — pro globální plánování",
            "local_costmap": "okno kolem robota — pro lokální řízení"
        },
        "vrstvy": {
            "static_layer": "statická mapa (ze SLAM)",
            "obstacle_layer": "dynamické překážky (ze senzorů)",
            "inflation_layer": "nafouklé překážky — bezpečná vzdálenost",
            "voxel_layer": "3D překážky (z depth kamery/pointcloud)"
        },
        "hodnoty": {
            "0": "volné místo (FREE_SPACE)",
            "253": "zapsaná překážka (INSCRIBED_INFLATED)",
            "254": "smrtelná překážka (LETHAL_OBSTACLE)",
            "255": "neznámé (NO_INFORMATION)"
        },
        "konfigurace": '''global_costmap:
  ros__parameters:
    update_frequency: 1.0
    publish_frequency: 1.0
    global_frame: map
    robot_base_frame: base_link
    resolution: 0.05
    plugins: ["static_layer", "obstacle_layer", "inflation_layer"]
    inflation_layer:
      inflation_radius: 0.55
      cost_scaling_factor: 2.58''',
        "inflation_radius": "vzdálenost, do které se 'nafukuje' překážka — větší = bezpečnější"
    }
    """
    # TODO: ↓
    pass


def plannery():
    """
    🎯 VÝZVA 3: Plánování cesty — globální a lokální.
    Vrať dict:
    {
        "globální_planner": {
            "účel": "najde cestu od startu k cíli na celé mapě",
            "algoritmy": {
                "NavFn": "Dijkstra/A* na mřížce — výchozí, spolehlivý",
                "Theta*": "any-angle plánování — hladší cesty",
                "Smac2D": "2D A* s více optimalizacemi",
                "SmacHybrid": "Hybrid A* pro Ackermann kinematiku",
                "SmacLattice": "state lattice planner"
            },
            "vstup": "globální costmapa + start + cíl",
            "výstup": "Path — sekvence PoseStamped bodů"
        },
        "lokální_controller": {
            "účel": "sleduje globální cestu a vyhýbá se překážkám",
            "algoritmy": {
                "DWB": "Dynamic Window approach — vzorkuje rychlosti",
                "TEB": "Timed Elastic Band — optimalizuje trajektorii",
                "RPP": "Regulated Pure Pursuit — jednoduchý, spolehlivý",
                "MPPI": "Model Predictive Path Integral — pokročilý"
            },
            "vstup": "lokální costmapa + globální cesta + odom",
            "výstup": "Twist — lineární a úhlová rychlost"
        },
        "konfigurace": '''planner_server:
  ros__parameters:
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner/NavfnPlanner"
      tolerance: 0.5
      use_astar: true'''
    }
    """
    # TODO: ↓
    pass


def amcl_lokalizace():
    """
    🎯 VÝZVA 4: AMCL — lokalizace na mapě.
    Vrať dict:
    {
        "co_je_amcl": "Adaptive Monte Carlo Localization — částicový filtr",
        "princip": {
            "particles": "množina hypotéz (částic) o pozici robota",
            "prediction": "posun částic podle odometrie",
            "update": "přehodnocení vah podle shody senzorů s mapou",
            "resampling": "výběr nejlepších částic, zahoď špatné"
        },
        "vstupy": ["mapa (/map)", "LaserScan (/scan)", "odometrie (/odom)", "TF (odom → base_link)"],
        "výstupy": ["TF (map → odom)", "pose (/amcl_pose)", "particle cloud (/particle_cloud)"],
        "konfigurace": '''amcl:
  ros__parameters:
    min_particles: 500
    max_particles: 2000
    alpha1: 0.2            # rotační šum z rotace
    alpha2: 0.2            # rotační šum z translace
    alpha3: 0.2            # translační šum z translace
    alpha4: 0.2            # translační šum z rotace
    laser_model_type: "likelihood_field"
    max_beams: 60
    z_hit: 0.5
    z_rand: 0.5
    update_min_d: 0.2      # min translace pro update
    update_min_a: 0.5      # min rotace pro update''',
        "initial_pose": "ros2 topic pub /initialpose geometry_msgs/PoseWithCovarianceStamped ...",
        "alternativy": ["slam_toolbox (SLAM + lokalizace)", "robot_localization (EKF/UKF fúze)"]
    }
    """
    # TODO: ↓
    pass


def navigace_api():
    """
    🎯 VÝZVA 5: Programatická navigace — Nav2 API v Pythonu.
    Vrať dict:
    {
        "navigator_class": '''from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped

navigator = BasicNavigator()''',
        "navigate_to_pose": '''goal = PoseStamped()
goal.header.frame_id = 'map'
goal.header.stamp = navigator.get_clock().now().to_msg()
goal.pose.position.x = 2.0
goal.pose.position.y = 1.0
goal.pose.orientation.w = 1.0

navigator.goToPose(goal)

while not navigator.isTaskComplete():
    feedback = navigator.getFeedback()
    if feedback:
        distance = feedback.distance_remaining
        print(f'Zbývá: {distance:.2f}m')

result = navigator.getResult()''',
        "waypoints": '''goals = []
for x, y in [(1, 0), (2, 1), (0, 2)]:
    goal = PoseStamped()
    goal.header.frame_id = 'map'
    goal.pose.position.x = float(x)
    goal.pose.position.y = float(y)
    goal.pose.orientation.w = 1.0
    goals.append(goal)

navigator.followWaypoints(goals)''',
        "lifecycle": {
            "waitUntilNav2Active": "čeká na inicializaci Nav2",
            "goToPose": "navigace k jednomu cíli",
            "followWaypoints": "navigace přes sérii bodů",
            "cancelTask": "zrušení aktuálního úkolu",
            "getResult": "výsledek navigace (SUCCEEDED, FAILED, CANCELED)"
        },
        "initial_pose": '''initial = PoseStamped()
initial.header.frame_id = 'map'
initial.pose.position.x = 0.0
initial.pose.position.y = 0.0
initial.pose.orientation.w = 1.0
navigator.setInitialPose(initial)'''
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Nav2 Stack — přehled",
        theory="""Nav2 = navigační stack pro ROS2:
  Planner → Controller → Recovery → BT Navigator

  Planner: najde cestu na mapě (A*, NavFn)
  Controller: sleduje cestu, vyhýbá se (DWB, TEB)
  Recovery: co dělat při uvíznutí (spin, backup)
  BT Navigator: behavior tree řídí celý proces

  Vstupy: mapa, odom, scan, TF
  Výstup: /cmd_vel (Twist)""",
        task="Popiš komponenty Nav2 a jejich vstupy/výstupy.",
        difficulty=1, points=15,
        hints=[
            "planner_server, controller_server, recovery_server, bt_navigator",
            "Vstupy: /map, /odom, /scan, TF; Výstup: /cmd_vel"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "komponenty" in r
                    and "planner_server" in r["komponenty"]
                    and "vstupy" in r
                    and "výstupy" in r,
                    "Nav2 přehled ✓"
                )
            )(nav2_prehled()),
        ]
    ),
    Challenge(
        title="Costmaps — mapy nákladů",
        theory="""Costmap = mřížka s cenou průchodu:
  0: volné, 254: překážka, 255: neznámé

  Dvě costmapy:
  - Global: celá mapa, pro globální plánování
  - Local: okno kolem robota, pro lokální řízení

  Vrstvy (plugins):
  - static_layer: statická mapa
  - obstacle_layer: dynamické překážky
  - inflation_layer: bezpečnostní zóna""",
        task="Popiš costmapy, vrstvy a konfiguraci.",
        difficulty=2, points=20,
        hints=[
            "Global vs Local costmapa, vrstvy jako plugins",
            "inflation_radius = bezpečná vzdálenost od překážek"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "typy" in r
                    and "vrstvy" in r
                    and "inflation_layer" in r["vrstvy"]
                    and "konfigurace" in r,
                    "Costmaps ✓"
                )
            )(costmapy()),
        ]
    ),
    Challenge(
        title="Plánování cesty",
        theory="""Globální planner: cesta na celé mapě
  NavFn (Dijkstra/A*), Theta*, SmacHybrid

  Lokální controller: sledování + vyhýbání
  DWB, TEB, Regulated Pure Pursuit, MPPI

  Vstup: costmapa + start + cíl
  Výstup: Path (global), Twist (local)""",
        task="Popiš globální a lokální plánování.",
        difficulty=2, points=20,
        hints=[
            "Globální: NavFn, Theta*; Lokální: DWB, TEB, RPP",
            "Globální → Path, Lokální → Twist"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "globální_planner" in r
                    and "lokální_controller" in r
                    and "algoritmy" in r["globální_planner"],
                    "Plannery ✓"
                )
            )(plannery()),
        ]
    ),
    Challenge(
        title="AMCL lokalizace",
        theory="""AMCL = částicový filtr pro lokalizaci:
  1. Rozhoď částice (hypotézy o pozici)
  2. Posuň podle odometrie (prediction)
  3. Zvaž podle shody LaserScan vs mapa (update)
  4. Znovu vyber nejlepší (resampling)

  Výstup: TF map → odom
  → robot ví, kde je na mapě""",
        task="Popiš AMCL a jeho konfiguraci.",
        difficulty=3, points=25,
        hints=[
            "Částicový filtr: prediction → update → resampling",
            "Vstupy: mapa, scan, odom; Výstup: TF map→odom"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "princip" in r
                    and "particles" in r["princip"]
                    and "konfigurace" in r,
                    "AMCL ✓"
                )
            )(amcl_lokalizace()),
        ]
    ),
    Challenge(
        title="Nav2 API v Pythonu",
        theory="""BasicNavigator = Python API pro Nav2:
  from nav2_simple_commander.robot_navigator import BasicNavigator

  nav = BasicNavigator()
  nav.waitUntilNav2Active()

  goal = PoseStamped()
  goal.pose.position.x = 2.0
  nav.goToPose(goal)

  while not nav.isTaskComplete():
      feedback = nav.getFeedback()
      print(f'Zbývá: {feedback.distance_remaining}m')""",
        task="Implementuj navigaci k cíli a přes waypoints.",
        difficulty=3, points=25,
        hints=[
            "BasicNavigator: goToPose(), followWaypoints()",
            "getFeedback() pro sledování průběhu"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "navigate_to_pose" in r
                    and "waypoints" in r
                    and "lifecycle" in r
                    and "goToPose" in r["lifecycle"],
                    "Nav2 API ✓"
                )
            )(navigace_api()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "ROS2 Navigation", "10_08")
