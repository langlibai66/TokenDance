from __future__ import annotations

from datetime import datetime
from typing import Any
from urllib.parse import urlparse

from src.models.card import NormalizedSearchResult, SearchBundle
from src.utils.bocha_search.api import web_search_batch


class SearchService:
    async def search_bundle(
        self,
        *,
        user_id: str,
        topic: str,
        queries: list[str],
        count: int = 5,
    ) -> SearchBundle:
        results = await web_search_batch(queries, count=count)

        normalized: list[NormalizedSearchResult] = []
        failures: list[str] = []
        for query, payload in zip(queries, results, strict=True):
            if isinstance(payload, Exception):
                failures.append(f"{query}: {payload}")
                continue
            normalized.extend(self._normalize_payload(query, payload))

        deduped = _dedupe_results(normalized)
        return SearchBundle(
            user_id=user_id,
            topic=topic,
            generated_at=datetime.now().isoformat(),
            queries=queries,
            results=deduped,
            failures=failures,
        )

    def _normalize_payload(
        self, query: str, payload: dict[str, Any]
    ) -> list[NormalizedSearchResult]:
        candidates = _collect_candidates(payload)
        normalized: list[NormalizedSearchResult] = []

        for item in candidates:
            title = str(item.get("title") or item.get("name") or "").strip()
            url = str(item.get("url") or item.get("link") or "").strip()
            snippet = str(
                item.get("summary")
                or item.get("snippet")
                or item.get("description")
                or ""
            ).strip()
            if not title or not url:
                continue
            site = _extract_site(url)
            normalized.append(
                NormalizedSearchResult(
                    query=query,
                    title=title,
                    snippet=snippet,
                    url=url,
                    site=site,
                )
            )

        return normalized


def _collect_candidates(node: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []

    if isinstance(node, dict):
        if any(key in node for key in ("title", "name")) and any(
            key in node for key in ("url", "link")
        ):
            found.append(node)
        for value in node.values():
            found.extend(_collect_candidates(value))
    elif isinstance(node, list):
        for item in node:
            found.extend(_collect_candidates(item))

    return found


def _dedupe_results(
    results: list[NormalizedSearchResult],
) -> list[NormalizedSearchResult]:
    seen: set[tuple[str, str]] = set()
    deduped: list[NormalizedSearchResult] = []
    for result in results:
        key = (result.url, result.title)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(result)
    return deduped


def _extract_site(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc or "unknown"
