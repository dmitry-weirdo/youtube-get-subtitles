from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)


LANGUAGE_PRIORITY = ("ru", "en")


def fetch_transcript(video_id: str) -> list[dict]:
    api = YouTubeTranscriptApi()
    try:
        transcript = api.fetch(video_id, languages=LANGUAGE_PRIORITY)
        return transcript.to_raw_data()
    except NoTranscriptFound:
        pass
    except TranscriptsDisabled as exc:
        raise RuntimeError(f"Subtitles are disabled for video: {video_id}") from exc
    except VideoUnavailable as exc:
        raise RuntimeError(f"Video is unavailable: {video_id}") from exc

    try:
        transcript_list = api.list(video_id)
        language_codes = [transcript.language_code for transcript in transcript_list]
        if not language_codes:
            raise RuntimeError(f"No subtitles found for video: {video_id}")

        transcript = transcript_list.find_generated_transcript(language_codes)
        return transcript.fetch().to_raw_data()
    except NoTranscriptFound as exc:
        raise RuntimeError(f"No subtitles found for video: {video_id}") from exc
    except TranscriptsDisabled as exc:
        raise RuntimeError(f"Subtitles are disabled for video: {video_id}") from exc
    except VideoUnavailable as exc:
        raise RuntimeError(f"Video is unavailable: {video_id}") from exc
