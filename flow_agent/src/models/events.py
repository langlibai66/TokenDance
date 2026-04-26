from __future__ import annotations

from pydantic import BaseModel, Field


class SearchInteraction(BaseModel):
    clicked: bool
    watch_duration_sec: int = 0
    completion_rate: float = 0.0
    liked: bool = False
    collected: bool = False
    shared: bool = False
    replayed: bool = False
    skip_reason: str = ""
    followup_action: str = "none"


class SearchResultImpression(BaseModel):
    rank: int
    video_id: str
    title: str
    topic_tags: list[str] = Field(default_factory=list)
    creator_type: str
    content_angle: str
    duration_sec: int
    interaction: SearchInteraction


class SearchChainStep(BaseModel):
    step: int
    query: str
    intent_label: str
    query_source: str


class TriggerEvent(BaseModel):
    event_type: str
    event_name: str
    event_time: str
    why_now: str


class ContextSnapshot(BaseModel):
    location_type: str
    time_slot: str
    device: str
    mood: str
    urgency: str


class InteractionSummary(BaseModel):
    top_signal: str
    avoided_signal: str
    next_query: str
    session_outcome: str


class DerivedEvidence(BaseModel):
    preferred_angles: list[str] = Field(default_factory=list)
    rejected_angles: list[str] = Field(default_factory=list)
    confidence_delta: float = 0.0


class SearchSession(BaseModel):
    session_id: str
    trigger_event: TriggerEvent
    context_snapshot: ContextSnapshot
    search_chain: list[SearchChainStep] = Field(default_factory=list)
    result_impressions: list[SearchResultImpression] = Field(default_factory=list)
    interaction_summary: InteractionSummary
    derived_evidence: DerivedEvidence


class EventSearchLog(BaseModel):
    user_id: str
    timezone: str
    log_version: str
    sessions: list[SearchSession] = Field(default_factory=list)


class EventSignal(BaseModel):
    type: str
    topic: str
    strength: float
    why_now: str


class CurrentEventContext(BaseModel):
    location_type: str | None = None
    device: str | None = None
    day_type: str | None = None
    note: str | None = None


class CurrentEvent(BaseModel):
    user_id: str
    observed_at: str
    time_slot: str
    context: CurrentEventContext = Field(default_factory=CurrentEventContext)
    event_signals: list[EventSignal] = Field(default_factory=list)
