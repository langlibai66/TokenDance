from pathlib import Path

from src.agents.extract_profile_skill import ProfileSkillExtractionAgent
from src.agents.render_push_card import PushCardRenderAgent
from src.models.card import CardBrief, CardSection, CardSource, CardSpec
from src.models.profile import (
    BehaviorPreferences,
    ConcernItem,
    Demographics,
    DeviceProfile,
    GoalItem,
    HabitSnapshot,
    LongTermInterest,
    PreferredCardStyle,
    ProfileSkillDocument,
    SkillDefinition,
)
from src.services.io import save_json


class FakeLLMForExtract:
    async def call_json(self, **kwargs):
        return ProfileSkillDocument(
            user_id="college_tech_award_student_001",
            persona_version="test-v1",
            profile_type="skill_like_persona",
            demographics=Demographics(
                education_stage="freshman_sophomore",
                persona_label="低年级技术奖学生",
                major_tendency="计算机相关",
                campus_role="竞赛活跃",
                career_phase="探索期",
                habit_snapshot=HabitSnapshot(
                    weekday_routine="白天上课，晚上刷技术内容",
                    decision_context="先大后小",
                    attention_style="信息密度高",
                ),
            ),
            device_profile=DeviceProfile(primary_phone="iPhone"),
            long_term_interests=[
                LongTermInterest(topic="换机决策", strength=0.9, keywords=["iPhone17"])
            ],
            core_goals=[GoalItem(goal="做出正确换机决策")],
            core_concerns=[ConcernItem(concern="容易在型号间纠结")],
            behavior_preferences=BehaviorPreferences(
                search_pattern="逐步细化",
                content_bias=["对比"],
                negative_bias=["纯开箱"],
                interaction_tendency=["收藏"],
            ),
            skills=[
                SkillDefinition(
                    skill_id="phone_upgrade_decision_skill",
                    name="换机决策画像",
                    intent_type="smartphone_upgrade_decision",
                    activation_events=["iPhone17 升温"],
                    keywords=["iPhone17 怎么选"],
                    negative_keywords=["纯开箱"],
                    confidence=0.91,
                    evidence_refs=["session_05_phone_upgrade_decision"],
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


class FakeLLMForRender:
    async def call_json(self, **kwargs):
        return CardSpec(
            card_id="iphone17-upgrade-card",
            user_id="college_tech_award_student_001",
            topic="iPhone17 换机",
            headline="iPhone17 先别急着冲 Pro Max",
            subheadline="如果你在 Air、Pro 和 Pro Max 之间纠结，先看使用场景和续航。",
            why_now="平台里的横评和换机内容都在升温，这时最需要一个直接结论。",
            sections=[
                CardSection(
                    kind="comparison",
                    title="该怎么选",
                    items=["Air 适合轻薄优先", "Pro 适合均衡党", "Pro Max 适合续航党"],
                )
            ],
            quick_actions=["只看 Air", "加入安卓备选"],
            sources=[
                CardSource(
                    title="iPhone17 系列对比",
                    url="https://example.com/iphone17",
                    site="example.com",
                ),
                CardSource(
                    title="安卓旗舰横评",
                    url="https://example.com/android",
                    site="example.com",
                ),
            ],
            theme="tech",
            aspect_ratio="9:16",
        )


class FakeSearchService:
    async def search_bundle(self, *, user_id, topic, queries, count=5):
        from src.models.card import NormalizedSearchResult, SearchBundle

        return SearchBundle(
            user_id=user_id,
            topic=topic,
            generated_at="2026-01-01T00:00:00",
            queries=queries,
            results=[
                NormalizedSearchResult(
                    query=queries[0],
                    title="iPhone17 系列对比",
                    snippet="全系定位分析",
                    url="https://example.com/iphone17",
                    site="example.com",
                ),
                NormalizedSearchResult(
                    query=queries[-1],
                    title="安卓旗舰横评",
                    snippet="跨品牌对比",
                    url="https://example.com/android",
                    site="example.com",
                ),
            ],
            failures=[],
        )


def test_extract_profile_skill_agent_writes_markdown(tmp_path: Path) -> None:
    output_dir = tmp_path / "output"
    agent = ProfileSkillExtractionAgent(llm_service=FakeLLMForExtract())

    input_path = Path(__file__).resolve().parents[2] / "dataset" / "users" / "college_tech_award_student_001" / "event_search_log.json"

    import asyncio

    output_path = asyncio.run(agent.run(input_path=input_path, output_dir=output_dir))

    text = output_path.read_text(encoding="utf-8")
    assert output_path.name == "profile_skill.md"
    assert text.startswith("---\n{")
    assert "phone_upgrade_decision_skill" in text


def test_render_push_card_agent_writes_html(tmp_path: Path) -> None:
    output_dir = tmp_path / "output"
    brief_path = output_dir / "selected_card_brief.json"
    save_json(
        brief_path,
        CardBrief(
            user_id="college_tech_award_student_001",
            status="selected",
            selected_skill_id="phone_upgrade_decision_skill",
            trigger_score=0.93,
            trigger_reason="手机换机内容升温",
            push_topic="iPhone17 系列怎么选",
            card_goal="给出换机建议",
            freshness_required=True,
            search_queries_seed=["iPhone17 系列怎么选", "iPhone17 Air 17 Pro 区别"],
            section_hints=["comparison", "key_points"],
            style_hints={"theme": "tech"},
        ).model_dump(mode="json"),
    )

    agent = PushCardRenderAgent(
        llm_service=FakeLLMForRender(),
        search_service=FakeSearchService(),
    )

    import asyncio

    html_path = asyncio.run(agent.run(brief_path=brief_path, output_dir=output_dir))

    assert html_path.name.endswith(".html")
    assert "iPhone17 先别急着冲 Pro Max" in html_path.read_text(encoding="utf-8")
