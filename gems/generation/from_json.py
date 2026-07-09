"""Nạp nội dung bài học từ JSON do AI agent tự soạn (Claude/Antigravity...)
thay cho việc gọi Gemini API — dùng khi người dùng không có/không muốn dùng
GEMINI_API_KEY và để chính agent đang trò chuyện soạn nội dung trực tiếp.

JSON phải khớp đúng schema Pydantic tương ứng (`gems/models/*.py`) — sai
trường/kiểu dữ liệu sẽ báo lỗi rõ ràng ngay khi nạp, không âm thầm bỏ qua.
"""
from __future__ import annotations

from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

from gems.models.architect import GEMSArchitect
from gems.models.homework import HomeworkContent
from gems.models.lesson_plan import LessonPlanContent
from gems.models.worksheet import LessonWorksheet

T = TypeVar("T", bound=BaseModel)


def _load(path: Path, model: type[T]) -> T:
    if not path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy file nội dung: {path}. "
            f"AI agent cần ghi file JSON khớp schema {model.__name__} tại đường dẫn này trước."
        )
    return model.model_validate_json(path.read_text(encoding="utf-8"))


def load_architect(path: str | Path) -> GEMSArchitect:
    return _load(Path(path), GEMSArchitect)


def load_worksheet(path: str | Path) -> LessonWorksheet:
    return _load(Path(path), LessonWorksheet)


def load_homework(path: str | Path) -> HomeworkContent:
    return _load(Path(path), HomeworkContent)


def load_lesson_plan(path: str | Path) -> LessonPlanContent:
    return _load(Path(path), LessonPlanContent)
