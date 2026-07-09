"""Wrapper duy nhất cho mọi lệnh gọi `nlm` CLI (Google NotebookLM).

Sửa 3 vấn đề của bản cũ:
1. Trước đây mỗi lệnh được build bằng f-string rồi chạy `subprocess.run(cmd,
   shell=True, ...)` — tự ghép dấu ngoặc kép thủ công quanh path/tiêu đề.
   Đường dẫn hay tiêu đề bài học chứa khoảng trắng/ký tự đặc biệt (chính
   thư mục dự án này đã có khoảng trắng + dấu tiếng Việt) có thể vỡ quoting.
   Ở đây dùng `subprocess.run(list_arg, shell=False)` — mỗi phần tử list là
   1 argument riêng biệt, không cần tự escape.
2. `--profile` (dùng để xoay vòng tài khoản né rate-limit NotebookLM free
   tier) trước đây chỉ là hướng dẫn thao tác thủ công trong tài liệu, không
   hề có trong code. Ở đây mọi hàm đều nhận `profile: str | None` thật.
3. Không có timeout nào cả — phát hiện trực tiếp khi kiểm thử: nếu `nlm`
   chưa đăng nhập (hoặc phiên hết hạn) mà `nlm login --check` cần mở trình
   duyệt/chờ mạng, tiến trình có thể treo VÔ THỜI HẠN, kéo theo treo luôn cả
   pipeline. Mọi lệnh giờ có timeout mặc định, hết giờ thì coi là lỗi thay
   vì treo mãi.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

DEFAULT_TIMEOUT_SECONDS = 30.0
UPLOAD_TIMEOUT_SECONDS = 180.0


def run_nlm(*args: str, profile: str | None = None, timeout: float = DEFAULT_TIMEOUT_SECONDS) -> tuple[int, str, str]:
    cmd = ["nlm", *args]
    if profile:
        cmd += ["--profile", profile]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=timeout)
        return res.returncode, res.stdout, res.stderr
    except FileNotFoundError:
        return -1, "", "Không tìm thấy lệnh `nlm` trên PATH — cần cài NotebookLM CLI trước."
    except subprocess.TimeoutExpired:
        return -1, "", f"Lệnh `nlm {' '.join(args)}` quá thời gian chờ ({timeout}s) — có thể chưa đăng nhập hoặc mạng treo."
    except Exception as exc:  # noqa: BLE001
        return -1, "", str(exc)


def login_check(profile: str | None = None) -> bool:
    code, _, _ = run_nlm("login", "--check", profile=profile)
    return code == 0


def list_notebooks(profile: str | None = None) -> list[dict] | None:
    code, stdout, _ = run_nlm("list", "notebooks", "--json", profile=profile)
    if code != 0:
        return None
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return None


def create_notebook(title: str, profile: str | None = None) -> str | None:
    code, stdout, _ = run_nlm("create", "notebook", title, profile=profile)
    if code != 0:
        return None
    try:
        return json.loads(stdout).get("notebook_id")
    except json.JSONDecodeError:
        return None


def list_sources(notebook_id: str, profile: str | None = None) -> dict[str, str]:
    code, stdout, _ = run_nlm("list", "sources", notebook_id, "--json", profile=profile)
    if code != 0:
        return {}
    try:
        sources = json.loads(stdout)
        return {src["title"]: src["id"] for src in sources}
    except (json.JSONDecodeError, KeyError, TypeError):
        return {}


def delete_source(source_id: str, profile: str | None = None) -> bool:
    code, _, _ = run_nlm("delete", "source", source_id, "-y", profile=profile)
    return code == 0


def add_source(notebook_id: str, file_path: Path, profile: str | None = None) -> bool:
    code, _, _ = run_nlm("source", "add", notebook_id, "-f", str(file_path), "--wait",
                          profile=profile, timeout=UPLOAD_TIMEOUT_SECONDS)
    return code == 0


def _extract_artifact_id(stdout: str) -> str | None:
    import re
    match = re.search(r"Artifact ID:\s*([a-f0-9\-]+)", stdout)
    return match.group(1) if match else None


def create_slides(notebook_id: str, focus_path: Path, profile: str | None = None) -> str | None:
    code, stdout, _ = run_nlm("create", "slides", notebook_id, "--focus", f"@{focus_path}",
                               "--language", "vi", "--confirm", profile=profile)
    return _extract_artifact_id(stdout) if code == 0 else None


def create_infographic(notebook_id: str, focus_path: Path, profile: str | None = None) -> str | None:
    """`nlm create infographic` có flag gốc `--orientation`/`--style` (xem
    `nlm create infographic --help`) đáng tin cậy hơn nhiều so với chỉ dựa
    vào câu chữ trong prompt để yêu cầu ảnh dọc/khoa học — trước đây hàm
    này không truyền 2 flag này nên ảnh luôn ra landscape mặc định dù prompt
    đã yêu cầu portrait bằng lời văn."""
    code, stdout, _ = run_nlm("create", "infographic", notebook_id, "--focus", f"@{focus_path}",
                               "--orientation", "portrait", "--style", "scientific",
                               "--language", "vi", "--confirm", profile=profile)
    return _extract_artifact_id(stdout) if code == 0 else None


def list_artifacts(notebook_id: str, profile: str | None = None) -> list[dict] | None:
    code, stdout, _ = run_nlm("list", "artifacts", notebook_id, "--json", profile=profile)
    if code != 0:
        return None
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return None


def download_slide_deck(notebook_id: str, artifact_id: str, fmt: str, dest: Path,
                         profile: str | None = None) -> bool:
    code, _, _ = run_nlm("download", "slide-deck", notebook_id, "--id", artifact_id,
                          "--format", fmt, "-o", str(dest), profile=profile)
    return code == 0 and dest.exists()


def download_infographic(notebook_id: str, artifact_id: str, dest: Path, profile: str | None = None) -> bool:
    code, _, _ = run_nlm("download", "infographic", notebook_id, "--id", artifact_id,
                          "-o", str(dest), profile=profile)
    return code == 0 and dest.exists()
