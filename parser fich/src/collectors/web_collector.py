"""Collect HTML/text from competitor pages. Saves to data/raw/ with timestamp and structure."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import httpx
from bs4 import BeautifulSoup

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
SOURCE_TYPES = (
    "changelog", "pricing", "features", "blog", "docs", "reviews"
)


@dataclass
class PageSnapshot:
    competitor: str
    source_type: str
    url: str
    html_path: str
    text: str


def _sanitize_name(name: str) -> str:
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in name)


def collect_pages_for_competitor(
    competitor_name: str,
    base_url: str,
    data_raw_dir: Path | None = None,
) -> list[PageSnapshot]:
    """
    Fetch main page types (features, pricing, etc.) for a competitor, save HTML under
    data/raw/<competitor>/<source_type>/<date>.html, return list of snapshots with extracted text.
    """
    raw_dir = data_raw_dir or RAW_DIR
    competitor_dir = raw_dir / _sanitize_name(competitor_name)
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    snapshots = []

    # Stub: only fetch the main page as "features" for simplicity
    urls_to_try = [
        (base_url.rstrip("/") + "/", "features"),
        (base_url.rstrip("/") + "/features", "features"),
        (base_url.rstrip("/") + "/pricing", "pricing"),
    ]
    seen = set()
    with httpx.Client(follow_redirects=True, timeout=15) as client:
        for url, source_type in urls_to_try:
            if url in seen:
                continue
            seen.add(url)
            try:
                resp = client.get(url)
                resp.raise_for_status()
                html = resp.text
                soup = BeautifulSoup(html, "html.parser")
                for tag in soup(["script", "style"]):
                    tag.decompose()
                text = soup.get_text(separator="\n", strip=True)[:50000]

                save_dir = competitor_dir / source_type / date_str
                save_dir.mkdir(parents=True, exist_ok=True)
                html_file = save_dir / "index.html"
                html_file.write_text(html, encoding="utf-8")

                snapshots.append(PageSnapshot(
                    competitor=competitor_name,
                    source_type=source_type,
                    url=url,
                    html_path=str(html_file),
                    text=text,
                ))
                logger.info("Collected %s %s -> %s", competitor_name, source_type, url)
                break  # at least one page per competitor for stub
            except Exception as e:
                logger.warning("Failed to fetch %s: %s", url, e)
    return snapshots
