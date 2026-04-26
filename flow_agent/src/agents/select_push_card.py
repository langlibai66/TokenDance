from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from src.models.card import CardBrief
from src.models.events import CurrentEvent
from src.models.profile import ProfileSkillDocument, SkillDefinition
from src.services.io import load_json, save_json
from src.services.llm import AsyncLLMService
from src.services.paths import default_current_event_path, default_output_dir
from src.services.profile_skill_doc import parse_profile_skill_markdown
from src.services.text_utils import extract_tokens

MIN_TRIGGER_SCORE = 0.3


class PushCardSelectionAgent:
    def __init__(self, llm_service: AsyncLLMService | None = None) -> None:
        self.llm = llm_service or AsyncLLMService()

    async def run(
        self,
        *,
        profile_skill_path: Path,
        current_event_path: Path,
        output_dir: Path,
    ) -> Path:
        profile = parse_profile_skill_markdown(profile_skill_path.read_text(encoding="utf-8"))
        current_event = CurrentEvent.model_validate(load_json(current_event_path))
        brief = await self._select_card(profile, current_event)
        output_path = output_dir / "selected_card_brief.json"
        save_json(output_path, brief.model_dump(mode="json"))
        return output_path

    async def _select_card(
        self, profile: ProfileSkillDocument, current_event: CurrentEvent
    ) -> CardBrief:
        ranked = sorted(
            (
                (skill, self._score_skill(skill, current_event))
                for skill in profile.skills
            ),
            key=lambda item: item[1],
            reverse=True,
        )

        if not ranked or ranked[0][1] < MIN_TRIGGER_SCORE:
            return CardBrief(
                user_id=profile.user_id,
                status="no_card",
                trigger_reason="当前事件与已有技能画像匹配度不足，暂不推送。",
            )

        top_candidates = [
            {
                "skill_id": skill.skill_id,
                "name": skill.name,
                "intent_type": skill.intent_type,
                "heuristic_score": round(score, 3),
                "activation_events": skill.activation_events,
                "keywords": skill.keywords,
                "preferred_card_style": skill.preferred_card_style.model_dump(mode="json"),
            }
            for skill, score in ranked[:3]
        ]

        system_prompt = (
            "你是信息流卡片触发决策器。"
            "请从候选 skill 中选择当前最该推的一张卡。"
            "输出严格 JSON，不要解释，不要输出代码块。"
            "如果不适合推送，则 status 设为 no_card。"
        )
        user_prompt = (
            "请根据 current_event 和 top candidates，输出 CardBrief JSON。\n"
            "要求：\n"
            "1. status 只能是 selected 或 no_card。\n"
            "2. selected 时必须填写 selected_skill_id、push_topic、card_goal、search_queries_seed、section_hints。\n"
            "3. 只输出一张主卡。\n"
            "4. search_queries_seed 保持 3 到 5 条，便于后续在线搜索。\n"
            "5. style_hints 只保留简单键值，如 theme、tone、density。\n\n"
            f"profile_user_id: {profile.user_id}\n"
            f"current_event:\n{json.dumps(current_event.model_dump(mode='json'), ensure_ascii=False, indent=2)}\n\n"
            f"top_candidates:\n{json.dumps(top_candidates, ensure_ascii=False, indent=2)}"
        )

        brief = await self.llm.call_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model_cls=CardBrief,
            retries=1,
        )
        if brief.status == "selected" and not brief.selected_skill_id:
            raise ValueError("Selected card brief is missing selected_skill_id")
        return brief

    def _score_skill(self, skill: SkillDefinition, current_event: CurrentEvent) -> float:
        score = skill.confidence * 0.35
        reference_texts = skill.activation_events + skill.keywords

        for signal in current_event.event_signals:
            signal_text = f"{signal.topic} {signal.why_now}"
            signal_tokens = extract_tokens(signal_text)
            best_match = 0.0
            for reference in reference_texts:
                reference_lower = reference.lower()
                signal_lower = signal_text.lower()
                if reference_lower in signal_lower or signal_lower in reference_lower:
                    best_match = max(best_match, 1.0)
                    continue
                reference_tokens = extract_tokens(reference)
                overlap = signal_tokens & reference_tokens
                if overlap:
                    token_score = len(overlap) / max(len(reference_tokens), 1)
                    best_match = max(best_match, min(token_score, 1.0))
            score += best_match * signal.strength * 0.65

        return min(score, 1.0)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Select top-1 push card")
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--profile-skill", type=Path, default=None)
    parser.add_argument("--current-event", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    return parser


async def _async_main() -> None:
    args = build_parser().parse_args()
    output_dir = args.output_dir or default_output_dir(args.user_id)
    profile_skill_path = args.profile_skill or output_dir / "profile_skill.md"
    current_event_path = args.current_event or default_current_event_path()
    agent = PushCardSelectionAgent()
    output_path = await agent.run(
        profile_skill_path=profile_skill_path,
        current_event_path=current_event_path,
        output_dir=output_dir,
    )
    print(output_path)


def main() -> None:
    asyncio.run(_async_main())


if __name__ == "__main__":
    main()
