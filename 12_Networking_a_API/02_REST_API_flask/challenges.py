#!/usr/bin/env python3
"""🍶 REST API s Flask — routy, metody, JSON odpovědi, blueprinty, CRUD."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def flask_zaklady():
    """
    🎯 VÝZVA 1: Flask — základy a první aplikace.
    Vrať dict:
    {
        "instalace": "pip install flask",
        "minimální_aplikace": {
            "kód": "from flask import Flask\\napp = Flask(__name__)\\n\\n@app.route('/')\\ndef index():\\n    return 'Ahoj, svetе!'\\n\\nif __name__ == '__main__':\\n    app.run(debug=True, host='0.0.0.0', port=5000)",
            "spuštění": "python app.py  nebo  flask run"
        },
        "routy": {
            "statická": "@app.route('/about')",
            "dynamická": "@app.route('/user/<jmeno>')  # <jmeno> je proměnná",
            "typ_proměnné": "@app.route('/item/<int:item_id>')  # int, float, string, path, uuid",
            "url_for": "from flask import url_for\\nurl_for('index')  # generuje URL z názvu funkce"
        },
        "konfigurace": {
            "debug":       "app.config['DEBUG'] = True  # NIKDY v produkci",
            "secret_key":  "app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')",
            "z_objektu":   "app.config.from_object('config.ProductionConfig')"
        },
        "vývojový_server": {
            "pozn": "Werkzeug dev server — použitelný jen pro vývoj",
            "produkce": "gunicorn -w 4 'app:create_app()'  nebo  uWSGI"
        }
    }
    """
    # TODO: ↓
    pass


def rest_metody():
    """
    🎯 VÝZVA 2: HTTP metody a REST konvence.
    Vrať dict:
    {
        "rest_konvence": {
            "GET    /items":      "seznam všech položek",
            "GET    /items/<id>": "detail jedné položky",
            "POST   /items":      "vytvoř novou položku",
            "PUT    /items/<id>": "nahraď celou položku",
            "PATCH  /items/<id>": "uprav část položky",
            "DELETE /items/<id>": "smaž položku"
        },
        "dekorátor_methods": {
            "kód": "@app.route('/items', methods=['GET', 'POST'])\\ndef items():\\n    if request.method == 'GET':\\n        return ...\\n    elif request.method == 'POST':\\n        return ...",
            "pozn": "jeden handler pro více metod — zkontroluj request.method"
        },
        "request_objekt": {
            "import":          "from flask import request",
            "request.method":  "HTTP metoda jako string ('GET', 'POST',...)",
            "request.json":    "tělo požadavku naparsované jako dict (Content-Type: json)",
            "request.form":    "formulářová data",
            "request.args":    "query string parametry (?key=val)",
            "request.headers": "hlavičky požadavku",
            "request.files":   "nahraté soubory"
        },
        "stavové_kódy_v_odpovědi": {
            "kód": "return jsonify(data), 201  # tuple (odpověď, kód)",
            "zkratky": {
                "200": "OK — výchozí",
                "201": "Created — po úspěšném POST",
                "204": "No Content — po DELETE (prázdné tělo)",
                "400": "Bad Request — chybná data",
                "404": "Not Found",
                "409": "Conflict — duplicitní záznam"
            }
        }
    }
    """
    # TODO: ↓
    pass


def json_responses():
    """
    🎯 VÝZVA 3: JSON odpovědi a zpracování vstupu.
    Vrať dict:
    {
        "jsonify": {
            "import": "from flask import jsonify",
            "příklady": [
                "return jsonify({'id': 1, 'name': 'robot'})",
                "return jsonify(items_list), 200",
                "return jsonify({'error': 'Not found'}), 404"
            ],
            "pozn": "automaticky nastaví Content-Type: application/json"
        },
        "čtení_json_vstupu": {
            "kód": "data = request.get_json()\\nif not data:\\n    return jsonify({'error': 'Chybný JSON'}), 400\\nname = data.get('name')",
            "validace": "vždy validuj vstupní data — nikdy nevěř klientovi"
        },
        "error_handlery": {
            "kód": "@app.errorhandler(404)\\ndef not_found(e):\\n    return jsonify({'error': 'Nenalezeno'}), 404\\n\\n@app.errorhandler(500)\\ndef server_error(e):\\n    return jsonify({'error': 'Chyba serveru'}), 500",
            "účel": "jednotný formát chybových odpovědí"
        },
        "cors": {
            "problém": "prohlížeč blokuje požadavky z jiné domény",
            "řešení": "pip install flask-cors\\nfrom flask_cors import CORS\\nCORS(app)  # povolí vše — v produkci nastavit origins",
            "produkce": "CORS(app, origins=['https://moje-domena.cz'])"
        },
        "make_response": {
            "kód": "resp = make_response(jsonify(data), 200)\\nresp.headers['X-Custom'] = 'hodnota'\\nreturn resp",
            "účel": "přidej vlastní hlavičky k odpovědi"
        }
    }
    """
    # TODO: ↓
    pass


def blueprints():
    """
    🎯 VÝZVA 4: Flask Blueprinty a Application Factory.
    Vrať dict:
    {
        "blueprint_definice": {
            "kód": "from flask import Blueprint\\n\\nrobots_bp = Blueprint('robots', __name__, url_prefix='/robots')\\n\\n@robots_bp.route('/')\\ndef list_robots():\\n    return jsonify(robots)",
            "účel": "rozdělí velkou aplikaci do modulů"
        },
        "registrace_blueprintu": {
            "kód": "from .robots import robots_bp\\napp.register_blueprint(robots_bp)",
            "url_prefix": "všechny routy blueprintu budou prefixovány /robots"
        },
        "app_factory": {
            "kód": "def create_app(config=None):\\n    app = Flask(__name__)\\n    if config:\\n        app.config.from_object(config)\\n    from .robots import robots_bp\\n    app.register_blueprint(robots_bp)\\n    return app",
            "spuštění": "app = create_app(); app.run()",
            "výhody": [
                "testovatelnost — různé konfigurace pro test/prod",
                "čistá inicializace závislostí",
                "sdílení instance bez circular imports"
            ]
        },
        "struktura_projektu": {
            "doporučená": [
                "myapp/",
                "  __init__.py   ← create_app()",
                "  robots/",
                "    __init__.py ← robots_bp",
                "    routes.py",
                "    models.py",
                "  config.py",
                "run.py"
            ]
        }
    }
    """
    # TODO: ↓
    pass


def crud_api():
    """
    🎯 VÝZVA 5: Kompletní CRUD API — vzorový příklad.
    Vrať dict:
    {
        "datový_model": {
            "příklad": "robots = {}  # {id: {name, speed, active}} — in-memory DB",
            "produkce": "SQLAlchemy + PostgreSQL / SQLite"
        },
        "create_post": {
            "kód": "@app.route('/robots', methods=['POST'])\\ndef create_robot():\\n    data = request.get_json()\\n    if not data or 'name' not in data:\\n        return jsonify({'error': 'name povinný'}), 400\\n    rid = str(uuid.uuid4())\\n    robots[rid] = {'id': rid, 'name': data['name'], 'speed': data.get('speed', 1.0)}\\n    return jsonify(robots[rid]), 201"
        },
        "read_get": {
            "seznam": "@app.route('/robots')\\ndef list_robots():\\n    return jsonify(list(robots.values()))",
            "detail": "@app.route('/robots/<rid>')\\ndef get_robot(rid):\\n    r = robots.get(rid)\\n    if not r: return jsonify({'error': 'Not found'}), 404\\n    return jsonify(r)"
        },
        "update_put": {
            "kód": "@app.route('/robots/<rid>', methods=['PUT'])\\ndef update_robot(rid):\\n    if rid not in robots: return jsonify({'error': 'Not found'}), 404\\n    robots[rid].update(request.get_json())\\n    return jsonify(robots[rid])"
        },
        "delete": {
            "kód": "@app.route('/robots/<rid>', methods=['DELETE'])\\ndef delete_robot(rid):\\n    if rid not in robots: return jsonify({'error': 'Not found'}), 404\\n    del robots[rid]\\n    return '', 204"
        },
        "testování_curl": [
            "curl -X POST http://localhost:5000/robots -H 'Content-Type: application/json' -d '{\"name\":\"R2D2\"}'",
            "curl http://localhost:5000/robots",
            "curl -X DELETE http://localhost:5000/robots/<id>"
        ]
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🏆 VÝZVY
# ============================================================

challenges = [
    Challenge(
        title="Flask základy",
        theory="""Flask — minimalistický webový framework pro Python:

  pip install flask

  from flask import Flask
  app = Flask(__name__)

  @app.route('/')
  def index():
      return 'Ahoj!'

  Dynamické routy: /user/<jmeno>,  /item/<int:id>
  url_for('název_funkce')  — generuj URL bezpečně
  debug=True  — reload při změně kódu (jen v dev!)
  Produkce: gunicorn, uWSGI""",
        task="Popiš Flask aplikaci: instalace, routy, konfigurace a vývojový vs produkční server.",
        difficulty=1, points=15,
        hints=["Flask(__name__), @app.route, <int:id>, url_for, debug=True, gunicorn"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "minimální_aplikace" in r
                    and "routy" in r
                    and "dynamická" in r.get("routy", {})
                    and "konfigurace" in r,
                    "Flask základy ✓"
                )
            )(flask_zaklady()),
        ]
    ),
    Challenge(
        title="HTTP metody a REST",
        theory="""REST konvence — mapování HTTP metod na operace:

  GET    /items        — seznam
  GET    /items/<id>   — detail
  POST   /items        — vytvoř
  PUT    /items/<id>   — nahraď
  PATCH  /items/<id>   — uprav
  DELETE /items/<id>   — smaž

  @app.route('/items', methods=['GET','POST'])
  def items():
      if request.method == 'POST':
          data = request.json   # tělo požadavku
      ...
  return jsonify(data), 201""",
        task="Popiš REST konvence, dekorátor methods, objekt request a stavové kódy odpovědí.",
        difficulty=2, points=20,
        hints=["GET/POST/PUT/PATCH/DELETE, methods=[], request.json/args/form, 201/204/400/404"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "rest_konvence" in r
                    and "request_objekt" in r
                    and "request.json" in str(r.get("request_objekt", {}))
                    and "stavové_kódy_v_odpovědi" in r,
                    "REST metody ✓"
                )
            )(rest_metody()),
        ]
    ),
    Challenge(
        title="JSON odpovědi",
        theory="""jsonify() — vrací JSON odpověď s Content-Type: application/json:

  return jsonify({'id': 1, 'name': 'R2D2'}), 200
  return jsonify({'error': 'Not found'}), 404

  Čtení vstupu:
    data = request.get_json()   # naparsuje JSON tělo

  Error handlery:
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': '...'}), 404

  CORS (Cross-Origin):
    pip install flask-cors
    CORS(app, origins=['https://moje-app.cz'])""",
        task="Popiš jsonify, čtení JSON vstupu, error handlery a CORS.",
        difficulty=2, points=20,
        hints=["jsonify(), request.get_json(), @app.errorhandler, flask-cors, make_response"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "jsonify" in r
                    and isinstance(r["jsonify"].get("příklady"), list)
                    and len(r["jsonify"]["příklady"]) >= 2
                    and "čtení_json_vstupu" in r
                    and "error_handlery" in r
                    and "cors" in r,
                    "JSON odpovědi ✓"
                )
            )(json_responses()),
        ]
    ),
    Challenge(
        title="Blueprinty a App Factory",
        theory="""Flask Blueprint — modul aplikace s vlastními routami:

  robots_bp = Blueprint('robots', __name__, url_prefix='/robots')

  @robots_bp.route('/')    →  GET /robots/
  app.register_blueprint(robots_bp)

  Application Factory — funkce vracející instanci app:
  def create_app(config=None):
      app = Flask(__name__)
      app.register_blueprint(robots_bp)
      return app

  Výhody: testovatelnost, různé konfigurace, čistá architektura""",
        task="Popiš Flask Blueprinty, Application Factory a doporučenou strukturu projektu.",
        difficulty=3, points=25,
        hints=["Blueprint('name', __name__, url_prefix), register_blueprint, create_app(), struktura"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "blueprint_definice" in r
                    and "registrace_blueprintu" in r
                    and "app_factory" in r
                    and "výhody" in r.get("app_factory", {})
                    and isinstance(r["app_factory"]["výhody"], list)
                    and "struktura_projektu" in r,
                    "Blueprinty ✓"
                )
            )(blueprints()),
        ]
    ),
    Challenge(
        title="Kompletní CRUD API",
        theory="""CRUD = Create Read Update Delete — základ každého REST API:

  POST   /robots       → 201 Created  + nový objekt
  GET    /robots       → 200 OK       + seznam
  GET    /robots/<id>  → 200 OK / 404
  PUT    /robots/<id>  → 200 OK / 404
  DELETE /robots/<id>  → 204 No Content / 404

  Validace vstupu (VŽDY!):
    data = request.get_json()
    if 'name' not in data: return 400

  Testování:
    curl, Postman, HTTPie, pytest + flask test client""",
        task="Napiš vzorové CRUD API pro roboty: POST, GET (seznam+detail), PUT, DELETE. Uved curl příklady.",
        difficulty=3, points=25,
        hints=["201 po POST, 204 po DELETE, 404 když nenalezeno, uuid.uuid4(), curl -X POST"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "create_post" in r
                    and "read_get" in r
                    and "seznam" in r.get("read_get", {})
                    and "update_put" in r
                    and "delete" in r
                    and isinstance(r.get("testování_curl"), list)
                    and len(r["testování_curl"]) >= 2,
                    "CRUD API ✓"
                )
            )(crud_api()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "REST API s Flask", "12_02")
