import json
import os
from pathlib import Path

import openai

from newsfeed.datatypes import BlogSummary

# Get key
with open("api-key.json") as f:
    OPENAI_API_KEY = json.load(f)

openai.api_key = OPENAI_API_KEY["OPENAI_API_KEY"]


def summarize_text(article_text, prefix=None) -> str:
    base_prompt = f"Summarize the following text:\n{article_text}\n"

    if prefix is None:
        prompt = base_prompt + "Summary:"
    else:
        prompt = f"{prefix}, " + base_prompt + "Summary:"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"You are a creative assistant that summarizes text. The user have provided you with an additional request: {prefix}",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=200,
    )
    summary = response.choices[0].message["content"].strip()
    return summary


# Generate new json files with BlogSummary class


def create_summary_json(input_dir, output_dir, summary_type):
    # Create subdir for each summary type
    output_dir = os.path.join(output_dir, summary_type)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Set to keep track of existing output files
    existing_outputs = set(os.listdir(output_dir))

    # Iterate through input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            json_path = os.path.join(input_dir, filename)

            with open(json_path, "r") as file:
                json_content = json.load(file)

                # Here we can call summarize_text()
                # To avoid api-calls, this should not be done before Prompt Engineering stage has been complete
                blog_summary = BlogSummary(**json_content)

                blog_summary.summary = summarize_text(
                    json_content["blog_text"], prefix=summary_type
                )

                # Only static text (e.g. "English Simplified", "Swedish Technical")
                blog_summary.type_of_summary = summary_type

                sum_file = blog_summary.get_filename()
                new_json_path = os.path.join(output_dir, sum_file)

                # Check if output already exist (Or should we overwrite?)
                if sum_file not in existing_outputs:
                    with open(new_json_path, "w") as new_file:
                        json.dump(blog_summary.dict(), new_file, indent=4)
                    existing_outputs.add(sum_file)
                else:
                    print(f"{sum_file} already exist.")
