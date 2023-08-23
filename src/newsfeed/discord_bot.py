import requests
import asyncio

# Define an asynchronous function to send a message to a Discord webhook
async def send_discord_message(webhook_url, group_name, blog_title, summary):
    # Create the message content with provided data
    message = f"**Group-name:** {group_name}\n# {blog_title}\n### Summary:\n{summary}"
    
    # Create an embed dictionary to hold the formatted message
    embed = {
        "description": message,
        "color": 0x00FF00  # Embed color (green)
    }
    
    # Create a payload dictionary to hold the embed content
    payload = {
        "embeds": [embed]
    }
    
    # Send a POST request to the provided webhook URL with the payload
    response = requests.post(webhook_url, json=payload)
    
    # Check if the request was successful, otherwise raise an exception
    response.raise_for_status()

# Define the main asynchronous function
async def main():
    # URL of the Discord webhook to send the message to
    webhook_url = "https://discord.com/api/webhooks/1131522847509069874/Lwk1yVc4w623xpRPkKYu9faFdMNvV5HTZ3TCcL5DgsIgeqhEvo9tBookvuh2S4IWysTt"
    
    # Data for the message
    group_name = "alexnet"
    blog_title = "New AI Breakthrough!"
    placeholder_summary = """The article discusses the advancements and challenges in the field of Artificial Intelligence (A.I.). It highlights how A.I. technologies are being integrated into various industries, such as healthcare and finance, to improve efficiency and decision-making. The article also explores ethical considerations surrounding A.I., like bias in algorithms and data privacy concerns. It concludes by emphasizing the need for responsible development and regulation of A.I. to ensure its positive impact on society."""
    
    # Call the send_discord_message function to send the message
    await send_discord_message(webhook_url, group_name, blog_title, placeholder_summary)

# Check if the script is being run directly (not imported as a module)
if __name__ == "__main__":
    # Run the main asynchronous function using the asyncio.run() function
    asyncio.run(main())
