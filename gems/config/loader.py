"""Bộ nạp cấu hình duy nhất cho GEMS: curriculum.yaml + identity.yaml.

Thay thế hoàn toàn LESSON_MAP (đã khai trùng ở 2 file) và default_yccds
(dict fallback hardcode trong gems_agent.py cũ). Thêm bài học mới chỉ cần
sửa curriculum.yaml, không cần sửa code.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

CONFIG_DIR = Path(__file__).resolve().parent
DEFAULT_CURRICULUM_PATH = CONFIG_DIR / "curriculum.yaml"
DEFAULT_IDENTITY_PATH = CONFIG_DIR / "identity.yaml"


class LessonSpec(BaseModel):
    key: str
    name: str
    slug: str
    yccd_file: str
    yccd_fallback: str
    num_knowledge_units: int = 2


class Curriculum(BaseModel):
    version: int
    lessons: dict[str, LessonSpec]

    def get(self, key: str) -> LessonSpec | None:
        return self.lessons.get(key)


class Identity(BaseModel):
    teacher_name: str
    department: str
    brand_label: str
    default_font: str = "Times New Roman"
    gemini_model_architect: str = "gemini-2.5-pro"
    gemini_model_content: str = "gemini-2.5-flash"


def load_curriculum(path: Path = DEFAULT_CURRICULUM_PATH) -> Curriculum:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    lessons = {}
    for key, entry in raw["lessons"].items():
        lessons[key] = LessonSpec(key=key, **entry)
    return Curriculum(version=raw["version"], lessons=lessons)


def load_identity(path: Path = DEFAULT_IDENTITY_PATH) -> Identity:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    return Identity(**raw)


def match_lesson_from_prompt(prompt: str, curriculum: Curriculum) -> LessonSpec | None:
    """Khớp bài học từ prompt tự nhiên ngữ.

    Trả về None nếu không khớp được bài nào — KHÔNG âm thầm mặc định về
    bai1 như hành vi cũ (đây là nguồn của lỗi "báo thành công nhưng sinh
    nhầm bài" trong hệ thống trước).
    """
    prompt_lower = prompt.lower()

    match = re.search(r"(?:bài|bai|lesson)\s*(\d+)", prompt_lower)
    if match:
        key = f"bai{match.group(1)}"
        if key in curriculum.lessons:
            return curriculum.lessons[key]

    for lesson in curriculum.lessons.values():
        if lesson.slug in prompt_lower:
            return lesson

    for lesson in curriculum.lessons.values():
        name_words = lesson.name.lower().split()
        if any(word in prompt_lower for word in name_words if len(word) > 2):
            return lesson

    return None
