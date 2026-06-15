import argparse
import asyncio
import os
import shutil
import sys
import tempfile
from pathlib import Path

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from youtube_transcript_api.proxies import ProxyConfig

from fetch_subtitles import resolve_webshare_proxy_config
from subtitle_pipeline import generate_subtitles
from video_id import extract_video_id

HELP_TEXT = (
    "Отправьте ссылку на YouTube-видео или video ID (11 символов).\n"
    "В ответ вы получите файлы .srt (с таймкодами) и .txt (только текст)."
)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(HELP_TEXT)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(HELP_TEXT)


def make_message_handler(proxy_config: ProxyConfig | None):
    async def handle_message(
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        if not update.message or not update.message.text:
            return

        text = update.message.text.strip()
        status_message = await update.message.reply_text("Загружаю субтитры…")

        try:
            video_id = extract_video_id(text)
        except ValueError as exc:
            await status_message.edit_text(str(exc))
            return

        temp_dir = Path(tempfile.mkdtemp())
        try:
            srt_path, txt_path = await asyncio.to_thread(
                generate_subtitles, video_id, temp_dir, proxy_config
            )

            await status_message.edit_text(f"Готово: {video_id}")

            with srt_path.open("rb") as srt_file:
                await update.message.reply_document(
                    document=srt_file,
                    filename=srt_path.name,
                )

            with txt_path.open("rb") as txt_file:
                await update.message.reply_document(
                    document=txt_file,
                    filename=txt_path.name,
                )
        except (RuntimeError, ValueError) as exc:
            await status_message.edit_text(str(exc))
        except Exception:
            await status_message.edit_text(
                "Не удалось загрузить субтитры. Попробуйте позже."
            )
            raise
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    return handle_message


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Telegram bot for YouTube subtitles")
    parser.add_argument(
        "--token",
        help="Telegram bot token (overrides TELEGRAM_BOT_TOKEN env var)",
    )
    parser.add_argument(
        "--webshare-proxy-username",
        help="Webshare proxy username (overrides WEBSHARE_PROXY_USERNAME env var)",
    )
    parser.add_argument(
        "--webshare-proxy-password",
        help="Webshare proxy password (overrides WEBSHARE_PROXY_PASSWORD env var)",
    )
    return parser.parse_args()


def resolve_token(args: argparse.Namespace) -> str:
    token = args.token or os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print(
            "Error: bot token is required. "
            "Use --token or set TELEGRAM_BOT_TOKEN environment variable.",
            file=sys.stderr,
        )
        sys.exit(1)
    return token


def resolve_proxy_config(args: argparse.Namespace) -> ProxyConfig | None:
    username = args.webshare_proxy_username or os.environ.get(
        "WEBSHARE_PROXY_USERNAME"
    )
    password = args.webshare_proxy_password or os.environ.get(
        "WEBSHARE_PROXY_PASSWORD"
    )
    try:
        return resolve_webshare_proxy_config(username, password)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    args = parse_args()
    token = resolve_token(args)
    proxy_config = resolve_proxy_config(args)

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, make_message_handler(proxy_config))
    )

    print("Bot is running. Press Ctrl+C to stop.")
    application.run_polling()


if __name__ == "__main__":
    main()
