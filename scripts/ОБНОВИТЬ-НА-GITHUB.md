# Как обновить два файла на GitHub (вручную)

При загрузке папки GitHub **не перезаписывает** уже существующие файлы. Нужно отредактировать их в браузере.

## 1. config/agent.yml

1. Открой в браузере:  
   **https://github.com/linaaleks/competitor-feature-research-agent/edit/main/parser%20fich/config/agent.yml**

2. Выдели весь текст в редакторе (Ctrl+A / Cmd+A), удали.

3. Открой на компьютере файл **config/agent.yml** (в этой же папке parser fich), скопируй всё (Ctrl+A → Ctrl+C), вставь в окно GitHub.

4. Внизу нажми **Commit changes**.

---

## 2. src/llm/client.py

1. Открой в браузере:  
   **https://github.com/linaaleks/competitor-feature-research-agent/edit/main/parser%20fich/src/llm/client.py**

2. Выдели весь текст в редакторе, удали.

3. Открой на компьютере файл **src/llm/client.py**, скопируй всё, вставь в окно GitHub.

4. Внизу нажми **Commit changes**.

---

После этого в репо будет актуальная версия с OpenRouter по умолчанию.
