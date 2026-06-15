# YouTube Get Subtitles

Скачивает субтитры с YouTube-видео в полный формат `.srt`, затем извлекает из них текстовый файл `.txt`.

## Требования

- Python 3.10+

## Установка

```bash
pip install -r requirements.txt
```

## Запуск

```bash
python main.py <youtube-url-or-video-id> [output-dir]
```

Пример:

```bash
python main.py https://www.youtube.com/watch?v=o4_Etmw9Zy8
```

Результат по умолчанию сохраняется в `output/`:

- `{videoId}.srt` — полные субтитры с таймкодами
- `{videoId}.txt` — только текст без таймкодов

## Telegram-бот

1. Создайте бота через [@BotFather](https://t.me/BotFather) и получите токен.
2. Установите зависимости (см. выше).
3. Запустите бота:

```bash
python bot.py --token YOUR_BOT_TOKEN
```

Или через переменную окружения:

```bash
set TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
python bot.py
```

Отправьте боту ссылку на YouTube-видео или video ID — в ответ придут файлы `.srt` и `.txt`.

Команды бота: `/start`, `/help`.

## Сборка в один файл (Linux)

Код остаётся в отдельных модулях. Для деплоя можно собрать один `.pyz` со всеми зависимостями (аналог uber-jar) через [shiv](https://github.com/linkedin/shiv):

```bash
chmod +x build.sh
./build.sh
```

Результат: `dist/youtube-subtitles-bot.pyz` (~15–25 MB). Скопируйте этот файл на сервер — `pip install` на целевой машине не нужен, только Python 3.10+.

```bash
python youtube-subtitles-bot.pyz --token YOUR_BOT_TOKEN
```

Или через переменную окружения:

```bash
export TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
python youtube-subtitles-bot.pyz
```

| Режим | Команда |
|-------|---------|
| Разработка | `pip install -r requirements.txt && python bot.py --token ...` |
| Сборка | `./build.sh` |
| Деплой | `python youtube-subtitles-bot.pyz --token ...` |

## Структура

- `main.py` — CLI
- `bot.py` — Telegram-бот
- `build.sh` — сборка `dist/youtube-subtitles-bot.pyz`
- `pyproject.toml` — метаданные проекта и entry point для shiv
- `subtitle_pipeline.py` — общий пайплайн SRT + TXT
- `video_id.py` — извлечение video ID из URL
- `fetch_subtitles.py` — загрузка субтитров через `youtube-transcript-api`
- `srt_writer.py` — запись SRT
- `text_extractor.py` — извлечение plain text из SRT
