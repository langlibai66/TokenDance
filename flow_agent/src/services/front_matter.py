from __future__ import annotations

import json


class FrontMatterError(ValueError):
    pass


def render_front_matter(payload: dict) -> str:
    # JSON is valid YAML 1.2, so this satisfies the YAML front matter requirement
    return f"---\n{json.dumps(payload, ensure_ascii=False, indent=2)}\n---"


def parse_front_matter(document: str) -> tuple[dict, str]:
    if not document.startswith("---\n"):
        raise FrontMatterError("Document does not start with front matter delimiter")

    end_marker = "\n---\n"
    end_index = document.find(end_marker, 4)
    if end_index == -1:
        raise FrontMatterError("Closing front matter delimiter not found")

    front_matter = document[4:end_index]
    body = document[end_index + len(end_marker) :]

    try:
        payload = json.loads(front_matter)
    except json.JSONDecodeError as exc:
        raise FrontMatterError(f"Failed to parse front matter JSON: {exc}") from exc

    return payload, body
