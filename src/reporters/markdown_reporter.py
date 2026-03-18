"""Generate full Markdown research report from features, mechanics, competitors."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models import FeatureCard, MechanicsDescription, Competitor

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
REPORTS_DIR = PROJECT_ROOT / "data" / "output" / "reports"


def build_report_markdown(
    topic: str,
    competitors: list,
    features: list,
    mechanics: list,
    gaps_and_opportunities: list[str] | None = None,
) -> str:
    """
    Build one Markdown report: competitors, feature matrix, per-feature details (with mechanics),
    UX & mechanics patterns, Gaps & opportunities. Screenshot paths as relative links.
    """
    lines = [
        f"# Competitive Feature Research: {topic}",
        "",
        "## Competitors",
        "",
    ]
    for c in competitors:
        lines.append(f"- **{c.name}** — {c.short_description}")
        lines.append(f"  - URL: {c.url}")
        lines.append("")
    lines.append("## Feature Matrix")
    lines.append("")
    lines.append("| Competitor | Feature | Category | Short description |")
    lines.append("|------------|---------|----------|--------------------|")
    for f in features:
        desc = (f.short_description or "")[:80] + ("..." if len((f.short_description or "")) > 80 else "")
        lines.append(f"| {f.competitor} | {f.feature_name} | {f.category} | {desc} |")
    lines.append("")
    lines.append("## Feature details (mechanics)")
    lines.append("")
    mechanics_by_key = {(m.competitor, m.feature_name): m for m in mechanics}
    for f in features:
        key = (f.competitor, f.feature_name)
        m = mechanics_by_key.get(key)
        lines.append(f"### {f.feature_name} ({f.competitor})")
        lines.append("")
        lines.append(f"- **Description:** {f.short_description}")
        lines.append(f"- **User job:** {f.user_job}")
        lines.append(f"- **Pricing tier:** {f.pricing_tier}")
        if m and m.scenario_summary:
            lines.append(f"- **Scenario:** {m.scenario_summary}")
        if m and m.mechanics_steps:
            lines.append("- **Mechanics steps:**")
            for step in m.mechanics_steps:
                lines.append(f"  - {step}")
        lines.append("- **Evidence:** " + ", ".join(f.evidence_urls))
        if f.screenshot_paths:
            lines.append("- **Screenshots:**")
            for p in f.screenshot_paths:
                lines.append(f"  - ![]({p})")
        if f.needs_manual_review:
            lines.append("- ⚠️ *Needs manual review*")
        lines.append("")
    lines.append("## UX & mechanics patterns")
    lines.append("")
    lines.append("(Summary of common patterns from mechanics descriptions.)")
    for m in mechanics:
        if m.ui_and_states or m.system_behaviour:
            lines.append(f"- **{m.feature_name}** ({m.competitor}): UI states / system behaviour captured in mechanics.")
    lines.append("")
    lines.append("## Gaps & opportunities")
    lines.append("")
    for s in gaps_and_opportunities or []:
        lines.append(f"- {s}")
    if not (gaps_and_opportunities or []):
        lines.append("- (Run gap analysis to fill this section.)")
    return "\n".join(lines)
