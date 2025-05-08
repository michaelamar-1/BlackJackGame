import json
from pathlib import Path
from rich.console import Console

STAT_FILE = Path(__file__).parent / "stats.json"
console = Console()


def _load():
    if STAT_FILE.exists():
        return json.loads(STAT_FILE.read_text())
    return {"games_played": 0, "player_wins": 0, "dealer_wins": 0, "ties": 0}


def _save(stats):
    STAT_FILE.write_text(json.dumps(stats, indent=2))


def update_stats(result):
    """
    Increment stats for 'player', 'dealer', or 'tie'.
    :param result: str
    """
    s = _load()
    s["games_played"] += 1
    if result == "player":
        s["player_wins"] += 1
    elif result == "dealer":
        s["dealer_wins"] += 1
    else:
        s["ties"] += 1
    _save(s)


def print_stats():
    """
    Pretty-print current statistics via Rich.
    """
    s = _load()
    rate = (s["player_wins"] / s["games_played"] * 100) if s["games_played"] else 0
    console.print("🎲 **Game Statistics** 🎲")
    console.print(f"Games played: {s['games_played']}")
    console.print(f"Player wins: {s['player_wins']}")
    console.print(f"Dealer wins: {s['dealer_wins']}")
    console.print(f"Ties: {s['ties']}")
    console.print(f"Player win rate: {rate:.2f}%\n")
