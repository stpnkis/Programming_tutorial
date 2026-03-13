#!/usr/bin/env python3
"""🔄 ROS2 Services & Actions — Request/response, action server/client, feedback."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def service_zaklady():
    """
    🎯 VÝZVA 1: Základy ROS2 Services.
    Vrať dict:
    {
        "co_je_service": "synchronní request/response komunikace mezi nody",
        "vs_topic": {
            "topic": "jednosměrný proud dat (pub→sub), asynchronní",
            "service": "dotaz → odpověď, synchronní, 1:1"
        },
        "srv_soubor": '''# AddTwoInts.srv
int64 a
int64 b
---
int64 sum''',
        "server": '''from example_interfaces.srv import AddTwoInts

class AddServer(Node):
    def __init__(self):
        super().__init__('add_server')
        self.srv = self.create_service(
            AddTwoInts, 'add_two_ints', self.callback)

    def callback(self, request, response):
        response.sum = request.a + request.b
        return response''',
        "klient_cli": "ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts '{a: 2, b: 3}'"
    }
    """
    # TODO: ↓
    pass


def service_klient():
    """
    🎯 VÝZVA 2: Service Client — volání služby z kódu.
    Vrať dict:
    {
        "vytvoření": "self.cli = self.create_client(AddTwoInts, 'add_two_ints')",
        "čekání": "self.cli.wait_for_service(timeout_sec=5.0)",
        "request": '''req = AddTwoInts.Request()
req.a = 2
req.b = 3''',
        "volání_sync": "response = self.cli.call(req)  # blokující",
        "volání_async": '''future = self.cli.call_async(req)
rclpy.spin_until_future_complete(self, future)
result = future.result()''',
        "příklad": '''class AddClient(Node):
    def __init__(self):
        super().__init__('add_client')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Čekám na službu...')

    def send_request(self, a, b):
        req = AddTwoInts.Request()
        req.a = a
        req.b = b
        future = self.cli.call_async(req)
        return future'''
    }
    """
    # TODO: ↓
    pass


def action_zaklady():
    """
    🎯 VÝZVA 3: ROS2 Actions — základy.
    Vrať dict:
    {
        "co_je_action": "asynchronní long-running úkol s průběžnou zpětnou vazbou",
        "vs_service": {
            "service": "rychlý dotaz/odpověď, žádný feedback",
            "action": "dlouhý úkol, průběžný feedback, lze zrušit"
        },
        "action_soubor": '''# Fibonacci.action
int32 order         # Goal (cíl)
---
int32[] sequence    # Result (výsledek)
---
int32[] partial_sequence  # Feedback (průběh)''',
        "části": {
            "goal": "co chceme dosáhnout (request)",
            "result": "konečný výsledek po dokončení",
            "feedback": "průběžná info během provádění"
        },
        "použití": ["navigace k cíli", "pohyb ramena", "skenování prostoru", "dlouhý výpočet"]
    }
    """
    # TODO: ↓
    pass


def action_server():
    """
    🎯 VÝZVA 4: Action Server — zpracování cílů.
    Vrať dict:
    {
        "import": "from rclpy.action import ActionServer\nfrom custom_interfaces.action import MyAction",
        "vytvoření": '''self.action_server = ActionServer(
    self, MyAction, 'my_action',
    execute_callback=self.execute_callback,
    goal_callback=self.goal_callback)''',
        "goal_callback": '''def goal_callback(self, goal_request):
    self.get_logger().info('Přijat cíl')
    return GoalResponse.ACCEPT  # nebo REJECT''',
        "execute_callback": '''async def execute_callback(self, goal_handle):
    feedback = MyAction.Feedback()
    for i in range(goal_handle.request.order):
        feedback.progress = float(i) / goal_handle.request.order
        goal_handle.publish_feedback(feedback)
        await asyncio.sleep(1)
    goal_handle.succeed()
    result = MyAction.Result()
    result.success = True
    return result''',
        "stavy": ["ACCEPTED", "EXECUTING", "CANCELING", "SUCCEEDED", "ABORTED", "CANCELED"]
    }
    """
    # TODO: ↓
    pass


def action_klient():
    """
    🎯 VÝZVA 5: Action Client — odesílání cílů a sledování feedbacku.
    Vrať dict:
    {
        "import": "from rclpy.action import ActionClient",
        "vytvoření": "self.action_client = ActionClient(self, MyAction, 'my_action')",
        "odeslání_cíle": '''goal = MyAction.Goal()
goal.order = 10
future = self.action_client.send_goal_async(
    goal, feedback_callback=self.feedback_cb)
future.add_done_callback(self.goal_response_cb)''',
        "feedback_callback": '''def feedback_cb(self, feedback_msg):
    progress = feedback_msg.feedback.progress
    self.get_logger().info(f'Průběh: {progress:.0%}')''',
        "result_callback": '''def goal_response_cb(self, future):
    goal_handle = future.result()
    if not goal_handle.accepted:
        self.get_logger().info('Cíl odmítnut')
        return
    result_future = goal_handle.get_result_async()
    result_future.add_done_callback(self.result_cb)

def result_cb(self, future):
    result = future.result().result
    self.get_logger().info(f'Výsledek: {result}')''',
        "zrušení": "goal_handle.cancel_goal_async()"
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Services — request/response",
        theory="""Service = synchronní komunikace:
  Client → Request → Server → Response → Client

  Na rozdíl od topiců (jednosměrný proud):
  - Service je 1:1, dotaz/odpověď
  - Vhodné pro: konfigurace, výpočty, přepínání

  .srv soubor definuje formát:
  int64 a
  int64 b
  ---         ← odděluje request od response
  int64 sum""",
        task="Popiš ROS2 service a vytvoř server.",
        difficulty=1, points=15,
        hints=[
            "create_service(typ, 'jméno', callback)",
            "callback přijímá request a response, vrací response"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "vs_topic" in r and "server" in r and "srv_soubor" in r,
                    "Service základy ✓"
                )
            )(service_zaklady()),
        ]
    ),
    Challenge(
        title="Service Client",
        theory="""Client volá službu:
  cli = self.create_client(AddTwoInts, 'add_two_ints')

  Asynchronní volání (doporučené):
  future = cli.call_async(request)
  rclpy.spin_until_future_complete(node, future)

  Vždy čekej, než je service dostupná:
  cli.wait_for_service(timeout_sec=5.0)""",
        task="Implementuj service klienta s async voláním.",
        difficulty=2, points=20,
        hints=[
            "create_client(typ, 'jméno')",
            "call_async vrací Future, spin_until_future_complete čeká"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "volání_async" in r and "příklad" in r and "čekání" in r,
                    "Service klient ✓"
                )
            )(service_klient()),
        ]
    ),
    Challenge(
        title="Actions — základy",
        theory="""Actions = long-running úkoly s feedbackem:
  Client → Goal → Server → Feedback... → Result

  Tři části .action souboru:
  Goal    (co chceme)
  ---
  Result  (konečný výsledek)
  ---
  Feedback (průběžné info)

  Příklad: navigace → goal=pozice, feedback=aktuální_pozice, result=úspěch""",
        task="Popiš ROS2 actions a jejich tři části.",
        difficulty=2, points=20,
        hints=[
            "Action = Goal + Result + Feedback, oddělené ---",
            "Použití: navigace, pohyb ramena, dlouhé úkoly"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "části" in r and "goal" in r["části"] and "feedback" in r["části"],
                    "Action základy ✓"
                )
            )(action_zaklady()),
        ]
    ),
    Challenge(
        title="Action Server",
        theory="""Action Server zpracovává cíle:
  ActionServer(self, MyAction, 'action_name',
      execute_callback=..., goal_callback=...)

  goal_callback: přijme/odmítne cíl
  execute_callback: provede úkol, posílá feedback

  Stavy: ACCEPTED → EXECUTING → SUCCEEDED/ABORTED
  Lze zrušit: CANCELING → CANCELED""",
        task="Implementuj action server s goal a execute callbacky.",
        difficulty=3, points=25,
        hints=[
            "GoalResponse.ACCEPT, goal_handle.publish_feedback()",
            "goal_handle.succeed() → nastaví stav na SUCCEEDED"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "execute_callback" in r and "stavy" in r and len(r["stavy"]) >= 4,
                    "Action server ✓"
                )
            )(action_server()),
        ]
    ),
    Challenge(
        title="Action Client",
        theory="""Action Client odesílá cíle a sleduje průběh:
  client = ActionClient(self, MyAction, 'action_name')

  send_goal_async(goal, feedback_callback=...)
  → vrací Future s goal_handle

  goal_handle.get_result_async()
  → vrací Future s výsledkem

  goal_handle.cancel_goal_async()
  → zruší probíhající action""",
        task="Implementuj action klienta s feedbackem a zrušením.",
        difficulty=3, points=25,
        hints=[
            "send_goal_async + feedback_callback pro průběh",
            "cancel_goal_async() pro zrušení probíhajícího cíle"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "feedback_callback" in r
                    and "result_callback" in r
                    and "zrušení" in r,
                    "Action klient ✓"
                )
            )(action_klient()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "ROS2 Services & Actions", "10_03")
