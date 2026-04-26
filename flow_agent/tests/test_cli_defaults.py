from src.agents.extract_profile_skill import build_parser as build_extract_parser
from src.agents.render_push_card import build_parser as build_render_parser
from src.agents.select_push_card import build_parser as build_select_parser
from src.services.paths import DEFAULT_USER_ID


def test_cli_default_user_id() -> None:
    extract_args = build_extract_parser().parse_args([])
    select_args = build_select_parser().parse_args([])
    render_args = build_render_parser().parse_args([])

    assert extract_args.user_id == DEFAULT_USER_ID
    assert select_args.user_id == DEFAULT_USER_ID
    assert render_args.user_id == DEFAULT_USER_ID
