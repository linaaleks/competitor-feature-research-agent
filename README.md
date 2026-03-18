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

### 2. Окружение и ключ нейросети (подробно)

Делай всё по порядку в терминале (из папки `parser fich`).

**2.1. Создать виртуальное окружение**

Введи и нажми Enter:
```bash
python3 -m venv .venv
```
Потом включи его:
- **Mac/Linux:** `source .venv/bin/activate`
- **Windows:** `.venv\Scripts\activate`

После этого в начале строки появится `(.venv)` — окружение включено.

**2.2. Поставить зависимости**

```bash
pip install -r requirements.txt
```
Дождись окончания.

**2.3. Создать файл с настройками**

Если `.env.example` лежит **в этой же папке** (`parser fich`):
```bash
cp .env.example .env
```
Если `.env.example` в **корне репо** (на уровень выше):
```bash
cp ../.env.example .env
```

Файл `.env` появится в папке `parser fich`. Открой его в редакторе.

**2.4. Получить бесплатный ключ OpenRouter**

1. Открой в браузере: **https://openrouter.ai/keys**
2. Зарегистрируйся при необходимости.
3. Нажми **Create Key**, придумай имя, скопируй ключ (начинается с `sk-or-v1-...`). Сохрани — потом не покажут.

**2.5. Вписать ключ в проект**

В файле `.env` найди строку `OPENROUTER_API_KEY=sk-or-v1-...` и замени `sk-or-v1-...` на свой ключ. Без кавычек, без пробелов вокруг `=`. Сохрани файл.

**2.6. Конфиг**

В `config/agent.yml` по умолчанию уже стоит `provider: openrouter` и `model: openrouter/free`. Менять не нужно — переходи к шагу 3.

### 3. Запустить research

```bash
python -m src.cli "Тема для анализа" --max-competitors 1 --mechanics-limit 1
```

Если команда ругается на аргументы — попробуй с темой в конце:
```bash
python -m src.cli --max-competitors 1 --mechanics-limit 1 "Тема для анализа"
```

Пример:
```bash
python -m src.cli "EdTech blue-collar training platforms" --max-competitors 1 --mechanics-limit 1
```

Результаты:
- `data/output/features.json` — карточки фич
- `data/output/mechanics.json` — описания механики
- `data/output/reports/research_*.md` — отчёт в Markdown

Опции: `--max-competitors N`, `--mechanics-limit N`, `-v` / `--verbose`.

---

## Какую нейросеть использовать

По умолчанию — **OpenRouter** (бесплатные модели, без пополнения).

| Провайдер    | Условия | Настройка |
|-------------|---------|-----------|
| **OpenRouter** | Бесплатно | В `.env`: `OPENROUTER_API_KEY=sk-or-v1-...`. В конфиге уже по умолчанию. |
| **Groq**       | Бесплатный тариф | В `.env`: `GROQ_API_KEY=gsk_...`. В `config/agent.yml`: `provider: groq`, `model: llama-3.1-70b-versatile`. |
| **DeepSeek**   | Нужен баланс | В `.env`: `DEEPSEEK_API_KEY=...`. В конфиге: `provider: deepseek`, `model: deepseek-chat`. |
| **OpenAI**     | Подписка/кредиты | В `.env`: `OPENAI_API_KEY=sk-...`. В конфиге: `provider: openai`, `model: gpt-4o-mini`. |

Подробнее: `config/agent.yml` и `.env.example`.

---

## Структура проекта

```
parser fich/
  src/
    cli.py              # точка входа: python -m src.cli "тема"
    llm/client.py       # вызов LLM (config/agent.yml + .env)
    collectors/         # сбор страниц
    extractors/         # поиск конкурентов, извлечение фич
    models/             # FeatureCard, MechanicsDescription, Competitor, Report
    analyzer/           # описание механики
    reporters/          # Markdown-отчёт
  prompts/              # шаблоны промптов (.md)
  config/agent.yml      # провайдер, модель, пути
  data/raw/             # сохранённый HTML
  data/output/          # features.json, mechanics.json, reports/
```

---

## Что реализовано

Поиск конкурентов (stub), сбор страниц, извлечение фич, описание механики, JSON и Markdown-отчёт. Заглушки: screenshotter, feature_gaps, market_insights.

---

## Требования

- Python 3.9+ (рекомендуется 3.11)
- Один API-ключ: OpenRouter (рекомендуется), Groq, DeepSeek или OpenAI.

---

## Если при push в Git ошибка 403

- **GitHub CLI:** `brew install gh` → `gh auth login` → вход через браузер. Дальше `git push origin main` без токена.
- **SSH:** ключ на https://github.com/settings/keys → `git remote set-url origin git@github.com:linaaleks/competitor-feature-research-agent.git` → `git push origin main`.
- **HTTPS + токен:** Personal Access Token (scope `repo`) на https://github.com/settings/tokens → при запросе пароля вставлять токен.

---

## Лицензия

MIT (или укажите свою).
