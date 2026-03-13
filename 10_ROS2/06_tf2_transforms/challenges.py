#!/usr/bin/env python3
"""🔄 TF2 Transforms — Souřadnicové rámce, broadcaster, listener, statické transformy."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def tf2_zaklady():
    """
    🎯 VÝZVA 1: Základy TF2 — souřadnicové rámce.
    Vrať dict:
    {
        "co_je_tf2": "systém pro sledování souřadnicových rámců (frames) v čase",
        "frame": "souřadnicový rámec — pozice + orientace v prostoru",
        "strom": {
            "popis": "TF2 tvoří strom (ne graf) — každý frame má právě jednoho rodiče",
            "příklad": "world → odom → base_link → laser_frame",
            "běžné_frames": {
                "world/map": "globální reference",
                "odom": "odometrický referenční rámec",
                "base_link": "střed robota",
                "base_footprint": "průmět na zem",
                "laser_frame": "pozice lidaru",
                "camera_frame": "pozice kamery"
            }
        },
        "transform": {
            "translace": "[x, y, z] — posunutí v metrech",
            "rotace": "[x, y, z, w] — quaternion orientace"
        },
        "cli": {
            "strom": "ros2 run tf2_tools view_frames",
            "echo": "ros2 run tf2_ros tf2_echo base_link laser_frame",
            "monitor": "ros2 run tf2_ros tf2_monitor"
        }
    }
    """
    # TODO: ↓
    pass


def tf2_broadcaster():
    """
    🎯 VÝZVA 2: TF2 Broadcaster — publikování transformací.
    Vrať dict:
    {
        "import": '''from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import tf_transformations''',
        "vytvoření": "self.br = TransformBroadcaster(self)",
        "publikování": '''t = TransformStamped()
t.header.stamp = self.get_clock().now().to_msg()
t.header.frame_id = 'odom'          # rodičovský frame
t.child_frame_id = 'base_link'       # potomek

t.transform.translation.x = 1.0
t.transform.translation.y = 0.5
t.transform.translation.z = 0.0

q = tf_transformations.quaternion_from_euler(0, 0, 1.57)
t.transform.rotation.x = q[0]
t.transform.rotation.y = q[1]
t.transform.rotation.z = q[2]
t.transform.rotation.w = q[3]

self.br.sendTransform(t)''',
        "quaternion": {
            "co_je": "4D reprezentace rotace — bez gimbal locku",
            "euler_to_quat": "tf_transformations.quaternion_from_euler(roll, pitch, yaw)",
            "quat_to_euler": "tf_transformations.euler_from_quaternion([x, y, z, w])",
            "identity": "[0, 0, 0, 1] — žádná rotace"
        },
        "timer": "Broadcaster typicky běží v timeru — posílá aktuální pozici"
    }
    """
    # TODO: ↓
    pass


def tf2_listener():
    """
    🎯 VÝZVA 3: TF2 Listener — získání transformace.
    Vrať dict:
    {
        "import": '''from tf2_ros import Buffer, TransformListener
from rclpy.duration import Duration''',
        "setup": '''self.tf_buffer = Buffer()
self.tf_listener = TransformListener(self.tf_buffer, self)''',
        "lookup": '''try:
    trans = self.tf_buffer.lookup_transform(
        'base_link',      # cílový frame
        'laser_frame',    # zdrojový frame
        rclpy.time.Time() # nejnovější dostupný
    )
    x = trans.transform.translation.x
    y = trans.transform.translation.y
    yaw = tf_transformations.euler_from_quaternion([
        trans.transform.rotation.x,
        trans.transform.rotation.y,
        trans.transform.rotation.z,
        trans.transform.rotation.w
    ])[2]
except (LookupException, ExtrapolationException) as e:
    self.get_logger().warn(f'TF chyba: {e}')''',
        "timeout": '''self.tf_buffer.lookup_transform(
    'base_link', 'laser_frame',
    rclpy.time.Time(),
    timeout=Duration(seconds=1.0)
)''',
        "can_transform": "self.tf_buffer.can_transform('base_link', 'laser_frame', rclpy.time.Time())",
        "chyby": {
            "LookupException": "frame neexistuje ve stromu",
            "ConnectivityException": "frames nejsou propojené",
            "ExtrapolationException": "požadovaný čas mimo rozsah dat"
        }
    }
    """
    # TODO: ↓
    pass


def staticke_transformy():
    """
    🎯 VÝZVA 4: Statické transformace — neměnné vztahy.
    Vrať dict:
    {
        "co_je": "transformace, která se nemění v čase (pevné umístění senzoru)",
        "příklady": ["lidar na střeše robota", "kamera na rameni", "IMU v těle"],
        "broadcaster": '''from tf2_ros import StaticTransformBroadcaster

self.static_br = StaticTransformBroadcaster(self)

t = TransformStamped()
t.header.stamp = self.get_clock().now().to_msg()
t.header.frame_id = 'base_link'
t.child_frame_id = 'laser_frame'
t.transform.translation.x = 0.2
t.transform.translation.y = 0.0
t.transform.translation.z = 0.3
t.transform.rotation.w = 1.0  # žádná rotace
self.static_br.sendTransform(t)''',
        "cli": "ros2 run tf2_ros static_transform_publisher 0.2 0 0.3 0 0 0 base_link laser_frame",
        "launch": '''Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    arguments=['0.2', '0', '0.3', '0', '0', '0', 'base_link', 'laser_frame']
)''',
        "vs_dynamic": {
            "statický": "publikuje jednou, platí navždy (TRANSIENT_LOCAL QoS)",
            "dynamický": "publikuje opakovaně, mění se v čase"
        }
    }
    """
    # TODO: ↓
    pass


def tf2_prakticky():
    """
    🎯 VÝZVA 5: TF2 v praxi — transformace senzorových dat.
    Vrať dict:
    {
        "scénář": "převod bodu z kamery do souřadnic robota",
        "tf_strom": "map → odom → base_link → camera_link → camera_optical",
        "transformace_bodu": '''import tf2_geometry_msgs
from geometry_msgs.msg import PointStamped

point_camera = PointStamped()
point_camera.header.frame_id = 'camera_link'
point_camera.header.stamp = self.get_clock().now().to_msg()
point_camera.point.x = 1.0
point_camera.point.y = 0.0
point_camera.point.z = 0.5

try:
    point_base = self.tf_buffer.transform(
        point_camera, 'base_link',
        timeout=Duration(seconds=0.5))
    self.get_logger().info(
        f'Bod v base_link: [{point_base.point.x:.2f}, '
        f'{point_base.point.y:.2f}, {point_base.point.z:.2f}]')
except TransformException as e:
    self.get_logger().warn(f'Transformace selhala: {e}')''',
        "do_transform": "tf2_geometry_msgs.do_transform_point(point, transform)",
        "závislosti": ["tf2_ros", "tf2_geometry_msgs", "tf_transformations"],
        "debug_tipy": [
            "ros2 run tf2_tools view_frames → PDF stromu",
            "ros2 run tf2_ros tf2_echo frame1 frame2",
            "rviz2 → Add → TF → zobrazí všechny frames"
        ]
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="TF2 — souřadnicové rámce",
        theory="""TF2 = systém pro tracking souřadnicových rámců:
  world → odom → base_link → laser_frame

  Každý frame má:
  - Rodiče (parent frame)
  - Translaci [x, y, z]
  - Rotaci [quaternion]

  Umožňuje: "kde je laser_frame vzhledem k base_link?"

  CLI: ros2 run tf2_tools view_frames → PDF stromu""",
        task="Popiš TF2 strom a běžné souřadnicové rámce.",
        difficulty=1, points=15,
        hints=[
            "Strom frames: world → odom → base_link → senzory",
            "Transform = translace [x,y,z] + rotace [quaternion]"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "strom" in r
                    and "transform" in r
                    and "cli" in r,
                    "TF2 základy ✓"
                )
            )(tf2_zaklady()),
        ]
    ),
    Challenge(
        title="TF2 Broadcaster",
        theory="""Broadcaster publikuje transformace:
  br = TransformBroadcaster(self)

  t = TransformStamped()
  t.header.frame_id = 'odom'      # rodič
  t.child_frame_id = 'base_link'  # potomek
  t.transform.translation.x = 1.0
  t.transform.rotation.w = 1.0    # identity quaternion

  br.sendTransform(t)

  Quaternion: [x,y,z,w] — 4D rotace bez gimbal locku""",
        task="Implementuj broadcaster s quaternion rotací.",
        difficulty=2, points=20,
        hints=[
            "TransformStamped s header.frame_id a child_frame_id",
            "quaternion_from_euler(roll, pitch, yaw) pro konverzi"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "publikování" in r
                    and "quaternion" in r
                    and "identity" in r["quaternion"],
                    "Broadcaster ✓"
                )
            )(tf2_broadcaster()),
        ]
    ),
    Challenge(
        title="TF2 Listener",
        theory="""Listener získává transformace:
  buffer = Buffer()
  listener = TransformListener(buffer, self)

  trans = buffer.lookup_transform(
      'target_frame', 'source_frame', time)

  Pozor na chyby:
  - LookupException: frame neexistuje
  - ExtrapolationException: čas mimo rozsah

  Vždy ošetřuj try/except!""",
        task="Implementuj listener s error handlingem.",
        difficulty=2, points=20,
        hints=[
            "Buffer + TransformListener, lookup_transform()",
            "try/except pro LookupException, ExtrapolationException"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "lookup" in r
                    and "chyby" in r
                    and "LookupException" in r["chyby"],
                    "Listener ✓"
                )
            )(tf2_listener()),
        ]
    ),
    Challenge(
        title="Statické transformace",
        theory="""Statický transform = neměnný v čase:
  Příklad: lidar pevně přišroubovaný na robot

  StaticTransformBroadcaster — publikuje jednou
  TRANSIENT_LOCAL QoS → nové nody dostanou info

  CLI shortcut:
  ros2 run tf2_ros static_transform_publisher \\
      x y z yaw pitch roll parent child""",
        task="Publikuj statickou transformaci pro senzor.",
        difficulty=2, points=20,
        hints=[
            "StaticTransformBroadcaster — sendTransform jednou",
            "static_transform_publisher v launch souboru"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "broadcaster" in r
                    and "cli" in r
                    and "vs_dynamic" in r,
                    "Statické TF ✓"
                )
            )(staticke_transformy()),
        ]
    ),
    Challenge(
        title="TF2 v praxi — transformace dat",
        theory="""Reálný scénář: převod senzorových dat mezi frames:

  Kamera vidí objekt na [1, 0, 0.5] v camera_link
  → "Kde je ten objekt v base_link?"

  tf_buffer.transform(point_stamped, 'target_frame')

  Debug:
  - view_frames → PDF stromu
  - tf2_echo → živý výpis
  - RViz → vizualizace TF""",
        task="Transformuj bod z kamery do souřadnic robota.",
        difficulty=3, points=25,
        hints=[
            "tf2_geometry_msgs, PointStamped, tf_buffer.transform()",
            "view_frames pro debugging TF stromu"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "transformace_bodu" in r
                    and "debug_tipy" in r
                    and len(r["debug_tipy"]) >= 2,
                    "TF2 praxe ✓"
                )
            )(tf2_prakticky()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "TF2 Transforms", "10_06")
