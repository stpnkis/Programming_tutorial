#!/usr/bin/env python3
"""📡 ROS2 Nodes & Topics — Vytváření nodů, publisherů, subscriberů a správa zpráv."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def node_zaklady():
    """
    🎯 VÝZVA 1: Základy ROS2 Node.
    Vrať dict:
    {
        "co_je_node": "základní výpočetní jednotka v ROS2 grafu",
        "vytvoření": {
            "import": "import rclpy\nfrom rclpy.node import Node",
            "init": "rclpy.init()",
            "node": "node = Node('muj_node')",
            "spin": "rclpy.spin(node)",
            "shutdown": "node.destroy_node()\nrclpy.shutdown()"
        },
        "class_based": '''class MujNode(Node):
    def __init__(self):
        super().__init__('muj_node')
        self.get_logger().info('Node spuštěn!')''',
        "lifecycle": ["unconfigured", "inactive", "active", "finalized"],
        "pojmenování": "malá písmena, podtržítka, bez mezer"
    }
    """
    # TODO: ↓
    pass


def publisher_node():
    """
    🎯 VÝZVA 2: Publisher — odesílání zpráv na topic.
    Vrať dict:
    {
        "co_je_publisher": "node, který odesílá zprávy na topic",
        "vytvoření": "self.pub = self.create_publisher(String, 'topic_name', 10)",
        "parametry": {
            "msg_type": "typ zprávy (např. String, Int32, Twist)",
            "topic": "název topicu (str)",
            "qos": "queue size — kolik zpráv uchovávat ve frontě"
        },
        "odeslání": "self.pub.publish(msg)",
        "timer": "self.timer = self.create_timer(0.5, self.timer_callback)",
        "příklad": '''from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.pub = self.create_publisher(String, 'topic', 10)
        self.timer = self.create_timer(0.5, self.timer_cb)
        self.count = 0

    def timer_cb(self):
        msg = String()
        msg.data = f'Hello {self.count}'
        self.pub.publish(msg)
        self.count += 1'''
    }
    """
    # TODO: ↓
    pass


def subscriber_node():
    """
    🎯 VÝZVA 3: Subscriber — příjem zpráv z topicu.
    Vrať dict:
    {
        "co_je_subscriber": "node, který přijímá zprávy z topicu",
        "vytvoření": "self.sub = self.create_subscription(String, 'topic', self.callback, 10)",
        "parametry": {
            "msg_type": "typ zprávy (musí sedět s publisherem)",
            "topic": "název topicu (stejný jako publisher)",
            "callback": "funkce volaná při příchodu zprávy",
            "qos": "queue size"
        },
        "callback": '''def listener_callback(self, msg):
    self.get_logger().info(f'Přijato: {msg.data}')''',
        "příklad": '''class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.sub = self.create_subscription(
            String, 'topic', self.listener_cb, 10)

    def listener_cb(self, msg):
        self.get_logger().info(f'Slyším: {msg.data}')'''
    }
    """
    # TODO: ↓
    pass


def message_typy():
    """
    🎯 VÝZVA 4: Typy zpráv v ROS2.
    Vrať dict:
    {
        "std_msgs": ["String", "Int32", "Float64", "Bool", "Header"],
        "geometry_msgs": ["Twist", "Pose", "Point", "Quaternion", "Vector3", "TransformStamped"],
        "sensor_msgs": ["Image", "LaserScan", "PointCloud2", "Imu", "JointState"],
        "nav_msgs": ["Odometry", "Path", "OccupancyGrid"],
        "import_syntax": "from geometry_msgs.msg import Twist",
        "twist_příklad": {
            "linear": {"x": "vpřed/vzad", "y": "vlevo/vpravo", "z": "nahoru/dolů"},
            "angular": {"x": "roll", "y": "pitch", "z": "yaw (otáčení)"}
        },
        "inspekce": "ros2 interface show geometry_msgs/msg/Twist"
    }
    """
    # TODO: ↓
    pass


def qos_profily():
    """
    🎯 VÝZVA 5: Quality of Service (QoS) profily.
    Vrať dict:
    {
        "co_je_qos": "nastavení spolehlivosti a chování komunikace",
        "parametry": {
            "reliability": "RELIABLE (TCP-like) vs BEST_EFFORT (UDP-like)",
            "durability": "VOLATILE (jen nové) vs TRANSIENT_LOCAL (i staré)",
            "history": "KEEP_LAST(N) vs KEEP_ALL",
            "depth": "počet zpráv v historii (u KEEP_LAST)",
            "deadline": "maximální čas mezi zprávami",
            "liveliness": "detekce výpadku nodu"
        },
        "profily": {
            "default": "RELIABLE, VOLATILE, KEEP_LAST(10)",
            "sensor_data": "BEST_EFFORT, VOLATILE, KEEP_LAST(5)",
            "services": "RELIABLE, VOLATILE"
        },
        "import": "from rclpy.qos import QoSProfile, ReliabilityPolicy",
        "příklad": '''from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

qos = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    durability=DurabilityPolicy.VOLATILE,
    depth=5
)
self.sub = self.create_subscription(Image, '/camera', self.cb, qos)'''
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="ROS2 Node — základy",
        theory="""Node = základní výpočetní jednotka v ROS2:
  - Každý node je samostatný proces
  - Komunikuje přes topics, services, actions
  - Pojmenování: malá písmena + podtržítka

  import rclpy
  from rclpy.node import Node

  class MujNode(Node):
      def __init__(self):
          super().__init__('muj_node')

  rclpy.init()
  node = MujNode()
  rclpy.spin(node)  # drží node aktivní
  rclpy.shutdown()""",
        task="Popiš, jak vytvořit ROS2 node a jeho lifecycle.",
        difficulty=1, points=15,
        hints=[
            "Klíčové: rclpy.init(), Node('jméno'), rclpy.spin(node)",
            "Lifecycle: unconfigured → inactive → active → finalized"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "vytvoření" in r and "class_based" in r,
                    "Node základy ✓"
                )
            )(node_zaklady()),
        ]
    ),
    Challenge(
        title="Publisher — odesílání zpráv",
        theory="""Publisher posílá zprávy na topic:
  self.pub = self.create_publisher(String, '/chat', 10)

  msg = String()
  msg.data = 'Ahoj světe!'
  self.pub.publish(msg)

  Timer pro periodické odesílání:
  self.timer = self.create_timer(0.5, self.callback)
  → callback se volá každých 0.5 sekundy""",
        task="Vytvoř publisher node s timerem.",
        difficulty=1, points=15,
        hints=[
            "create_publisher(typ_zprávy, 'topic', queue_size)",
            "create_timer(perioda_v_sec, callback_funkce)"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "vytvoření" in r and "timer" in r and "příklad" in r,
                    "Publisher ✓"
                )
            )(publisher_node()),
        ]
    ),
    Challenge(
        title="Subscriber — příjem zpráv",
        theory="""Subscriber naslouchá zprávám z topicu:
  self.sub = self.create_subscription(
      String, '/chat', self.callback, 10)

  def callback(self, msg):
      self.get_logger().info(f'Přijato: {msg.data}')

  Publisher i subscriber musí používat stejný:
  - topic name ('/chat')
  - message type (String)""",
        task="Vytvoř subscriber node s callbackem.",
        difficulty=1, points=15,
        hints=[
            "create_subscription(typ, 'topic', callback, qos)",
            "Callback přijímá msg jako parametr"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "callback" in r and "příklad" in r and "parametry" in r,
                    "Subscriber ✓"
                )
            )(subscriber_node()),
        ]
    ),
    Challenge(
        title="Typy zpráv",
        theory="""ROS2 zprávy jsou definované v balíčcích:
  std_msgs:      String, Int32, Float64, Bool
  geometry_msgs: Twist, Pose, Point, Vector3
  sensor_msgs:   Image, LaserScan, PointCloud2

  from geometry_msgs.msg import Twist
  cmd = Twist()
  cmd.linear.x = 0.5   # vpřed
  cmd.angular.z = 1.0   # otáčení

  Inspekce: ros2 interface show geometry_msgs/msg/Twist""",
        task="Vyjmenuj důležité typy zpráv a jejich použití.",
        difficulty=2, points=20,
        hints=[
            "std_msgs pro jednoduché typy, geometry_msgs pro pohyb/pozici",
            "Twist = lineární + úhlová rychlost (pro řízení robota)"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "std_msgs" in r
                    and "geometry_msgs" in r
                    and "sensor_msgs" in r
                    and len(r["geometry_msgs"]) >= 4,
                    "Typy zpráv ✓"
                )
            )(message_typy()),
        ]
    ),
    Challenge(
        title="QoS profily",
        theory="""QoS = Quality of Service — jak spolehlivá je komunikace:
  RELIABLE: zaručené doručení (jako TCP)
  BEST_EFFORT: bez záruky, rychlejší (jako UDP)

  Profily:
  - default: spolehlivý pro většinu
  - sensor_data: BEST_EFFORT — senzory generují hodně dat
  - services: vždy RELIABLE

  Publisher a subscriber musí mít kompatibilní QoS!
  RELIABLE pub → RELIABLE sub ✓
  BEST_EFFORT pub → RELIABLE sub ✗ (nefunguje!)""",
        task="Popiš QoS parametry a předdefinované profily.",
        difficulty=2, points=20,
        hints=[
            "reliability, durability, history, depth, deadline, liveliness",
            "QoSProfile z rclpy.qos, ReliabilityPolicy.BEST_EFFORT"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "parametry" in r
                    and "profily" in r
                    and "reliability" in r["parametry"],
                    "QoS profily ✓"
                )
            )(qos_profily()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "ROS2 Nodes & Topics", "10_02")
