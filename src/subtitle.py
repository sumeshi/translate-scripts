import sys
import datetime
from pathlib import Path

import srt
import torch
from faster_whisper import WhisperModel


def seconds_to_timedelta(seconds: float) -> datetime.timedelta:
    return datetime.timedelta(seconds=seconds)

def generate_subtitles(audio_file: Path, model: WhisperModel):
    segments, info = model.transcribe(str(audio_file), beam_size=5)
    segments = list(segments)
    total = len(segments)
    subtitles = []
    for index, segment in enumerate(segments, start=1):
        print(f"Processing segment {index}/{total}...", flush=True)
        start = segment.start
        end = segment.end
        text = segment.text.strip()
        subtitle = srt.Subtitle(
            index=index,
            start=seconds_to_timedelta(start),
            end=seconds_to_timedelta(end),
            content=text
        )
        subtitles.append(subtitle)
    return subtitles

def main():
    audio_file = Path(sys.argv[1])

    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "float32"
    model = WhisperModel("base.en", device=device, compute_type=compute_type)

    subtitles = generate_subtitles(audio_file, model)
    srt_output = srt.compose(subtitles)

    output_file = audio_file.with_suffix('.srt')
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(srt_output)

if __name__ == "__main__":
    main()