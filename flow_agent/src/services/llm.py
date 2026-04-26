from __future__ import annotations

import json
import re
from typing import Any, TypeVar

from openai import AsyncOpenAI
from pydantic import BaseModel

from src.config.env import settings

T = TypeVar("T", bound=BaseModel)


class LLMError(RuntimeError):
    pass


class AsyncLLMService:
    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
        model_name: str | None = None,
    ) -> None:
        self.model_name = model_name or settings.LLM_MODEL_NAME
        self.client = AsyncOpenAI(
            base_url=base_url or settings.LLM_BASE_URL,
            api_key=api_key or settings.ARK_API_KEY,
        )

    async def call_text(self, *, system_prompt: str, user_prompt: str) -> str:
        response = await self.client.responses.create(
            model=self.model_name,
            input=[
                {
                    "role": "system",
                    "content": [{"type": "input_text", "text": system_prompt}],
                },
                {
                    "role": "user",
                    "content": [{"type": "input_text", "text": user_prompt}],
                },
            ],
        )
        text = getattr(response, "output_text", "")
        if text:
            return text.strip()
        return self._extract_text_from_output(response)

    async def call_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        model_cls: type[T],
        retries: int = 1,
    ) -> T:
        attempts = retries + 1
        last_error: Exception | None = None

        for _ in range(attempts):
            try:
                text = await self.call_text(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                )
                payload = self._extract_json(text)
                return model_cls.model_validate(payload)
            except Exception as exc:  # noqa: PERF203
                last_error = exc

        raise LLMError(f"Failed to get valid JSON from LLM: {last_error}") from last_error

    def _extract_text_from_output(self, response: Any) -> str:
        lines: list[str] = []
        for item in getattr(response, "output", []) or []:
            for content in getattr(item, "content", []) or []:
                text = getattr(content, "text", None)
                if text:
                    lines.append(text)
        if not lines:
            raise LLMError("LLM response did not include text output")
        return "\n".join(lines).strip()

    def _extract_json(self, text: str) -> dict[str, Any]:
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if not match:
            raise LLMError(f"No JSON object found in LLM output: {cleaned[:200]}")

        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError as exc:
            raise LLMError(f"Failed to parse JSON object: {exc}") from exc
