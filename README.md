# 🎓 Programming Tutorial & Training Center

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![ROS2](https://img.shields.io/badge/ROS2-Humble-red?style=for-the-badge&logo=ros&logoColor=white)](https://docs.ros.org/en/humble/index.html)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active_Development-orange?style=for-the-badge)]()

**Komplexní interaktivní výukový systém** navržený pro efektivní osvojení moderního softwarového inženýrství. Od základů Pythonu přes pokročilé algoritmy a Machine Learning až po vývoj robotických systémů v ROS2.

Tento projekt kombinuje teorii s praxí formou **Test-Driven Development (TDD)** výzev, které simulují reálné pracovní úkoly.

---

## 🏗️ Architektura a Obsah Kurzu

Repozitář je strukturován do logických celků kopírujících kariérní růst od juniorního vývojáře po experta na robotiku a AI.

### 🔹 Fáze 1: Core Engineering (Základy inženýrství)
*   **[01] Python Core:** Hloubková syntaxe, paměťový model, typing.
*   **[02] OOP & Design Patterns:** SOLID principy, kompozice, dědičnost.
*   **[03] Algorithms & Data Structures:** Big O notace, grafy, optimalizace.
*   **[04] Software Craftsmanship:** Git flow, Code Review, CI/CD pipelines.

### 🔹 Fáze 2: Professional Development (Profesionální vývoj)
*   **[05] Testing & QA:** Pytest, Mocking, TDD metodiky.
*   **[06] Debugging & Profiling:** Analýza výkonu, refactoring legacy kódu.
*   **[11] System Engineering:** Linux kernel, Bash scripting, Docker kontejnerizace.
*   **[12] Networking & Protocols:** REST API, WebSockets, MQTT, Serial.

### 🔹 Fáze 3: Data Science & AI (Věda a umělá inteligence)
*   **[07] Applied Mathematics:** Lineární algebra, statistika, Scientific computing (NumPy).
*   **[08] Machine Learning:** Scikit-learn, neuronové sítě, PyTorch, Deep Learning.
*   **[09] Computer Vision:** Zpracování obrazu, OpenCV, 3D vision, Point Clouds.

### 🔹 Fáze 4: Robotics & Real-time Systems (Robotika)
*   **[10] ROS2 (Robot Operating System):** Nodes, Topics, Services, TF2, Navigace.
*   **[13] Concurrency & Async:** Multiprocessing, Threading, AsyncIO, Real-time limity.

---

## 🚀 Jak systém funguje?

Aplikace běží kompletně v CLI (Command Line Interface) a poskytuje gamifikované prostředí pro výuku.

### Ukázka rozhraní (CLI)
```text
  🏆 User: stpnkis | Level: Junior Engineer | Points: 1250 

  Active Module: [02_OOP] / [03_Polymorfismus]
  Target: Implement abstract method 'calculate_area' for all shapes.

  > Running tests...
  [✔] Shape class defined correctly
  [✔] Circle implements calculate_area
  [✘] Square is missing implementation
  
  ❌ Challenge Failed. Fix the code in 'challenges.py' and try again.
```

---

## 🛠️ Instalace a Spuštění

Pro spuštění tréninkového prostředí stačí naklonovat repozitář a spustit vstupní bod.

### Prerekvizity
*   Python 3.8+
*   Git

### Setup
```bash
# 1. Klonování repozitáře
git clone git@github.com:stpnkis/Programming_tutorial.git
cd Programming_tutorial

# 2. Vytvoření virtuálního prostředí (doporučeno)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instalace závislostí
pip install -r requirements.txt  # (Pokud soubor existuje, jinak přeskočit)

# 4. Spuštění systému
python3 start.py
```

---

## 🤝 Contributing & Spolupráce

Tento projekt je open-source a slouží jako vzdělávací platforma. Kód je psán s důrazem na čitelnost a dodržování PEP8 standardů.

Pokud chcete přispět novou výzvou nebo opravou:
1.  Forkněte repozitář.
2.  Vytvořte větev (`feature/new-challenge`).
3.  Odešlete Pull Request s popisem změn.

---

## 📝 Licence

Tento projekt je licencován pod **MIT License** - viz soubor [LICENSE](LICENSE) pro detaily.

---
*Created & Maintained by [stpnkis](https://github.com/stpnkis)*
