# Телеграм бот для игры Arkham Horror the card game.

Заменяет собой мешок с жетонами хаоса. Позволяет хранить все жетоны в приложении, доставать их из мешка и т.п.

## Как запустить
Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Создать таблицы в базе данных:

```
python3 db.py make_db
```

Запустить проект:

```
python3 Telegram_bot.py main
```

