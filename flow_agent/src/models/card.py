from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class CardBrief(BaseModel):
    user_id: str
    status: Literal["selected", "no_card"] = "selected"
    selected_skill_id: str | None = None
    trigger_score: float | None = None
    trigger_reason: str
    push_topic: str | None = None
    card_goal: str | None = None
    freshness_required: bool = False
    search_queries_seed: list[str] = Field(default_factory=list)
    section_hints: list[str] = Field(default_factory=list)
    style_hints: dict[str, str] = Field(default_factory=dict)


class NormalizedSearchResult(BaseModel):
    query: str
    title: str
    snippet: str
    url: str
    site: str


class SearchBundle(BaseModel):
    user_id: str
    topic: str
    generated_at: str
    queries: list[str] = Field(default_factory=list)
    results: list[NormalizedSearchResult] = Field(default_factory=list)
    failures: list[str] = Field(default_factory=list)


class CardSection(BaseModel):
    kind: Literal["key_points", "comparison", "steps", "watchlist"]
    title: str
    items: list[str] = Field(default_factory=list)


class CardSource(BaseModel):
    title: str
    url: str
    site: str


class CardSpec(BaseModel):
    card_id: str
    user_id: str
    topic: str
    headline: str
    subheadline: str
    why_now: str
    sections: list[CardSection] = Field(default_factory=list)
    quick_actions: list[str] = Field(default_factory=list)
    sources: list[CardSource] = Field(default_factory=list)
    theme: str = "default"
    aspect_ratio: str = "9:16"
