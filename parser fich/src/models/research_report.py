"""Models for research report and competitor list."""
from __future__ import annotations

from pydantic import BaseModel


class Competitor(BaseModel):
    name: str
    url: str
    short_description: str = ""


class ResearchReport(BaseModel):
    topic: str
    competitors: list[Competitor] = []
    # Filled by reporter from features + mechanics
    feature_matrix: list[dict] = []
    mechanics_section: list[dict] = []
    gaps_and_opportunities: list[str] = []
