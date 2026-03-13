"""
🎨 UI modul — barvy, formátování, ASCII art pro terminál.
Všechno co dělá trénink vizuálně atraktivní.
"""
import os
import shutil


class Colors:
    """ANSI escape kódy pro barvy v terminálu."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    # Barvy
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    ORANGE = "\033[38;5;208m"
    GRAY = "\033[90m"

    # Pozadí
    BG_GREEN = "\033[42m"
    BG_RED = "\033[41m"
    BG_BLUE = "\033[44m"
    BG_YELLOW = "\033[43m"
    BG_MAGENTA = "\033[45m"


C = Colors


class UI:
    """Hlavní UI třída pro výstup do terminálu."""

    @staticmethod
    def width():
        """Šířka terminálu."""
        return shutil.get_terminal_size().columns

    @staticmethod
    def clear():
        """Vyčistí terminál."""
        os.system('clear' if os.name != 'nt' else 'cls')

    @staticmethod
    def line(char="─", color=C.GRAY):
        """Horizontální čára."""
        w = min(UI.width(), 80)
        print(f"{color}{char * w}{C.RESET}")

    @staticmethod
    def double_line(color=C.CYAN):
        UI.line("═", color)

    @staticmethod
    def banner(text, color=C.CYAN):
        """Velký banner s textem."""
        w = min(UI.width(), 80)
        print()
        print(f"{color}{C.BOLD}{'═' * w}")
        padding = (w - len(text)) // 2
        print(f"{' ' * padding}{text}")
        print(f"{'═' * w}{C.RESET}")
        print()

    @staticmethod
    def welcome():
        """Hlavní uvítací obrazovka."""
        UI.clear()
        logo = f"""{C.CYAN}{C.BOLD}
    ██████╗ ██████╗  ██████╗  ██████╗     ████████╗██████╗  █████╗ ██╗███╗   ██╗
    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝     ╚══██╔══╝██╔══██╗██╔══██╗██║████╗  ██║
    ██████╔╝██████╔╝██║   ██║██║  ███╗       ██║   ██████╔╝███████║██║██╔██╗ ██║
    ██╔═══╝ ██╔══██╗██║   ██║██║   ██║       ██║   ██╔══██╗██╔══██║██║██║╚██╗██║
    ██║     ██║  ██║╚██████╔╝╚██████╔╝       ██║   ██║  ██║██║  ██║██║██║ ╚████║
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝        ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
{C.RESET}
{C.YELLOW}{C.BOLD}          ⚡ PROGRAMÁTORSKÉ TRÉNINKOVÉ CENTRUM ⚡{C.RESET}
{C.DIM}          Buduj programátorskou intuici krok za krokem{C.RESET}
"""
        print(logo)

    @staticmethod
    def section_header(number, title, emoji="📦"):
        """Hlavička sekce."""
        w = min(UI.width(), 80)
        print()
        print(f"{C.BLUE}{C.BOLD}{'─' * w}")
        print(f"  {emoji} {number}. {title}")
        print(f"{'─' * w}{C.RESET}")
        print()

    @staticmethod
    def challenge_header(number, title, difficulty=1, points=10):
        """Hlavička výzvy."""
        stars = "⭐" * difficulty + "☆" * (3 - difficulty)
        print()
        UI.line("─", C.MAGENTA)
        print(f"  {C.MAGENTA}{C.BOLD}🏆 VÝZVA {number}: {title}{C.RESET}")
        print(f"  {C.YELLOW}Obtížnost: {stars}  |  Body: {points}b{C.RESET}")
        UI.line("─", C.MAGENTA)

    @staticmethod
    def theory(text):
        """Blok teorie."""
        print(f"\n  {C.CYAN}{C.BOLD}📚 TEORIE:{C.RESET}")
        for line in text.strip().split('\n'):
            print(f"  {C.CYAN}{line.strip()}{C.RESET}")
        print()

    @staticmethod
    def task(text):
        """Zadání úkolu."""
        print(f"  {C.YELLOW}{C.BOLD}📝 ÚKOL:{C.RESET}")
        for line in text.strip().split('\n'):
            print(f"  {C.YELLOW}  {line.strip()}{C.RESET}")
        print()

    @staticmethod
    def success(text="Správně! 🎉"):
        """Úspěšná zpráva."""
        print(f"  {C.GREEN}{C.BOLD}✅ {text}{C.RESET}")

    @staticmethod
    def fail(text="Špatně, zkus to znovu."):
        """Chybová zpráva."""
        print(f"  {C.RED}{C.BOLD}❌ {text}{C.RESET}")

    @staticmethod
    def hint(text):
        """Nápověda."""
        print(f"  {C.YELLOW}💡 Hint: {text}{C.RESET}")

    @staticmethod
    def info(text):
        """Informační zpráva."""
        print(f"  {C.BLUE}ℹ️  {text}{C.RESET}")

    @staticmethod
    def warning(text):
        """Varování."""
        print(f"  {C.ORANGE}⚠️  {text}{C.RESET}")

    @staticmethod
    def code(text):
        """Blok kódu."""
        print(f"  {C.GREEN}  >>> {text}{C.RESET}")

    @staticmethod
    def example(code_text, output_text=None):
        """Příklad s kódem a výstupem."""
        print(f"  {C.DIM}Příklad:{C.RESET}")
        for line in code_text.strip().split('\n'):
            print(f"  {C.GREEN}  >>> {line.strip()}{C.RESET}")
        if output_text:
            print(f"  {C.WHITE}  {output_text}{C.RESET}")
        print()

    @staticmethod
    def progress_bar(completed, total, width=40):
        """Ukazatel postupu."""
        if total == 0:
            return
        pct = completed / total
        filled = int(width * pct)
        bar = f"{'█' * filled}{'░' * (width - filled)}"
        color = C.GREEN if pct >= 0.8 else C.YELLOW if pct >= 0.4 else C.RED
        print(f"  {color}[{bar}] {completed}/{total} ({pct:.0%}){C.RESET}")

    @staticmethod
    def score_display(points, total_points):
        """Zobrazení skóre."""
        pct = (points / total_points * 100) if total_points > 0 else 0
        if pct >= 90:
            rank = "🏆 MISTR"
            color = C.YELLOW
        elif pct >= 70:
            rank = "🥈 POKROČILÝ"
            color = C.CYAN
        elif pct >= 40:
            rank = "🥉 ZAČÁTEČNÍK"
            color = C.GREEN
        else:
            rank = "🌱 NOVÁČEK"
            color = C.WHITE
        print(f"\n  {color}{C.BOLD}{rank}  |  {points}/{total_points} bodů ({pct:.0f}%){C.RESET}\n")

    @staticmethod
    def menu(options, title="Vyber možnost"):
        """Interaktivní menu."""
        print(f"\n  {C.BOLD}{title}:{C.RESET}")
        for i, (label, _) in enumerate(options, 1):
            print(f"  {C.CYAN}  [{i}]{C.RESET} {label}")
        print(f"  {C.CYAN}  [0]{C.RESET} Zpět / Konec")
        print()
        while True:
            try:
                choice = input(f"  {C.BOLD}→ {C.RESET}").strip()
                if choice == '0':
                    return None
                idx = int(choice) - 1
                if 0 <= idx < len(options):
                    return options[idx][1]
            except (ValueError, KeyboardInterrupt):
                pass
            print(f"  {C.RED}Neplatná volba, zkus znovu.{C.RESET}")

    @staticmethod
    def wait():
        """Čeká na Enter."""
        input(f"\n  {C.DIM}⏎ Stiskni Enter pro pokračování...{C.RESET}")

    @staticmethod
    def ask_hint():
        """Zeptá se jestli chce hint."""
        answer = input(f"  {C.YELLOW}Chceš nápovědu? (a/n): {C.RESET}").strip().lower()
        return answer in ('a', 'y', 'ano', 'yes')

    @staticmethod
    def celebration():
        """Oslavná animace po dokončení sekce."""
        art = f"""
{C.YELLOW}{C.BOLD}
    🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆

         ██╗    ██╗██╗███╗   ██╗██╗
         ██║    ██║██║████╗  ██║██║
         ██║ █╗ ██║██║██╔██╗ ██║██║
         ██║███╗██║██║██║╚██╗██║╚═╝
         ╚███╔███╔╝██║██║ ╚████║██╗
          ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═╝

    🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆
{C.RESET}
{C.GREEN}{C.BOLD}    Všechny výzvy v této sekci splněny!{C.RESET}
"""
        print(art)

    @staticmethod
    def mission_briefing(mission_name, description, objectives):
        """Briefing mise ve stylu hry."""
        w = min(UI.width(), 80)
        print(f"\n{C.ORANGE}{C.BOLD}{'▓' * w}")
        print(f"  🎯 MISE: {mission_name}")
        print(f"{'▓' * w}{C.RESET}")
        print(f"\n  {C.WHITE}{description}{C.RESET}\n")
        print(f"  {C.CYAN}{C.BOLD}Cíle:{C.RESET}")
        for i, obj in enumerate(objectives, 1):
            print(f"  {C.CYAN}  {i}. {obj}{C.RESET}")
        print()
