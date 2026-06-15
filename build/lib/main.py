import sys
from pathlib import Path

from subtitle_pipeline import generate_subtitles
from video_id import extract_video_id


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python main.py <youtube-url-or-video-id> [output-dir]")
        return 1

    video_id = extract_video_id(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("output")

    print(f"Fetching subtitles for video: {video_id}")
    srt_path, txt_path = generate_subtitles(video_id, output_dir)

    print(f"SRT saved: {srt_path.resolve()}")
    print(f"Text saved: {txt_path.resolve()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
