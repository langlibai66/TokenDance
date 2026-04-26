from __future__ import annotations

import re


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE).strip().lower()
    slug = re.sub(r"[-\s]+", "-", cleaned)
    return slug or "card"


def extract_tokens(text: str) -> set[str]:
    ascii_tokens = re.findall(r"[A-Za-z0-9][A-Za-z0-9.+_-]*", text.lower())
    chinese_chunks = re.findall(r"[\u4e00-\u9fff]{2,}", text)
    tokens = set(ascii_tokens)
    for chunk in chinese_chunks:
        tokens.add(chunk)
        if len(chunk) > 2:
            for idx in range(len(chunk) - 1):
                tokens.add(chunk[idx : idx + 2])
    return {token for token in tokens if token}
