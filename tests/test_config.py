"""Tests for the config module."""

from daily_audio_summary.config import load_config


def test_load_config_defaults(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    config = load_config("nonexistent.json")
    assert config["output_path"] == "output/summary.mp3"
    assert config["content"] == ""


def test_load_config_from_file(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text('{"content": "test content", "output_path": "out.mp3"}')
    config = load_config(str(config_file))
    assert config["content"] == "test content"
    assert config["output_path"] == "out.mp3"
