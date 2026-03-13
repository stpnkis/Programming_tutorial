#!/usr/bin/env python3
"""🔌 WebSockets — asyncio websockets, Socket.IO, real-time komunikace."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def websocket_protokol():
    """
    🎯 VÝZVA 1: WebSocket protokol — základy a handshake.
    Vrať dict:
    {
        "co_je_websocket": {
            "definice": "plně duplexní komunikační kanál přes jedno TCP spojení",
            "vs_http": {
                "HTTP":      "request-response, klient vždy zahajuje, bez persistent connection",
                "WebSocket": "obousměrné posílání zpráv, server může posílat bez požadavku"
            },
            "url_schéma": {
                "ws":  "ws://host:port/cesta  — nešifrovaný",
                "wss": "wss://host:port/cesta — šifrovaný (TLS), jako HTTPS"
            }
        },
        "handshake": {
            "postup": [
                "1. Klient pošle HTTP GET s Upgrade: websocket",
                "2. Server odpoví 101 Switching Protocols",
                "3. Spojení upgraded — od teď WS rámce, ne HTTP"
            ],
            "klíčové_hlavičky": {
                "Upgrade":               "websocket",
                "Connection":            "Upgrade",
                "Sec-WebSocket-Key":     "base64 náhodný klíč",
                "Sec-WebSocket-Accept":  "SHA-1(key + GUID), potvrzení serveru",
                "Sec-WebSocket-Version": "13"
            }
        },
        "rámce": {
            "typy": {
                "Text":   "textová zpráva (UTF-8)",
                "Binary": "binární data",
                "Ping":   "keepalive ping",
                "Pong":   "odpověď na Ping",
                "Close":  "ukončení spojení"
            },
            "fragmentation": "velké zprávy lze rozsekat na více rámců"
        },
        "použití_v_robotice": [
            "real-time telemetrie z robota do dashboardu",
            "ovládání robota z webového rozhraní",
            "streamování kamerového obrazu (MJPEG over WS)",
            "synchronizace stavu více klientů najednou"
        ]
    }
    """
    # TODO: ↓
    pass


def asyncio_websockets():
    """
    🎯 VÝZVA 2: asyncio websockets — server a klient.
    Vrať dict:
    {
        "instalace": "pip install websockets",
        "server": {
            "kód": "import asyncio\\nimport websockets\\n\\nasync def handler(websocket):\\n    async for message in websocket:\\n        print(f'Přijato: {message}')\\n        await websocket.send(f'Echo: {message}')\\n\\nasync def main():\\n    async with websockets.serve(handler, 'localhost', 8765):\\n        await asyncio.Future()  # běží navždy\\n\\nasyncio.run(main())",
            "pozn": "každý nový klient dostane vlastní coroutine handler"
        },
        "klient": {
            "kód": "import asyncio\\nimport websockets\\n\\nasync def klient():\\n    async with websockets.connect('ws://localhost:8765') as ws:\\n        await ws.send('Ahoj, robote!')\\n        odpověď = await ws.recv()\\n        print(odpověď)\\n\\nasyncio.run(klient())"
        },
        "broadcast": {
            "kód": "connected = set()\\n\\nasync def handler(ws):\\n    connected.add(ws)\\n    try:\\n        async for msg in ws:\\n            # pošli všem připojeným klientům\\n            websockets.broadcast(connected, msg)\\n    finally:\\n        connected.discard(ws)",
            "účel": "distribuuj zprávu všem připojeným klientům"
        },
        "json_zprávy": {
            "kód": "import json\\n# odeslání\\nawait ws.send(json.dumps({'type': 'position', 'x': 1.5, 'y': 2.3}))\\n# příjem\\ndata = json.loads(await ws.recv())\\nprint(data['type'])",
            "doporučení": "vždy používej strukturované JSON zprávy s polem 'type'"
        }
    }
    """
    # TODO: ↓
    pass


def socketio_zaklady():
    """
    🎯 VÝZVA 3: Flask-SocketIO — eventy a rooms.
    Vrať dict:
    {
        "instalace": "pip install flask-socketio",
        "server_setup": {
            "kód": "from flask import Flask\\nfrom flask_socketio import SocketIO\\n\\napp = Flask(__name__)\\nsio = SocketIO(app, cors_allowed_origins='*')\\n\\n@sio.on('connect')\\ndef on_connect():\\n    print(f'Klient připojen: {request.sid}')\\n\\n@sio.on('disconnect')\\ndef on_disconnect():\\n    print('Klient odpojen')\\n\\n@sio.on('robot_cmd')\\ndef on_cmd(data):\\n    print(f'Příkaz: {data}')\\n    sio.emit('status', {'ok': True}, to=request.sid)\\n\\nif __name__ == '__main__':\\n    sio.run(app, port=5000)"
        },
        "emitování_událostí": {
            "jednomu_klientovi": "sio.emit('event', data, to=request.sid)",
            "všem":              "sio.emit('event', data)",
            "místnosti":         "sio.emit('event', data, room='robot_1')",
            "broadcast_ostatní": "sio.emit('event', data, broadcast=True, skip_sid=request.sid)"
        },
        "rooms": {
            "join":  "from flask_socketio import join_room\\njoin_room('robot_1')",
            "leave": "from flask_socketio import leave_room\\nleave_room('robot_1')",
            "účel":  "skupiny klientů — různé roboty, různé dashboardy"
        },
        "js_klient": {
            "kód": "<script src='/socket.io/socket.io.js'></script>\\nconst socket = io();\\nsocket.on('status', data => console.log(data));\\nsocket.emit('robot_cmd', {speed: 1.5, direction: 'forward'});",
            "pozn": "Socket.IO klient dostupný NPM nebo CDN"
        }
    }
    """
    # TODO: ↓
    pass


def realtime_komunikace():
    """
    🎯 VÝZVA 4: Vzory real-time komunikace.
    Vrať dict:
    {
        "komunikační_vzory": {
            "pub_sub": {
                "princip": "vydavatel posílá zprávy, odběratelé je přijímají bez znalosti sebe",
                "příklad": "robot publikuje polohu → dashboard odebírá"
            },
            "request_response_přes_ws": {
                "princip": "klient šle dotaz, server vrátí odpověď přes stejné WS spojení",
                "výhoda":  "nižší latence než HTTP pro časté dotazy"
            },
            "event_streaming": {
                "princip": "server posílá proud událostí jako log, telemetrii, senzorová data",
                "alternativa": "SSE (Server-Sent Events) pro jednosměrný tok server → klient"
            }
        },
        "stavové_zprávy": {
            "formát": "{'type': 'odometry', 'seq': 42, 'timestamp': 1700000000.0, 'x': 1.5, 'y': 2.3, 'theta': 0.78}",
            "seq":   "sekvenční číslo pro detekci ztracených zpráv",
            "doporučení": "vždy přidej timestamp a typ zprávy"
        },
        "heartbeat_keepalive": {
            "problem":   "WS spojení může být tiše ukončeno firewallem/NAT po nečinnosti",
            "řešení":    "pravidelně posílej Ping / vlastní heartbeat zprávy",
            "kód":       "await asyncio.sleep(30)\\nawait ws.ping()"
        },
        "reconnect": {
            "strategie": "exponenciální backoff: 1s, 2s, 4s, 8s, ...",
            "kód":       "delay = 1\\nwhile True:\\n    try:\\n        async with websockets.connect(uri) as ws:\\n            delay = 1  # resetuj po úspěchu\\n            await handle(ws)\\n    except Exception:\\n        await asyncio.sleep(delay)\\n        delay = min(delay * 2, 60)"
        }
    }
    """
    # TODO: ↓
    pass


def websocket_v_robotice():
    """
    🎯 VÝZVA 5: WebSockets v robotice — praktické vzory.
    Vrať dict:
    {
        "telemetrie_dashboard": {
            "architektura": "Robot → WS Server → Web Dashboard",
            "kód_serveru": "# robot pošle telemetrii\\n@sio.on('telemetry')\\ndef on_telemetry(data):\\n    # přepošli dashboardu\\n    sio.emit('telemetry_update', data, room='dashboard')",
            "datový_tok": "senzor → ROS2 node → WS bridge → browser dashboard"
        },
        "ovládání_robota": {
            "bezpečnost": [
                "autentizace tokenu při connect",
                "rate limiting příkazů (max N/s)",
                "watchdog timeout — zastav robota pokud WS selže",
                "validace rozsahu hodnot (rychlost, úhel)"
            ],
            "zpráva_příkazu": "{'type': 'cmd_vel', 'linear': 0.5, 'angular': 0.1}"
        },
        "ros2_ws_bridge": {
            "knihovny": ["rosbridge_suite (JSON přes WS)", "roslibpy (Python klient)", "rclnodejs (Node.js)"],
            "rosbridge_url": "ws://robot:9090",
            "příklad_subscribe": "{'op': 'subscribe', 'topic': '/odom', 'type': 'nav_msgs/Odometry'}"
        },
        "výkon": {
            "frekvence":    "telemetrie 10–50 Hz, video 30 Hz (komprimovaný JPEG)",
            "komprese":     "JSON minifikace, nebo msgpack pro binární efektivitu",
            "throttling":   "posílej jen při změně stavu, ne fixně každých N ms"
        },
        "alternativy_ws": {
            "SSE":      "Server-Sent Events — jednosměrný server→klient, jednodušší",
            "MQTT":     "lehký protokol pro IoT zařízení (viz modul 05_mqtt)",
            "gRPC":     "binární RPC — vyšší výkon, složitější integrace do web UI"
        }
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🏆 VÝZVY
# ============================================================

challenges = [
    Challenge(
        title="WebSocket protokol",
        theory="""WebSocket — plně duplexní komunikace přes TCP:

  HTTP:      klient žádá → server odpovídá (request-response)
  WebSocket: server i klient posílají kdykoli (full-duplex)

  Handshake:
    1. GET + Upgrade: websocket  → 101 Switching Protocols
    2. Spojení je teď WS, ne HTTP

  Schéma URL:
    ws://   — nešifrovaný
    wss://  — šifrovaný (TLS), jako HTTPS

  Rámce: Text, Binary, Ping/Pong, Close""",
        task="Popiš WebSocket protokol: rozdíl od HTTP, handshake, typy rámců a použití v robotice.",
        difficulty=1, points=15,
        hints=["full-duplex, 101 Switching Protocols, ws:// vs wss://, Ping/Pong, telemetrie"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "co_je_websocket" in r
                    and "handshake" in r
                    and "rámce" in r
                    and isinstance(r.get("použití_v_robotice"), list)
                    and len(r["použití_v_robotice"]) >= 2,
                    "WS protokol ✓"
                )
            )(websocket_protokol()),
        ]
    ),
    Challenge(
        title="asyncio websockets",
        theory="""Python websockets knihovna — async WS server/klient:

  pip install websockets

  Server:
    async with websockets.serve(handler, 'localhost', 8765):
        await asyncio.Future()

  Klient:
    async with websockets.connect('ws://localhost:8765') as ws:
        await ws.send('zpráva')
        data = await ws.recv()

  Broadcast: websockets.broadcast(connected_set, msg)
  JSON: json.dumps() / json.loads() pro strukturované zprávy""",
        task="Napiš asyncio WS server (echo + broadcast) a klient. Popiš JSON zprávy.",
        difficulty=2, points=20,
        hints=["websockets.serve, websockets.connect, async for msg in ws, broadcast, json.dumps"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "server" in r
                    and "klient" in r
                    and "broadcast" in r
                    and "json_zprávy" in r
                    and "json.dumps" in str(r.get("json_zprávy", {})),
                    "asyncio WS ✓"
                )
            )(asyncio_websockets()),
        ]
    ),
    Challenge(
        title="Flask-SocketIO",
        theory="""Flask-SocketIO — WebSockets s event systémem:

  pip install flask-socketio

  sio = SocketIO(app, cors_allowed_origins='*')

  @sio.on('connect')    — klient se připojil
  @sio.on('disconnect') — klient se odpojil
  @sio.on('robot_cmd')  — vlastní event

  Emitování:
    sio.emit('event', data, to=sid)   — jednomu
    sio.emit('event', data)            — všem
    sio.emit('event', data, room='x') — místnosti

  Rooms: join_room('robot_1'), leave_room('robot_1')""",
        task="Popiš Flask-SocketIO: setup, eventy, emitování (singlecast/broadcast/rooms), JS klient.",
        difficulty=2, points=20,
        hints=["SocketIO(app), @sio.on, sio.emit, to=request.sid, room=, join_room"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "server_setup" in r
                    and "emitování_událostí" in r
                    and "rooms" in r
                    and "join" in r.get("rooms", {})
                    and "js_klient" in r,
                    "Flask-SocketIO ✓"
                )
            )(socketio_zaklady()),
        ]
    ),
    Challenge(
        title="Real-time vzory",
        theory="""Vzory real-time komunikace:

  Pub/Sub: vydavatel → broker → odběratel
  Event streaming: nepřetržitý tok událostí

  Stavové zprávy — vždy přidej:
    {'type': 'odometry', 'seq': 42, 'timestamp': ..., ...}

  Heartbeat: pravidelný Ping aby NAT/firewall nezavřel spojení

  Reconnect s exponenciálním backoffem:
    delay = 1
    delay = min(delay * 2, 60)""",
        task="Popiš pub/sub vzor, formát stavových zpráv, heartbeat/keepalive a reconnect strategii.",
        difficulty=3, points=25,
        hints=["pub/sub, seq+timestamp, Ping/keepalive, exponenciální backoff, SSE alternativa"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "komunikační_vzory" in r
                    and "pub_sub" in r.get("komunikační_vzory", {})
                    and "stavové_zprávy" in r
                    and "heartbeat_keepalive" in r
                    and "reconnect" in r,
                    "Real-time vzory ✓"
                )
            )(realtime_komunikace()),
        ]
    ),
    Challenge(
        title="WebSockets v robotice",
        theory="""WebSockets pro robotické systémy:

  Robot → WS Server → Web Dashboard (telemetrie)
  Dashboard → WS Server → Robot (příkazy)

  ROS2 bridge: rosbridge_suite
    ws://robot:9090
    {'op': 'subscribe', 'topic': '/odom', ...}

  Bezpečnost příkazů:
    - autentizace tokenu
    - rate limiting
    - watchdog timeout (zastav robot pokud WS selže)

  Výkon: 10–50 Hz telemetrie, msgpack pro efektivitu""",
        task="Popiš architekturu WS telemetrie/ovládání, ROS2 bridge a bezpečnostní aspekty.",
        difficulty=3, points=25,
        hints=["telemetrie_dashboard, rosbridge_suite, watchdog, rate limiting, msgpack"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "telemetrie_dashboard" in r
                    and "ovládání_robota" in r
                    and isinstance(r["ovládání_robota"].get("bezpečnost"), list)
                    and len(r["ovládání_robota"]["bezpečnost"]) >= 3
                    and "ros2_ws_bridge" in r
                    and "alternativy_ws" in r,
                    "WS v robotice ✓"
                )
            )(websocket_v_robotice()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "WebSockets", "12_03")
