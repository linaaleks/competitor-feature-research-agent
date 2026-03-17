"""
Centralized LLM client: loads prompts from prompts/ and calls the configured model.
Configuration: config/agent.yml + .env (OPENAI_API_KEY, optional LLM_MODEL, LLM_TEMPERATURE).
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


def call_llm(prompt: str, input_vars: dict | None = None) -> str:
    """
    Substitute input_vars into prompt (e.g. {text}, {url}) and call the configured LLM.
    Returns raw response string. Configuration from config/agent.yml and .env.
    """
    if input_vars:
        prompt = _substitute_vars(prompt, input_vars)

    config = _load_config()
    llm_cfg = config.get("llm", {})
    provider = llm_cfg.get("provider", "openai")
    model = os.getenv("LLM_MODEL") or llm_cfg.get("model", "gpt-4o-mini")
    temperature = float(os.getenv("LLM_TEMPERATURE", llm_cfg.get("temperature", 0.2)))
    max_tokens = llm_cfg.get("max_tokens", 4096)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key and provider == "openai":
        logger.warning("OPENAI_API_KEY not set; LLM call may fail")

    if provider == "openai":
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return (response.choices[0].message.content or "").strip()
        except Exception as e:
            logger.exception("OpenAI API call failed: %s", e)
            raise

    raise ValueError(f"Unsupported LLM provider: {provider}")
