import sys
import requests

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
    translation = translate_with_api(sys.argv[1])
    print(translation)

if __name__ == "__main__":
    main()