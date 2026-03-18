"""
Feature extraction from competitor page text using LLM.
Uses prompt: prompts/extract_features.md → output validated as list of FeatureCard.
"""
from __future__ import annotations

import json
import logging
import re
from typing import TYPE_CHECKING, List, Optional

from src.llm import load_prompt, call_llm
from src.models import FeatureCard

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


def _extract_json_from_response(raw: str) -> list[dict]:
    """Try to get a JSON array from LLM response (may be wrapped in markdown code block)."""
    raw = raw.strip()
    # Strip markdown code block if present
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```\s*$", "", raw)
    data = json.loads(raw)
    if not isinstance(data, list):
        data = [data]
    return data


def extract_features_from_page(
    competitor: str,
    source_url: str,
    text: str,
    screenshot_paths: Optional[List[str]] = None,
) -> List[FeatureCard]:
    """
    Load prompt extract_features.md, substitute (text, url, screenshot_paths), call LLM,
    parse JSON into list of FeatureCard. On invalid JSON retries once with a reformat hint.
    Marks needs_manual_review=True and logs on final failure.
    """
    # Prompt used: prompts/extract_features.md
    template = load_prompt("extract_features")
    screens_str = json.dumps(screenshot_paths or [], ensure_ascii=False)
    input_vars = {
        "text": text[:30000],  # cap size for API
        "url": source_url,
        "screenshot_paths": screens_str,
    }
    # Prompt may use {text}, {url}, {screenshot_paths} — ensure keys match prompt placeholders
    if "{screenshot_paths}" not in template and "screenshot" in template.lower():
        input_vars["screenshot_paths"] = "\n".join(screenshot_paths or ["(none)"])

    raw_response = call_llm(template, input_vars)

    for attempt in range(2):
        try:
            items = _extract_json_from_response(raw_response)
            cards = []
            for item in items:
                if "evidence_urls" in item and not item["evidence_urls"]:
                    item["evidence_urls"] = [source_url]
                if "competitor" not in item or not item["competitor"]:
                    item["competitor"] = competitor
                if "source_url" not in item or not item["source_url"]:
                    item["source_url"] = source_url
                cards.append(FeatureCard.model_validate(item))
            return cards
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            logger.warning("Feature extraction JSON parse attempt %s failed: %s", attempt + 1, e)
            if attempt == 0:
                # Retry once: ask to return only valid JSON array
                raw_response = call_llm(
                    "Return only a valid JSON array of feature objects, no markdown or extra text. "
                    "Each object must have: competitor, source_url, feature_name, category, short_description, "
                    "raw_mechanics_notes, user_job, target_segment, pricing_tier, evidence_urls (array), "
                    "screenshot_paths (array), launch_date (or null), user_benefits, limitations, "
                    "confidence (0-1), needs_manual_review (boolean).\n\n" + raw_response,
                    {},
                )
            else:
                # Final failure: return a single card that flags manual review
                logger.error("Feature extraction failed for %s %s: %s", competitor, source_url, e)
                return [
                    FeatureCard(
                        competitor=competitor,
                        source_url=source_url,
                        feature_name="(extraction failed)",
                        category="other",
                        short_description="LLM returned invalid JSON; manual review required.",
                        evidence_urls=[source_url],
                        screenshot_paths=list(screenshot_paths or []),
                        confidence=0.0,
                        needs_manual_review=True,
                    )
                ]
    return []
