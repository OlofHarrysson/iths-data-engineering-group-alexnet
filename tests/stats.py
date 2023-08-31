import json
import os

import nltk
import pandas as pd
from nltk.tokenize import word_tokenize

nltk.download("punkt")


def load_json_file(file_path):
    try:
        with open(file_path, "r") as json_file:
            return json.load(json_file)
    except json.JSONDecodeError as e:
        print("Error loading JSON in file:", file_path)
        print("Error message:", e)
        return None


def calculate_cost(total_tokens, price_per_1k_tokens):
    total_tokens_in_1k = total_tokens / 1000
    total_cost = total_tokens_in_1k * price_per_1k_tokens

    return total_cost


def main():
    article_path = "data/data_warehouse/mit/articles"
    data_list = []

    files_and_directories = os.listdir(article_path)

    for item in files_and_directories:
        if os.path.isfile(os.path.join(article_path, item)) and item.endswith(".json"):
            data = load_json_file(os.path.join(article_path, item))
            if data:
                data_list.append(data)

    df = pd.DataFrame(data_list)

    # print(df.columns)

    df["blog_text_length"] = df["blog_text"].apply(len)
    average_length = df["blog_text_length"].mean()

    print(f"Average length of 'blog_text': {average_length:.2f} characters")

    # Tokenize 'blog_text' and calculate total number of tokens
    total_tokens = 0
    for text in df["blog_text"]:
        tokens = word_tokenize(text)
        total_tokens += len(tokens)

    print("Total number of tokens in 'blog_text':", total_tokens)

    price_per_1k_tokens = 0.0015  # GPT-3.5 Turbo

    total_cost = calculate_cost(total_tokens, price_per_1k_tokens)
    print(f"Total cost: ${total_cost:.4f}")


if __name__ == "__main__":
    main()
