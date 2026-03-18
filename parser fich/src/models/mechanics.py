"""Pydantic schema for mechanics description (output of describe_mechanics.md → LLM)."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


EntityType = Literal["user", "content", "config", "data", "other"]


class EntityObject(BaseModel):
    name: str
    type: EntityType
    description: str = ""


class RolePermission(BaseModel):
    role: str
    actions: list[str] = Field(default_factory=list)


class ScreenshotCommentary(BaseModel):
    screenshot_path: str
    description: str


class MechanicsDescription(BaseModel):
    """Structured mechanics description as returned by describe_mechanics.md → LLM."""

    competitor: str
    feature_name: str
    scenario_summary: str = ""
    mechanics_steps: list[str] = Field(default_factory=list)
    entities_and_objects: list[EntityObject] = Field(default_factory=list)
    roles_and_permissions: list[RolePermission] = Field(default_factory=list)
    config_and_rules: list[str] = Field(default_factory=list)
    system_behaviour: list[str] = Field(default_factory=list)
    ui_and_states: list[str] = Field(default_factory=list)
    screenshot_commentary: list[ScreenshotCommentary] = Field(default_factory=list)
    known_limitations: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    needs_manual_review: bool = False
