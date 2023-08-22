import requests
import asyncio

async def send_discord_message(webhook_url, group_name, blog_title, summary):
    message = f"Group-name: {group_name}\nBlog-title: {blog_title}\nSummary: {summary}"
    payload = {
        "content": message
    }
    response = requests.post(webhook_url, json=payload)
    response.raise_for_status()  # Raise an exception if the request was not successful

async def main():
    webhook_url = "https://discord.com/api/webhooks/1143526122076778578/ZTVB5Ln8BZ2YCDZTzmMzTfohK0A-Uyi-ZjNUVV3ZBvK0fWBU9aI5LnHTHaIvBOoKSCV0"
    group_name = "alexnet"
    blog_title = "Turtle on his way to seek revenge"
    placeholder_summary = "Title says it all... and Alexander is an issue... turtle is coming."

    await send_discord_message(webhook_url, group_name, blog_title, placeholder_summary)

if __name__ == "__main__":
    asyncio.run(main())
