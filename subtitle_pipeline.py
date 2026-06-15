from pathlib import Path

from fetch_subtitles import fetch_transcript
from srt_writer import write_srt
from text_extractor import write_text_file


def generate_subtitles(video_id: str, output_dir: Path) -> tuple[Path, Path]:
    segments = fetch_transcript(video_id)
    srt_path = output_dir / f"{video_id}.srt"
    txt_path = output_dir / f"{video_id}.txt"
    write_srt(segments, srt_path)
    write_text_file(srt_path, txt_path)
    return srt_path, txt_path
