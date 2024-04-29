import os
import openai
from openai import OpenAI
from dotenv import load_dotenv


def chat(user_prompt, system_prompt,openai_api_key):
    client = OpenAI(api_key= openai_api_key)
    messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages= messages,
    temperature=0,
    max_tokens=4000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    return response.choices[0].message.content