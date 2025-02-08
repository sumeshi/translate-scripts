import os
import sys
from pathlib import Path
import datetime

import srt
import torch
import whisper
from transformers import MarianMTModel, MarianTokenizer


def seconds_to_timedelta(seconds: float) -> datetime.timedelta:
    return datetime.timedelta(seconds=seconds)

def load_translation_model(model_name: str = "Helsinki-NLP/opus-mt-en-jap"):
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    if torch.cuda.is_available():
        model.cuda()
    return tokenizer, model

def translate_text(text: str, tokenizer, model) -> str:
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    if torch.cuda.is_available():
        inputs = {key: val.cuda() for key, val in inputs.items()}
    translated_tokens = model.generate(**inputs)
    return tokenizer.decode(translated_tokens[0], skip_special_tokens=True)

def generate_subtitles(audio_file: Path, whisper_model, tokenizer, translation_model):
    result = whisper_model.transcribe(str(audio_file), language="en")
    segments = result.get("segments", [])
    subtitles = []
    for index, seg in enumerate(segments, start=1):
        start = seg["start"]
        end = seg["end"]
        english_text = seg["text"].strip()
        japanese_text = translate_text(english_text, tokenizer, translation_model)
        content = f"{english_text}\n{japanese_text}"
        subtitle = srt.Subtitle(
            index=index,
            start=seconds_to_timedelta(start),
            end=seconds_to_timedelta(end),
            content=content
        )
        subtitles.append(subtitle)
    return subtitles

def main():
    audio_file = Path(sys.argv[1])
    whisper_model = whisper.load_model("medium")

    tokenizer, translation_model = load_translation_model()
    subtitles = generate_subtitles(audio_file, whisper_model, tokenizer, translation_model)
    srt_output = srt.compose(subtitles)

    output_file = audio_file.with_suffix('.srt')
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(srt_output)

if __name__ == "__main__":
    main()
