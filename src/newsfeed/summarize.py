import json

import langchain
import openai

# Get key
with open("api-key.json") as f:
    OPENAI_API_KEY = json.load(f)

openai.api_key = OPENAI_API_KEY["OPENAI_API_KEY"]


def summarize_text(article) -> str:
    prompt = f"Summarize the following text:\n{article}\nSummary:"
    response = openai.Completion.create(
        engine="text-davinci-003",  # GPT-3 since it's cheaper
        prompt=prompt,
        max_tokens=200,  # We might want to make this an input argument, or in some other way adjust this
    )
    summary = response.choices[
        0
    ].text.strip()  # GPT-3 can provide multiple completion suggestions, we just take the first
    return summary
