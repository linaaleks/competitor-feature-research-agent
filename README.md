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
Ничего не должно упасть. Потом включи его:
- **Mac/Linux:** `source .venv/bin/activate`
- **Windows:** `.venv\Scripts\activate`

После этого в начале строки в терминале появится `(.venv)` — значит, окружение включено.

**2.2. Поставить зависимости**

Введи и нажми Enter:
```bash
pip install -r requirements.txt
```
Дождись окончания (установятся библиотеки). Ошибок быть не должно.

**2.3. Создать файл с настройками**

Введи и нажми Enter:
```bash
cp .env.example .env
```
Так из примера создаётся твой файл `.env` (в нём будут храниться ключи). Файл `.env` лежит в папке `parser fich` — там же, где README.

**2.4. Получить бесплатный ключ OpenRouter**

1. Открой в браузере: **https://openrouter.ai/keys**
2. Если просят — зарегистрируйся (логин/пароль или через Google/GitHub).
3. На странице нажми кнопку **Create Key** (или «Создать ключ»).
4. Придумай имя ключу (например: `agent`) и нажми создать.
5. **Скопируй ключ** — он выглядит как длинная строка, начинается с `sk-or-v1-...`. Сохрани её: потом она больше не покажется целиком.

**2.5. Вписать ключ в проект**

1. Открой папку `parser fich` в проводнике (Finder на Mac) или в Cursor/VS Code.
2. Найди файл **`.env`** (он может быть скрыт — включи «показывать скрытые файлы» при необходимости).
3. Открой `.env` в любом редакторе (Блокнот, Cursor, VS Code).
4. Найди строку: `OPENROUTER_API_KEY=sk-or-v1-...`
5. **Замени** `sk-or-v1-...` на твой скопированный ключ. Должно получиться что-то вроде:
   ```
   OPENROUTER_API_KEY=sk-or-v1-abc123xyz...
   ```
   Без кавычек, без пробелов вокруг `=`. Сохрани файл (Ctrl+S / Cmd+S).

**2.6. Конфиг агента**

Файл `config/agent.yml` менять не нужно — там уже указано использовать OpenRouter и бесплатную модель. Просто переходи к шагу 3.

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
