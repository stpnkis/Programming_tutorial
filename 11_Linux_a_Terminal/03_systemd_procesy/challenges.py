#!/usr/bin/env python3
"""⚙️ Systemd & Procesy — ps, top, kill, systemctl, journalctl, cron."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def procesy_ps_top():
    """
    🎯 VÝZVA 1: Správa procesů — ps, top, htop.
    Vrať dict:
    {
        "ps": {
            "všechny_procesy": "ps aux",
            "strom_procesů": "ps axjf nebo pstree",
            "hledej_proces": "ps aux | grep python",
            "sloupce_aux": ["USER", "PID", "%CPU", "%MEM", "VSZ", "RSS", "TTY", "STAT", "START", "TIME", "COMMAND"]
        },
        "top": {
            "spuštění": "top",
            "klávesy": {
                "q": "quit",
                "k": "kill proces (zadej PID)",
                "r": "renice (změna priority)",
                "M": "seřaď dle RAM",
                "P": "seřaď dle CPU",
                "1": "zobraz jednotlivá CPU jádra"
            },
            "load_average": "průměrná zátěž za 1, 5, 15 minut"
        },
        "htop": {
            "instalace": "sudo apt install htop",
            "výhody": ["barevné UI", "myš", "F9=kill, F7/F8=priorita", "procesy jako strom"],
            "alternativy": ["btop", "glances", "nmon"]
        },
        "pgrep_pkill": {
            "pgrep": "pgrep python  # najde PID dle jména",
            "pkill": "pkill -f 'skript.py'  # ukončí dle jména/patternu"
        }
    }
    """
    # TODO: ↓
    pass


def signaly_a_kill():
    """
    🎯 VÝZVA 2: Signály a příkaz kill.
    Vrať dict:
    {
        "signály": {
            "SIGTERM (15)": "žádost o ukončení (výchozí kill) — lze zachytit",
            "SIGKILL (9)": "okamžité ukončení — NELZE zachytit ani ignorovat",
            "SIGINT (2)": "přerušení z klávesnice (Ctrl+C)",
            "SIGQUIT (3)": "quit s core dump (Ctrl+\\)",
            "SIGHUP (1)": "zavěšení; služby jej používají pro reload konfigurace",
            "SIGSTOP (19)": "pauza procesu — NELZE zachytit",
            "SIGCONT (18)": "obnovení zastaveného procesu"
        },
        "kill": {
            "výchozí": "kill PID  # pošle SIGTERM",
            "vynucené": "kill -9 PID  # pošle SIGKILL",
            "dle_jména": "killall python3  # ukončí všechny python3 procesy",
            "pattern": "pkill -f 'muj_skript.py'"
        },
        "pozadí_a_popředí": {
            "na_pozadí": "příkaz &  # spustí na pozadí",
            "seznam_úloh": "jobs  # zobrazí procesy na pozadí",
            "do_popředí": "fg %1  # přenese úlohu 1 do popředí",
            "zpět_na_pozadí": "Ctrl+Z pak bg %1",
            "nohup": "nohup příkaz &  # nevypne se při odhlášení"
        },
        "nice_a_priorita": {
            "nice": "nice -n 10 příkaz  # spustí s nižší prioritou (10)",
            "renice": "renice -n -5 -p PID  # změní prioritu běžícího procesu",
            "rozsah": "-20 (nejvyšší) až 19 (nejnižší), výchozí 0"
        }
    }
    """
    # TODO: ↓
    pass


def systemd_a_sluzby():
    """
    🎯 VÝZVA 3: Systemd a správa služeb.
    Vrať dict:
    {
        "systemctl": {
            "start": "sudo systemctl start nginx",
            "stop": "sudo systemctl stop nginx",
            "restart": "sudo systemctl restart nginx",
            "reload": "sudo systemctl reload nginx  # bez výpadku (SIGHUP)",
            "status": "systemctl status nginx",
            "enable": "sudo systemctl enable nginx  # spustí po startu systému",
            "disable": "sudo systemctl disable nginx",
            "list_units": "systemctl list-units --type=service --state=running",
            "daemon_reload": "sudo systemctl daemon-reload  # po změně unit souboru"
        },
        "unit_soubor": {
            "umístění": "/etc/systemd/system/moje-sluzba.service",
            "základní_obsah": [
                "[Unit]",
                "Description=Moje aplikace",
                "After=network.target",
                "",
                "[Service]",
                "Type=simple",
                "User=robolab",
                "WorkingDirectory=/opt/moje-app",
                "ExecStart=/usr/bin/python3 /opt/moje-app/main.py",
                "Restart=on-failure",
                "RestartSec=5",
                "",
                "[Install]",
                "WantedBy=multi-user.target"
            ]
        },
        "typy_startů": {
            "simple": "hlavní proces = ExecStart (výchozí)",
            "forking": "fork do pozadí (daemony staré generace)",
            "oneshot": "jednorázový příkaz, systemd čeká na dokončení",
            "notify": "proces pošle sd_notify() = připraven"
        }
    }
    """
    # TODO: ↓
    pass


def journalctl_logy():
    """
    🎯 VÝZVA 4: Journalctl a správa logů.
    Vrať dict:
    {
        "journalctl": {
            "vše": "journalctl  # všechny záznamy (od nejstarších)",
            "od_konce": "journalctl -e  # skočí na konec",
            "sledování": "journalctl -f  # jako tail -f",
            "pro_službu": "journalctl -u nginx.service",
            "od_rebootu": "journalctl -b  # od posledního startu",
            "časový_rozsah": "journalctl --since '2026-01-01' --until '2026-01-02'",
            "priority": "journalctl -p err  # jen chyby a horší",
            "bez_stránkování": "journalctl --no-pager | grep ERROR"
        },
        "priority_syslog": {
            "0 emerg": "systém nelze použít",
            "1 alert": "nutný okamžitý zásah",
            "2 crit": "kritický stav",
            "3 err": "chybový stav",
            "4 warning": "varování",
            "5 notice": "normální, ale důležité",
            "6 info": "informační",
            "7 debug": "ladící zprávy"
        },
        "syslog_soubory": {
            "/var/log/syslog": "obecné systémové logy",
            "/var/log/auth.log": "autentizace a autorizace",
            "/var/log/kern.log": "zprávy jádra",
            "/var/log/apt/": "logy správce balíčků"
        },
        "logrotate": "automatická rotace logů (komprimace, mazání starých)"
    }
    """
    # TODO: ↓
    pass


def cron_a_planovani():
    """
    🎯 VÝZVA 5: Cron a plánování úloh.
    Vrať dict:
    {
        "crontab": {
            "editace": "crontab -e  # edituj crontab aktuálního uživatele",
            "seznam": "crontab -l  # zobraz crontab",
            "smazat": "crontab -r  # smaž crontab",
            "pro_uživatele": "sudo crontab -u www-data -e"
        },
        "formát_záznamu": {
            "struktura": "MINUTA HODINA DEN_MĚSÍCE MĚSÍC DEN_TÝDNE PŘÍKAZ",
            "příklady": {
                "každou_minutu": "* * * * * /skript.sh",
                "každou_hodinu": "0 * * * * /skript.sh",
                "každý_den_ve_3": "0 3 * * * /skript.sh",
                "každé_pondělí": "0 9 * * 1 /skript.sh",
                "každých_5_minut": "*/5 * * * * /skript.sh",
                "1._každého_měsíce": "0 0 1 * * /skript.sh"
            },
            "speciální": {
                "@reboot": "po každém startu systému",
                "@daily": "jednou denně (= 0 0 * * *)",
                "@weekly": "jednou týdně",
                "@monthly": "jednou měsíčně"
            }
        },
        "systemd_timers": {
            "výhody_oproti_cron": ["logování přes journald", "závislosti", "catch-up po výpadku"],
            "list": "systemctl list-timers --all",
            "příklad_timer": [
                "[Timer]",
                "OnCalendar=daily",
                "Persistent=true"
            ]
        },
        "at": "at now + 1 hour <<< '/skript.sh'  # jednorázové naplánování"
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Procesy — ps, top, htop",
        theory="""Správa procesů v Linuxu:

  ps aux      — vypíše všechny běžící procesy
  ps axjf     — strom procesů
  top / htop  — interaktivní monitor (q=exit, k=kill, M=RAM, P=CPU)

  PID — unikátní identifikátor procesu
  PPID — parent PID
  Load average: průměrná zátěž za 1/5/15 min""",
        task="Popiš příkazy pro zobrazení procesů (ps, top, htop) a klíčové informace.",
        difficulty=1, points=15,
        hints=["ps aux, ps axjf, top klávesy, htop, pgrep, pkill"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "ps" in r
                    and "všechny_procesy" in r.get("ps", {})
                    and "top" in r
                    and "klávesy" in r.get("top", {})
                    and "htop" in r,
                    "Procesy ✓"
                )
            )(procesy_ps_top()),
        ]
    ),
    Challenge(
        title="Signály a kill",
        theory="""Signály = způsob komunikace s procesy:

  SIGTERM (15) — zdvořilá žádost o ukončení (zachytitelný)
  SIGKILL (9)  — okamžité zabití (nezachytitelný!)
  SIGINT (2)   — Ctrl+C
  SIGHUP (1)   — reload konfigurace

  kill PID     — pošle SIGTERM
  kill -9 PID  — pošle SIGKILL (poslední záchrana)
  killall / pkill — dle jména procesu""",
        task="Popiš Unix signály, příkaz kill a práci s procesy na pozadí (bg/fg/nohup).",
        difficulty=2, points=20,
        hints=["SIGTERM vs SIGKILL, kill -9, jobs, fg, bg, nohup, nice, renice"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "signály" in r
                    and "SIGKILL (9)" in r.get("signály", {})
                    and "kill" in r
                    and "pozadí_a_popředí" in r
                    and "nice_a_priorita" in r,
                    "Signály a kill ✓"
                )
            )(signaly_a_kill()),
        ]
    ),
    Challenge(
        title="Systemd a služby",
        theory="""systemd — init systém #1 na Linuxu (PID 1)

  systemctl start/stop/restart/status SLUŽBA
  systemctl enable/disable  — autostart po bootu
  systemctl daemon-reload   — po změně unit souboru

  Unit soubor (.service):
  [Unit] Description, After=
  [Service] ExecStart=, Restart=, User=
  [Install] WantedBy=multi-user.target""",
        task="Popiš správu systemd služeb (systemctl) a strukturu .service unit souboru.",
        difficulty=2, points=20,
        hints=["start/stop/restart/reload/status/enable/disable, unit soubor [Unit][Service][Install]"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "systemctl" in r
                    and "daemon_reload" in r.get("systemctl", {})
                    and "unit_soubor" in r
                    and "základní_obsah" in r.get("unit_soubor", {}),
                    "Systemd ✓"
                )
            )(systemd_a_sluzby()),
        ]
    ),
    Challenge(
        title="Journalctl a logy",
        theory="""journalctl — čtení systemd journalu:

  journalctl -f          — sleduj živé logy
  journalctl -u nginx    — logy konkrétní služby
  journalctl -b          — od posledního bootu
  journalctl -p err      — jen chyby (priority 0-7)
  journalctl --since '1 hour ago'

  Syslog priority: 0=emerg, 3=err, 6=info, 7=debug""",
        task="Popiš příkaz journalctl, syslog priority a klíčové soubory v /var/log/.",
        difficulty=2, points=20,
        hints=["journalctl -f/-u/-b/-p/-e, --since/--until, priority 0-7, /var/log/"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "journalctl" in r
                    and "sledování" in r.get("journalctl", {})
                    and "priority_syslog" in r
                    and "syslog_soubory" in r,
                    "Journalctl ✓"
                )
            )(journalctl_logy()),
        ]
    ),
    Challenge(
        title="Cron a plánování",
        theory="""cron — démon pro plánování opakujících se úloh

  Formát záznamu: MIN HOD DEN_M MĚSÍC DEN_T PŘÍKAZ
  * = libovolná hodnota, */5 = každých 5

  Příklady:
  0 3 * * *   = každý den ve 3:00
  */5 * * * * = každých 5 minut
  0 9 * * 1   = každé pondělí v 9:00

  @reboot, @daily, @weekly — zkratky""",
        task="Popiš formát crontab záznamu, editaci crontabu a systemd timers jako moderní alternativu.",
        difficulty=2, points=20,
        hints=["crontab -e/-l, MIN HOD DEN_M MES DEN_T, */5, @reboot, @daily, systemd timers"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "crontab" in r
                    and "editace" in r.get("crontab", {})
                    and "formát_záznamu" in r
                    and "příklady" in r.get("formát_záznamu", {})
                    and "systemd_timers" in r,
                    "Cron ✓"
                )
            )(cron_a_planovani()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Systemd & Procesy", "11_03")
