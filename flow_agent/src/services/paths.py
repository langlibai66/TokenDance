from __future__ import annotations

from pathlib import Path


def flow_agent_root() -> Path:
    return Path(__file__).resolve().parents[2]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def default_user_event_log_path(user_id: str) -> Path:
    return repo_root() / "dataset" / "users" / user_id / "event_search_log.json"


def default_current_event_path() -> Path:
    return flow_agent_root() / "data" / "current_event.json"


def default_output_dir(user_id: str) -> Path:
    return flow_agent_root() / "output" / "users" / user_id
