"""
Deep mechanics description for a single feature using LLM.
Uses prompt: prompts/describe_mechanics.md → output validated as MechanicsDescription.
"""
from __future__ import annotations

import json
import logging
import re
from typing import TYPE_CHECKING, List, Optional

from src.llm import load_prompt, call_llm
from src.models import FeatureCard, MechanicsDescription

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


def _extract_json_object(raw: str) -> dict:
    """Extract a single JSON object from LLM response (may be wrapped in markdown)."""
    raw = raw.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```\s*$", "", raw)
    return json.loads(raw)


def describe_mechanics(
    feature_card: FeatureCard,
    extra_context: str = "",
    screenshot_paths: Optional[List[str]] = None,
) -> MechanicsDescription:
    """
    Load prompt describe_mechanics.md, substitute feature card JSON, extra_context, screenshot_paths,
    call LLM, parse JSON into MechanicsDescription.
    """
    # Prompt used: prompts/describe_mechanics.md
    template = load_prompt("describe_mechanics")
    card_json = feature_card.model_dump_json(indent=0)
    screens_str = "\n".join(screenshot_paths or [])
    input_vars = {
        "feature_card_json": card_json,
        "extra_context": extra_context or "(нет дополнительного контекста)",
        "screenshot_paths": screens_str or "(нет скриншотов)",
    }
    raw_response = call_llm(template, input_vars)
    try:
        data = _extract_json_object(raw_response)
        if "competitor" not in data:
            data["competitor"] = feature_card.competitor
        if "feature_name" not in data:
            data["feature_name"] = feature_card.feature_name
        return MechanicsDescription.model_validate(data)
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        logger.warning("Mechanics description parse failed for %s: %s", feature_card.feature_name, e)
        return MechanicsDescription(
            competitor=feature_card.competitor,
            feature_name=feature_card.feature_name,
            scenario_summary="(не удалось извлечь описание механики)",
            mechanics_steps=[],
            confidence=0.0,
            needs_manual_review=True,
        )
