from pathlib import Path

from fetch_subtitles import fetch_transcript
from srt_writer import write_srt
from text_extractor import write_text_file
from youtube_transcript_api.proxies import ProxyConfig


def generate_subtitles(
    video_id: str,
    output_dir: Path,
    proxy_config: ProxyConfig | None = None,
) -> tuple[Path, Path]:
    segments = fetch_transcript(video_id, proxy_config=proxy_config)
    srt_path = output_dir / f"{video_id}.srt"
    txt_path = output_dir / f"{video_id}.txt"
    write_srt(segments, srt_path)
    write_text_file(srt_path, txt_path)
    return srt_path, txt_path
