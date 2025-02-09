import sys
import requests
import srt
from pathlib import Path

def translate_with_api(text: str) -> str:
    response = requests.post(
        "http://127.0.0.1:1337/v1/chat/completions",
        headers = {"Content-Type": "application/json"},
        json={
            "messages": [
                {
                    "role": "user",
                    "content": f"You are a professional translator. Translate the following English text into Japanese. Do not include any additional explanations, system messages, or formatting—provide only the translated text as your answer. : {text}"
                }
            ],
            "model": "Llama-3-ELYZA-JP-8B-q4_k_m",
            "stream": False,
            "max_tokens": 1024,
            "stop": ["End"]
        }
    )
    answer = response.json()['choices'][0]['message']['content']
    return answer.replace("<|eot_id|>", "")

def main():
    srt_file = Path(sys.argv[1])
    with srt_file.open("r", encoding="utf-8") as f:
        srt_content = f.read()

    subtitles = list(srt.parse(srt_content))
    total = len(subtitles)
    for idx, subtitle in enumerate(subtitles, start=1):
        english_text = subtitle.content.strip()
        translation = translate_with_api(english_text)
        print(f"[{idx}/{total}] {translation}")
        subtitle.content = f"{english_text}\n{translation}"

    output_content = srt.compose(subtitles)
    output_file = srt_file.with_name(srt_file.stem + "_translated.srt")
    with output_file.open("w", encoding="utf-8") as f:
        f.write(output_content)

if __name__ == "__main__":
    main()