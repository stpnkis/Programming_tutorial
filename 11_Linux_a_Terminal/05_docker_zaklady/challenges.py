#!/usr/bin/env python3
"""🐳 Docker Základy — Dockerfile, build, run, compose, volumes, networking."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def docker_koncepty():
    """
    🎯 VÝZVA 1: Klíčové koncepty Dockeru.
    Vrať dict:
    {
        "co_je_docker": "platforma pro kontejnerizaci aplikací — balíček kódu + závislostí + prostředí",
        "kontejner_vs_vm": {
            "kontejner": "sdílí jádro OS hostitele, start v ms, MB",
            "VM": "vlastní OS, start v minutách, GB",
            "výhoda_kontejneru": "rychlost, efektivita zdrojů, přenositelnost"
        },
        "klíčové_pojmy": {
            "image": "šablona (read-only) — blueprint kontejneru",
            "kontejner": "běžící instance image",
            "Dockerfile": "instrukce pro sestavení image",
            "registry": "úložiště imagí (Docker Hub, GHCR, ECR)",
            "layer": "každá instrukce Dockerfile = vrstva (cache!)",
            "tag": "verze image (nginx:1.25, python:3.12-slim)"
        },
        "docker_cli": {
            "verze": "docker --version",
            "info": "docker info  # statistiky a konfigurace",
            "pull": "docker pull nginx:latest  # stáhni image",
            "images": "docker images  # seznam lokálních imagí",
            "ps": "docker ps  # běžící kontejnery",
            "ps_all": "docker ps -a  # všechny kontejnery",
            "rm_image": "docker rmi nginx:latest",
            "system_prune": "docker system prune -af  # vyčisti vše nepoužívané"
        }
    }
    """
    # TODO: ↓
    pass


def dockerfile():
    """
    🎯 VÝZVA 2: Psaní Dockerfile.
    Vrať dict:
    {
        "instrukce": {
            "FROM": "FROM python:3.12-slim  # základní image",
            "WORKDIR": "WORKDIR /app  # pracovní adresář",
            "COPY": "COPY requirements.txt .  # zkopíruj soubory",
            "ADD": "ADD archiv.tar.gz /app/  # kopíruj a rozbal",
            "RUN": "RUN pip install -r requirements.txt  # příkaz při buildu",
            "ENV": "ENV PYTHONDONTWRITEBYTECODE=1  # proměnná prostředí",
            "EXPOSE": "EXPOSE 8080  # dokumentační! neotevírá port",
            "CMD": "CMD ['python', 'app.py']  # výchozí příkaz při startu",
            "ENTRYPOINT": "ENTRYPOINT ['gunicorn']  # pevný příkaz, CMD = argumenty",
            "USER": "USER nobody  # spusť jako neprivilegiovaný uživatel",
            "ARG": "ARG VERSION=latest  # build-time argument",
            "VOLUME": "VOLUME /data  # bod pro připojení volume",
            "LABEL": "LABEL maintainer='Karel <karel@example.com>'"
        },
        "příklad_python_app": [
            "FROM python:3.12-slim",
            "",
            "WORKDIR /app",
            "",
            "# Závislosti zvlášť pro lepší cache",
            "COPY requirements.txt .",
            "RUN pip install --no-cache-dir -r requirements.txt",
            "",
            "COPY . .",
            "",
            "ENV PYTHONDONTWRITEBYTECODE=1 \\",
            "    PYTHONUNBUFFERED=1",
            "",
            "USER nobody",
            "EXPOSE 8000",
            "CMD [\"python\", \"-m\", \"uvicorn\", \"app:app\", \"--host\", \"0.0.0.0\"]"
        ],
        "best_practices": [
            "používej slim/alpine base image (menší útočná plocha)",
            "závislosti COPY+RUN dříve než kód (lepší využití cache)",
            "nespouštěj jako root — USER nobody",
            "použij .dockerignore (jako .gitignore)",
            "jeden proces na kontejner",
            "immutable kontejnery — konfigurace přes ENV a volumes"
        ],
        "dockerignore": [
            ".git/",
            "__pycache__/",
            "*.pyc",
            ".env",
            "node_modules/"
        ]
    }
    """
    # TODO: ↓
    pass


def docker_run_a_sprava():
    """
    🎯 VÝZVA 3: Spouštění a správa kontejnerů.
    Vrať dict:
    {
        "docker_build": {
            "základní": "docker build -t moje-app:1.0 .",
            "bez_cache": "docker build --no-cache -t moje-app .",
            "s_arg": "docker build --build-arg VERSION=2.0 -t moje-app .",
            "jiný_dockerfile": "docker build -f Dockerfile.prod -t moje-app:prod ."
        },
        "docker_run": {
            "základní": "docker run nginx",
            "na_pozadí": "docker run -d nginx  # detached",
            "s_portem": "docker run -d -p 8080:80 nginx  # hostPort:containerPort",
            "s_env": "docker run -e DATABASE_URL=postgresql://... moje-app",
            "s_volume": "docker run -v /host/data:/app/data moje-app",
            "odstranit_po_skončení": "docker run --rm ubuntu echo ahoj",
            "interaktivní": "docker run -it ubuntu bash  # -i stdin, -t terminal",
            "s_názvem": "docker run -d --name muj-nginx nginx",
            "restart_policy": "docker run -d --restart unless-stopped nginx"
        },
        "správa_kontejnerů": {
            "stop": "docker stop muj-nginx  # SIGTERM → SIGKILL po 10s",
            "start": "docker start muj-nginx",
            "restart": "docker restart muj-nginx",
            "smaž": "docker rm muj-nginx",
            "smaž_running": "docker rm -f muj-nginx",
            "logy": "docker logs -f muj-nginx  # jako tail -f",
            "exec": "docker exec -it muj-nginx bash  # vstup do běžícího",
            "inspect": "docker inspect muj-nginx  # detailní JSON info",
            "stats": "docker stats  # live CPU/RAM/sítě"
        }
    }
    """
    # TODO: ↓
    pass


def docker_compose():
    """
    🎯 VÝZVA 4: Docker Compose — orchestrace více kontejnerů.
    Vrať dict:
    {
        "co_je": "nástroj pro definici a spuštění multi-kontejnerových aplikací v jednom YAML souboru",
        "příkazy": {
            "start": "docker compose up -d  # start na pozadí",
            "stop": "docker compose down  # stop + smaž kontejnery",
            "build": "docker compose build  # sestaví image",
            "logy": "docker compose logs -f service_name",
            "exec": "docker compose exec web bash",
            "ps": "docker compose ps",
            "restart": "docker compose restart web"
        },
        "příklad_compose": [
            "version: '3.9'",
            "",
            "services:",
            "  web:",
            "    build: .",
            "    ports:",
            "      - '8000:8000'",
            "    environment:",
            "      - DATABASE_URL=postgresql://user:pass@db:5432/mydb",
            "    volumes:",
            "      - ./app:/app",
            "    depends_on:",
            "      db:",
            "        condition: service_healthy",
            "    restart: unless-stopped",
            "",
            "  db:",
            "    image: postgres:15-alpine",
            "    environment:",
            "      POSTGRES_USER: user",
            "      POSTGRES_PASSWORD: pass",
            "      POSTGRES_DB: mydb",
            "    volumes:",
            "      - postgres_data:/var/lib/postgresql/data",
            "    healthcheck:",
            "      test: ['CMD-SHELL', 'pg_isready -U user']",
            "      interval: 5s",
            "      timeout: 5s",
            "      retries: 5",
            "",
            "volumes:",
            "  postgres_data:"
        ],
        "klíčové_vlastnosti": {
            "depends_on": "pořadí spouštění + healthcheck čekání",
            "volumes": "pojmenované volumes = persistentní data",
            "networks": "izolovaná síť mezi službami (dns dle jména služby)",
            "env_file": ".env soubor pro citlivé proměnné"
        }
    }
    """
    # TODO: ↓
    pass


def volumes_a_networking():
    """
    🎯 VÝZVA 5: Volumes a Docker networking.
    Vrať dict:
    {
        "volumes": {
            "typy": {
                "bind_mount": "-v /host/cesta:/container/cesta  # přímé mapování",
                "named_volume": "-v muj_volume:/container/cesta  # spravuje Docker",
                "tmpfs": "--tmpfs /tmp  # v paměti, zanikne se kontejnerem"
            },
            "správa": {
                "vytvoř": "docker volume create muj_volume",
                "seznam": "docker volume ls",
                "inspect": "docker volume inspect muj_volume",
                "smaž": "docker volume rm muj_volume",
                "prune": "docker volume prune  # smaž nepoužívané"
            },
            "kdy_co": {
                "bind_mount": "vývoj — kód se ihned projeví v kontejneru",
                "named_volume": "produkce — data perzistují, spravuje Docker"
            }
        },
        "networking": {
            "výchozí_bridge": "docker run = připojí se k bridge síti (NAT)",
            "custom_network": {
                "vytvoř": "docker network create moje-sit",
                "použití": "docker run --network moje-sit moje-app",
                "výhoda": "kontejnery se navzájem vidí dle jména (DNS)"
            },
            "módy": {
                "bridge": "výchozí, izolovaná virtuální síť s NAT (výchozí)",
                "host": "--network host  # sdílí síť s hostem (Linux only)",
                "none": "--network none  # bez sítě",
                "overlay": "Swarm — komunikace přes více Docker hostů"
            },
            "správa": {
                "seznam": "docker network ls",
                "inspect": "docker network inspect moje-sit",
                "prune": "docker network prune"
            },
            "publish_vs_expose": {
                "EXPOSE": "jen dokumentace v Dockerfile, neotevírá port",
                "-p host:container": "skutečně mapuje port na host",
                "-P": "automaticky mapuje všechny EXPOSE porty na náhodné porty hostu"
            }
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
        title="Docker koncepty",
        theory="""Docker — kontejnerizace aplikací:

  Image   — read-only šablona (layers)
  Kontejner — běžící instance image
  Dockerfile — instrukce pro sestavení image
  Registry — úložiště imagí (Docker Hub)

  Kontejner ≠ VM:
  - sdílí OS jádro hostitele
  - start v milisekundách, MB místo GB
  - přenositelný (funguje všude kde je Docker)""",
        task="Popiš klíčové koncepty Dockeru — image, kontejner, layer, registry, a rozdíl oproti VM.",
        difficulty=1, points=15,
        hints=["image vs kontejner vs VM, layer, registry, docker ps/images/pull/rmi"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "klíčové_pojmy" in r
                    and "image" in r.get("klíčové_pojmy", {})
                    and "kontejner_vs_vm" in r
                    and "docker_cli" in r
                    and "ps_all" in r.get("docker_cli", {}),
                    "Docker koncepty ✓"
                )
            )(docker_koncepty()),
        ]
    ),
    Challenge(
        title="Dockerfile",
        theory="""Dockerfile — recept pro sestavení image:

  FROM    — základní image (začni od slim/alpine)
  WORKDIR — pracovní adresář v kontejneru
  COPY    — kopíruj soubory do image
  RUN     — spusť příkaz při buildu (vytvoří vrstvu)
  ENV     — proměnná prostředí
  EXPOSE  — jen dokumentace (neotevírá port!)
  CMD     — výchozí příkaz při spuštění
  USER    — spusť jako neprivilegovaný uživatel

  Tip: závislosti COPY+RUN před kódem → lepší cache""",
        task="Napiš Dockerfile pro Python aplikaci a vysvětli klíčové instrukce a best practices.",
        difficulty=2, points=20,
        hints=["FROM slim, WORKDIR, COPY requirements.txt, RUN pip, ENV, USER nobody, CMD, .dockerignore"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "instrukce" in r
                    and "CMD" in r.get("instrukce", {})
                    and "USER" in r.get("instrukce", {})
                    and "příklad_python_app" in r
                    and isinstance(r.get("best_practices"), list)
                    and len(r["best_practices"]) >= 3,
                    "Dockerfile ✓"
                )
            )(dockerfile()),
        ]
    ),
    Challenge(
        title="docker run a správa kontejnerů",
        theory="""Spuštění a správa kontejnerů:

  docker build -t app:1.0 .
  docker run -d -p 8080:80 --name web nginx
    -d  na pozadí
    -p  mapuj port host:container
    -e  env proměnná
    -v  volume
    --rm  smaž po skončení
    -it  interaktivní terminál

  docker logs -f, docker exec -it, docker stats
  docker stop/start/restart/rm""",
        task="Popiš docker build a docker run s klíčovými přepínači. Popiš správu běžících kontejnerů.",
        difficulty=2, points=20,
        hints=["docker build -t --no-cache, run -d -p -e -v --rm -it --restart, logs stop exec inspect"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "docker_build" in r
                    and "docker_run" in r
                    and "na_pozadí" in r.get("docker_run", {})
                    and "s_volume" in r.get("docker_run", {})
                    and "správa_kontejnerů" in r
                    and "exec" in r.get("správa_kontejnerů", {}),
                    "docker run ✓"
                )
            )(docker_run_a_sprava()),
        ]
    ),
    Challenge(
        title="Docker Compose",
        theory="""Docker Compose — multi-kontejnerové aplikace v jednom YAML:

  docker compose up -d    — start
  docker compose down     — stop + cleanup
  docker compose logs -f  — logy
  docker compose exec web bash

  docker-compose.yml:
  services: web, db
  volumes: pojmenované
  depends_on: pořadí + healthcheck
  networks: automatická DNS dle názvu služby""",
        task="Popiš Docker Compose — příkazy, strukturu YAML souboru a klíčové vlastnosti (depends_on, healthcheck, volumes).",
        difficulty=2, points=20,
        hints=["compose up/down/build/logs/exec/ps, services/volumes/networks, depends_on, healthcheck"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "příkazy" in r
                    and "start" in r.get("příkazy", {})
                    and "příklad_compose" in r
                    and isinstance(r["příklad_compose"], list)
                    and len(r["příklad_compose"]) >= 10
                    and "klíčové_vlastnosti" in r,
                    "Docker Compose ✓"
                )
            )(docker_compose()),
        ]
    ),
    Challenge(
        title="Volumes a Docker networking",
        theory="""Persistentní data a izolace sítě:

  Volumes:
  - bind mount: -v /host:/container (vývoj)
  - named volume: -v data:/container (produkce)
  - tmpfs: v paměti, dočasné

  Networking:
  - bridge (výchozí) — NAT, izolace
  - host — sdílí síť s hostem
  - custom network — DNS dle jména služby
  EXPOSE ≠ -p (EXPOSE jen dokumentace!)""",
        task="Popiš typy Docker volumes (bind/named/tmpfs) a síťové módy (bridge/host/custom).",
        difficulty=3, points=25,
        hints=["bind mount vs named volume, docker volume ls/create/prune, bridge/host, custom network DNS, EXPOSE vs -p"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "volumes" in r
                    and "typy" in r.get("volumes", {})
                    and "named_volume" in r["volumes"]["typy"]
                    and "networking" in r
                    and "custom_network" in r.get("networking", {})
                    and "publish_vs_expose" in r.get("networking", {}),
                    "Volumes a networking ✓"
                )
            )(volumes_a_networking()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Docker Základy", "11_05")
