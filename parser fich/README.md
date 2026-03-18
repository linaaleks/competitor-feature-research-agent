# Competitor Feature Research Agent

ИИ‑агент для конкурентного анализа: поиск конкурентов по теме, сбор страниц, извлечение фич, описание механики, отчёт в Markdown.

Работает в любом окружении: терминал (macOS, Linux, Windows), VS Code, Cursor, PyCharm и т.д. Нужны только **Python 3.9+** и **один бесплатный API-ключ** (OpenRouter по умолчанию).

---

## Запуск с нуля (3 шага)

### 1. Клонировать и зайти в проект

```bash
git clone https://github.com/linaaleks/competitor-feature-research-agent.git
cd competitor-feature-research-agent
cd "parser fich"
```

Все следующие команды — из папки `parser fich`.

### 2. Окружение и ключ нейросети

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Открой `.env` и укажи ключ **OpenRouter** (бесплатно, без пополнения):

- Зайди на https://openrouter.ai/keys → зарегистрируйся → **Create Key**
- В `.env` пропиши: `OPENROUTER_API_KEY=sk-or-v1-твой-ключ`

В `config/agent.yml` по умолчанию уже стоит `provider: openrouter` и `model: openrouter/free` — менять не нужно.

### 3. Запустить research

```bash
python -m src.cli "Тема для анализа" --max-competitors 1 --mechanics-limit 1
```

Если команда ругается на аргументы, попробуй вариант с темой в конце:

```bash
python -m src.cli --max-competitors 1 --mechanics-limit 1 "Тема для анализа"
```

Пример:

```bash
python -m src.cli "EdTech blue-collar training platforms" --max-competitors 1 --mechanics-limit 1
```

Результаты появятся в:
- `data/output/features.json` — карточки фич
- `data/output/mechanics.json` — описания механики
- `data/output/reports/research_*.md` — отчёт в Markdown

Опции:
- `--max-competitors N` — макс. число конкурентов (по умолчанию 2)
- `--mechanics-limit N` — макс. фич для детального описания (по умолчанию 3)
- `-v` / `--verbose` — подробные логи

---

## Какую нейросеть использовать

По умолчанию агент использует **OpenRouter** с бесплатными моделями — не нужно пополнять баланс.

| Провайдер    | Условия | Настройка |
|-------------|---------|-----------|
| **OpenRouter** | Бесплатные модели, один ключ | В `.env`: `OPENROUTER_API_KEY=sk-or-v1-...`. В конфиге уже стоит по умолчанию. |
| **Groq**       | Бесплатный тариф, лимиты запросов | В `.env`: `GROQ_API_KEY=gsk_...`. В `config/agent.yml`: `provider: groq`, `model: llama-3.1-70b-versatile`. |
| **DeepSeek**   | Нужен баланс на платформе | В `.env`: `DEEPSEEK_API_KEY=...`. В конфиге: `provider: deepseek`, `model: deepseek-chat`. |
| **OpenAI**     | Нужна подписка/кредиты | В `.env`: `OPENAI_API_KEY=sk-...`. В конфиге: `provider: openai`, `model: gpt-4o-mini`. |

Подробнее: смотри `config/agent.yml` и `.env.example`.

---

## Структура проекта

```
parser fich/
  src/
    cli.py              # точка входа: python -m src.cli "тема"
    llm/client.py       # вызов LLM (конфиг: config/agent.yml + .env)
    collectors/         # сбор страниц
    extractors/         # поиск конкурентов, извлечение фич
    models/             # FeatureCard, MechanicsDescription, Competitor, Report
    analyzer/           # описание механики
    reporters/          # Markdown-отчёт
  prompts/              # шаблоны промптов для LLM (.md)
  config/agent.yml      # провайдер, модель, пути
  data/raw/             # сохранённый HTML
  data/output/          # features.json, mechanics.json, reports/
```

Промпты: `prompts/extract_features.md` (извлечение фич), `prompts/describe_mechanics.md` (описание механики). Подставляются через `src.llm.load_prompt` и `call_llm`.

---

## Что реализовано

- Поиск конкурентов (stub: 2 фиксированных), сбор страниц, извлечение фич по промпту, описание механики, сохранение JSON и Markdown-отчёт.
- Заглушки: screenshotter (без реальных скриншотов), feature_gaps, market_insights.

---

## Требования

- Python 3.9+ (рекомендуется 3.11)
- Один API-ключ: OpenRouter (рекомендуется, бесплатно), Groq, DeepSeek или OpenAI — см. раздел «Какую нейросеть использовать».

---

## Если при push в Git ошибка 403

- **GitHub CLI:** `brew install gh` → `gh auth login` → выбрать вход через браузер. После этого `git push origin main` работает без токена.
- **SSH:** добавить ключ на https://github.com/settings/keys, затем `git remote set-url origin git@github.com:linaaleks/competitor-feature-research-agent.git` и `git push origin main`.
- **HTTPS + токен:** создать Personal Access Token (scope `repo`) на https://github.com/settings/tokens и при запросе пароля вставлять токен.

---

## Лицензия

MIT (или укажите свою).
