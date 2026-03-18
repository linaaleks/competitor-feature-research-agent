# Если git push даёт 403

Кратко: Git использует сохранённый в системе логин/токен. Если он неверный или просрочен — GitHub возвращает 403.

## Что сделать

1. **Удалить старый пароль для GitHub** (терминал):
   ```bash
   git credential-osxkeychain erase
   host=github.com
   protocol=https
   ```
   (Ввести три строки по очереди, в конце дважды Enter.)

2. **Создать новый токен:** https://github.com/settings/tokens → Generate new token (classic) → включить **repo** → скопировать токен.

3. **Снова выполнить push** из папки проекта. При запросе: Username — логин GitHub, Password — вставить **токен** (не пароль от аккаунта).

Альтернативы (без токена): **GitHub CLI** (`gh auth login`) или **SSH** — см. раздел «Если при push в Git ошибка 403» в основном [README](../README.md).
