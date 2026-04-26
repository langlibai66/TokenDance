from src.agents.select_push_card import PushCardSelectionAgent
from src.models.events import CurrentEvent, CurrentEventContext, EventSignal
from src.models.profile import (
    BehaviorPreferences,
    Demographics,
    DeviceProfile,
    HabitSnapshot,
    PreferredCardStyle,
    ProfileSkillDocument,
    SkillDefinition,
)


def build_profile() -> ProfileSkillDocument:
    return ProfileSkillDocument(
        user_id="user-1",
        persona_version="v1",
        profile_type="skill_like_persona",
        demographics=Demographics(
            education_stage="freshman_sophomore",
            persona_label="测试用户",
            major_tendency="计算机",
            campus_role="学生",
            career_phase="探索期",
            habit_snapshot=HabitSnapshot(
                weekday_routine="晚上刷抖音",
                decision_context="先大问题后细化",
                attention_style="高信息密度",
            ),
        ),
        device_profile=DeviceProfile(primary_phone="iPhone"),
        long_term_interests=[],
        core_goals=[],
        core_concerns=[],
        behavior_preferences=BehaviorPreferences(
            search_pattern="逐步细化",
            content_bias=["对比"],
            negative_bias=["鸡汤"],
            interaction_tendency=["收藏"],
        ),
        skills=[
            SkillDefinition(
                skill_id="phone_upgrade_decision_skill",
                name="换机决策画像",
                intent_type="smartphone_upgrade_decision",
                activation_events=["iPhone17 系列与安卓旗舰横评内容升温"],
                keywords=["iPhone17 怎么选", "安卓旗舰对比"],
                negative_keywords=["纯开箱"],
                confidence=0.91,
                evidence_refs=["session_phone"],
                preferred_card_style=PreferredCardStyle(
                    tone="决策型",
                    information_density="high",
                    default_modules=["对比"],
                    cta=["切换"],
                ),
                interaction_preferences=["参数对比"],
            ),
            SkillDefinition(
                skill_id="world_cup_france_skill",
                name="法国队画像",
                intent_type="match_preview",
                activation_events=["法国队大名单内容升温"],
                keywords=["法国队首发"],
                negative_keywords=["混剪"],
                confidence=0.76,
                evidence_refs=["session_sports"],
                preferred_card_style=PreferredCardStyle(
                    tone="速看型",
                    information_density="medium",
                    default_modules=["看点"],
                    cta=["切换"],
                ),
                interaction_preferences=["阵容切换"],
            ),
        ],
    )


def test_score_skill_prefers_phone_upgrade() -> None:
    agent = PushCardSelectionAgent(llm_service=None)
    current_event = CurrentEvent(
        user_id="user-1",
        observed_at="2026-09-18T21:20:00+08:00",
        time_slot="late_evening",
        context=CurrentEventContext(location_type="campus_dorm", device="iphone"),
        event_signals=[
            EventSignal(
                type="platform_heat_rise",
                topic="iPhone17 系列与安卓旗舰横评内容升温",
                strength=0.93,
                why_now="大量新机横评和换机决策内容同时出现",
            )
        ],
    )
    profile = build_profile()

    scores = {
        skill.skill_id: agent._score_skill(skill, current_event) for skill in profile.skills
    }

    assert (
        scores["phone_upgrade_decision_skill"]
        > scores["world_cup_france_skill"]
    )
