"""Mô hình báo cáo kết quả chạy pipeline — trung thực thay vì in-và-nuốt-lỗi.

Bản cũ (`gems_agent.py`): mọi lỗi ở mọi giai đoạn chỉ in ra console rồi đi
tiếp, và luôn kết thúc bằng banner "HOÀN THÀNH" dù có thể đã âm thầm thiếu
1-2 tài liệu. Ở đây mỗi bước tạo ra đúng 1 file được ghi lại thành 1
`StageResult` riêng — `RunReport.ok` chỉ True khi TẤT CẢ các bước đều ok,
và CLI dùng giá trị này để trả về exit code đúng.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class StageResult:
    stage: str
    ok: bool
    detail: str = ""
    artifact_path: Path | None = None
    warnings: list[str] = field(default_factory=list)
    error: str | None = None


@dataclass
class RunReport:
    lesson_slug: str
    stages: list[StageResult] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(s.ok for s in self.stages)

    def add(self, stage: str, *, ok: bool, detail: str = "", artifact_path: Path | None = None,
            warnings: list[str] | None = None, error: str | None = None) -> StageResult:
        result = StageResult(stage=stage, ok=ok, detail=detail, artifact_path=artifact_path,
                              warnings=warnings or [], error=error)
        self.stages.append(result)
        return result

    def summary_lines(self) -> list[str]:
        lines = [f"Kết quả cho bài học: {self.lesson_slug}"]
        for s in self.stages:
            mark = "✓" if s.ok else "✗"
            line = f"  [{mark}] {s.stage}"
            if s.detail:
                line += f" — {s.detail}"
            lines.append(line)
            for w in s.warnings:
                lines.append(f"      ⚠ {w}")
            if s.error:
                lines.append(f"      Lỗi: {s.error}")
        lines.append("HOÀN THÀNH — tất cả các bước đều thành công." if self.ok
                      else "CÓ LỖI — xem chi tiết các bước bị đánh dấu ✗ ở trên.")
        return lines
