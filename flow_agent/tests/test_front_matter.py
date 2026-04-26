from src.models.profile import (
    BehaviorPreferences,
    Demographics,
    DeviceProfile,
    HabitSnapshot,
    PreferredCardStyle,
    ProfileSkillDocument,
    SkillDefinition,
)
from src.services.front_matter import parse_front_matter
from src.services.profile_skill_doc import (
    parse_profile_skill_markdown,
    render_profile_skill_markdown,
)


def build_profile_document() -> ProfileSkillDocument:
    return ProfileSkillDocument(
        user_id="u-1",
        persona_version="v1",
        profile_type="skill_like_persona",
        demographics=Demographics(
            education_stage="freshman_sophomore",
            persona_label="低年级技术奖学生",
            major_tendency="计算机相关",
            campus_role="竞赛活跃",
            career_phase="探索期",
            habit_snapshot=HabitSnapshot(
                weekday_routine="晚上搜索技术内容",
                decision_context="先大问题后细化",
                attention_style="结构化总结",
            ),
        ),
        device_profile=DeviceProfile(
            primary_phone="iPhone",
            current_phone_status="有换机意向",
            digital_tendency="数码发烧友",
            tech_stack_interest=["前端开发"],
        ),
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
                skill_id="phone_upgrade",
                name="换机画像",
                intent_type="smartphone_upgrade_decision",
                activation_events=["新机发布"],
                keywords=["iPhone17 怎么选"],
                negative_keywords=["纯开箱"],
                confidence=0.9,
                evidence_refs=["session_01"],
                preferred_card_style=PreferredCardStyle(
                    tone="决策型",
                    information_density="high",
                    default_modules=["对比"],
                    cta=["切换"],
                ),
                interaction_preferences=["参数对比"],
            )
        ],
    )


def test_front_matter_round_trip() -> None:
    document = build_profile_document()
    markdown = render_profile_skill_markdown(document)

    front_matter, body = parse_front_matter(markdown)
    parsed_document = parse_profile_skill_markdown(markdown)

    assert front_matter["user_id"] == "u-1"
    assert "## Skills" in body
    assert parsed_document.user_id == document.user_id
    assert parsed_document.skills[0].skill_id == "phone_upgrade"
