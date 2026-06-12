import re
from urllib.parse import parse_qs, urlparse


def extract_video_id(url_or_id: str) -> str:
    value = url_or_id.strip()
    if re.fullmatch(r"[\w-]{11}", value):
        return value

    parsed = urlparse(value)
    if parsed.hostname in {"youtu.be", "www.youtu.be"}:
        video_id = parsed.path.lstrip("/").split("/")[0]
        if video_id:
            return video_id

    if parsed.hostname in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        query_id = parse_qs(parsed.query).get("v", [None])[0]
        if query_id:
            return query_id

        path_parts = [part for part in parsed.path.split("/") if part]
        if len(path_parts) >= 2 and path_parts[0] in {"embed", "shorts", "live"}:
            return path_parts[1]

    raise ValueError(f"Could not extract video ID from: {url_or_id}")
