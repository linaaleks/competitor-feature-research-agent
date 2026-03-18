"""Screenshots for key pages. Stub: returns empty list; can be replaced with headless browser."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SCREENSHOTS_DIR = PROJECT_ROOT / "data" / "output" / "screenshots"


def take_screenshots_for_competitor(
    competitor_name: str,
    page_urls: list[tuple[str, str]],
    screenshots_dir: Path | None = None,
) -> list[tuple[str, str]]:
    """
    For each (url, page_type) create a screenshot and save under
    data/output/screenshots/<competitor>/<feature_or_page>.png.
    Returns list of (page_type_or_feature, screenshot_path).
    Stub: creates directory and returns empty list; replace with Playwright/Puppeteer when needed.
    """
    out = screenshots_dir or SCREENSHOTS_DIR
    competitor_dir = out / competitor_name.replace(" ", "_")
    competitor_dir.mkdir(parents=True, exist_ok=True)
    # Stub: no actual screenshot; caller can still pass paths to extractor for structure
    logger.info("Screenshotter (stub): %s, %s pages", competitor_name, len(page_urls))
    return []
