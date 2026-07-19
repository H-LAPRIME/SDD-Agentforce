import importlib


def test_default_model_config_uses_ollama_without_paid_api_key(monkeypatch):
    monkeypatch.setenv("NVIDIA_API_KEY", "")
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)

    import core.config as config

    config = importlib.reload(config)

    assert config.MODEL_CONFIG["provider"] == "ollama"
    assert config.MODEL_CONFIG["api_key"] == "ollama"
    assert config.MODEL_CONFIG["base_url"] == "http://localhost:11434/v1"
