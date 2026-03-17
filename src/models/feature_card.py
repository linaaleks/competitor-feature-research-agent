"""Pydantic schema for a single feature extracted from competitor pages."""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


Category = Literal[
    "AI", "analytics", "integrations", "content", "workflow",
    "assessment", "reporting", "authoring", "automation", "other"
]
TargetSegment = Literal["SMB", "mid-market", "enterprise", "individual", "mixed", "unknown"]
PricingTier = Literal[
    "free", "trial", "basic", "pro", "enterprise", "add-on", "usage-based", "unknown"
]


class FeatureCard(BaseModel):
    """Structured feature card as returned by extract_features.md → LLM."""

    competitor: str
    source_url: str
    feature_name: str
    category: Category
    short_description: str = Field(..., min_length=1, max_length=500)
    raw_mechanics_notes: str = ""
    user_job: str = ""
    target_segment: TargetSegment = "unknown"
    pricing_tier: PricingTier = "unknown"
    evidence_urls: list[str] = Field(default_factory=list, min_length=1)
    screenshot_paths: list[str] = Field(default_factory=list)
    launch_date: Optional[str] = None  # YYYY-MM or null
    user_benefits: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    needs_manual_review: bool = False

    @property
    def mechanics_description(self) -> str:
        """Alias for compatibility: detailed mechanics = raw_mechanics_notes until enriched."""
        return self.raw_mechanics_notes or self.short_description
