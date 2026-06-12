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

## Структура

- `main.py` — CLI
- `video_id.py` — извлечение video ID из URL
- `fetch_subtitles.py` — загрузка субтитров через `youtube-transcript-api`
- `srt_writer.py` — запись SRT
- `text_extractor.py` — извлечение plain text из SRT
