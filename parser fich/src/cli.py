"""
CLI for competitor feature research agent.
Main command: python -m src.cli research "TOPIC STRING"
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

import typer

from src.collectors import collect_pages_for_competitor, take_screenshots_for_competitor
from src.extractors import find_competitors, extract_features_from_page
from src.analyzer import describe_mechanics
from src.models import FeatureCard, MechanicsDescription
from src.reporters import build_report_markdown

app = typer.Typer(help="Competitor feature research agent")
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "data" / "output"
RAW_DIR = PROJECT_ROOT / "data" / "raw"
REPORTS_DIR = OUTPUT_DIR / "reports"
SCREENSHOTS_DIR = OUTPUT_DIR / "screenshots"


def _setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s %(name)s: %(message)s")


@app.command()
def research(
    topic: str = typer.Argument(..., help="Research topic, e.g. 'EdTech blue-collar training platforms'"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose logging"),
    max_competitors: int = typer.Option(2, "--max-competitors", help="Max competitors to process (stub often uses 2)"),
    describe_mechanics_limit: int = typer.Option(3, "--mechanics-limit", help="Max features to run describe_mechanics on"),
) -> None:
    """
    Run full research pipeline: find competitors → collect pages → extract features →
    describe mechanics (for key features) → save features.json, mechanics.json → generate Markdown report.
    """
    _setup_logging(verbose)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    # 1) Find competitors
    competitors = find_competitors(topic, limit=max_competitors)
    if not competitors:
        typer.echo("No competitors found. Exiting.")
        raise typer.Exit(1)

    all_features: list[FeatureCard] = []
    all_mechanics: list[MechanicsDescription] = []

    for comp in competitors:
        # 2) Collect pages (HTML + text)
        snapshots = collect_pages_for_competitor(comp.name, comp.url, data_raw_dir=RAW_DIR)
        if not snapshots:
            logger.warning("No pages collected for %s", comp.name)
            continue

        # 3) Screenshots (stub returns [])
        page_urls = [(s.url, s.source_type) for s in snapshots]
        screenshot_list = take_screenshots_for_competitor(comp.name, page_urls, screenshots_dir=SCREENSHOTS_DIR)
        screenshot_paths_by_url: dict[str, list[str]] = {url: [] for url, _ in page_urls}
        for page_type, path in screenshot_list:
            for url, _ in page_urls:
                screenshot_paths_by_url.setdefault(url, []).append(path)
                break

        # 4) Extract features from each page (uses prompt prompts/extract_features.md)
        for snap in snapshots:
            screenshot_paths = screenshot_paths_by_url.get(snap.url, [])
            cards = extract_features_from_page(
                competitor=comp.name,
                source_url=snap.url,
                text=snap.text,
                screenshot_paths=screenshot_paths,
            )
            all_features.extend(cards)

        # 5) Describe mechanics for key features (uses prompt prompts/describe_mechanics.md)
        comp_features = [f for f in all_features if f.competitor == comp.name]
        for card in comp_features[:describe_mechanics_limit]:
            mechanics_desc = describe_mechanics(
                feature_card=card,
                extra_context="",
                screenshot_paths=card.screenshot_paths,
            )
            all_mechanics.append(mechanics_desc)

    # 6) Save outputs
    features_path = OUTPUT_DIR / "features.json"
    mechanics_path = OUTPUT_DIR / "mechanics.json"
    features_path.write_text(
        json.dumps([f.model_dump() for f in all_features], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    mechanics_path.write_text(
        json.dumps([m.model_dump() for m in all_mechanics], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    typer.echo(f"Saved {len(all_features)} features -> {features_path}")
    typer.echo(f"Saved {len(all_mechanics)} mechanics -> {mechanics_path}")

    # 7) Markdown report
    report_md = build_report_markdown(
        topic=topic,
        competitors=competitors,
        features=all_features,
        mechanics=all_mechanics,
        gaps_and_opportunities=[],
    )
    safe_topic = "".join(c if c.isalnum() or c in " -" else "_" for c in topic)[:50]
    report_path = REPORTS_DIR / f"research_{safe_topic.strip().replace(' ', '_')}.md"
    report_path.write_text(report_md, encoding="utf-8")
    typer.echo(f"Report written -> {report_path}")
    typer.echo("Done.")


if __name__ == "__main__":
    app()
