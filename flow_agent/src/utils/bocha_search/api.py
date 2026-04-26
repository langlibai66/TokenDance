from __future__ import annotations

import asyncio
from typing import Any

import aiohttp

from src.config.env import settings


class BochaAPIError(RuntimeError):
    """Bocha API 请求错误"""


async def web_search(
    query: str,
    *,
    summary: bool = True,
    count: int = 10,
    api_key: str | None = None,
    timeout: int = 30,
    include: str | None = None,
) -> dict[str, Any]:
    """
    单个查询

    Args:
        query: 搜索查询
        summary: 是否返回摘要
        count: 返回结果数量
        api_key: API key (默认从 settings.BOCHA_API_KEY 读取)
        timeout: 超时时间(秒)
        include: 限制搜索的域名范围，多个域名使用|或,分隔

    Returns:
        API 响应的 JSON 数据

    Raises:
        BochaAPIError: API 请求失败时抛出
    """
    key = api_key or settings.BOCHA_API_KEY

    timeout_config = aiohttp.ClientTimeout(total=float(timeout))
    async with aiohttp.ClientSession(timeout=timeout_config) as session:
        return await _make_request(
            session=session,
            query=query,
            summary=summary,
            count=count,
            api_key=key,
            include=include,
        )


async def web_search_batch(
    queries: list[str],
    *,
    summary: bool = True,
    count: int = 10,
    api_key: str | None = None,
    timeout: int = 30,
    max_concurrent: int = 5,
    include: str | None = None,
) -> list[dict[str, Any] | Exception]:
    """
    批量查询 (并发执行)

    Args:
        queries: 查询列表
        summary: 是否返回摘要
        count: 返回结果数量
        api_key: API key (默认从 settings.BOCHA_API_KEY 读取)
        timeout: 超时时间(秒)
        max_concurrent: 最大并发数
        include: 限制搜索的域名范围，多个域名使用|或,分隔

    Returns:
        响应列表，顺序与输入 queries 对应。如果某个查询失败，对应位置为 Exception 对象
    """
    key = api_key or settings.BOCHA_API_KEY
    semaphore = asyncio.Semaphore(max_concurrent)

    timeout_config = aiohttp.ClientTimeout(total=float(timeout))
    async with aiohttp.ClientSession(timeout=timeout_config) as session:

        async def _search_with_limit(q: str) -> dict[str, Any]:
            async with semaphore:
                return await _make_request(
                    session=session,
                    query=q,
                    summary=summary,
                    count=count,
                    api_key=key,
                    include=include,
                )

        tasks = [_search_with_limit(q) for q in queries]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return list(results)


async def _make_request(
    *,
    session: aiohttp.ClientSession,
    query: str,
    summary: bool,
    count: int,
    api_key: str,
    include: str | None = None,
) -> dict[str, Any]:
    """
    执行实际的 HTTP 请求

    Args:
        session: aiohttp ClientSession
        query: 搜索查询
        summary: 是否返回摘要
        count: 返回结果数量
        api_key: API key
        include: 限制搜索的域名范围

    Returns:
        API 响应的 JSON 数据

    Raises:
        BochaAPIError: API 请求失败时抛出
    """
    url = "https://api.bocha.cn/v1/web-search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "query": query,
        "summary": summary,
        "count": count,
    }

    if include:
        payload["include"] = include

    async with session.post(url, headers=headers, json=payload) as response:
        raw_text = await response.text()

        if response.status >= 400:
            raise BochaAPIError(
                f"Bocha API request failed ({response.status}): {raw_text}"
            )

        try:
            data = await response.json()
        except Exception as e:
            raise BochaAPIError(f"Failed to parse JSON response: {e}") from e

        return data
