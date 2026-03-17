"""Helpers for screenshot paths and output assets."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SCREENSHOTS_DIR = PROJECT_ROOT / "data" / "output" / "screenshots"


def ensure_screenshots_dir(competitor: str) -> Path:
    """Ensure data/output/screenshots/<competitor> exists; return path."""
    d = SCREENSHOTS_DIR / competitor.replace(" ", "_")
    d.mkdir(parents=True, exist_ok=True)
    return d
