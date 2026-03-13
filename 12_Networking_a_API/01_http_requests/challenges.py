#!/usr/bin/env python3
"""🌐 HTTP & Requests — GET, POST, hlavičky, JSON, stavové kódy, autentizace, error handling."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def http_zaklady():
    """
    🎯 VÝZVA 1: HTTP protokol — základy.
    Vrať dict popisující HTTP:
    {
        "http_metody": {
            "GET":    "získej zdroj (čtení, bez těla)",
            "POST":   "vytvoř zdroj (odešli data v těle)",
            "PUT":    "nahraď celý zdroj",
            "PATCH":  "uprav část zdroje",
            "DELETE": "smaž zdroj",
            "HEAD":   "jen hlavičky (bez těla odpovědi)",
            "OPTIONS":"zjisti povolené metody"
        },
        "stavové_kódy": {
            "2xx": {
                "200": "OK",
                "201": "Created",
                "204": "No Content"
            },
            "3xx": {
                "301": "Moved Permanently",
                "302": "Found (dočasné přesměrování)",
                "304": "Not Modified (cache)"
            },
            "4xx": {
                "400": "Bad Request",
                "401": "Unauthorized (nutná autentizace)",
                "403": "Forbidden (nemáš právo)",
                "404": "Not Found",
                "429": "Too Many Requests (rate limit)"
            },
            "5xx": {
                "500": "Internal Server Error",
                "502": "Bad Gateway",
                "503": "Service Unavailable"
            }
        },
        "hlavičky": {
            "Content-Type":  "typ těla požadavku/odpovědi, např. application/json",
            "Accept":        "jaké typy odpovědi klient akceptuje",
            "Authorization": "autentizační token, např. Bearer <token>",
            "User-Agent":    "identifikace klienta",
            "Cache-Control": "instrukce pro cache"
        },
        "url_struktura": "schéma://host:port/cesta?query=param&další=hodnota#fragment"
    }
    """
    # TODO: ↓
    pass


def get_requests():
    """
    🎯 VÝZVA 2: GET požadavky s knihovnou requests.
    Vrať dict:
    {
        "instalace": "pip install requests",
        "základní_get": {
            "kód": "import requests\\nr = requests.get('https://api.example.com/data')\\nprint(r.status_code)\\nprint(r.json())",
            "atributy_odpovědi": {
                "r.status_code": "HTTP stavový kód (int)",
                "r.text":        "tělo odpovědi jako string",
                "r.json()":      "tělo odpovědi jako Python dict/list",
                "r.headers":     "hlavičky odpovědi (dict)",
                "r.url":         "výsledná URL po přesměrování",
                "r.elapsed":     "doba trvání požadavku"
            }
        },
        "parametry_url": {
            "kód": "params = {'limit': 10, 'offset': 0}\\nr = requests.get(url, params=params)\\n# vytvoří: url?limit=10&offset=0",
            "použití": "filtrování, stránkování, řazení v REST API"
        },
        "vlastní_hlavičky": {
            "kód": "headers = {'Accept': 'application/json', 'X-API-Key': '...'}\\nr = requests.get(url, headers=headers)"
        },
        "příklady_api": [
            "requests.get('https://api.github.com/users/octocat')",
            "requests.get('https://httpbin.org/get', params={'key': 'val'})",
            "requests.get('https://jsonplaceholder.typicode.com/todos/1')"
        ]
    }
    """
    # TODO: ↓
    pass


def post_a_json():
    """
    🎯 VÝZVA 3: POST požadavky, JSON a formulářová data.
    Vrať dict:
    {
        "post_json": {
            "kód": "import requests\\ndata = {'name': 'robot', 'speed': 1.5}\\nr = requests.post(url, json=data)\\n# automaticky nastaví Content-Type: application/json",
            "pozn": "parametr json= automaticky serializuje dict a nastaví hlavičku"
        },
        "post_formdata": {
            "kód": "r = requests.post(url, data={'username': 'user', 'password': 'pass'})",
            "pozn": "Content-Type: application/x-www-form-urlencoded"
        },
        "post_soubor": {
            "kód": "with open('image.jpg', 'rb') as f:\\n    r = requests.post(url, files={'file': f})",
            "pozn": "Content-Type: multipart/form-data"
        },
        "put_a_patch": {
            "PUT":   "r = requests.put(url + '/1', json={'name': 'nový'})",
            "PATCH": "r = requests.patch(url + '/1', json={'speed': 2.0})"
        },
        "delete": "r = requests.delete(url + '/1')",
        "kontrola_úspěchu": {
            "manuální":    "if r.status_code == 201: ...",
            "výjimka":     "r.raise_for_status()  # vyvolá HTTPError pro 4xx/5xx",
            "bool_check":  "if r.ok: ...  # True pro 200-299"
        }
    }
    """
    # TODO: ↓
    pass


def autentizace_a_sessions():
    """
    🎯 VÝZVA 4: Autentizace a Sessions.
    Vrať dict:
    {
        "basic_auth": {
            "kód": "r = requests.get(url, auth=('uživatel', 'heslo'))",
            "http_hlavička": "Authorization: Basic <base64(user:pass)>"
        },
        "bearer_token": {
            "kód": "headers = {'Authorization': 'Bearer eyJhb...'}\\nr = requests.get(url, headers=headers)",
            "použití": "JWT tokeny, OAuth 2.0 access tokeny"
        },
        "api_key": {
            "v_hlavičce":   "headers = {'X-API-Key': 'muj-tajny-klic'}",
            "v_parametru":  "params = {'api_key': 'muj-tajny-klic'}",
            "varování":     "nikdy nekládej API klíče do zdrojového kódu — použij .env"
        },
        "session": {
            "kód": "s = requests.Session()\\ns.headers.update({'Authorization': 'Bearer ...'})\\ns.get(url + '/endpoint')  # hlavičky se posílají automaticky\\ns.post(url + '/data', json=data)",
            "výhody": [
                "sdílené hlavičky a cookies přes všechny požadavky",
                "opakované použití TCP spojení (Connection: keep-alive)",
                "uchování sezení (login → chráněné stránky)"
            ]
        },
        "env_pro_tajemství": {
            "kód": "import os\\napi_key = os.getenv('API_KEY')  # načti z prostředí",
            "soubor_.env": "API_KEY=muj-tajny-klic",
            "python_dotenv": "from dotenv import load_dotenv; load_dotenv()"
        }
    }
    """
    # TODO: ↓
    pass


def error_handling():
    """
    🎯 VÝZVA 5: Error handling, timeouty a opakování požadavků.
    Vrať dict:
    {
        "timeout": {
            "kód": "r = requests.get(url, timeout=5)       # 5s připojení i čtení\\nr = requests.get(url, timeout=(3, 10))  # (connect_timeout, read_timeout)",
            "pozn": "bez timeoutu může požadavek viset donekonečna — VŽDY nastav timeout"
        },
        "výjimky": {
            "requests.exceptions.Timeout":         "požadavek překročil timeout",
            "requests.exceptions.ConnectionError":  "chyba připojení (DNS, refused...)",
            "requests.exceptions.HTTPError":        "4xx/5xx po r.raise_for_status()",
            "requests.exceptions.RequestException": "základní třída všech requests výjimek"
        },
        "vzor_try_except": {
            "kód": "try:\\n    r = requests.get(url, timeout=5)\\n    r.raise_for_status()\\n    data = r.json()\\nexcept requests.exceptions.Timeout:\\n    print('Timeout!')\\nexcept requests.exceptions.HTTPError as e:\\n    print(f'HTTP chyba: {e.response.status_code}')\\nexcept requests.exceptions.RequestException as e:\\n    print(f'Síťová chyba: {e}')"
        },
        "opakování_retry": {
            "urllib3": "from urllib3.util.retry import Retry\\nfrom requests.adapters import HTTPAdapter\\nretry = Retry(total=3, backoff_factor=1, status_forcelist=[502,503,504])\\ns = requests.Session()\\ns.mount('https://', HTTPAdapter(max_retries=retry))",
            "popis": "automatické opakování při selhání s exponenciálním čekáním"
        },
        "debugging": {
            "verbose": "import logging; logging.basicConfig(level=logging.DEBUG)",
            "curl_ekvivalent": "curl -X GET -H 'Accept: application/json' https://api.example.com/data"
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
        title="HTTP základy",
        theory="""HTTP (HyperText Transfer Protocol) — základ komunikace na webu:

  Metody: GET (čtení), POST (vytvoř), PUT (nahraď), PATCH (uprav), DELETE (smaž)

  Stavové kódy:
    2xx  — úspěch (200 OK, 201 Created, 204 No Content)
    3xx  — přesměrování (301, 302, 304)
    4xx  — chyba klienta (400, 401, 403, 404, 429)
    5xx  — chyba serveru (500, 502, 503)

  Hlavičky: Content-Type, Authorization, Accept, Cache-Control
  URL: schéma://host:port/cesta?query#fragment""",
        task="Popiš HTTP metody, stavové kódy (2xx–5xx) a klíčové hlavičky.",
        difficulty=1, points=15,
        hints=["GET/POST/PUT/PATCH/DELETE, 200/201/404/500, Content-Type, Authorization"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "http_metody" in r
                    and "stavové_kódy" in r
                    and "2xx" in r.get("stavové_kódy", {})
                    and "4xx" in r.get("stavové_kódy", {})
                    and "hlavičky" in r,
                    "HTTP základy ✓"
                )
            )(http_zaklady()),
        ]
    ),
    Challenge(
        title="GET požadavky",
        theory="""requests.get() — stahování dat z API:

  pip install requests

  r = requests.get(url)          # základní GET
  r = requests.get(url, params={'k': 'v'})   # query string
  r = requests.get(url, headers={'Accept': 'application/json'})

  Atributy odpovědi:
    r.status_code  — int (200, 404, ...)
    r.json()       — naparsuje JSON tělo
    r.text         — tělo jako string
    r.headers      — dict hlaviček""",
        task="Popiš GET požadavky s knihovnou requests: params, headers, atributy odpovědi.",
        difficulty=1, points=15,
        hints=["requests.get(url), params={}, headers={}, r.status_code, r.json()"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "základní_get" in r
                    and "atributy_odpovědi" in r.get("základní_get", {})
                    and "parametry_url" in r
                    and isinstance(r.get("příklady_api"), list)
                    and len(r["příklady_api"]) >= 2,
                    "GET požadavky ✓"
                )
            )(get_requests()),
        ]
    ),
    Challenge(
        title="POST a JSON",
        theory="""Odesílání dat na server:

  POST s JSON:
    r = requests.post(url, json=data)
    # automaticky: Content-Type: application/json

  POST s formulárem:
    r = requests.post(url, data={'key': 'val'})

  POST se souborem:
    r = requests.post(url, files={'file': open('f.jpg','rb')})

  Kontrola úspěchu:
    r.raise_for_status()   # HTTPError pro 4xx/5xx
    r.ok                   # True pro 200–299""",
        task="Popiš POST požadavky s JSON, formulářovými daty a soubory. Jak zkontrolovat úspěch?",
        difficulty=2, points=20,
        hints=["json=data, data={}, files={}, raise_for_status(), r.ok, PUT, PATCH, DELETE"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "post_json" in r
                    and "post_formdata" in r
                    and "kontrola_úspěchu" in r
                    and "raise_for_status" in str(r.get("kontrola_úspěchu", {})),
                    "POST a JSON ✓"
                )
            )(post_a_json()),
        ]
    ),
    Challenge(
        title="Autentizace a Sessions",
        theory="""Způsoby autentizace HTTP požadavků:

  Basic Auth:    auth=('user', 'pass')
  Bearer token:  headers={'Authorization': 'Bearer <token>'}
  API Key:       headers={'X-API-Key': '...'} nebo params={'api_key': '...'}

  Session — sdílené hlavičky/cookies:
    s = requests.Session()
    s.headers.update({'Authorization': 'Bearer ...'})
    s.get(url)  # hlavičky posílány automaticky

  Tajemství — NIKDY v kódu:
    api_key = os.getenv('API_KEY')  # z prostředí
    from dotenv import load_dotenv""",
        task="Popiš Basic Auth, Bearer token, API Key, Sessions a bezpečné uchovávání tajemství.",
        difficulty=2, points=20,
        hints=["auth=(), Bearer, X-API-Key, Session(), os.getenv, .env soubor"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "basic_auth" in r
                    and "bearer_token" in r
                    and "session" in r
                    and "výhody" in r.get("session", {})
                    and isinstance(r["session"]["výhody"], list)
                    and "env_pro_tajemství" in r,
                    "Autentizace ✓"
                )
            )(autentizace_a_sessions()),
        ]
    ),
    Challenge(
        title="Error handling a timeouty",
        theory="""Robustní HTTP klient vždy ošetřuje chyby:

  Timeout:
    requests.get(url, timeout=5)         # 5s obojí
    requests.get(url, timeout=(3, 10))   # (connect, read)

  Výjimky (dědičnost):
    RequestException
      ├── ConnectionError
      ├── Timeout
      └── HTTPError  (raise_for_status())

  Retry s urllib3:
    Retry(total=3, backoff_factor=1, status_forcelist=[502,503])
    s.mount('https://', HTTPAdapter(max_retries=retry))""",
        task="Popiš timeouty, výjimky requests a vzor pro opakování neúspěšných požadavků.",
        difficulty=3, points=25,
        hints=["timeout=(3,10), Timeout/ConnectionError/HTTPError, raise_for_status, Retry, backoff_factor"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "timeout" in r
                    and "výjimky" in r
                    and "Timeout" in str(r.get("výjimky", {}))
                    and "vzor_try_except" in r
                    and "opakování_retry" in r,
                    "Error handling ✓"
                )
            )(error_handling()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "HTTP & Requests", "12_01")
