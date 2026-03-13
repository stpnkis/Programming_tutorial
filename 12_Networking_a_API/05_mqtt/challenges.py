#!/usr/bin/env python3
"""📡 MQTT — broker, publish/subscribe, topics, QoS, Paho klient, IoT & robotika."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def mqtt_protokol():
    """
    🎯 VÝZVA 1: MQTT protokol — základy a architektura.
    Vrať dict:
    {
        "co_je_mqtt": {
            "definice": "Message Queuing Telemetry Transport — lehký pub/sub protokol pro IoT",
            "verze": {"3.1.1": "nejrozšířenější", "5.0": "nová s vlastnostmi zpráv, shared subs"},
            "transport": "TCP/IP (port 1883) nebo TLS (port 8883)",
            "použití": ["IoT senzory", "chytrá domácnost", "průmysl (IIoT)", "robotika"]
        },
        "architektura": {
            "broker": "centrální server, přijímá a distribuuje zprávy (Mosquitto, EMQX, HiveMQ)",
            "klient": "publisher nebo subscriber — zařízení, server, aplikace",
            "princip": [
                "1. Klienti se připojí k brokeru",
                "2. Subscriber se přihlásí k topiku",
                "3. Publisher publikuje zprávu na topik",
                "4. Broker doručí zprávu všem odběratelům topiku"
            ]
        },
        "výhody_vs_http": {
            "lightweight":   "malá hlavička (min. 2 bytes), ideální pro MCU s omezenou RAM",
            "persistent_conn": "stálé TCP spojení — broker tlačí zprávy bez polling",
            "pub_sub":       "decoupling — publisher a subscriber se neznají",
            "offline_msg":   "retained a queued zprávy pro offline zařízení"
        },
        "brokeři": {
            "mosquitto":    "open-source, lehký, ideální pro Raspberry Pi / embedded",
            "emqx":         "škálovatelný, webové rozhraní, vhodný pro produkci",
            "hivemq":       "enterprise, cloud verze dostupná",
            "test_broker":  "broker.hivemq.com:1883 nebo test.mosquitto.org — veřejný test broker"
        }
    }
    """
    # TODO: ↓
    pass


def paho_klient():
    """
    🎯 VÝZVA 2: Paho MQTT klient v Pythonu.
    Vrať dict:
    {
        "instalace": "pip install paho-mqtt",
        "publisher": {
            "kód": "import paho.mqtt.client as mqtt\\n\\nclient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, 'publisher_id')\\nclient.connect('broker.hivemq.com', 1883, keepalive=60)\\n\\nclient.publish('robot/speed', payload='1.5', qos=1, retain=False)\\nclient.disconnect()"
        },
        "subscriber": {
            "kód": "import paho.mqtt.client as mqtt\\n\\ndef on_connect(client, userdata, flags, rc, props):\\n    print(f'Připojeno: {rc}')\\n    client.subscribe('robot/#', qos=1)\\n\\ndef on_message(client, userdata, msg):\\n    print(f'Topik: {msg.topic}')\\n    print(f'Zpráva: {msg.payload.decode()}')\\n\\nclient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)\\nclient.on_connect = on_connect\\nclient.on_message = on_message\\nclient.connect('broker.hivemq.com', 1883)\\nclient.loop_forever()  # blokující smyčka"
        },
        "callbacky": {
            "on_connect":    "volán po úspěšném připojení → zde přihlašuj subscribce",
            "on_disconnect": "volán při odpojení — loguj nebo reconnect",
            "on_message":    "volán při příchozí zprávě",
            "on_publish":    "volán po potvrzení doručení (QoS 1+2)"
        },
        "loop_metody": {
            "loop_forever()": "blokující — vhodné pro dedikované vlákno/skript",
            "loop_start()":   "neblokující — spustí background vlákno, program běží dál",
            "loop_stop()":    "zastaví vlákno z loop_start()",
            "loop(timeout)":  "manuální — zavolej periodicky sám"
        },
        "tls_bezpečnost": {
            "kód": "client.tls_set(ca_certs='ca.crt')  # TLS šifrování\\nclient.connect(host, 8883)  # port 8883 pro TLS",
            "autentizace": "client.username_pw_set('user', 'password')"
        }
    }
    """
    # TODO: ↓
    pass


def topiky_a_qos():
    """
    🎯 VÝZVA 3: Struktura topik a Quality of Service.
    Vrať dict:
    {
        "topiky": {
            "formát": "hierarchický řetězec oddělený '/', case-sensitive",
            "příklady": [
                "robot/arm/joint1/angle",
                "factory/line1/sensor/temperature",
                "home/livingroom/lamp/state"
            ],
            "doporučení": "začni od obecného → konkrétní, vyhni se mezerám a speciálním znakům"
        },
        "zástupné_znaky": {
            "+": {
                "popis": "jednolevelový wildcard — jedno libovolné úrovně",
                "příklad": "robot/+/temperature  →  robot/arm/temperature, robot/base/temperature",
                "pozn": "nahrazuje právě jednu úroveň"
            },
            "#": {
                "popis": "víceúrovňový wildcard — vše od tohoto místa",
                "příklad": "robot/#  →  robot/speed, robot/arm/joint1/angle, robot/sensor/...",
                "pozn": "musí být na konci, odebírá celý podstrom"
            },
            "$SYS": "interní brokeri topiky — statistiky, stav (jen čtení)"
        },
        "qos": {
            "0": {
                "název":  "At most once (fire and forget)",
                "popis":  "zpráva odeslána max 1×, žádné potvrzení, může být ztracena",
                "použití": "telemetrie kde ztráta nevadí — rychlost, logging"
            },
            "1": {
                "název":  "At least once",
                "popis":  "zpráva doručena min 1× — PUBACK potvrzení, možné duplikáty",
                "použití": "příkazy, alerting — duplikát je lepší než ztráta"
            },
            "2": {
                "název":  "Exactly once",
                "popis":  "zpráva doručena přesně 1× — 4-way handshake (PUBREC/PUBREL/PUBCOMP)",
                "použití": "platby, kritické příkazy, vysoká latence"
            }
        }
    }
    """
    # TODO: ↓
    pass


def iot_vzory():
    """
    🎯 VÝZVA 4: IoT vzory — retained, LWT, bridging.
    Vrať dict:
    {
        "retained_zprávy": {
            "popis": "broker uloží poslední zprávu — noví odběratelé ji dostanou okamžitě",
            "kód": "client.publish('robot/status', 'online', retain=True)",
            "použití": [
                "stav zařízení — online/offline",
                "aktuální konfigurace",
                "poslední naměřená hodnota"
            ],
            "smazání": "publish prázdné payload s retain=True maže retained zprávu"
        },
        "lwt": {
            "název": "Last Will and Testament — poslední vůle",
            "popis": "zpráva odeslaná brokerem automaticky pokud klient neočekávaně odpojí",
            "kód": "client.will_set('robot/status', payload='offline', qos=1, retain=True)\\n# nastav PŘED connect()!",
            "použití": "detekce pádu zařízení, alive monitoring, supervisory systémy"
        },
        "clean_session": {
            "True":  "broker zapomene subscribce a frontu po odpojení (výchozí)",
            "False": "perzistentní session — broker drží QoS1/2 zprávy pro offline klienta",
            "podmínka": "klient se musí připojit se stejným client_id"
        },
        "přihlášení_více_topik": {
            "kód": "client.subscribe([('robot/speed', 1), ('robot/status', 0), ('factory/#', 2)])",
            "popis": "subscribe přijme список tuplic (topik, qos)"
        },
        "bridging": {
            "popis": "propojení dvou brokerů — zprávy se přenáší mezi nimi",
            "použití": "edge broker (lokální) ↔ cloud broker (AWS IoT, Azure IoT Hub)",
            "mosquitto_conf": "connection cloud\\n    address mqtt.example.com:8883\\n    topic robot/# out 1"
        }
    }
    """
    # TODO: ↓
    pass


def mqtt_v_robotice():
    """
    🎯 VÝZVA 5: MQTT v robotice — praktická architektura.
    Vrať dict:
    {
        "topik_schéma_robota": {
            "doporučená_struktura": {
                "robot/<id>/cmd/vel":       "příkaz rychlosti → robot",
                "robot/<id>/status":         "stav robota → všichni",
                "robot/<id>/telemetry/odom": "odometrie → dashboard",
                "robot/<id>/telemetry/imu":  "IMU data → dashboard",
                "robot/<id>/alert":          "alarmy → operátor",
                "factory/all/cmd/stop":      "E-STOP pro všechny roboty"
            }
        },
        "ros2_mqtt_bridge": {
            "knihovny": ["mqtt_ros2 bridge", "mqtt_client (ROS2 package)", "vlastní bridge"],
            "příklad_bridge": "# ROS2 subscriber → MQTT publisher\\ndef odom_callback(msg):\\n    data = json.dumps({'x': msg.pose.pose.position.x, 'y': msg.pose.pose.position.y})\\n    mqtt_client.publish('robot/1/telemetry/odom', data, qos=0)"
        },
        "bezpečnost": {
            "autentizace": "client.username_pw_set('robot1', 'tajnytoken')",
            "tls":         "client.tls_set(ca_certs, certfile, keyfile)  # mTLS pro zařízení",
            "acl":         "Access Control List — každý klient jen na povolené topiky",
            "doporučení":  "v produkci nikdy nepoužívej anonymní přístup"
        },
        "cloud_integrace": {
            "aws_iot": {
                "endpoint":  "xxxx.iot.eu-west-1.amazonaws.com:8883",
                "auth":      "X.509 certifikáty — každé zařízení má unikátní cert",
                "výhody":    "pravidla, Lambda triggery, stínění zařízení"
            },
            "mosquitto_lokální": "apt install mosquitto mosquitto-clients\\nmosquitto -c /etc/mosquitto/mosquitto.conf"
        },
        "výkon_a_optimalizace": {
            "payload_formát": "JSON pro čitelnost, CBOR/MessagePack pro efektivitu",
            "frekvence":      "telemetrie 1–10 Hz typicky, alarmy okamžitě",
            "qos_volba":      "QoS 0 pro telemetrii, QoS 1 pro příkazy, QoS 2 pro kritické",
            "client_id":      "unikátní! duplicitní ID způsobí odpojování zařízení"
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
        title="MQTT protokol",
        theory="""MQTT — Message Queuing Telemetry Transport:

  Architektura:
    Publisher → Broker → Subscriber (decoupled)
    Broker: Mosquitto, EMQX, HiveMQ

  vs HTTP:
    ✓ 2-byte min hlavička (ideální pro MCU)
    ✓ persistent connection — broker tlačí zprávy
    ✓ pub/sub — zařízení se neznají

  Transport: TCP port 1883 (plaintext), 8883 (TLS)
  Verze: 3.1.1 (nejrozšířenější), 5.0 (nová)

  Test broker: broker.hivemq.com:1883""",
        task="Popiš MQTT protokol, pub/sub architekturu, výhody vs HTTP a dostupné brokery.",
        difficulty=1, points=15,
        hints=["broker, publisher, subscriber, TCP 1883/TLS 8883, Mosquitto, lightweight"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "co_je_mqtt" in r
                    and "architektura" in r
                    and "broker" in r.get("architektura", {})
                    and "výhody_vs_http" in r
                    and "brokeři" in r,
                    "MQTT protokol ✓"
                )
            )(mqtt_protokol()),
        ]
    ),
    Challenge(
        title="Paho MQTT klient",
        theory="""paho-mqtt — Python MQTT klient:

  pip install paho-mqtt

  Publisher:
    client = mqtt.Client(CallbackAPIVersion.VERSION2, 'id')
    client.connect('broker.hivemq.com', 1883)
    client.publish('topik', 'zpráva', qos=1)

  Subscriber:
    client.on_connect = on_connect   # přihlásit subscripce zde!
    client.on_message = on_message   # zpracuj zprávu
    client.loop_forever()            # blokující event loop

  TLS: client.tls_set(ca_certs='ca.crt')  + port 8883
  Auth: client.username_pw_set('user', 'pass')""",
        task="Napiš Paho publisher a subscriber. Popiš callbacky, loop metody a TLS/auth.",
        difficulty=2, points=20,
        hints=["mqtt.Client, connect, publish, on_connect, on_message, loop_forever/start, tls_set"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "publisher" in r
                    and "subscriber" in r
                    and "callbacky" in r
                    and "on_connect" in str(r.get("callbacky", {}))
                    and "loop_metody" in r
                    and "tls_bezpečnost" in r,
                    "Paho klient ✓"
                )
            )(paho_klient()),
        ]
    ),
    Challenge(
        title="Topiky a QoS",
        theory="""MQTT topiky — hierarchická struktura:

  robot/arm/joint1/angle    — konkrétní topik
  Wildcards:
    +  (jednolevelový): robot/+/temperature
    #  (víceúrovňový): robot/#  (vše pod robot/)

  QoS — garancia doručení:
    QoS 0: At most once  — fire & forget
    QoS 1: At least once — PUBACK, možné duplikáty
    QoS 2: Exactly once  — 4-way handshake, nejpomalejší

  Volba: QoS 0 pro telemetrii, QoS 1 pro příkazy,
         QoS 2 jen pro kritické transakce""",
        task="Popiš strukturu MQTT topik, wildcardy + a #, a tři úrovně QoS s příklady použití.",
        difficulty=2, points=20,
        hints=["/ oddělení, + jednolevelový, # víceúrovňový, QoS 0/1/2, PUBACK, PUBREC"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "topiky" in r
                    and "zástupné_znaky" in r
                    and "+" in r.get("zástupné_znaky", {})
                    and "#" in r.get("zástupné_znaky", {})
                    and "qos" in r
                    and "0" in r.get("qos", {})
                    and "1" in r.get("qos", {})
                    and "2" in r.get("qos", {}),
                    "Topiky a QoS ✓"
                )
            )(topiky_a_qos()),
        ]
    ),
    Challenge(
        title="IoT vzory",
        theory="""MQTT pokročilé funkce:

  Retained zpráva:
    publish(topic, msg, retain=True)
    → noví odběratelé ji dostanou okamžitě

  LWT (Last Will and Testament):
    client.will_set('status', 'offline', retain=True)
    → broker pošle automaticky při neočekávaném odpojení

  Clean session:
    True  — zapomene subscribce po odpojení
    False — perzistentní, drží QoS1/2 zprávy

  Bridging: edge broker ↔ cloud broker (AWS IoT)
  Multi-subscribe: client.subscribe([('t1',1),('t2',0)])""",
        task="Popiš retained zprávy, LWT, clean session, multi-subscribe a broker bridging.",
        difficulty=3, points=25,
        hints=["retain=True, will_set, clean_session=False, subscribe seznam, bridge cloud"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "retained_zprávy" in r
                    and isinstance(r["retained_zprávy"].get("použití"), list)
                    and "lwt" in r
                    and "will_set" in str(r.get("lwt", {}))
                    and "clean_session" in r
                    and "bridging" in r,
                    "IoT vzory ✓"
                )
            )(iot_vzory()),
        ]
    ),
    Challenge(
        title="MQTT v robotice",
        theory="""MQTT architektura pro robotiku:

  Topik schéma:
    robot/<id>/cmd/vel       — příkaz rychlosti
    robot/<id>/telemetry/odom — odometrie
    robot/<id>/status        — stav (retained)
    factory/all/cmd/stop     — E-STOP všem

  ROS2 bridge:
    ROS2 subscriber → MQTT publisher
    json.dumps({'x': pos.x, 'y': pos.y})

  Bezpečnost (POVINNÉ v produkci):
    mTLS + ACL — každý robot má certifikát + povolené topiky

  Cloud: AWS IoT Core, Azure IoT Hub, HiveMQ Cloud
  Výkon: QoS 0 pro telemetrii (10 Hz), QoS 1 pro příkazy""",
        task="Navrhni MQTT topik schéma pro robota, ROS2 bridge, bezpečnost a cloud integraci.",
        difficulty=3, points=25,
        hints=["topik schéma, ROS2 bridge, mTLS+ACL, AWS IoT, QoS volba, CBOR/JSON, client_id unikátní"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "topik_schéma_robota" in r
                    and "ros2_mqtt_bridge" in r
                    and "bezpečnost" in r
                    and "tls" in str(r.get("bezpečnost", {}))
                    and "cloud_integrace" in r
                    and "výkon_a_optimalizace" in r,
                    "MQTT v robotice ✓"
                )
            )(mqtt_v_robotice()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "MQTT", "12_05")
