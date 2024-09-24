import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set. Please set it before using this library.")

client = OpenAI(api_key=api_key)


def get_completion(messages, model="gpt-4o-mini", temperature=0, logprobs=True, top_logprobs=20):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        logprobs=logprobs,
        top_logprobs=top_logprobs
    )
    return response
