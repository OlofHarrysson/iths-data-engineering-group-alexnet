import datetime as dt
import json
import os
from pathlib import Path

import openai

from newsfeed.datatypes import BlogSummary

summary_types = {
    "normal": "",
    "non_technical": "in a clear and simple manner suitable for a broad audience. Avoid technical jargon and keep sentences concise. Make sure a 4 year old could read and understand it. The text must simple enough that a 4 year old could read and understand it. People with no previous knowledge in technology needs to be able to read it. The english must be simple and plain, so that people with english as second language can understand it. Include descriptions in parenthesis for any acronyms such as AI (Artifical Intellegence)",
    "french": "and translate it into French and in max 30 words",
    "swedish": "in Swedish and in max 30 words",
}


def summarize_text(article_text, suffix="normal") -> str:
    with open("api-key.json") as f:
        OPENAI_API_KEY = json.load(f)

    openai.api_key = OPENAI_API_KEY["OPENAI_API_KEY"]

    prompt = f"Summarize the following text {suffix}:\nText:{article_text}\n"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"""You are an assistant that summarizes text. You only respond with the summarized text.""",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=200,
    )
    summary = response.choices[0].message["content"].strip()
    return summary


def translate_title(title, type):
    with open("api-key.json") as f:
        OPENAI_API_KEY = json.load(f)

    openai.api_key = OPENAI_API_KEY["OPENAI_API_KEY"]

    # prompt / context to chat gpt.
    conversation = [
        {"role": "system", "content": "You are a helpful assistant that translates titles."},
        {
            "role": "user",
            "content": f"Translate the following title from English to {type}: {title}",
        },
    ]

    # the response from chat gpt.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=conversation, max_tokens=50
    )

    # gets the title from the response.
    translated_title = response["choices"][0]["message"]["content"].strip()
    return translated_title
