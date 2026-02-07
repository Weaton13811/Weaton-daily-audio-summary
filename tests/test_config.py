"""Tests for the config module."""

from daily_audio_summary.config import DEFAULTS, load_config


def test_load_config_defaults(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("DAS_IMESSAGE_TO", raising=False)
    config = load_config("nonexistent.json")
    for key, value in DEFAULTS.items():
        assert config[key] == value


def test_load_config_from_file(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text('{"location": "Syracuse, NY", "tts_voice": "Samantha"}')
    config = load_config(str(config_file))
    assert config["location"] == "Syracuse, NY"
    assert config["tts_voice"] == "Samantha"
    # Defaults still filled in
    assert config["output_dir"] == "output"


def test_env_var_overrides(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-123")
    monkeypatch.setenv("DAS_IMESSAGE_TO", "+15551234567")
    config = load_config("nonexistent.json")
    assert config["anthropic_api_key"] == "sk-test-123"
    assert config["imessage_to"] == "+15551234567"
