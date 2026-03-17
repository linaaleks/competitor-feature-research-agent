# Competitor Feature Research Agent

ИИ‑агент для глубокого конкурентного анализа фич: поиск конкурентов по теме, сбор страниц, извлечение фич, описание механики, скриншоты, отчёт в Markdown.

---

## Как скопировать и запустить в Cursor

Любой пользователь может склонировать репозиторий и запустить агента локально в Cursor.

### 1. Клонировать репозиторий

```bash
git clone https://github.com/linaaleks/competitor-feature-research-agent.git
cd competitor-feature-research-agent
cd "parser fich"
```

Проект лежит в папке `parser fich` — все следующие команды выполняйте из неё.

### 2. Открыть проект в Cursor

- **File → Open Folder** → выберите папку `parser fich` (внутри склонированного репо)
- Или в терминале Cursor: `cursor .` из корня проекта

### 3. Установить зависимости и настроить окружение

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

В файле `.env` укажите ваш **OPENAI_API_KEY** (обязательно для извлечения фич и описания механики):

```
OPENAI_API_KEY=sk-...
```

### 4. Запустить research

Из корня проекта (с активированным `.venv`):

```bash
python -m src.cli research "EdTech blue-collar training platforms"
```

С ограничением числа конкурентов и вызовов LLM (для теста):

```bash
python -m src.cli research "EdTech blue-collar training" --max-competitors 1 --mechanics-limit 1
```

Результаты:
- `data/output/features.json` — карточки фич
- `data/output/mechanics.json` — описания механики
- `data/output/reports/research_*.md` — отчёт в Markdown
- `data/raw/` — сохранённый HTML страниц

---

## Запуск (кратко)

```bash
pip install -r requirements.txt
cp .env.example .env   # задать OPENAI_API_KEY

python -m src.cli research "EdTech blue-collar training platforms"
```

Опции:
- `--verbose` / `-v` — подробные логи
- `--max-competitors N` — макс. число конкурентов (по умолчанию 2)
- `--mechanics-limit N` — макс. число фич для describe_mechanics (по умолчанию 3)

## Структура проекта

```
src/
  cli.py                 # команда research
  llm/client.py          # load_prompt, call_llm (конфиг: config/agent.yml + .env)
  collectors/            # web_collector, screenshotter
  extractors/            # competitor_finder, feature_extractor
  models/                # FeatureCard, MechanicsDescription, Competitor, ResearchReport
  analyzer/              # mechanics_describer, feature_gaps, market_insights
  reporters/             # markdown_reporter, assets
prompts/                 # промпты для LLM (.md)
data/raw/                # HTML-снимки
data/output/             # reports/, screenshots/, features.json, mechanics.json
config/agent.yml         # модель, пути, провайдер LLM
```

## How prompts are used

Промпты лежат в `prompts/*.md` и подставляются в вызовы LLM через `src.llm.load_prompt` и `call_llm`.

| Файл промпта | Назначение | Выход (Pydantic) |
|--------------|------------|-------------------|
| **extract_features.md** | Извлечение фич из текста страницы (features, pricing, changelog, docs). Переменные: `{text}`, `{url}`, `{screenshot_paths}`. | Список **FeatureCard** |
| **describe_mechanics.md** | Детальное описание механики одной фичи: шаги, сущности, настройки, UI. Переменные: `{feature_card_json}`, `{extra_context}`, `{screenshot_paths}`. | **MechanicsDescription** |

## Что реализовано / заглушки

- **Реализовано:** структура проекта, Pydantic-модели, CLI `research`, загрузка промптов и вызов LLM, извлечение фич по `extract_features.md`, описание механики по `describe_mechanics.md`, сохранение `features.json` и `mechanics.json`, генерация Markdown-отчёта, сбор страниц (web_collector).
- **Заглушки:** competitor_finder (2 фиксированных конкурента), screenshotter (без реальных скриншотов), feature_gaps, market_insights.

## Требования

- Python 3.9+ (рекомендуется 3.11)
- OpenAI API key (в `.env`)

## Лицензия

MIT (или укажите свою).
