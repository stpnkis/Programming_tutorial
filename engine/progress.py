"""
📊 Progress modul — sledování postupu uživatele.
Ukládá do JSON souboru v kořenu projektu.
"""
import json
import os
from datetime import datetime


PROGRESS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    ".progress.json"
)


class Progress:
    """Správa postupu uživatele."""

    def __init__(self):
        self.data = self._load()

    def _load(self):
        """Načte progress ze souboru."""
        if os.path.exists(PROGRESS_FILE):
            try:
                with open(PROGRESS_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {
            "total_points": 0,
            "total_challenges": 0,
            "sections": {},
            "streak_days": [],
            "started": datetime.now().isoformat()
        }

    def _save(self):
        """Uloží progress do souboru."""
        try:
            with open(PROGRESS_FILE, 'w') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"  ⚠️  Nepodařilo se uložit progress: {e}")

    def save_section(self, section_id, completed, total, points):
        """Uloží výsledek sekce."""
        today = datetime.now().strftime("%Y-%m-%d")

        self.data["sections"][section_id] = {
            "completed": completed,
            "total": total,
            "points": points,
            "last_attempt": datetime.now().isoformat(),
            "best_points": max(
                points,
                self.data.get("sections", {}).get(section_id, {}).get("best_points", 0)
            )
        }

        # Aktualizuj celkové statistiky
        self.data["total_points"] = sum(
            s.get("best_points", 0) for s in self.data["sections"].values()
        )
        self.data["total_challenges"] = sum(
            s.get("completed", 0) for s in self.data["sections"].values()
        )

        # Streak
        if today not in self.data.get("streak_days", []):
            self.data.setdefault("streak_days", []).append(today)

        self._save()

    def get_section(self, section_id):
        """Vrátí progress pro sekci."""
        return self.data.get("sections", {}).get(section_id, {})

    def get_streak(self):
        """Spočítá aktuální streak (po sobě jdoucí dny)."""
        days = sorted(self.data.get("streak_days", []))
        if not days:
            return 0
        streak = 1
        for i in range(len(days) - 1, 0, -1):
            d1 = datetime.strptime(days[i], "%Y-%m-%d")
            d2 = datetime.strptime(days[i-1], "%Y-%m-%d")
            if (d1 - d2).days == 1:
                streak += 1
            else:
                break
        return streak

    def get_summary(self):
        """Vrátí přehledné shrnutí."""
        return {
            "total_points": self.data.get("total_points", 0),
            "total_challenges": self.data.get("total_challenges", 0),
            "sections_started": len(self.data.get("sections", {})),
            "streak": self.get_streak(),
            "days_active": len(self.data.get("streak_days", []))
        }

    def reset(self):
        """Reset progressu."""
        self.data = {
            "total_points": 0,
            "total_challenges": 0,
            "sections": {},
            "streak_days": [],
            "started": datetime.now().isoformat()
        }
        self._save()
