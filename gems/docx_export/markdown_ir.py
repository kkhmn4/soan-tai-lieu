"""Parser Markdown dùng chung cho cả 3 loại tài liệu (PHT/KHBD/Bài tập).

Bản cũ có 3 bản sao gần giống nhau của logic này (phát hiện ảnh, blockquote,
heading, bullet) chép tay trong từng exporter, và đã lệch nhau theo thời
gian (PHT không hỗ trợ bảng pipe-table, KHBD hỗ trợ; heading bị cắt chuỗi
theo offset cố định `[3:]`/`[4:]`/`[5:]` thay vì đếm số `#` thật...). Module
này chỉ làm 1 việc, làm đúng, dùng chung cho tất cả — phần ngữ pháp riêng
của từng loại tài liệu (câu hỏi trắc nghiệm, bảng GV/HS 4 pha...) vẫn nằm
ở exporter tương ứng, xử lý sau khi qua parser này.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

_IMAGE_RE = re.compile(r"([\(\s]*)(ready[^\(\s]+\.(?:png|jpg|jpeg))([\s\)]*)", re.IGNORECASE)
_HEADING_RE = re.compile(r"^(#{1,4})\s+(.*)$")
_SEPARATOR_RE = re.compile(r"^-{3,}$")
_DOT_LINE_TOKEN = "[DOT_LINE_90]"


@dataclass
class Block:
    kind: str  # "heading" | "bullet" | "body" | "blockquote" | "dotline" | "table" | "separator"
    text: str = ""
    level: int = 1
    image_path: Path | None = None
    table_headers: list[str] | None = None
    table_rows: list[list[str]] = field(default_factory=list)


def resolve_image_path(raw_path: str, search_dirs: list[Path]) -> Path | None:
    """Thử lần lượt các cách suy ra đường dẫn ảnh thật từ chuỗi ghi trong
    markdown nguồn (thường dạng tương đối `ready/hinh_anh/...`)."""
    candidates = [Path(raw_path)]
    for base in search_dirs:
        candidates.append(base / raw_path)
        candidates.append(base / "ready" / "hinh_anh" / Path(raw_path).name)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _extract_image(line: str, search_dirs: list[Path]) -> tuple[str, Path | None]:
    match = _IMAGE_RE.search(line)
    if not match:
        return line, None
    image_path = resolve_image_path(match.group(2), search_dirs)
    cleaned = _IMAGE_RE.sub(" ", line)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned, image_path


def _heading_level(hash_count: int) -> int:
    return max(1, min(3, hash_count - 1))


def _parse_table(lines: list[str], start: int) -> tuple[Block, int]:
    def parse_row(raw: str) -> list[str]:
        return [c.strip() for c in raw.strip().strip("|").split("|")]

    headers = parse_row(lines[start])
    i = start + 1
    if i < len(lines) and re.match(r"^\s*\|?[\s:\-|]+\|?\s*$", lines[i]):
        i += 1  # dòng phân cách |---|---|
    rows: list[list[str]] = []
    while i < len(lines) and lines[i].strip().startswith("|"):
        rows.append(parse_row(lines[i]))
        i += 1
    return Block(kind="table", table_headers=headers, table_rows=rows), i


def parse_markdown_blocks(lines: list[str], *, image_search_dirs: list[Path] | None = None) -> list[Block]:
    search_dirs = image_search_dirs or []
    blocks: list[Block] = []
    i = 0
    n = len(lines)
    while i < n:
        raw_line = lines[i].replace("﻿", "")
        stripped = raw_line.strip()

        if not stripped:
            i += 1
            continue

        if stripped == _DOT_LINE_TOKEN:
            blocks.append(Block(kind="dotline"))
            i += 1
            continue

        if _SEPARATOR_RE.match(stripped):
            blocks.append(Block(kind="separator"))
            i += 1
            continue

        if stripped.startswith("|"):
            block, i = _parse_table(lines, i)
            blocks.append(block)
            continue

        is_blockquote = False
        if stripped.startswith("> "):
            stripped = stripped[2:]
            is_blockquote = True
        elif stripped.startswith(">"):
            stripped = stripped[1:].strip()
            is_blockquote = True

        stripped, image_path = _extract_image(stripped, search_dirs)

        heading_match = _HEADING_RE.match(stripped)
        if heading_match:
            level = _heading_level(len(heading_match.group(1)))
            blocks.append(Block(kind="heading", text=heading_match.group(2).strip(), level=level, image_path=image_path))
            i += 1
            continue

        if stripped.startswith("- ") or stripped.startswith("* "):
            blocks.append(Block(kind="bullet", text=stripped, level=1, image_path=image_path))
            i += 1
            continue
        if stripped.startswith("+ "):
            blocks.append(Block(kind="bullet", text=stripped, level=2, image_path=image_path))
            i += 1
            continue

        kind = "blockquote" if is_blockquote else "body"
        blocks.append(Block(kind=kind, text=stripped, image_path=image_path))
        i += 1

    return blocks
