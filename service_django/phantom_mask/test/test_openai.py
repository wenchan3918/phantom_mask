import json
import os

import openai

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(model="text-davinci-003",
                                    prompt="請自我介紹一下",
                                    temperature=1,
                                    max_tokens=1024)

print(json.dumps(response, ensure_ascii=False, indent=4))

"""
{
    "id": "cmpl-6SQT6xM358ZK44l59XESVtsWpoVWq",
    "object": "text_completion",
    "created": 1672232948,
    "model": "text-davinci-003",
    "choices": [
        {
            "text": "\n\n大家好，我叫XXX，是從XX大學畢業的學生，熱衷於新科技與數據分析，最近正在研究如何利用數據科學、機器學習和大數據分析來解決一些問題。有三年計算機科學的經驗，包多價值，為公司創造更大的收益。",
            "index": 0,
            "logprobs": null,
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 16,
        "completion_tokens": 372,
        "total_tokens": 388
    }
}


"""
