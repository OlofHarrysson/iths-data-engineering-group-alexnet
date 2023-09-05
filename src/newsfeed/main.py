import asyncio

from newsfeed import discord_bot_v3 as bot
from newsfeed import download_blogs_from_rss, extract_articles
from newsfeed.blog_scraper import get_openai_blog_articles, save_articles_as_json


def main(blog_name="openai"):
    if blog_name.lower() == "openai":
        articles = get_openai_blog_articles()
        save_path = "data/data_warehouse/openai/articles"
        save_articles_as_json(articles, save_path)
    else:  # Assumes it's MIT or other RSS/XML-based blog
        download_blogs_from_rss.main(blog_name)
        extract_articles.main(blog_name)

        # Run the bot
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(bot.check_and_send(blog_name), bot.main()))


if __name__ == "__main__":
    main(blog_name="openai")
