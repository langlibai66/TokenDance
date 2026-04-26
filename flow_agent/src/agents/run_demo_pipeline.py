from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from src.agents.extract_profile_skill import ProfileSkillExtractionAgent
from src.agents.render_push_card import PushCardRenderAgent
from src.agents.select_push_card import PushCardSelectionAgent
from src.services.paths import (
    DEFAULT_USER_ID,
    default_current_event_path,
    default_output_dir,
    default_user_event_log_path,
)


async def run_pipeline(
    *,
    user_id: str,
    input_path: Path,
    current_event_path: Path,
    output_dir: Path,
) -> Path:
    profile_path = await ProfileSkillExtractionAgent().run(
        input_path=input_path,
        output_dir=output_dir,
    )
    brief_path = await PushCardSelectionAgent().run(
        profile_skill_path=profile_path,
        current_event_path=current_event_path,
        output_dir=output_dir,
    )
    html_path = await PushCardRenderAgent().run(
        brief_path=brief_path,
        output_dir=output_dir,
    )
    return html_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the full demo pipeline with default sample data"
    )
    parser.add_argument("--user-id", default=DEFAULT_USER_ID)
    parser.add_argument("--input", type=Path, default=None)
    parser.add_argument("--current-event", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    return parser


async def _async_main() -> None:
    args = build_parser().parse_args()
    user_id = args.user_id
    input_path = args.input or default_user_event_log_path(user_id)
    current_event_path = args.current_event or default_current_event_path()
    output_dir = args.output_dir or default_output_dir(user_id)
    html_path = await run_pipeline(
        user_id=user_id,
        input_path=input_path,
        current_event_path=current_event_path,
        output_dir=output_dir,
    )
    print(html_path)


def main() -> None:
    asyncio.run(_async_main())


if __name__ == "__main__":
    main()
