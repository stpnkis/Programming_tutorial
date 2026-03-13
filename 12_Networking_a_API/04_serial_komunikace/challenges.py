#!/usr/bin/env python3
"""🔌 Sériová komunikace — pyserial, baudrate, protokoly, Arduino, RS-232/485."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def serial_zaklady():
    """
    🎯 VÝZVA 1: Sériová komunikace — základní pojmy.
    Vrať dict:
    {
        "uart": {
            "definice": "Universal Asynchronous Receiver/Transmitter — nejběžnější serial protokol",
            "signály": {
                "TX": "Transmit — datový výstup",
                "RX": "Receive — datový vstup",
                "GND": "společná zem (povinná!)",
                "CTS/RTS": "hardwarové řízení toku (volitelné)"
            },
            "křížení": "TX jednoho zařízení → RX druhého (crossed connection)"
        },
        "baudrate": {
            "definice": "počet symbolů za sekundu (baud = bit/s pro binární signál)",
            "standardní_hodnoty": [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 921600],
            "doporučení": "9600 pro pomalá zařízení, 115200 pro rychlejší přenos, musí souhlasit na obou stranách"
        },
        "parametry_rámce": {
            "formát": "START_BIT + DATA_BITS + PARITY + STOP_BITS",
            "nejčastější": "8N1 = 8 datových bitů, žádná parita, 1 stop bit",
            "parita": {
                "None": "bez parity (N)",
                "Even": "sudá parita (E)",
                "Odd":  "lichá parita (O)"
            }
        },
        "standardy": {
            "RS-232": "point-to-point, ±3V–±15V, PC COM port, max ~15m",
            "RS-485": "multi-drop sběrnice, diferenciální, až 32 zařízení, 1200m, průmysl",
            "TTL":    "0V/3.3V nebo 0V/5V, mikrokontroléry (Arduino, ESP32, RPi)",
            "USB-serial": "USB ↔ UART převodník (CP2102, CH340, FT232), vytvoří /dev/ttyUSB*"
        }
    }
    """
    # TODO: ↓
    pass


def pyserial_api():
    """
    🎯 VÝZVA 2: pyserial — API a práce s portem.
    Vrať dict:
    {
        "instalace": "pip install pyserial",
        "otevření_portu": {
            "kód": "import serial\\n\\nser = serial.Serial(\\n    port='/dev/ttyUSB0',  # Linux: /dev/ttyUSB0, Windows: 'COM3'\\n    baudrate=115200,\\n    bytesize=serial.EIGHTBITS,\\n    parity=serial.PARITY_NONE,\\n    stopbits=serial.STOPBITS_ONE,\\n    timeout=1.0  # čtecí timeout v sekundách\\n)",
            "seznam_portů": "python -m serial.tools.list_ports  # nebo: serial.tools.list_ports.comports()"
        },
        "zápis": {
            "string":  "ser.write(b'Hello\\r\\n')              # bytes",
            "bytes":   "ser.write(bytes([0x01, 0xFF, 0xA0]))",
            "encode":  "ser.write('příkaz\\n'.encode('utf-8'))"
        },
        "čtení": {
            "jeden_byte":   "byte = ser.read(1)",
            "N_bytů":       "data = ser.read(100)  # čeká na timeout nebo N bytů",
            "řádek":        "line = ser.readline()           # čte do \\n",
            "vše_dostupné": "data = ser.read(ser.in_waiting) # přečti vše v bufferu"
        },
        "správa_spojení": {
            "zavřít":   "ser.close()",
            "with":     "with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:\\n    ...",
            "is_open":  "ser.is_open  # bool",
            "flush":    "ser.flush()   # počkej na odeslání všech dat"
        },
        "kódování": {
            "decode":   "text = data.decode('utf-8').strip()",
            "pozn":     "sériová data jsou vždy bytes — vždy explicitně encode/decode"
        }
    }
    """
    # TODO: ↓
    pass


def protokoly():
    """
    🎯 VÝZVA 3: Komunikační protokoly přes serial.
    Vrať dict:
    {
        "textový_protokol": {
            "popis": "příkazy jako ASCII text, každý ukončen \\n nebo \\r\\n",
            "příklad_příkazů": ["SPEED 1.5\\n", "READ_SENSOR\\n", "STATUS?\\n"],
            "výhody":  ["čitelný lidský debug", "snadný vývoj"],
            "nevýhody": ["pomalý parsování", "neefektivní pro binární data"]
        },
        "binární_protokol": {
            "struktura": "[MAGIC][CMD][LEN][DATA...][CHECKSUM]",
            "magic_byte": "fixní start sekvence pro synchronizaci, např. 0xAA 0x55",
            "příklad_python": "import struct\\npkt = struct.pack('<BHf', 0xAA, cmd, value)  # LE: uint8, uint16, float",
            "výhody": ["kompaktní", "rychlý", "přesný přenos čísel"],
            "nevýhody": ["složitý debug", "nutná dokumentace"]
        },
        "checksum": {
            "XOR":  "xor = 0\\nfor b in data: xor ^= b\\n# jednoduché, detekuje lichý počet chyb",
            "CRC8": "crc8 = libscrc.crc8(data)  # pip install libscrc",
            "CRC16": "crc = crc16.crc16xmodem(data)",
            "účel": "detekce přenosových chyb — povinné v průmyslové komunikaci"
        },
        "framing": {
            "problém": "jak oddělit zprávy v proudu bytů",
            "řešení": {
                "delimiter":    "ukončovací znak (\\n, 0x00) — pro textové protokoly",
                "length_prefix": "prvních N bytů = délka zprávy — pro binární",
                "magic_bytes":   "start sekvence + délka — nejrobustnější"
            }
        },
        "modbus_rtu": {
            "popis": "průmyslový protokol nad RS-485, adresování zařízení 1-247",
            "knihovna": "pip install pymodbus",
            "příklad": "from pymodbus.client import ModbusSerialClient\\nclient = ModbusSerialClient('COM1', baudrate=9600)\\nresult = client.read_holding_registers(0, 10, unit=1)"
        }
    }
    """
    # TODO: ↓
    pass


def arduino_komunikace():
    """
    🎯 VÝZVA 4: Komunikace s Arduinem přes pyserial.
    Vrať dict:
    {
        "arduino_serial_setup": {
            "cpp_kód": "void setup() {\\n  Serial.begin(115200);\\n}\\nvoid loop() {\\n  if (Serial.available()) {\\n    String cmd = Serial.readStringUntil('\\\\n');\\n    Serial.println('OK: ' + cmd);\\n  }\\n}"
        },
        "python_komunikace": {
            "kód": "import serial, time\\n\\nser = serial.Serial('/dev/ttyACM0', 115200, timeout=2)\\ntime.sleep(2)  # čekej na reset Arduina po otevření portu!\\n\\ndef send_cmd(cmd):\\n    ser.write((cmd + '\\\\n').encode())\\n    return ser.readline().decode().strip()\\n\\nprint(send_cmd('STATUS'))  # → 'OK: STATUS'"
        },
        "detekce_arduina": {
            "kód": "import serial.tools.list_ports\\nports = serial.tools.list_ports.comports()\\nfor p in ports:\\n    if 'Arduino' in p.description or 'CH340' in p.manufacturer:\\n        print(f'Arduino na {p.device}')"
        },
        "reset_problém": {
            "popis": "otevření sériového portu způsobí RESET Arduina (DTR signál)",
            "řešení": "time.sleep(2) po Serial() před prvním zápisem",
            "zakázání_resetu": "kondenzátor 10µF mezi RST a GND (trvalé) nebo ser.dtr = False"
        },
        "čtení_senzorů": {
            "arduino_cpp": "Serial.print(analogRead(A0)); Serial.print(','); Serial.println(analogRead(A1));",
            "python_parse": "line = ser.readline().decode().strip()\\nvalues = [int(x) for x in line.split(',')]",
            "frekvence": "Arduino pošle každých N ms, Python čte v smyčce nebo vlákně"
        },
        "thread_čtení": {
            "kód": "import threading\\n\\ndef read_loop(ser, data_queue):\\n    while True:\\n        line = ser.readline().decode().strip()\\n        if line: data_queue.put(line)\\n\\nq = queue.Queue()\\nthread = threading.Thread(target=read_loop, args=(ser, q), daemon=True)\\nthread.start()",
            "účel": "neblokující čtení — hlavní vlákno může dělat jinou práci"
        }
    }
    """
    # TODO: ↓
    pass


def ladeni_a_nastroje():
    """
    🎯 VÝZVA 5: Ladění sériové komunikace — nástroje a tipy.
    Vrať dict:
    {
        "terminálové_nástroje": {
            "minicom":  "minicom -b 115200 -D /dev/ttyUSB0   # TUI terminál, q=quit",
            "screen":   "screen /dev/ttyUSB0 115200          # jednodušší alternativa",
            "picocom":  "picocom -b 115200 /dev/ttyUSB0     # lehký, doporučený",
            "cu":       "cu -l /dev/ttyUSB0 -s 115200"
        },
        "monitor_dat": {
            "screen_záznam": "screen -L /dev/ttyUSB0 115200  # zapisuje do screenlog.0",
            "tee":           "python3 serial_logger.py | tee serial_output.log",
            "wireshark":     "wireshark může zachytit sériový port (plugin)"
        },
        "logické_analyzátory": {
            "sigrok/pulseview": "open-source, 8+ kanálů, UART dekodér, dostupný zdarma",
            "saleae":          "komerční, nejlepší SW, 100MHz sample rate",
            "digiview":        "levná čínská alternativa",
            "použití":         "fyzická analýza signálu — detekuj framing chyby, noise, timing"
        },
        "časté_problémy": {
            "žádná_data":          "zkontroluj TX/RX křížení, baudrate, USB kabel (nejen napájení)",
            "špatná_data_rubbish": "nesouhlasí baudrate nebo formát rámce (8N1 vs 7E1)",
            "permission_denied":   "sudo adduser $USER dialout && znovu se přihlas",
            "reset_při_otevření":  "time.sleep(2) po Serial() nebo zakáže DTR",
            "buffer_overflow":     "čti data rychleji nebo nastavit menší frekvenci odesílání"
        },
        "testování_loopback": {
            "hw":     "propoj TX a RX stejného portu — vše co pošleš přijde zpět",
            "python": "ser.write(b'test')\\nassert ser.read(4) == b'test'  # loopback test"
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
        title="Sériová komunikace základy",
        theory="""UART — asynchronní sériová komunikace:

  Signály: TX, RX, GND  (TX jednoho → RX druhého!)
  Baudrate: symboly/s — musí souhlasit na obou stranách
    Běžné: 9600, 115200, 921600

  Formát rámce: 8N1 = 8 bitů, bez parity, 1 stop bit

  Standardy:
    RS-232  — ±15V, point-to-point, PC COM port
    RS-485  — diferenciální, multi-drop, 1200m, průmysl
    TTL     — 0V/3.3V nebo 5V, mikrokontroléry
    USB-serial — převodník → /dev/ttyUSB*""",
        task="Popiš UART signály, baudrate, formát rámce 8N1 a rozdíly RS-232 vs RS-485 vs TTL.",
        difficulty=1, points=15,
        hints=["TX/RX crossover, baudrate=9600/115200, 8N1, RS-232/RS-485/TTL, /dev/ttyUSB0"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "uart" in r
                    and "baudrate" in r
                    and isinstance(r["baudrate"].get("standardní_hodnoty"), list)
                    and "parametry_rámce" in r
                    and "standardy" in r
                    and "RS-485" in str(r.get("standardy", {})),
                    "Serial základy ✓"
                )
            )(serial_zaklady()),
        ]
    ),
    Challenge(
        title="pyserial API",
        theory="""pyserial — Python knihovna pro sériovou komunikaci:

  pip install pyserial

  ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

  Zápis (vždy bytes):
    ser.write(b'cmd\\n')
    ser.write('text'.encode('utf-8'))

  Čtení:
    ser.read(N)           — N bytů
    ser.readline()        — do \\n
    ser.read(ser.in_waiting)  — vše dostupné

  with serial.Serial(...) as ser:   — auto-close
  seznam portů: python -m serial.tools.list_ports""",
        task="Popiš pyserial API: otevření portu, zápis, čtení, správa spojení, kódování.",
        difficulty=2, points=20,
        hints=["Serial('/dev/ttyUSB0', 115200, timeout=1), read/readline/in_waiting, encode/decode, with"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "otevření_portu" in r
                    and "zápis" in r
                    and "čtení" in r
                    and "readline" in str(r.get("čtení", {}))
                    and "správa_spojení" in r
                    and "with" in str(r.get("správa_spojení", {})),
                    "pyserial ✓"
                )
            )(pyserial_api()),
        ]
    ),
    Challenge(
        title="Komunikační protokoly",
        theory="""Vrstvení protokolu nad sériovým portem:

  Textový: 'SPEED 1.5\\n'  — čitelný, snadný debug
  Binární: [MAGIC][CMD][LEN][DATA][CRC]  — kompaktní, přesný

  Framing — jak oddělit zprávy:
    delimiter: \\n pro textové
    length prefix: první 2 byty = délka
    magic bytes: 0xAA 0x55 + délka

  Checksum — detekce chyb:
    XOR  — jednoduché
    CRC8/CRC16  — spolehlivé

  Modbus RTU: průmyslový protokol nad RS-485
    pip install pymodbus""",
        task="Popiš textový vs binární protokol, framing, checksum a Modbus RTU.",
        difficulty=3, points=25,
        hints=["textový/binární, magic bytes, XOR/CRC, struct.pack, Modbus RTU, pymodbus"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "textový_protokol" in r
                    and "binární_protokol" in r
                    and "magic_byte" in str(r.get("binární_protokol", {}))
                    and "checksum" in r
                    and "framing" in r
                    and "modbus_rtu" in r,
                    "Protokoly ✓"
                )
            )(protokoly()),
        ]
    ),
    Challenge(
        title="Komunikace s Arduinem",
        theory="""Python ↔ Arduino přes pyserial:

  Arduino: Serial.begin(115200)
           Serial.readStringUntil('\\n')
           Serial.println("OK")

  Python: ser = serial.Serial('/dev/ttyACM0', 115200)
          time.sleep(2)   ← NUTNÉ! (reset po otevření)
          ser.write(b'cmd\\n')
          line = ser.readline().decode().strip()

  Detekce: serial.tools.list_ports.comports()
  Čtení senzorů: readline() + split(',')
  Neblokující čtení: vlákno + Queue""",
        task="Popiš Python↔Arduino komunikaci: setup, reset problém, čtení senzorů, neblokující vlákno.",
        difficulty=2, points=20,
        hints=["ttyACM0, time.sleep(2), readline, decode, split, threading + Queue, dtr=False"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "arduino_serial_setup" in r
                    and "python_komunikace" in r
                    and "reset_problém" in r
                    and "čtení_senzorů" in r
                    and "thread_čtení" in r,
                    "Arduino komunikace ✓"
                )
            )(arduino_komunikace()),
        ]
    ),
    Challenge(
        title="Ladění a nástroje",
        theory="""Nástroje pro ladění sériové komunikace:

  Terminál:
    minicom -b 115200 -D /dev/ttyUSB0
    picocom -b 115200 /dev/ttyUSB0
    screen /dev/ttyUSB0 115200

  Logický analyzátor: Sigrok/PulseView (zdarma!), Saleae
  Zachycení dat: tee, screen -L

  Časté problémy:
    ❌ Žádná data:          TX/RX křížení, baudrate, kabel
    ❌ Nesmysly:            nesouhlasí baudrate nebo 8N1
    ❌ Permission denied:   sudo adduser $USER dialout
    ❌ Reset při otevření:  time.sleep(2)

  Loopback test: propoj TX→RX — co pošleš, to přijmeš""",
        task="Popiš terminálové nástroje, logické analyzátory, časté problémy a loopback test.",
        difficulty=2, points=20,
        hints=["minicom/picocom/screen, sigrok, dialout skupina, loopback TX→RX, permission denied"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "terminálové_nástroje" in r
                    and "logické_analyzátory" in r
                    and "časté_problémy" in r
                    and "permission_denied" in str(r.get("časté_problémy", {}))
                    and "testování_loopback" in r,
                    "Ladění serial ✓"
                )
            )(ladeni_a_nastroje()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Sériová komunikace", "12_04")
