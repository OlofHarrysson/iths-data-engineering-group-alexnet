# What does the code do?

### 🔄 run_ci_cd.yml:
- Installs Python and checks so that the correct version is installed:
- Installs all requirements in requirements.txt
- Runs our tests automatically in the test folder with Pytest
- Runs Pre-commit code to ensure the quality standard of the code is set via running our code through different tools. Such as black formatter and iSort.

### 🌐 blog_dag.py
- This is a DAG file, pipeline instructions we use for our airflow pipeline.
- It contains all the steps and functions we need to run our entire program from start to finish.

### 📂 data folder
- 🌊 data_lake:
    - Contains raw XML files we downloaded via blogs RSS feeds
- 🏢 data_warehouse:
    - Contains the json files after we extract articles from the XML files. It also contains json files for the extracted blogs that does not have any RSS feeds that we need to webscrape.
    - Also contains the finished summarized articles ready for when the bot need to send them or when the dashboard needs new summarized blogs.

### 🕸 blog_scraper.py
- Webscrapes blogs via requests.get(link) and then parses the data via BeautifulSoup's html.parser.
- We have added all the necessary html elements in order to parse openAI's blog.
- After parsing the data it saves the files as JSON to our database.

### 🗄 create_table.py
- Creates all tables needed in our PostgreSQL database.
- Saves the history of blogs the bot has already posted to save on resources.
- Connects to the database using db_engine.py to create the tables.

### 📊 data_parser.py
- Gets database login credentials and connects to database using functions from db_engine.py.
- get_data function creates a list of JSON objects and uses store_in_database function to store the blog articles in database.
- parse_summary then generates summaries and saves them to the database as well.

### 🧪 datatypes.py
- File with two classes using the Pydantic package.
    - BlogInfo is used as a class to help us define data classes of the Attributes
    - BlogSummary, same as BlogInfo but for Summaries.
- The get_filename() function returns a filename based on the unique_id and tile/type_of_summary based on class, this helps us save the files.

### 🔗 db_enigne.py
- Contains connect_to_db function that helps our other scripts to connect to our database using login credentials from our api-key.json (obviously gitignored).

### 🤖 dicord_bot_commands.py
- Contains commands.HelpCommand class to define how the !help function should behave.
- Bot Initialization which gives us a way to communicate how the bot should start. In our case with the '!' prefix.
- @bot.event async def on_ready() Waits until the bot is ready to send a command.
- Simple error handling if the bot receives a command it does not know.
- Runs and gets all information required (such as discord webhook etc) through api-key.JSON.

### 📬 discord_bot_summary.py
- Sets global variables, One for the webhook and one for metadata file path.
- Uses Async with get_article to fetch the most recent article and animate dots. (thats a treat for us developers to see that the bot is running).
- The script contains functions for sending discord message with added line breaks and check if the summary has already been sent.

### 📥 download_blogs_from_rss.py
- Gets metadata info through function of the same name to download an XML file with the provided URL
- It then saves the XML files into our database.

### 📝 extract_articles.py
- Creates a uuid from the string in the XML blog file.
- Sanitizes the file name to remove any characters that does not work on Windows.
- Loads the XML files from database and parses it using BeautifulSoup and then returns it.
- It has two functions for extracting key information and fitting it to the BlogInfo class we mentioned earlier.
    - Function for MIT
    - Function for Tensorflow
- fetch_blog_content is needed for Tensorflow due to its unique html structure.
- It then saves the extracted blogs as JSON files to our database.

### 📄 summary.py
- Contains prompts for our different summary types.
- Summarizes extracted blog using OpenAI-api based on this summary type and returns the summary
- The script also contains a translate_title function that translates the function into the desired language.

### 🧪 tests folder.
- tests for our files

### ✔ pre-commit-config.yaml
- Checks to see if the code meets our style and quality before we can commit the code to github.
- If not returns an error we need to fix before we can continue

### 🤫 API-Key.json
- Shhhh (contains our secrets), Is not pushed to github.

### 🐳 docker-compose.yml
- Defines how our Docker containers should behave in our application environment.
- Mainly that we are using airflow as our web server and postgres as our database.

### 📦 Dockerfile
- Contains all necessary information to spin up our docker container.

### ⚙ Makefile
- Has terminal "shortcuts" to install the correct version of python, activate venv and install requirements and pre-commit.
- Checks to see if user is running MacOS or Windows and runs the necessary functions for the chosen OS.

### 📋 requirements.txt
- Contains all packages we need in order to run our scripts and pipeline.


