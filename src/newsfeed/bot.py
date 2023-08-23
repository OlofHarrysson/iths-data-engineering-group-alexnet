import requests
import asyncio

async def send_discord_message(webhook_url, content):
    payload = {
        "content": content
    }
    response = requests.post(webhook_url, json=payload)
    response.raise_for_status()

async def fetch_chuck_norris_joke():
    response = requests.get("https://api.chucknorris.io/jokes/random")
    joke_data = response.json()
    return joke_data.get("value", "No joke available")

async def process_command(command):
    if command == "!joke":
        joke = await fetch_chuck_norris_joke()
        return joke
    else:
        return "Unknown command. Type !joke for a Chuck Norris joke."

async def main():
    webhook_url = "YOUR_WEBHOOK_URL_HERE"
    prefix = "!"
    
    while True:
        user_input = input("Enter a command: ")
        if user_input.startswith(prefix):
            command = user_input[len(prefix):].strip()
            response = await process_command(command)
            await send_discord_message(webhook_url, response)

if __name__ == "__main__":
    asyncio.run(main())
