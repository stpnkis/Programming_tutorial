#!/usr/bin/env python3
"""👁️ Perception Pipeline — Zpracování senzorů, fúze dat a detekce překážek."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def senzory_v_ros2():
    """
    🎯 VÝZVA 1: Senzory a jejich zprávy v ROS2.
    Vrať dict:
    {
        "lidar": {
            "zpráva": "sensor_msgs/LaserScan",
            "topic": "/scan",
            "data": {
                "ranges": "pole vzdáleností [float32[]]",
                "angle_min": "počáteční úhel [rad]",
                "angle_max": "koncový úhel [rad]",
                "angle_increment": "krok úhlu [rad]",
                "range_min": "minimální vzdálenost",
                "range_max": "maximální vzdálenost"
            }
        },
        "kamera_rgb": {
            "zpráva": "sensor_msgs/Image",
            "topic": "/camera/image_raw",
            "bridge": "cv_bridge — konverze ROS Image ↔ OpenCV numpy",
            "komprimovaná": "sensor_msgs/CompressedImage"
        },
        "depth_kamera": {
            "zpráva": "sensor_msgs/Image (encoding: 32FC1 nebo 16UC1)",
            "topic": "/camera/depth/image_raw",
            "pointcloud": "sensor_msgs/PointCloud2 — 3D data"
        },
        "imu": {
            "zpráva": "sensor_msgs/Imu",
            "topic": "/imu/data",
            "data": ["orientation (quaternion)", "angular_velocity", "linear_acceleration"]
        },
        "odometrie": {
            "zpráva": "nav_msgs/Odometry",
            "topic": "/odom",
            "data": ["pose (pozice + orientace)", "twist (rychlost)"]
        }
    }
    """
    # TODO: ↓
    pass


def cv_bridge_zpracovani():
    """
    🎯 VÝZVA 2: CvBridge — zpracování obrazu v ROS2.
    Vrať dict:
    {
        "co_je_cv_bridge": "knihovna pro konverzi ROS Image ↔ OpenCV numpy array",
        "instalace": "sudo apt install ros-humble-cv-bridge",
        "ros_to_cv": '''from cv_bridge import CvBridge
import cv2

bridge = CvBridge()

def image_callback(self, msg):
    cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
    # Teď je to numpy array — použij OpenCV
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)''',
        "cv_to_ros": '''processed_msg = self.bridge.cv2_to_imgmsg(edges, encoding='mono8')
self.pub.publish(processed_msg)''',
        "depth": '''depth_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='32FC1')
# depth_image[y, x] = vzdálenost v metrech
distance = depth_image[240, 320]  # střed obrazu''',
        "compressed": '''from sensor_msgs.msg import CompressedImage
import numpy as np

def compressed_cb(self, msg):
    np_arr = np.frombuffer(msg.data, np.uint8)
    cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)''',
        "node_příklad": '''class ImageProcessor(Node):
    def __init__(self):
        super().__init__('image_processor')
        self.bridge = CvBridge()
        self.sub = self.create_subscription(Image, '/camera/image_raw', self.cb, 10)
        self.pub = self.create_publisher(Image, '/camera/processed', 10)

    def cb(self, msg):
        cv_img = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        result = cv2.GaussianBlur(cv_img, (5, 5), 0)
        self.pub.publish(self.bridge.cv2_to_imgmsg(result, 'bgr8'))'''
    }
    """
    # TODO: ↓
    pass


def lidar_zpracovani():
    """
    🎯 VÝZVA 3: Zpracování LaserScan dat.
    Vrať dict:
    {
        "čtení_dat": '''def scan_callback(self, msg):
    ranges = msg.ranges           # tuple vzdáleností
    angle = msg.angle_min         # počáteční úhel
    min_dist = min(r for r in ranges if r > msg.range_min)
    closest_idx = ranges.index(min_dist)
    closest_angle = msg.angle_min + closest_idx * msg.angle_increment''',
        "sektory": '''import math

def get_sector_min(ranges, angle_min, angle_inc, sector_start_deg, sector_end_deg):
    # Minimální vzdálenost v daném sektoru.
    start_idx = int((math.radians(sector_start_deg) - angle_min) / angle_inc)
    end_idx = int((math.radians(sector_end_deg) - angle_min) / angle_inc)
    sector = [r for r in ranges[start_idx:end_idx] if r > 0.1]
    return min(sector) if sector else float('inf')

# Příklad: překážka vpředu (±30°)?
front_dist = get_sector_min(ranges, msg.angle_min, msg.angle_increment, -30, 30)''',
        "filtrování": {
            "neplatné": "odfiltruj inf, nan a range mimo min/max",
            "mediánový": "mediánový filtr pro odstranění šumu",
            "podvzorkování": "beri každý N-tý paprsek pro rychlost"
        },
        "překážková_reakce": '''def obstacle_avoidance(self, msg):
    front = min(msg.ranges[len(msg.ranges)//3 : 2*len(msg.ranges)//3])
    cmd = Twist()
    if front < 0.5:  # překážka blízko
        cmd.angular.z = 0.5  # otoč se
    else:
        cmd.linear.x = 0.3   # jeď vpřed
    self.cmd_pub.publish(cmd)''',
        "scan_to_pointcloud": "laser_geometry balíček — LaserProjection().projectLaser(scan)"
    }
    """
    # TODO: ↓
    pass


def sensor_fusion():
    """
    🎯 VÝZVA 4: Fúze senzorů — robot_localization.
    Vrať dict:
    {
        "co_je_sensor_fusion": "kombinace dat z více senzorů pro přesnější odhad stavu",
        "robot_localization": {
            "popis": "ROS2 balíček pro fúzi senzorů (EKF/UKF)",
            "ekf_node": "rozšířený Kalmanův filtr — pro lineární systémy",
            "ukf_node": "unscented Kalmanův filtr — pro nelineární systémy"
        },
        "vstupy": ["odometrie (wheel encoders)", "IMU", "GPS", "vizuální odometrie"],
        "výstup": "nav_msgs/Odometry — fúzovaná pozice + orientace + rychlost",
        "konfigurace": '''ekf_filter_node:
  ros__parameters:
    frequency: 30.0
    two_d_mode: true
    publish_tf: true
    map_frame: map
    odom_frame: odom
    base_link_frame: base_link

    odom0: /wheel/odometry
    odom0_config: [true, true, false,   # x, y, z
                   false, false, true,    # roll, pitch, yaw
                   false, false, false,   # vx, vy, vz
                   false, false, true,    # vroll, vpitch, vyaw
                   false, false, false]   # ax, ay, az

    imu0: /imu/data
    imu0_config: [false, false, false,
                  false, false, true,
                  false, false, false,
                  false, false, true,
                  true, false, false]''',
        "princip_ekf": {
            "predict": "předpověď stavu na základě modelu pohybu",
            "update": "korekce na základě měření senzorů",
            "covariance": "nejistota — čím menší, tím důvěryhodnější"
        }
    }
    """
    # TODO: ↓
    pass


def obstacle_detection():
    """
    🎯 VÝZVA 5: Detekce a sledování překážek.
    Vrať dict:
    {
        "přístupy": {
            "lidar_based": "segmentace LaserScan — clustering blízkých bodů",
            "pointcloud_based": "PCL clustering na 3D datech",
            "vision_based": "detekce objektů neuronovou sítí (YOLO, SSD)",
            "depth_based": "depth image segmentace"
        },
        "lidar_clustering": '''import numpy as np
from sklearn.cluster import DBSCAN

def cluster_scan(ranges, angle_min, angle_inc, eps=0.3, min_samples=3):
    # Převod polárních na kartézské
    angles = np.arange(len(ranges)) * angle_inc + angle_min
    valid = np.array(ranges) < 10.0
    x = np.array(ranges)[valid] * np.cos(angles[valid])
    y = np.array(ranges)[valid] * np.sin(angles[valid])
    points = np.column_stack([x, y])

    # DBSCAN clustering
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(points)
    labels = clustering.labels_
    n_obstacles = len(set(labels)) - (1 if -1 in labels else 0)
    return points, labels, n_obstacles''',
        "bounding_box": '''from visualization_msgs.msg import Marker, MarkerArray

def publish_obstacle_markers(self, obstacles):
    markers = MarkerArray()
    for i, obs in enumerate(obstacles):
        m = Marker()
        m.header.frame_id = 'base_link'
        m.id = i
        m.type = Marker.CUBE
        m.pose.position.x = obs['center_x']
        m.pose.position.y = obs['center_y']
        m.scale.x = obs['width']
        m.scale.y = obs['height']
        m.scale.z = 0.5
        m.color.r = 1.0
        m.color.a = 0.8
        markers.markers.append(m)
    self.marker_pub.publish(markers)''',
        "tracking": "Sledování překážek v čase — Kalman filtr nebo Hungarian algorithm pro přiřazení",
        "integrace_s_nav2": "Detekované překážky → costmap přes obstacle_layer plugin"
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Senzory v ROS2",
        theory="""Hlavní senzory a jejich zprávy:
  LiDAR:  sensor_msgs/LaserScan → /scan
  Kamera: sensor_msgs/Image → /camera/image_raw
  Depth:  sensor_msgs/Image (32FC1) → /camera/depth
  IMU:    sensor_msgs/Imu → /imu/data
  Odom:   nav_msgs/Odometry → /odom

  LaserScan: ranges[] = pole vzdáleností po úhlech
  Image: výška × šířka × kanály (BGR nebo RGB)""",
        task="Vyjmenuj hlavní senzory a jejich ROS2 zprávy.",
        difficulty=1, points=15,
        hints=[
            "sensor_msgs: LaserScan, Image, Imu, PointCloud2",
            "Lidar → /scan, kamera → /camera/image_raw, IMU → /imu/data"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "lidar" in r
                    and "kamera_rgb" in r
                    and "imu" in r
                    and "zpráva" in r["lidar"],
                    "Senzory ✓"
                )
            )(senzory_v_ros2()),
        ]
    ),
    Challenge(
        title="CvBridge — zpracování obrazu",
        theory="""CvBridge = most mezi ROS Image a OpenCV:
  bridge = CvBridge()

  ROS → OpenCV:
  cv_img = bridge.imgmsg_to_cv2(msg, 'bgr8')

  OpenCV → ROS:
  ros_msg = bridge.cv2_to_imgmsg(cv_img, 'bgr8')

  Teď můžeš použít celé OpenCV na ROS datech!""",
        task="Implementuj zpracování obrazu s CvBridge.",
        difficulty=2, points=20,
        hints=[
            "imgmsg_to_cv2() a cv2_to_imgmsg() pro konverze",
            "desired_encoding: bgr8, rgb8, mono8, 32FC1 (depth)"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "ros_to_cv" in r
                    and "cv_to_ros" in r
                    and "node_příklad" in r,
                    "CvBridge ✓"
                )
            )(cv_bridge_zpracovani()),
        ]
    ),
    Challenge(
        title="LiDAR zpracování",
        theory="""LaserScan = pole vzdáleností po úhlech:
  ranges[0] = vzdálenost na angle_min
  ranges[i] = vzdálenost na angle_min + i * angle_increment

  Typické úlohy:
  - Nejbližší překážka (min z ranges)
  - Sektory (vpředu, vlevo, vpravo)
  - Obstacle avoidance (reakce na blízké překážky)""",
        task="Zpracuj LaserScan — sektory a obstacle avoidance.",
        difficulty=2, points=20,
        hints=[
            "min(ranges) pro nejbližší, sektory podle indexů",
            "Filtruj inf/nan, reaguj na překážky změnou cmd_vel"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "sektory" in r
                    and "překážková_reakce" in r
                    and "filtrování" in r,
                    "LiDAR zpracování ✓"
                )
            )(lidar_zpracovani()),
        ]
    ),
    Challenge(
        title="Fúze senzorů",
        theory="""robot_localization = EKF/UKF fúze:
  Kombinuje: odometrie + IMU + GPS + ...
  Výstup: přesný odhad pozice a orientace

  EKF (Extended Kalman Filter):
  1. Predict: odhad na základě modelu
  2. Update: korekce na základě měření
  3. Covariance: míra nejistoty

  Každý senzor má svou konfiguraci:
  odom0_config: [x, y, z, roll, pitch, yaw, ...]""",
        task="Nakonfiguruj sensor fusion s EKF.",
        difficulty=3, points=25,
        hints=[
            "robot_localization: ekf_filter_node s odom + IMU",
            "_config pole: true/false pro každou dimenzi stavu"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "robot_localization" in r
                    and "konfigurace" in r
                    and "princip_ekf" in r,
                    "Sensor fusion ✓"
                )
            )(sensor_fusion()),
        ]
    ),
    Challenge(
        title="Detekce překážek",
        theory="""Detekce překážek z senzorových dat:

  LiDAR: DBSCAN clustering bodů → skupiny = překážky
  Depth: segmentace hloubkového obrazu
  Vision: neuronové sítě (YOLO, SSD)

  Pipeline:
  1. Senzorová data → preprocessing
  2. Segmentace/clustering → kandidáti
  3. Bounding boxy → MarkerArray pro vizualizaci
  4. Tracking v čase → Kalman filtr""",
        task="Implementuj detekci překážek z LiDAR dat.",
        difficulty=3, points=25,
        hints=[
            "Polární → kartézské, DBSCAN clustering",
            "Visualization_msgs/MarkerArray pro zobrazení v RViz"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "lidar_clustering" in r
                    and "bounding_box" in r
                    and "přístupy" in r
                    and len(r["přístupy"]) >= 3,
                    "Detekce překážek ✓"
                )
            )(obstacle_detection()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Perception Pipeline", "10_09")
