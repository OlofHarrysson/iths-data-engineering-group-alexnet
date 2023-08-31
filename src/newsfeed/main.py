import asyncio

from newsfeed import discord_bot_v3 as bot
from newsfeed import download_blogs_from_rss, extract_articles


def main(blog_name="mit"):
    download_blogs_from_rss.main(blog_name)
    extract_articles.main(blog_name)

    # Refactor this?
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(bot_v3.check_and_send(), bot_v3.main()))


if __name__ == "__main__":
    main()