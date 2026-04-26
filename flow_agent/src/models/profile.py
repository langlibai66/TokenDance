from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class HabitSnapshot(BaseModel):
    weekday_routine: str
    decision_context: str
    attention_style: str


class Demographics(BaseModel):
    education_stage: str
    persona_label: str
    major_tendency: str
    campus_role: str
    career_phase: str
    habit_snapshot: HabitSnapshot


class DeviceProfile(BaseModel):
    primary_phone: str
    current_phone_status: str | None = None
    current_laptop_status: str | None = None
    laptop_interest: str | None = None
    digital_tendency: str | None = None
    tech_stack_interest: list[str] = Field(default_factory=list)


class LongTermInterest(BaseModel):
    topic: str
    strength: float
    keywords: list[str] = Field(default_factory=list)


class GoalItem(BaseModel):
    goal: str
    priority: str | None = None


class ConcernItem(BaseModel):
    concern: str
    severity: str | None = None


class BehaviorPreferences(BaseModel):
    search_pattern: str
    content_bias: list[str] = Field(default_factory=list)
    negative_bias: list[str] = Field(default_factory=list)
    interaction_tendency: list[str] = Field(default_factory=list)
    device_decision_bias: str | None = None


class PreferredCardStyle(BaseModel):
    tone: str
    information_density: str
    default_modules: list[str] = Field(default_factory=list)
    cta: list[str] = Field(default_factory=list)


class SkillDefinition(BaseModel):
    skill_id: str
    name: str
    intent_type: str
    activation_events: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    negative_keywords: list[str] = Field(default_factory=list)
    confidence: float
    evidence_refs: list[str] = Field(default_factory=list)
    preferred_card_style: PreferredCardStyle
    interaction_preferences: list[str] = Field(default_factory=list)


class ProfileSkillDocument(BaseModel):
    user_id: str
    persona_version: str
    profile_type: str
    demographics: Demographics
    device_profile: DeviceProfile
    long_term_interests: list[LongTermInterest] = Field(default_factory=list)
    core_goals: list[GoalItem] = Field(default_factory=list)
    core_concerns: list[ConcernItem] = Field(default_factory=list)
    behavior_preferences: BehaviorPreferences
    skills: list[SkillDefinition] = Field(default_factory=list)

    def front_matter_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json", exclude_none=True)
