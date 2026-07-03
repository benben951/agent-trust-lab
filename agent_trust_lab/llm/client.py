from __future__ import annotations

import json
import os
from typing import Any


class LLMNotAvailableError(RuntimeError):
    pass


class LLMClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
    ):
        self._api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self._base_url = base_url or os.environ.get("OPENAI_BASE_URL")
        self._model = model or os.environ.get("LLM_MODEL", "gpt-4o-mini")

        if not self._api_key:
            raise LLMNotAvailableError(
                "OPENAI_API_KEY is not set. Set it as an environment variable "
                "or pass api_key= explicitly."
            )

        try:
            import openai  # noqa: F811
        except ImportError:
            raise LLMNotAvailableError(
                "The 'openai' package is not installed. "
                "Install it with: pip install openai"
            )

        client_kwargs: dict[str, Any] = {"api_key": self._api_key}
        if self._base_url:
            client_kwargs["base_url"] = self._base_url
        self._client = openai.OpenAI(**client_kwargs)

    def chat(
        self,
        system: str,
        user: str,
        *,
        temperature: float = 0.1,
        max_tokens: int = 2048,
    ) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

    @property
    def model(self) -> str:
        return self._model


def _extract_json_block(text: str) -> str:
    """Extract the first JSON object block from LLM output.

    Handles ```json fences, bare JSON, and leading/trailing text.
    """
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines)

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return text


def parse_evaluation_json(raw: str) -> dict[str, Any]:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    try:
        return json.loads(_extract_json_block(raw))
    except json.JSONDecodeError:
        pass
    return {}
