import sys
from pathlib import Path

from fetch_subtitles import fetch_transcript
from srt_writer import write_srt
from text_extractor import write_text_file
from video_id import extract_video_id


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python main.py <youtube-url-or-video-id> [output-dir]")
        return 1

    video_id = extract_video_id(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("output")

    srt_path = output_dir / f"{video_id}.srt"
    txt_path = output_dir / f"{video_id}.txt"

    print(f"Fetching subtitles for video: {video_id}")
    segments = fetch_transcript(video_id)

    write_srt(segments, srt_path)
    print(f"SRT saved: {srt_path.resolve()}")

    write_text_file(srt_path, txt_path)
    print(f"Text saved: {txt_path.resolve()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
