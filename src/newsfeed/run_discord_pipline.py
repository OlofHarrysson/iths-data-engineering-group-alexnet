import asyncio

from newsfeed import download_blogs_from_rss, extract_articles
from newsfeed.discord_bot_commands import (
    main as bot_main,  # Updated import for your renamed bot file
)


def main(blog_name="mit"):
    download_blogs_from_rss.main(blog_name)
    extract_articles.main(blog_name)

    # Run the Discord bot as part of the pipeline
    asyncio.run(bot_main())


if __name__ == "__main__":
    main()
