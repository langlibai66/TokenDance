from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
from typing import Any

from src.models.events import EventSearchLog
from src.models.profile import ProfileSkillDocument
from src.services.io import load_json, save_text
from src.services.llm import AsyncLLMService
from src.services.paths import (
    DEFAULT_USER_ID,
    default_output_dir,
    default_user_event_log_path,
)
from src.services.profile_skill_doc import render_profile_skill_markdown


class ProfileSkillExtractionAgent:
    def __init__(self, llm_service: AsyncLLMService | None = None) -> None:
        self.llm = llm_service or AsyncLLMService()

    async def run(self, *, input_path: Path, output_dir: Path) -> Path:
        event_log = EventSearchLog.model_validate(load_json(input_path))
        signal_bundle = self._build_signal_bundle(event_log)
        document = await self._extract_profile_document(signal_bundle)
        markdown = render_profile_skill_markdown(document)
        output_path = output_dir / "profile_skill.md"
        save_text(output_path, markdown)
        return output_path

    def _build_signal_bundle(self, event_log: EventSearchLog) -> dict[str, Any]:
        session_summaries = []
        repeated_topics: dict[str, int] = {}

        for session in event_log.sessions:
            positive_tags: list[str] = []
            negative_tags: list[str] = []
            top_results: list[str] = []

            for item in session.result_impressions:
                if item.interaction.clicked and (
                    item.interaction.collected
                    or item.interaction.completion_rate >= 0.75
                    or item.interaction.watch_duration_sec >= 45
                ):
                    top_results.append(item.title)
                    positive_tags.extend(item.topic_tags)
                if item.interaction.skip_reason:
                    negative_tags.extend(item.topic_tags)

            for tag in positive_tags:
                repeated_topics[tag] = repeated_topics.get(tag, 0) + 1

            session_summaries.append(
                {
                    "session_id": session.session_id,
                    "trigger_event": session.trigger_event.model_dump(mode="json"),
                    "queries": [step.model_dump(mode="json") for step in session.search_chain],
                    "preferred_angles": session.derived_evidence.preferred_angles,
                    "rejected_angles": session.derived_evidence.rejected_angles,
                    "top_results": top_results[:3],
                    "positive_tags": sorted(set(positive_tags)),
                    "negative_tags": sorted(set(negative_tags)),
                    "top_signal": session.interaction_summary.top_signal,
                    "session_outcome": session.interaction_summary.session_outcome,
                }
            )

        repeated_interests = [
            {"topic": topic, "count": count}
            for topic, count in sorted(
                repeated_topics.items(), key=lambda item: (-item[1], item[0])
            )
            if count >= 2
        ]

        return {
            "user_id": event_log.user_id,
            "persona_version": event_log.log_version,
            "session_count": len(event_log.sessions),
            "session_summaries": session_summaries,
            "repeated_interests": repeated_interests,
        }

    async def _extract_profile_document(
        self, signal_bundle: dict[str, Any]
    ) -> ProfileSkillDocument:
        system_prompt = (
            "你是一个用户画像抽取器。"
            "请基于用户的搜索与浏览事件，输出严格 JSON。"
            "不要输出 Markdown，不要解释，不要添加代码块。"
            "字段必须与给定 schema 对齐，语言使用简体中文。"
            "skills 数量应与 session 数量一致，evidence_refs 必须引用现有 session_id。"
        )
        user_prompt = (
            "请根据下面的 signal bundle 生成 ProfileSkillDocument JSON。\n"
            "要求：\n"
            "1. profile_type 固定为 skill_like_persona。\n"
            "2. persona_version 使用 signal bundle 的 persona_version。\n"
            "3. core_goals 和 core_concerns 保持聚焦，不要空泛。\n"
            "4. skills 字段只包含高价值技能画像。\n"
            "5. keywords 和 negative_keywords 尽量可直接用于搜索和卡片生成。\n"
            "6. confidence 为 0 到 1 的小数。\n\n"
            f"signal_bundle:\n{json.dumps(signal_bundle, ensure_ascii=False, indent=2)}"
        )
        return await self.llm.call_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model_cls=ProfileSkillDocument,
            retries=1,
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract profile skill markdown")
    parser.add_argument("--user-id", default=DEFAULT_USER_ID)
    parser.add_argument("--input", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    return parser


async def _async_main() -> None:
    args = build_parser().parse_args()
    input_path = args.input or default_user_event_log_path(args.user_id)
    output_dir = args.output_dir or default_output_dir(args.user_id)
    agent = ProfileSkillExtractionAgent()
    output_path = await agent.run(input_path=input_path, output_dir=output_dir)
    print(output_path)


def main() -> None:
    asyncio.run(_async_main())


if __name__ == "__main__":
    main()
