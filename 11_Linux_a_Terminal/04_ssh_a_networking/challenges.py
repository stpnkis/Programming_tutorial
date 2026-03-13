#!/usr/bin/env python3
"""🔐 SSH & Networking — ssh, scp, rsync, port forwarding, klíče, config."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def ssh_zaklady():
    """
    🎯 VÝZVA 1: SSH — základní připojení a klíče.
    Vrať dict:
    {
        "ssh_připojení": {
            "základní": "ssh uživatel@server.example.com",
            "jiný_port": "ssh -p 2222 uživatel@server.example.com",
            "s_klíčem": "ssh -i ~/.ssh/muj_klic uživatel@server.example.com",
            "příkaz_přímo": "ssh uživatel@server 'ls /opt/app'"
        },
        "generování_klíčů": {
            "ed25519": "ssh-keygen -t ed25519 -C 'popis@stroj'  # doporučeno",
            "rsa": "ssh-keygen -t rsa -b 4096 -C 'popis@stroj'",
            "výsledek": ["~/.ssh/id_ed25519 (privátní)", "~/.ssh/id_ed25519.pub (veřejný)"],
            "NIKDY": "nikdy nesdílej privátní klíč!"
        },
        "nasazení_klíče": {
            "ssh-copy-id": "ssh-copy-id -i ~/.ssh/id_ed25519.pub uživatel@server",
            "manuálně": "cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys",
            "oprávnění": "chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys"
        },
        "ssh_agent": {
            "start": "eval $(ssh-agent)",
            "přidej_klíč": "ssh-add ~/.ssh/id_ed25519",
            "seznam_klíčů": "ssh-add -l",
            "účel": "klíče v paměti = zadáš passphrase jen jednou"
        }
    }
    """
    # TODO: ↓
    pass


def scp_a_rsync():
    """
    🎯 VÝZVA 2: Přenos souborů — scp a rsync.
    Vrať dict:
    {
        "scp": {
            "na_server": "scp soubor.txt uživatel@server:/cíl/cesta/",
            "ze_serveru": "scp uživatel@server:/vzdálená/cesta soubor.txt",
            "složku": "scp -r ./složka/ uživatel@server:/cíl/",
            "jiný_port": "scp -P 2222 soubor.txt uživatel@server:/cíl/",
            "poznámka": "jednoduchý, vhodný pro malé přenosy"
        },
        "rsync": {
            "základní": "rsync -av zdroj/ uživatel@server:/cíl/",
            "přes_ssh": "rsync -avz -e ssh zdroj/ uživatel@server:/cíl/",
            "suchý_běh": "rsync -avzn zdroj/ cíl/  # jen ukáže, co by provedl",
            "smazat_extra": "rsync -avz --delete zdroj/ cíl/  # synchronizace",
            "vyloučení": "rsync -avz --exclude='*.pyc' --exclude='.git/' zdroj/ cíl/",
            "parametry": {
                "-a": "archivní mód (rekurze + zachovej oprávnění/časy)",
                "-v": "verbose",
                "-z": "komprimuj při přenosu",
                "-n": "dry-run (simulace)",
                "--delete": "smaž soubory v cíli, které neexistují ve zdroji",
                "--progress": "ukaž průběh"
            }
        },
        "kdy_co": {
            "scp": "jednorázový přenos jednoho / pár souborů",
            "rsync": "synchronizace složek, zálohy, inkrementální přenosy"
        }
    }
    """
    # TODO: ↓
    pass


def port_forwarding():
    """
    🎯 VÝZVA 3: SSH tunelování a port forwarding.
    Vrať dict:
    {
        "lokální_forwarding": {
            "příkaz": "ssh -L 8080:localhost:80 uživatel@server",
            "princip": "přístup na localhost:8080 = přístup na server:80",
            "příklad_použití": "přistupuj na webserver za firewallem přes ssh tunel",
            "formát": "-L LOKÁLNÍ_PORT:VZDÁLENÝ_HOST:VZDÁLENÝ_PORT"
        },
        "vzdálený_forwarding": {
            "příkaz": "ssh -R 9090:localhost:3000 uživatel@server",
            "princip": "server:9090 se přesměruje na tvůj localhost:3000",
            "příklad_použití": "zpřístupni lokální vývojový server z internetu",
            "formát": "-R VZDÁLENÝ_PORT:LOKÁLNÍ_HOST:LOKÁLNÍ_PORT"
        },
        "dynamický_forwarding": {
            "příkaz": "ssh -D 1080 uživatel@server",
            "princip": "SOCKS5 proxy na localhost:1080 — veškerý provoz přes SSH",
            "použití": "prohlížeč nastavíš na SOCKS proxy localhost:1080"
        },
        "jump_host": {
            "příkaz": "ssh -J bastion_user@bastion.example.com cíl_user@vnitřní.server",
            "config": [
                "Host vnitřní",
                "    HostName 10.0.0.5",
                "    User deploy",
                "    ProxyJump bastion_user@bastion.example.com"
            ],
            "účel": "přístup na server v privátní síti přes prostředníka (bastion)"
        },
        "trvalé_spojení": {
            "příkaz": "ssh -N -f uživatel@server -L 8080:localhost:80",
            "-N": "nepouštěj příkaz (jen tunel)",
            "-f": "přejdi na pozadí"
        }
    }
    """
    # TODO: ↓
    pass


def ssh_config():
    """
    🎯 VÝZVA 4: SSH config soubor a pokročilé nastavení.
    Vrať dict:
    {
        "config_soubor": {
            "umístění": "~/.ssh/config",
            "oprávnění": "chmod 600 ~/.ssh/config",
            "příklad": [
                "# ~/.ssh/config",
                "",
                "Host *",
                "    ServerAliveInterval 60",
                "    ServerAliveCountMax 3",
                "    AddKeysToAgent yes",
                "",
                "Host muj-server",
                "    HostName server.example.com",
                "    User deploy",
                "    Port 2222",
                "    IdentityFile ~/.ssh/id_ed25519",
                "    ForwardAgent yes",
                "",
                "Host bastion",
                "    HostName 1.2.3.4",
                "    User ec2-user",
                "    IdentityFile ~/.ssh/aws_key.pem",
                "",
                "Host interní",
                "    HostName 10.0.0.10",
                "    User ubuntu",
                "    ProxyJump bastion"
            ]
        },
        "sshd_konfigurace": {
            "soubor": "/etc/ssh/sshd_config",
            "doporučené_změny": {
                "PermitRootLogin": "no",
                "PasswordAuthentication": "no",
                "PubkeyAuthentication": "yes",
                "Port": "2222  # nestandardní port",
                "AllowUsers": "deploy ubuntu"
            },
            "reload": "sudo systemctl reload sshd"
        },
        "known_hosts": {
            "soubor": "~/.ssh/known_hosts",
            "účel": "ukládá fingerprints serverů (ochrana před MITM)",
            "smaž_záznam": "ssh-keygen -R server.example.com"
        }
    }
    """
    # TODO: ↓
    pass


def sítové_nástroje():
    """
    🎯 VÝZVA 5: Síťové nástroje pro diagnostiku.
    Vrať dict:
    {
        "ip_a_ifconfig": {
            "ip_addr": "ip addr show  # zobraz síťová rozhraní a IP adresy",
            "ip_route": "ip route show  # směrovací tabulka",
            "ifconfig": "ifconfig  # starší příkaz (balíček net-tools)"
        },
        "ping_a_traceroute": {
            "ping": "ping -c 4 google.com  # otestuj dostupnost hostu",
            "traceroute": "traceroute google.com  # cesta paketu po síti",
            "mtr": "mtr google.com  # kombinace ping + traceroute (live)"
        },
        "porty_a_spojení": {
            "ss": "ss -tlnp  # zobraz naslouchající TCP porty (-u pro UDP)",
            "netstat": "netstat -tlnp  # starší alternativa",
            "lsof": "lsof -i :8080  # kdo naslouchá na portu 8080",
            "parametry_ss": {
                "-t": "TCP",
                "-u": "UDP",
                "-l": "naslouchající",
                "-n": "čísla portů (bez DNS)",
                "-p": "zobraz PID a jméno procesu"
            }
        },
        "dns_a_curl": {
            "nslookup": "nslookup example.com  # DNS dotaz",
            "dig": "dig example.com A  # detailní DNS dotaz",
            "curl": {
                "GET": "curl https://api.example.com/endpoint",
                "POST_json": "curl -X POST -H 'Content-Type: application/json' -d '{\"key\": \"value\"}' URL",
                "uložit_soubor": "curl -o soubor.zip https://example.com/soubor.zip",
                "verbose": "curl -v URL  # zobraz hlavičky"
            },
            "wget": "wget -c URL  # stáhni soubor (-c = pokračuj při přerušení)"
        },
        "firewall": {
            "ufw": {
                "povolení_portu": "sudo ufw allow 22/tcp",
                "blokování": "sudo ufw deny 80",
                "status": "sudo ufw status verbose",
                "enable": "sudo ufw enable"
            },
            "iptables": "iptables -L -v -n  # zobraz pravidla (nízkoúrovňový)"
        }
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="SSH základy a klíče",
        theory="""SSH (Secure Shell) — šifrované vzdálené připojení:

  ssh uživatel@server          — připoj se
  ssh -p 2222 uživatel@server  — jiný port
  ssh -i ~/.ssh/klic user@srv  — konkrétní klíč

  Klíčový pár:
  ssh-keygen -t ed25519  → privátní + veřejný klíč
  ssh-copy-id            → nasaď veřejný klíč na server

  ssh-agent: drží klíče v paměti (passphrase jednou)""",
        task="Popiš SSH připojení, generování klíčů a nasazení veřejného klíče na server.",
        difficulty=1, points=15,
        hints=["ssh user@host -p -i, ssh-keygen -t ed25519, ssh-copy-id, ssh-agent, authorized_keys"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "ssh_připojení" in r
                    and "generování_klíčů" in r
                    and "ed25519" in r.get("generování_klíčů", {})
                    and "nasazení_klíče" in r
                    and "ssh_agent" in r,
                    "SSH základy ✓"
                )
            )(ssh_zaklady()),
        ]
    ),
    Challenge(
        title="scp a rsync",
        theory="""Přenos souborů přes SSH:

  scp — jednoduchý přenos (jako cp přes síť)
    scp soubor.txt user@srv:/cíl/
    scp user@srv:/vzdálený soubor.txt

  rsync — efektivní synchronizace (přenáší jen změny)
    rsync -avz zdroj/ user@srv:/cíl/
    -a archiv, -v verbose, -z komprimuj
    -n dry-run, --delete synchronizace, --exclude""",
        task="Porovnej scp a rsync. Popiš klíčové parametry rsync a kde který použít.",
        difficulty=2, points=20,
        hints=["scp -r -P, rsync -avz -n --delete --exclude --progress, kdy co použít"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "scp" in r
                    and "rsync" in r
                    and "parametry" in r.get("rsync", {})
                    and "--delete" in r["rsync"]["parametry"]
                    and "kdy_co" in r,
                    "scp a rsync ✓"
                )
            )(scp_a_rsync()),
        ]
    ),
    Challenge(
        title="Port forwarding a tunelování",
        theory="""SSH tunneling — bezpečný přenos dat přes SSH:

  Lokální (-L): localhost:8080 → server:80
    ssh -L 8080:localhost:80 user@server

  Vzdálený (-R): server:9090 → tvůj localhost:3000
    ssh -R 9090:localhost:3000 user@server

  Dynamický (-D): SOCKS5 proxy
    ssh -D 1080 user@server

  Jump host (-J): přístupt přes bastion/prostředníka""",
        task="Popiš lokální, vzdálený a dynamický SSH port forwarding a jump host.",
        difficulty=3, points=25,
        hints=["ssh -L loc:host:port, ssh -R, ssh -D SOCKS5, ssh -J bastion, -N -f"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "lokální_forwarding" in r
                    and "vzdálený_forwarding" in r
                    and "dynamický_forwarding" in r
                    and "jump_host" in r,
                    "Port forwarding ✓"
                )
            )(port_forwarding()),
        ]
    ),
    Challenge(
        title="SSH config soubor",
        theory="""~/.ssh/config — ušetří psaní dlouhých příkazů:

  Host alias        → ssh alias  (místo ssh -p 2222 -i klíč user@host)

  Klíčové direktivy:
  HostName, User, Port, IdentityFile
  ProxyJump (přes bastion)
  ForwardAgent (přenos klíčů)
  ServerAliveInterval (keepalive)

  /etc/ssh/sshd_config — serverová konfigurace
  PermitRootLogin no, PasswordAuthentication no""",
        task="Popiš strukturu ~/.ssh/config, doporučenou konfiguraci sshd a known_hosts.",
        difficulty=2, points=20,
        hints=["Host alias, HostName/User/Port/IdentityFile/ProxyJump, sshd_config, known_hosts"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "config_soubor" in r
                    and "příklad" in r.get("config_soubor", {})
                    and "sshd_konfigurace" in r
                    and "known_hosts" in r,
                    "SSH config ✓"
                )
            )(ssh_config()),
        ]
    ),
    Challenge(
        title="Síťové nástroje",
        theory="""Diagnostika sítě v Linuxu:

  ip addr / ip route  — rozhraní, směrování
  ping -c 4 host      — dostupnost
  traceroute / mtr    — cesta paketu

  ss -tlnp       — naslouchající TCP porty
  lsof -i :8080  — kdo drží port

  dig / nslookup — DNS dotazy
  curl -v URL    — HTTP požadavky
  ufw            — jednoduchý firewall""",
        task="Popiš klíčové síťové nástroje Linuxu: ip, ping, ss, dig, curl, ufw.",
        difficulty=2, points=20,
        hints=["ip addr, ss -tlnp, lsof -i, dig, curl -X POST -H, ufw allow"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "ip_a_ifconfig" in r
                    and "porty_a_spojení" in r
                    and "ss" in r.get("porty_a_spojení", {})
                    and "dns_a_curl" in r
                    and "curl" in r.get("dns_a_curl", {})
                    and "firewall" in r,
                    "Síťové nástroje ✓"
                )
            )(sítové_nástroje()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "SSH & Networking", "11_04")
