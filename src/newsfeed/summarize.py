import json

import langchain
import openai

# Get key
with open("api-key.json") as f:
    keys = json.load(f)
