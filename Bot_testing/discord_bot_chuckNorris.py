import requests
import asyncio

async def send_discord_message(webhook_url, joke):
    payload = {
        "content": joke
    }
    response = requests.post(webhook_url, json=payload)
    response.raise_for_status()

async def fetch_chuck_norris_joke():
    response = requests.get("https://api.chucknorris.io/jokes/random")
    joke_data = response.json()
    return joke_data.get("value", "No joke available")

async def main():
    webhook_url = "https://discord.com/api/webhooks/1143558999237738577/ZJxXRlDKryW_BsLPHGfVa1JKeLAfj8A11yfpDSQbs4mMnc4Nb_AppoUxodbjHrA9Xke_"
    
    joke = await fetch_chuck_norris_joke()
    await send_discord_message(webhook_url, joke)

if __name__ == "__main__":
    asyncio.run(main())
