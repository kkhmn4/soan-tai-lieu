"""Wrapper mỏng quanh google-genai — 1 chỗ duy nhất gọi Gemini API.

Bản cũ có ~10 điểm gọi Gemini lặp lại cùng 1 khuôn:
`json.loads(response.text)` rồi tự dựng lại Pydantic model thủ công, dù
SDK đã tự parse sẵn ở `response.parsed`. Ngoài ra: mỗi module (gems_agent,
gems_analyzer, worksheet_generator...) đọc `GEMINI_API_KEY` độc lập,
không thống nhất chỗ load `.env`. Ở đây tập trung việc đọc key +
gọi API + parse kết quả về đúng 1 nơi.
"""
from __future__ import annotations

import os
from typing import TypeVar

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class GeminiClient:
    """Client mỏng — `None` nếu thiếu GEMINI_API_KEY (chế độ offline)."""

    def __init__(self, api_key: str | None = None):
        load_dotenv()
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self._client: genai.Client | None = genai.Client(api_key=self.api_key) if self.api_key else None

    @property
    def is_online(self) -> bool:
        return self._client is not None

    def generate_structured(self, *, model: str, schema: type[T], system_instruction: str,
                             prompt: str, temperature: float = 0.3) -> T:
        if not self._client:
            raise EnvironmentError("Thiếu GEMINI_API_KEY — không thể gọi Gemini API ở chế độ offline.")
        response = self._client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema,
                system_instruction=system_instruction,
                temperature=temperature,
            ),
        )
        parsed = response.parsed
        if parsed is None:
            raise ValueError(f"Gemini không trả về JSON hợp lệ khớp schema {schema.__name__}.")
        return parsed

    def generate_text(self, *, model: str, system_instruction: str, prompt: str,
                       temperature: float = 0.1) -> str:
        if not self._client:
            raise EnvironmentError("Thiếu GEMINI_API_KEY — không thể gọi Gemini API ở chế độ offline.")
        response = self._client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(system_instruction=system_instruction, temperature=temperature),
        )
        text = response.text or ""
        if text.startswith("```markdown"):
            text = text[len("```markdown"):]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
