"""
Centralized LLM client: loads prompts from prompts/ and calls the configured model.
Configuration: config/agent.yml + .env (API keys and optional overrides).

Supported providers: openai, deepseek, groq, openrouter, openai_compatible.
"""
from __future__ import annotations

import logging
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Resolve paths relative to project root (parent of src)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_CONFIG_PATH = _PROJECT_ROOT / "config" / "agent.yml"
_DEFAULT_PROMPTS_DIR = _PROJECT_ROOT / "prompts"

# Provider defaults (OpenAI-compatible endpoints)
PROVIDER_BASE_URLS = {
    "openai": "https://api.openai.com/v1",
    "deepseek": "https://api.deepseek.com",
    "groq": "https://api.groq.com/openai/v1",
    "openrouter": "https://openrouter.ai/api/v1",
}


def _load_config() -> dict:
    if not _CONFIG_PATH.exists():
        return {}
    with open(_CONFIG_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_prompts_dir() -> Path:
    config = _load_config()
    prompts_dir = config.get("paths", {}).get("prompts_dir", "prompts")
    if os.path.isabs(prompts_dir):
        return Path(prompts_dir)
    return _PROJECT_ROOT / prompts_dir


def load_prompt(name: str) -> str:
    """
    Read prompt template from prompts/{name}.md.
    """
    prompts_dir = get_prompts_dir()
    path = prompts_dir / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8")


def _substitute_vars(template: str, input_vars: dict) -> str:
    """Simple substitution: {key} -> input_vars[key]. Keys must exist."""
    result = template
    for key, value in input_vars.items():
        placeholder = "{" + key + "}"
        result = result.replace(placeholder, str(value))
    return result


def _get_llm_params(config: dict) -> tuple[str, str, str, float, int]:
    """Returns (api_key, base_url, model, temperature, max_tokens)."""
    llm_cfg = config.get("llm", {})
    provider = (os.getenv("LLM_PROVIDER") or llm_cfg.get("provider", "openai")).lower()
    model = os.getenv("LLM_MODEL") or llm_cfg.get("model", "gpt-4o-mini")
    temperature = float(os.getenv("LLM_TEMPERATURE", llm_cfg.get("temperature", 0.2)))
    max_tokens = int(os.getenv("LLM_MAX_TOKENS", llm_cfg.get("max_tokens", 4096)))

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("LLM_BASE_URL") or PROVIDER_BASE_URLS["openai"]
    elif provider == "deepseek":
        api_key = os.getenv("DEEPSEEK_API_KEY")
        base_url = os.getenv("LLM_BASE_URL") or PROVIDER_BASE_URLS["deepseek"]
        if not model or model.startswith("gpt-"):
            model = llm_cfg.get("model") or "deepseek-chat"
    elif provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        base_url = os.getenv("LLM_BASE_URL") or PROVIDER_BASE_URLS["groq"]
        if not model or model.startswith("gpt-") or model.startswith("deepseek"):
            model = llm_cfg.get("model") or "llama-3.1-70b-versatile"
    elif provider == "openrouter":
        api_key = os.getenv("OPENROUTER_API_KEY")
        base_url = os.getenv("LLM_BASE_URL") or PROVIDER_BASE_URLS["openrouter"]
        if not model or model.startswith("gpt-") or model.startswith("deepseek"):
            model = llm_cfg.get("model") or "openrouter/free"
    elif provider == "openai_compatible":
        api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("LLM_BASE_URL") or llm_cfg.get("base_url", "")
        model = os.getenv("LLM_MODEL") or llm_cfg.get("model", "gpt-4o-mini")
        if not base_url:
            raise ValueError("For provider openai_compatible set LLM_BASE_URL in .env or base_url in config")
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}. Use openai, deepseek, groq, openrouter, or openai_compatible.")

    if not api_key:
        logger.warning("API key not set for provider %s; LLM call may fail", provider)
    return api_key or "", base_url, model, temperature, max_tokens


def call_llm(prompt: str, input_vars: dict | None = None) -> str:
    """
    Substitute input_vars into prompt (e.g. {text}, {url}) and call the configured LLM.
    Returns raw response string. Configuration from config/agent.yml and .env.
    """
    if input_vars:
        prompt = _substitute_vars(prompt, input_vars)

    config = _load_config()
    api_key, base_url, model, temperature, max_tokens = _get_llm_params(config)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return (response.choices[0].message.content or "").strip()
    except Exception as e:
        logger.exception("LLM API call failed: %s", e)
        raise
