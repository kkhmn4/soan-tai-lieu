import pytest

from gems.generation import from_json
from gems.models.architect import GEMSArchitect


def test_load_architect_missing_file_raises_clear_error(tmp_path):
    with pytest.raises(FileNotFoundError, match="GEMSArchitect"):
        from_json.load_architect(tmp_path / "khong_ton_tai.json")


def test_load_architect_valid_json(tmp_path):
    payload = {
        "analysis": {
            "key_concepts": ["A"],
            "misconceptions": [{"misconception": "m", "correct_concept": "c", "explanation": "e"}],
            "teaching_methods": ["Khám phá"],
        },
        "matrix": {"lesson_name": "Bài test", "units": []},
    }
    path = tmp_path / "bai_test_architect.json"
    path.write_text(__import__("json").dumps(payload, ensure_ascii=False), encoding="utf-8")

    architect = from_json.load_architect(path)
    assert isinstance(architect, GEMSArchitect)
    assert architect.matrix.lesson_name == "Bài test"


def test_load_architect_invalid_schema_raises_validation_error(tmp_path):
    path = tmp_path / "bad_architect.json"
    path.write_text('{"analysis": "không đúng kiểu"}', encoding="utf-8")
    with pytest.raises(Exception):
        from_json.load_architect(path)
