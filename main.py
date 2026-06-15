import argparse
import os
import sys
from pathlib import Path

from fetch_subtitles import resolve_webshare_proxy_config
from subtitle_pipeline import generate_subtitles
from video_id import extract_video_id


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download YouTube subtitles as SRT and plain text"
    )
    parser.add_argument("video", help="YouTube URL or video ID")
    parser.add_argument(
        "output_dir",
        nargs="?",
        default="output",
        help="Output directory (default: output)",
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


def resolve_proxy_config(args: argparse.Namespace):
    username = args.webshare_proxy_username or os.environ.get(
        "WEBSHARE_PROXY_USERNAME"
    )
    password = args.webshare_proxy_password or os.environ.get(
        "WEBSHARE_PROXY_PASSWORD"
    )
    return resolve_webshare_proxy_config(username, password)


def main() -> int:
    args = parse_args()

    try:
        video_id = extract_video_id(args.video)
        proxy_config = resolve_proxy_config(args)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    output_dir = Path(args.output_dir)

    print(f"Fetching subtitles for video: {video_id}")
    srt_path, txt_path = generate_subtitles(video_id, output_dir, proxy_config)

    print(f"SRT saved: {srt_path.resolve()}")
    print(f"Text saved: {txt_path.resolve()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
