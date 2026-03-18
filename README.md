# Competitor Feature Research Agent

ИИ‑агент для глубокого конкурентного анализа фич: поиск конкурентов по теме, сбор страниц, извлечение фич, описание механики, скриншоты, отчёт в Markdown.

**Запускается где угодно:** в обычном терминале (macOS, Linux, Windows), в VS Code, PyCharm, Cursor, GitHub Codespaces и т.д. — нужны только Python 3.9+ и зависимости из `requirements.txt`. Cursor не обязателен.

---

## Как скопировать и запустить

Любой пользователь может склонировать репозиторий и запустить агента локально (в Cursor, VS Code или в терминале).

### 1. Клонировать репозиторий

```bash
git clone https://github.com/linaaleks/competitor-feature-research-agent.git
cd competitor-feature-research-agent
cd "parser fich"
```

Проект лежит в папке `parser fich` — все следующие команды выполняйте из неё.

### 2. Открыть проект (по желанию)

- В **Cursor** или **VS Code**: File → Open Folder → папка `parser fich`
- Или просто работайте в терминале из этой папки

### 3. Установить зависимости и настроить окружение

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

В файле `.env` укажите API-ключ в зависимости от выбранного провайдера (см. ниже **Бесплатные нейросети**).

### 4. Запустить research

Из корня проекта (с активированным `.venv`):

```bash
python -m src.cli "EdTech blue-collar training platforms"
```

С ограничением числа конкурентов и вызовов LLM (для теста):

```bash
python -m src.cli "EdTech blue-collar training" --max-competitors 1 --mechanics-limit 1
```

Результаты:
- `data/output/features.json` — карточки фич
- `data/output/mechanics.json` — описания механики
- `data/output/reports/research_*.md` — отчёт в Markdown
- `data/raw/` — сохранённый HTML страниц

---

## Бесплатные нейросети (DeepSeek и др.)

Агент умеет работать не только с OpenAI, но и с **DeepSeek** (бесплатный/дешёвый API) и любым **OpenAI-совместимым** API.

### DeepSeek

1. Получи ключ: https://platform.deepseek.com/
2. В `config/agent.yml` задай:
   ```yaml
   llm:
     provider: deepseek
     model: deepseek-chat
   ```
3. В `.env` добавь:
   ```
   DEEPSEEK_API_KEY=sk-твой-ключ
   ```

После этого запуск как обычно — агент будет вызывать DeepSeek вместо OpenAI.

### Другой OpenAI-совместимый API

В `config/agent.yml`:
```yaml
llm:
  provider: openai_compatible
  base_url: https://api.example.com/v1
  model: model-name
```
В `.env`: `LLM_API_KEY=твой-ключ` (и при необходимости `LLM_BASE_URL`, `LLM_MODEL`).

### Переключение обратно на OpenAI

В `config/agent.yml` поставь `provider: openai` и в `.env` задай `OPENAI_API_KEY=sk-...`.

---

## Запуск (кратко)

```bash
pip install -r requirements.txt
cp .env.example .env   # задать DEEPSEEK_API_KEY или OPENAI_API_KEY

python -m src.cli "EdTech blue-collar training platforms"
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
- API-ключ одного из провайдеров: OpenAI или DeepSeek (в `.env`)

---

## Если при push ошибка 403 или запрос логина

**Способ 1 — GitHub CLI (проще всего)**  
Устанавливаешь раз, логинишься через браузер — дальше `git push` работает без токена в терминале.

```bash
brew install gh
gh auth login
```

Выбери GitHub.com → HTTPS → Yes (authenticate Git) → Login with browser. После этого в этой папке снова: `git push origin main`.

**Способ 2 — SSH**  
Если уже добавила SSH-ключ в https://github.com/settings/keys:

```bash
git remote set-url origin git@github.com:linaaleks/competitor-feature-research-agent.git
git push origin main
```

**Способ 3 — новый токен (HTTPS)**  
Создай новый Personal Access Token: https://github.com/settings/tokens → Generate new token (classic) → включи только **repo** → скопируй токен. При запросе пароля в терминале вставляй этот токен (логин — твой GitHub username).

---

## Лицензия

MIT (или укажите свою).
