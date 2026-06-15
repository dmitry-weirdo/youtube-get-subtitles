import re
from pathlib import Path


TIMESTAMP_LINE = re.compile(
    r"^\d{2}:\d{2}:\d{2},\d{3}\s+-->\s+\d{2}:\d{2}:\d{2},\d{3}$"
)


def _parse_srt_text(content: str) -> list[str]:
    blocks = re.split(r"\n\s*\n", content.strip())
    texts: list[str] = []

    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue

        if lines[0].isdigit():
            lines = lines[1:]
        if lines and TIMESTAMP_LINE.match(lines[0]):
            lines = lines[1:]

        if lines:
            texts.append(" ".join(lines))

    return texts


def _deduplicate_overlap(texts: list[str]) -> list[str]:
    if not texts:
        return []

    result = [texts[0]]
    for text in texts[1:]:
        previous = result[-1]
        if text == previous:
            continue

        overlap = 0
        max_overlap = min(len(previous), len(text))
        for size in range(max_overlap, 0, -1):
            if previous.endswith(text[:size]):
                overlap = size
                break

        result.append(text[overlap:] if overlap else text)

    return result


def extract_text_from_srt(srt_path: Path) -> str:
    content = srt_path.read_text(encoding="utf-8")
    texts = _parse_srt_text(content)
    merged = _deduplicate_overlap(texts)
    return " ".join(part.strip() for part in merged if part.strip())


def write_text_file(srt_path: Path, output_path: Path) -> None:
    text = extract_text_from_srt(srt_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
