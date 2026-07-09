"""Giai đoạn NotebookLM hợp nhất — sinh 2 bộ Slide tách biệt (Giáo viên +
Phiếu học tập, xem `skills/gems_physics_skill.md` mục 4.2, v9.5.0) qua
NotebookLM, thay cơ chế "1 Slide + N+2 Infographic" trước đây.

Các lỗi/bài học đã áp dụng:
- Vòng polling kiểm tra trạng thái NGAY LẦN ĐẦU, chỉ sleep nếu chưa xong
  (không sleep 5 phút trước khi kiểm tra lần đầu như bản gốc).
- `nlm_cli.download_*` trả về bool thật, "download_failed" được ghi nhận
  riêng biệt thay vì bị bỏ qua.
- Trạng thái "failed"/"error"/"cancelled" được ghi nhận là lỗi thật, không
  còn bị coi như "đã xong".
- `--profile` (xoay tài khoản né rate-limit) được truyền xuyên suốt mọi lệnh
  `nlm`.
- **Bài học từ đợt Bài 28 (7 vòng thử thực tế):** NotebookLM có thể cắt
  ngang (silent truncation) khi 1 prompt yêu cầu quá nhiều slide/quy tắc cùng
  lúc — số "Trang X/Y" tự ghi trên slide KHÔNG đáng tin, luôn phải tự đếm số
  slide thật trong file `.pptx` tải về (`python-pptx`) và so với số slide kỳ
  vọng đã tính lúc dựng prompt. Nếu lệch, ghi cảnh báo rõ trong `RunReport`
  thay vì báo "downloaded" như đã xong đầy đủ.
"""
from __future__ import annotations

import time
from pathlib import Path

from pptx import Presentation

from gems.config.loader import Identity, LessonSpec
from gems.notebooklm import nlm_cli
from gems.notebooklm.prompt_builder import generate_notebooklm_prompt
from gems.pipeline.report import RunReport

POLL_INTERVAL_SECONDS = 300
MAX_WAIT_SECONDS = 3600


def _count_pptx_slides(path: Path) -> int | None:
    """Đếm số slide THẬT trong file .pptx đã tải về — không tin số trang tự
    ghi trên slide, vì NotebookLM có thể cắt ngang mà vẫn ghi "Trang X/Y" như
    dự kiến ban đầu (đã xác nhận thực tế ở đợt Bài 28)."""
    if not path.exists():
        return None
    try:
        return len(Presentation(str(path)).slides._sldIdLst)
    except Exception:  # noqa: BLE001 — file hỏng/không mở được, coi như không đếm được
        return None


_ACCENT_MAP = {
    "a": "áàảãạăắằẳẵặâấầẩẫậ", "A": "ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬ",
    "d": "đ", "D": "Đ",
    "e": "éèẻẽẹêếềểễệ", "E": "ÉÈẺẼẸÊẾỀỂỄỆ",
    "i": "íìỉĩị", "I": "ÍÌỈĨỊ",
    "o": "óòỏõọôốồổỗộơớờởỡợ", "O": "ÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢ",
    "u": "úùủũụưứừửữự", "U": "ÚÙỦŨỤƯỨỪỬỮỰ",
    "y": "ýỳỷỹỵ", "Y": "ÝỲỶỸỴ",
}


def strip_vietnamese_accents(text: str) -> str:
    """Trước đây bị chép tay y hệt ở CẢ HAI file (`restructure_output.py` và
    `generate_notebook_materials.py`) — giờ chỉ có 1 bản dùng chung."""
    result = text
    for plain, accented_chars in _ACCENT_MAP.items():
        for ch in accented_chars:
            result = result.replace(ch, plain)
    return result


def resolve_or_create_notebook(lesson: LessonSpec, *, notebook_id: str | None = None,
                                force_create: bool = False, profile: str | None = None) -> tuple[str | None, str]:
    """Trả về (notebook_id, detail)."""
    if notebook_id:
        return notebook_id, "dùng notebook_id được chỉ định"

    if not force_create:
        notebooks = nlm_cli.list_notebooks(profile=profile)
        if notebooks:
            lesson_num = lesson.key.replace("bai", "")
            target = strip_vietnamese_accents(lesson.name.lower())
            for nb in notebooks:
                nb_title = strip_vietnamese_accents(nb.get("title", "").lower())
                if f"bai {lesson_num}" in nb_title or f"bai{lesson_num}" in nb_title or target in nb_title:
                    return nb["id"], f"tái sử dụng notebook có sẵn: {nb.get('title')}"

    new_id = nlm_cli.create_notebook(f"GEMS Vat ly 12 - {lesson.name}", profile=profile)
    if new_id:
        return new_id, "đã tạo notebook mới"
    return None, "không thể tìm hoặc tạo notebook"


_CORE_SOURCE_SUFFIXES = ("phieu_hoc_tap.md", "ke_hoach_bai_day.md", "huong_dan_slide.md", "dac_ta_gems.md")


def upload_sources(notebook_id: str, md_dir: Path, *, profile: str | None = None) -> list[tuple[str, bool]]:
    files_to_upload = [f for f in sorted(md_dir.glob("*.md")) if f.name.endswith(_CORE_SOURCE_SUFFIXES)]
    existing_titles = nlm_cli.list_sources(notebook_id, profile=profile)

    results = []
    for fpath in files_to_upload:
        if fpath.name in existing_titles:
            nlm_cli.delete_source(existing_titles[fpath.name], profile=profile)
        ok = nlm_cli.add_source(notebook_id, fpath, profile=profile)
        results.append((fpath.name, ok))
    return results


def create_artifacts(notebook_id: str, teacher_prompt_path: Path, student_prompt_path: Path,
                      *, profile: str | None = None) -> tuple[str | None, str | None]:
    """Tạo 2 yêu cầu sinh Slide (Giáo viên + Phiếu học tập), thay 1 slide + N
    infographic của cơ chế cũ. Trả về (teacher_artifact_id, student_artifact_id)."""
    teacher_artifact_id = nlm_cli.create_slides(notebook_id, teacher_prompt_path, profile=profile)
    student_artifact_id = nlm_cli.create_slides(notebook_id, student_prompt_path, profile=profile)
    return teacher_artifact_id, student_artifact_id


def poll_and_download(notebook_id: str, lesson_slug: str, ready_dir: Path,
                       teacher_artifact_id: str | None, student_artifact_id: str | None, *,
                       teacher_expected_slides: int = 0, student_expected_slides: int = 0,
                       profile: str | None = None, poll_interval: int = POLL_INTERVAL_SECONDS,
                       max_wait: int = MAX_WAIT_SECONDS, sleep_fn=time.sleep,
                       count_slides_fn=_count_pptx_slides) -> dict[str, str]:
    """Kiểm tra trạng thái NGAY LẦN ĐẦU rồi mới sleep nếu chưa xong. Trả về
    status cho "giao_vien"/"phieu_hoc_tap": "downloaded" | "download_failed" |
    "failed:<trạng_thái>" | "timeout" | "slide_count_mismatch:X/Y" (đã tải về
    nhưng số slide thật ít hơn kỳ vọng — dấu hiệu bị NotebookLM cắt ngang,
    xem bài học ở đợt Bài 28 trong docstring module)."""
    targets = {
        "giao_vien": (teacher_artifact_id, ready_dir / f"{lesson_slug}_slide_giao_vien.pptx", teacher_expected_slides),
        "phieu_hoc_tap": (student_artifact_id, ready_dir / f"{lesson_slug}_slide_phieu_hoc_tap.pptx", student_expected_slides),
    }
    statuses: dict[str, str] = {}
    done = {name: art_id is None for name, (art_id, _, _) in targets.items()}
    elapsed = 0
    first_check = True

    while not all(done.values()):
        if elapsed >= max_wait:
            for name, finished in done.items():
                if not finished:
                    statuses[name] = "timeout"
            break

        if not first_check:
            sleep_fn(poll_interval)
            elapsed += poll_interval
        first_check = False

        artifacts = nlm_cli.list_artifacts(notebook_id, profile=profile)
        if artifacts is None:
            continue
        artifacts_map = {a["id"]: a for a in artifacts}

        for name, (art_id, dest_path, expected) in targets.items():
            if done[name] or art_id not in artifacts_map:
                continue
            status = (artifacts_map[art_id].get("status") or "").lower()
            if status == "completed":
                ok = nlm_cli.download_slide_deck(notebook_id, art_id, "pptx", dest_path, profile=profile)
                if not ok:
                    statuses[name] = "download_failed"
                else:
                    actual = count_slides_fn(dest_path)
                    if actual is not None and expected and actual < expected:
                        statuses[name] = f"slide_count_mismatch:{actual}/{expected}"
                    else:
                        statuses[name] = "downloaded"
                done[name] = True
            elif status in ("failed", "error", "cancelled"):
                statuses[name] = f"failed:{status}"
                done[name] = True

    return statuses


def run_notebooklm_stage(identity: Identity, lesson: LessonSpec, output_dir: Path, report: RunReport, *,
                          notebook_id: str | None = None, profile: str | None = None,
                          force_create: bool = False, sleep_fn=time.sleep) -> None:
    md_dir = output_dir / "md"
    ready_dir = output_dir / "ready"
    ready_dir.mkdir(parents=True, exist_ok=True)

    teacher_prompt_path, student_prompt_path, teacher_count, student_count = generate_notebooklm_prompt(
        output_dir, lesson.slug, lesson.name, identity)
    report.add("sinh_prompt_notebooklm", ok=bool(teacher_count and student_count),
               artifact_path=teacher_prompt_path,
               warnings=[] if teacher_count else [
                   "Không tìm thấy worksheet_data.json — chạy generate/offline/compose trước."])
    if not teacher_count or not student_count:
        return

    if not nlm_cli.login_check(profile=profile):
        report.add("nlm_login", ok=False, error="Chưa đăng nhập nlm CLI (chạy `nlm login` trước) hoặc thiếu nlm trên PATH.")
        return
    report.add("nlm_login", ok=True)

    resolved_id, detail = resolve_or_create_notebook(lesson, notebook_id=notebook_id, force_create=force_create,
                                                       profile=profile)
    if not resolved_id:
        report.add("resolve_notebook", ok=False, error=detail)
        return
    report.add("resolve_notebook", ok=True, detail=f"{detail} (id={resolved_id})")

    upload_results = upload_sources(resolved_id, md_dir, profile=profile)
    failed_uploads = [name for name, ok in upload_results if not ok]
    report.add("upload_nguon", ok=not failed_uploads,
                detail=f"{len(upload_results) - len(failed_uploads)}/{len(upload_results)} thành công",
                warnings=[f"Tải lên thất bại: {name}" for name in failed_uploads])

    teacher_artifact_id, student_artifact_id = create_artifacts(
        resolved_id, teacher_prompt_path, student_prompt_path, profile=profile)
    report.add("tao_yeu_cau_sinh", ok=bool(teacher_artifact_id and student_artifact_id),
                detail=f"giao_vien={'có' if teacher_artifact_id else 'không'}, "
                       f"phieu_hoc_tap={'có' if student_artifact_id else 'không'}")

    statuses = poll_and_download(resolved_id, lesson.slug, ready_dir, teacher_artifact_id, student_artifact_id,
                                   teacher_expected_slides=teacher_count, student_expected_slides=student_count,
                                   profile=profile, sleep_fn=sleep_fn)
    for name, status in statuses.items():
        ok = status == "downloaded"
        warnings = [f"Có thể bị NotebookLM cắt ngang giữa chừng — xem "
                    f"docs/reference/quy_trinh_tao_tai_lieu_chi_tiet.md mục Giai đoạn 5."] \
            if status.startswith("slide_count_mismatch") else []
        report.add(f"tai_ve:{name}", ok=ok, detail=status, warnings=warnings)
