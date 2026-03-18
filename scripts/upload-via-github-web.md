# Agent configuration: LLM, API keys (override via .env)
# provider: openrouter (бесплатно) | groq | deepseek | openai | openai_compatible
llm:
  provider: openrouter   # бесплатные модели — ключ: https://openrouter.ai/keys
  model: openrouter/free # или groq: llama-3.1-70b-versatile, deepseek: deepseek-chat
  temperature: 0.2
  max_tokens: 4096

# Paths
paths:
  prompts_dir: prompts
  data_raw: data/raw
  data_output: data/output
  reports_dir: data/output/reports
  screenshots_dir: data/output/screenshots
