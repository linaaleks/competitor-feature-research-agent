"""Find competitors by topic. Interface for search + product hubs; currently stub with sample data."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from src.models import Competitor

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


def find_competitors(topic: str, limit: int = 10) -> list[Competitor]:
    """
    Return list of competitors for the given topic.
    Sources: search results + product hubs (extensible). Currently returns stub data for e2e.
    """
    # Stub: predefined list for "EdTech blue-collar training" style topics
    stub_competitors = [
        Competitor(
            name="Axonify",
            url="https://www.axonify.com",
            short_description="Workforce training and microlearning platform.",
        ),
        Competitor(
            name="TalentLMS",
            url="https://www.talentlms.com",
            short_description="LMS for training and onboarding.",
        ),
    ]
    logger.info("Competitor finder (stub): topic=%s, returning %s competitors", topic, len(stub_competitors))
    return stub_competitors[:limit]
