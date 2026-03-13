#!/usr/bin/env python3
"""
🚀 PROGRAMÁTORSKÉ TRÉNINKOVÉ CENTRUM
Hlavní spouštěč — vstupní bod do celého systému.

Spusť: python3 start.py
"""
import os
import sys
import importlib
import glob

# Nastavení cesty
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from engine.ui import UI, Colors as C
from engine.progress import Progress


# ============================================================
# Definice sekcí
# ============================================================
SECTIONS = [
    ("01", "Python Základy", "🐍", "01_Python_Zaklady"),
    ("02", "OOP", "🏗️", "02_OOP"),
    ("03", "Datové Struktury & Algoritmy", "🌳", "03_Datove_Struktury_Algoritmy"),
    ("04", "Git & Workflow", "📝", "04_Git_a_Workflow"),
    ("05", "Testing", "🧪", "05_Testing"),
    ("06", "Čtení & Debugování Kódu", "🔍", "06_Cteni_a_Debugovani_Kodu"),
    ("07", "NumPy & Matematika", "📐", "07_Numpy_a_Matematika"),
    ("08", "Machine Learning", "🤖", "08_Machine_Learning"),
    ("09", "Computer Vision", "👁️", "09_Computer_Vision"),
    ("10", "ROS2", "🤖", "10_ROS2"),
    ("11", "Linux & Terminál", "🐧", "11_Linux_a_Terminal"),
    ("12", "Networking & API", "🌐", "12_Networking_a_API"),
    ("13", "Paralelismus & Async", "⚡", "13_Paralelismus_a_Async"),
    ("14", "Projekty & Portfolio", "🏆", "14_Projekty_a_Portfolio"),
]


def find_challenges(section_dir):
    """Najde všechny challenge soubory v sekci."""
    challenges = []
    section_path = os.path.join(ROOT, section_dir)

    if not os.path.isdir(section_path):
        return challenges

    # Hledej podsložky s challenges.py
    for subdir in sorted(os.listdir(section_path)):
        subpath = os.path.join(section_path, subdir)
        challenge_file = os.path.join(subpath, "challenges.py")
        if os.path.isdir(subpath) and os.path.isfile(challenge_file):
            # Extrahuj název z adresáře
            name = subdir.split("_", 1)[1] if "_" in subdir else subdir
            name = name.replace("_", " ").title()
            challenges.append((name, challenge_file, subdir))

    return challenges


def run_challenge_file(filepath):
    """Spustí challenge soubor jako skript."""
    # Spustíme jako subprocess pro čistý stav
    os.system(f'cd "{os.path.dirname(filepath)}" && python3 "{filepath}"')


def show_section_menu(section_num, section_name, section_dir):
    """Zobrazí menu podsložek v sekci."""
    while True:
        UI.clear()
        UI.section_header(section_num, section_name)

        challenges = find_challenges(section_dir)

        if not challenges:
            UI.warning(f"Zatím žádné výzvy v sekci {section_name}.")
            UI.info("Brzy budou přidány!")
            UI.wait()
            return

        progress = Progress()

        # Zobraz seznam
        print(f"  {C.BOLD}Dostupné tréninky:{C.RESET}\n")
        for i, (name, filepath, subdir) in enumerate(challenges, 1):
            section_id = f"{section_num}_{subdir[:2]}"
            sec_progress = progress.get_section(section_id)
            completed = sec_progress.get("completed", 0)
            total = sec_progress.get("total", 0)

            if completed > 0 and completed == total:
                status = f"{C.GREEN}✅"
            elif completed > 0:
                status = f"{C.YELLOW}🔶"
            else:
                status = f"{C.GRAY}⬜"

            print(f"    {status} {C.CYAN}[{i}]{C.RESET} {name}"
                  f" {C.DIM}({completed}/{total} hotovo){C.RESET}" if total > 0
                  else f"    {status} {C.CYAN}[{i}]{C.RESET} {name}")

        print(f"\n    {C.CYAN}[0]{C.RESET} Zpět do hlavního menu")
        print()

        try:
            choice = input(f"  {C.BOLD}→ {C.RESET}").strip()
            if choice == '0' or choice == '':
                return
            idx = int(choice) - 1
            if 0 <= idx < len(challenges):
                name, filepath, subdir = challenges[idx]
                run_challenge_file(filepath)
                input(f"\n  {C.DIM}⏎ Enter pro návrat do menu...{C.RESET}")
        except (ValueError, KeyboardInterrupt):
            pass


def show_progress_screen():
    """Zobrazí celkový progress."""
    UI.clear()
    UI.banner("📊 TVŮJ PROGRESS")

    progress = Progress()
    summary = progress.get_summary()

    print(f"  {C.BOLD}🏆 Celkové body:{C.RESET}  {C.YELLOW}{summary['total_points']}{C.RESET}")
    print(f"  {C.BOLD}✅ Splněno výzev:{C.RESET} {C.GREEN}{summary['total_challenges']}{C.RESET}")
    print(f"  {C.BOLD}📂 Zahájeno sekcí:{C.RESET} {summary['sections_started']}")
    print(f"  {C.BOLD}🔥 Streak:{C.RESET}        {summary['streak']} dní")
    print(f"  {C.BOLD}📅 Aktivních dní:{C.RESET} {summary['days_active']}")

    # Detail po sekcích
    print(f"\n  {C.BOLD}Detail po sekcích:{C.RESET}\n")

    for sec_num, sec_name, emoji, sec_dir in SECTIONS:
        sec_data = progress.data.get("sections", {})
        total_completed = 0
        total_total = 0
        total_pts = 0

        for key, val in sec_data.items():
            if key.startswith(sec_num + "_"):
                total_completed += val.get("completed", 0)
                total_total += val.get("total", 0)
                total_pts += val.get("best_points", 0)

        if total_total > 0:
            pct = total_completed / total_total
            bar_w = 20
            filled = int(bar_w * pct)
            bar = f"{'█' * filled}{'░' * (bar_w - filled)}"
            color = C.GREEN if pct >= 0.8 else C.YELLOW if pct >= 0.4 else C.RED
            print(f"    {emoji} {sec_name:<30} {color}[{bar}]{C.RESET} "
                  f"{total_completed}/{total_total}  {C.YELLOW}{total_pts}b{C.RESET}")
        else:
            print(f"    {emoji} {sec_name:<30} {C.DIM}[{'░' * 20}] Nezahájeno{C.RESET}")

    UI.wait()


def show_roadmap():
    """Zobrazí doporučenou cestu učení."""
    UI.clear()
    UI.banner("🗺️ MAPA UČENÍ")

    roadmap = f"""
  {C.BOLD}Doporučený postup pro budování programátorské intuice:{C.RESET}

  {C.GREEN}╔══════════════════════════════════════════════════════════════╗
  ║  FÁZE 1: ZÁKLADY (2-4 týdny)                                ║
  ║  01 Python Základy → 02 OOP → 03 Datové struktury           ║
  ║  {C.DIM}Bez tohohle se nedá stavět nic dalšího.{C.GREEN}                      ║
  ╚══════════════════════════════════════════════════════════════╝{C.RESET}
                              │
                              ▼
  {C.YELLOW}╔══════════════════════════════════════════════════════════════╗
  ║  FÁZE 2: PROFESNÍ NÁVYKY (1-2 týdny)                        ║
  ║  04 Git → 05 Testing → 06 Čtení a debugování kódu           ║
  ║  {C.DIM}To co odděluje amatéra od profíka.{C.YELLOW}                          ║
  ╚══════════════════════════════════════════════════════════════╝{C.RESET}
                              │
                              ▼
  {C.CYAN}╔══════════════════════════════════════════════════════════════╗
  ║  FÁZE 3: DATA A ML (2-4 týdny)                              ║
  ║  07 NumPy & Matematika → 08 Machine Learning                 ║
  ║  {C.DIM}Od čísel k inteligentním modelům.{C.CYAN}                            ║
  ╚══════════════════════════════════════════════════════════════╝{C.RESET}
                              │
                              ▼
  {C.MAGENTA}╔══════════════════════════════════════════════════════════════╗
  ║  FÁZE 4: ROBOTIKA (2-4 týdny)                               ║
  ║  09 Computer Vision → 10 ROS2                                ║
  ║  {C.DIM}Tvůj hlavní obor — vidění a ovládání robotů.{C.MAGENTA}                ║
  ╚══════════════════════════════════════════════════════════════╝{C.RESET}
                              │
                              ▼
  {C.BLUE}╔══════════════════════════════════════════════════════════════╗
  ║  FÁZE 5: INFRASTRUKTURA (1-2 týdny)                         ║
  ║  11 Linux → 12 Networking → 13 Paralelismus                  ║
  ║  {C.DIM}To co drží vše pohromadě v reálném světě.{C.BLUE}                    ║
  ╚══════════════════════════════════════════════════════════════╝{C.RESET}
                              │
                              ▼
  {C.ORANGE}╔══════════════════════════════════════════════════════════════╗
  ║  FÁZE 6: PROJEKTY 🏆                                        ║
  ║  14 Reálné projekty do portfolia                             ║
  ║  {C.DIM}Spojení všeho do funkčních aplikací.{C.ORANGE}                        ║
  ╚══════════════════════════════════════════════════════════════╝{C.RESET}

  {C.BOLD}💡 Pravidlo:{C.RESET} Nepřecházej na další fázi, dokud neumíš aktuální
     napsat bez nápovědy. Opakování je klíč k intuici!
"""
    print(roadmap)
    UI.wait()


def main():
    """Hlavní smyčka."""
    while True:
        UI.welcome()

        # Krátké shrnutí progressu
        progress = Progress()
        summary = progress.get_summary()
        if summary["total_points"] > 0:
            print(f"  {C.YELLOW}🏆 {summary['total_points']} bodů{C.RESET}  "
                  f"{C.GREEN}✅ {summary['total_challenges']} výzev{C.RESET}  "
                  f"{C.ORANGE}🔥 {summary['streak']} dní streak{C.RESET}")

        print(f"\n  {C.BOLD}Hlavní Menu:{C.RESET}\n")

        # Zobraz sekce
        for i, (num, name, emoji, _) in enumerate(SECTIONS):
            sec_data = progress.data.get("sections", {})
            has_progress = any(k.startswith(num + "_") for k in sec_data)
            marker = f"{C.GREEN}●" if has_progress else f"{C.GRAY}○"
            print(f"    {marker} {C.CYAN}[{num}]{C.RESET} {emoji} {name}")

        print(f"\n    {C.CYAN}[p]{C.RESET}  📊 Progress")
        print(f"    {C.CYAN}[m]{C.RESET}  🗺️  Mapa učení")
        print(f"    {C.CYAN}[q]{C.RESET}  🚪 Konec\n")

        try:
            choice = input(f"  {C.BOLD}→ {C.RESET}").strip().lower()

            if choice in ('q', 'quit', 'exit'):
                UI.clear()
                print(f"\n  {C.CYAN}Hodně štěstí na tréninku! 💪{C.RESET}\n")
                break
            elif choice == 'p':
                show_progress_screen()
            elif choice == 'm':
                show_roadmap()
            else:
                # Najdi sekci
                for num, name, emoji, sec_dir in SECTIONS:
                    if choice == num or choice == num.lstrip('0'):
                        show_section_menu(num, name, sec_dir)
                        break

        except KeyboardInterrupt:
            print()
            continue
        except EOFError:
            break


if __name__ == "__main__":
    main()
