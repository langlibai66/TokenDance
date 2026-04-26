from __future__ import annotations

import argparse
import asyncio
import json
from datetime import datetime
from pathlib import Path

from src.models.card import CardBrief, CardSpec
from src.services.html_renderer import render_card_html
from src.services.io import load_json, save_json, save_text
from src.services.llm import AsyncLLMService
from src.services.paths import default_output_dir
from src.services.search import SearchService
from src.services.text_utils import slugify


class PushCardRenderAgent:
    def __init__(
        self,
        llm_service: AsyncLLMService | None = None,
        search_service: SearchService | None = None,
    ) -> None:
        self.llm = llm_service or AsyncLLMService()
        self.search = search_service or SearchService()

    async def run(self, *, brief_path: Path, output_dir: Path) -> Path:
        brief = CardBrief.model_validate(load_json(brief_path))
        if brief.status != "selected":
            raise ValueError("Card brief status is not selected; render step aborted")

        queries = self._build_queries(brief)
        search_bundle = await self.search.search_bundle(
            user_id=brief.user_id,
            topic=brief.push_topic or "push-card",
            queries=queries,
        )
        if len(search_bundle.results) < 2:
            raise ValueError("Search results are insufficient to build a factual card")

        card_spec = await self._build_card_spec(brief, search_bundle)
        html = render_card_html(card_spec)

        save_json(output_dir / "search_bundle.json", search_bundle.model_dump(mode="json"))
        save_json(output_dir / "card_spec.json", card_spec.model_dump(mode="json"))

        file_name = f"{slugify(card_spec.card_id)}.html"
        html_path = output_dir / file_name
        save_text(html_path, html)
        return html_path

    def _build_queries(self, brief: CardBrief) -> list[str]:
        queries: list[str] = []
        for query in brief.search_queries_seed:
            cleaned = query.strip()
            if cleaned and cleaned not in queries:
                queries.append(cleaned)

        if brief.push_topic and brief.push_topic not in queries:
            queries.append(brief.push_topic)

        if brief.card_goal:
            candidate = f"{brief.push_topic} {brief.card_goal}" if brief.push_topic else brief.card_goal
            if candidate not in queries:
                queries.append(candidate)

        return queries[:5]

    async def _build_card_spec(self, brief: CardBrief, search_bundle) -> CardSpec:
        system_prompt = (
            "你是竖版信息流卡片生成器。"
            "请基于推送主题和搜索结果，输出严格 JSON。"
            "不要输出 HTML，不要输出代码块。"
            "section.kind 只能使用 key_points、comparison、steps、watchlist。"
            "theme 只能使用 tech、sports、study、default。"
            "aspect_ratio 固定写 9:16。"
        )
        user_prompt = (
            "请根据下面信息输出 CardSpec JSON。\n"
            "要求：\n"
            "1. headline 一眼看懂，subheadline 不要重复 headline。\n"
            "2. why_now 必须解释此刻为什么该推这张卡。\n"
            "3. sections 保持 2 到 3 组，每组最多 4 条。\n"
            "4. quick_actions 保持 2 到 3 个短动作。\n"
            "5. sources 只保留 2 到 4 条高相关来源。\n"
            "6. 主题如果是数码或技术，优先用 tech；如果是赛事，优先用 sports；学习成长类优先用 study。\n\n"
            f"generated_at: {datetime.now().isoformat()}\n"
            f"card_brief:\n{json.dumps(brief.model_dump(mode='json'), ensure_ascii=False, indent=2)}\n\n"
            f"search_bundle:\n{json.dumps(search_bundle.model_dump(mode='json'), ensure_ascii=False, indent=2)}"
        )
        return await self.llm.call_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model_cls=CardSpec,
            retries=1,
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render push card html")
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--brief", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    return parser


async def _async_main() -> None:
    args = build_parser().parse_args()
    output_dir = args.output_dir or default_output_dir(args.user_id)
    brief_path = args.brief or output_dir / "selected_card_brief.json"
    agent = PushCardRenderAgent()
    output_path = await agent.run(brief_path=brief_path, output_dir=output_dir)
    print(output_path)


def main() -> None:
    asyncio.run(_async_main())


if __name__ == "__main__":
    main()
