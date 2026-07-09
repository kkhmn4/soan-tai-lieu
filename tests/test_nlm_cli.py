import subprocess

from gems.notebooklm import nlm_cli


def test_run_nlm_handles_missing_binary(monkeypatch):
    def fake_run(*a, **kw):
        raise FileNotFoundError()
    monkeypatch.setattr(subprocess, "run", fake_run)
    code, out, err = nlm_cli.run_nlm("login", "--check")
    assert code == -1
    assert "PATH" in err


def test_run_nlm_handles_timeout_instead_of_hanging(monkeypatch):
    """Phát hiện khi kiểm thử thật: nlm login --check có thể treo vô thời hạn
    nếu chưa đăng nhập — mọi lệnh phải có timeout, không được treo mãi."""
    def fake_run(*a, **kw):
        raise subprocess.TimeoutExpired(cmd=a[0], timeout=kw.get("timeout", 30))
    monkeypatch.setattr(subprocess, "run", fake_run)
    code, out, err = nlm_cli.run_nlm("login", "--check", timeout=1)
    assert code == -1
    assert "quá thời gian" in err


def test_run_nlm_passes_profile_after_subcommand(monkeypatch):
    captured = {}

    def fake_run(cmd, **kw):
        captured["cmd"] = cmd
        class R:
            returncode = 0
            stdout = ""
            stderr = ""
        return R()

    monkeypatch.setattr(subprocess, "run", fake_run)
    nlm_cli.run_nlm("login", "--check", profile="account2")
    assert captured["cmd"] == ["nlm", "login", "--check", "--profile", "account2"]
