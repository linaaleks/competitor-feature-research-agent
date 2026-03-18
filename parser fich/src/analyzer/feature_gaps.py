"""Compare competitor features with our taxonomy. Marks parity / gap / advantage / unknown."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models import FeatureCard

logger = logging.getLogger(__name__)


def compute_feature_gaps(
    features: list,
    our_taxonomy_path: Path | None = None,
) -> list[dict]:
    """
    Compare each competitor feature to our feature matrix (YAML).
    Return list of {feature, status: parity|gap|advantage|unknown}.
    Stub: returns empty list.
    """
    logger.info("Feature gaps (stub): %s features", len(features))
    return []
