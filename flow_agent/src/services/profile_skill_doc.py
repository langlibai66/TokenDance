from __future__ import annotations

from src.models.profile import ProfileSkillDocument
from src.services.front_matter import parse_front_matter, render_front_matter


def render_profile_skill_markdown(document: ProfileSkillDocument) -> str:
    front_matter = render_front_matter(document.front_matter_dict())
    body_lines: list[str] = [
        "# Profile Skill",
        "",
        "## Persona",
        "",
        f"- 身份：{document.demographics.persona_label}",
        f"- 学段：{document.demographics.education_stage}",
        f"- 专业倾向：{document.demographics.major_tendency}",
        f"- 校园角色：{document.demographics.campus_role}",
        f"- 当前阶段：{document.demographics.career_phase}",
        "",
        "## Habit Snapshot",
        "",
        f"- 工作日习惯：{document.demographics.habit_snapshot.weekday_routine}",
        f"- 决策方式：{document.demographics.habit_snapshot.decision_context}",
        f"- 注意力偏好：{document.demographics.habit_snapshot.attention_style}",
        "",
        "## Device Profile",
        "",
        f"- 主设备：`{document.device_profile.primary_phone}`",
    ]

    if document.device_profile.current_phone_status:
        body_lines.append(f"- 当前手机状态：{document.device_profile.current_phone_status}")
    if document.device_profile.current_laptop_status:
        body_lines.append(f"- 当前电脑状态：{document.device_profile.current_laptop_status}")
    if document.device_profile.laptop_interest:
        body_lines.append(f"- 设备兴趣：`{document.device_profile.laptop_interest}`")
    if document.device_profile.digital_tendency:
        body_lines.append(f"- 数码倾向：{document.device_profile.digital_tendency}")
    if document.device_profile.tech_stack_interest:
        body_lines.append("- 技术栈兴趣：")
        for item in document.device_profile.tech_stack_interest:
            body_lines.append(f"  - {item}")

    body_lines.extend(["", "## Long-term Interests", ""])
    for interest in document.long_term_interests:
        body_lines.append(f"- {interest.topic}：`{interest.strength}`")
        body_lines.append(f"  - 关键词：{'、'.join(interest.keywords)}")

    body_lines.extend(["", "## Core Goals", ""])
    for item in document.core_goals:
        body_lines.append(f"- {item.goal}")

    body_lines.extend(["", "## Core Concerns", ""])
    for item in document.core_concerns:
        body_lines.append(f"- {item.concern}")

    body_lines.extend(["", "## Behavior Preferences", ""])
    body_lines.append(f"- 搜索模式：{document.behavior_preferences.search_pattern}")
    body_lines.append(
        f"- 内容偏好：{'、'.join(document.behavior_preferences.content_bias)}"
    )
    if document.behavior_preferences.device_decision_bias:
        body_lines.append(
            f"- 数码决策偏好：{document.behavior_preferences.device_decision_bias}"
        )
    body_lines.append(
        f"- 负向偏好：{'、'.join(document.behavior_preferences.negative_bias)}"
    )
    body_lines.append(
        f"- 互动倾向：{'、'.join(document.behavior_preferences.interaction_tendency)}"
    )

    body_lines.extend(["", "## Skills", ""])
    for skill in document.skills:
        body_lines.extend(
            [
                f"### `{skill.skill_id}`",
                "",
                f"- 名称：{skill.name}",
                f"- `intent_type`: `{skill.intent_type}`",
                "- 触发事件：",
            ]
        )
        for event in skill.activation_events:
            body_lines.append(f"  - {event}")
        body_lines.append("- 关键词：")
        for keyword in skill.keywords:
            body_lines.append(f"  - {keyword}")
        body_lines.append("- 负向关键词：")
        for keyword in skill.negative_keywords:
            body_lines.append(f"  - {keyword}")
        body_lines.extend(
            [
                f"- `confidence`: `{skill.confidence}`",
                f"- 证据引用：{', '.join(f'`{item}`' for item in skill.evidence_refs)}",
                "- 推荐卡片风格：",
                f"  - 语气：{skill.preferred_card_style.tone}",
                f"  - 信息密度：{skill.preferred_card_style.information_density}",
                f"  - 默认模块：{'、'.join(skill.preferred_card_style.default_modules)}",
                f"  - CTA：{'、'.join(skill.preferred_card_style.cta)}",
                f"- 互动偏好：{'、'.join(skill.interaction_preferences)}",
                "",
            ]
        )

    return front_matter + "\n\n" + "\n".join(body_lines).rstrip() + "\n"


def parse_profile_skill_markdown(document: str) -> ProfileSkillDocument:
    payload, _ = parse_front_matter(document)
    return ProfileSkillDocument.model_validate(payload)
