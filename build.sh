#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

python -m pip install --upgrade pip shiv
mkdir -p dist

python -m shiv \
    --entry-point bot:main \
    --output-file dist/youtube-subtitles-bot.pyz \
    --compressed \
    .

echo "Built: dist/youtube-subtitles-bot.pyz"
echo "Run:   python dist/youtube-subtitles-bot.pyz --token YOUR_BOT_TOKEN"
