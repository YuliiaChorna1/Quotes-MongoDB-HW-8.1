## Quotes Project - README.md

This project provides a command-line tool to search for quotes based on author name or tags.

### Dependencies

* Python 3.x
* MongoDB
* pymongo
* redis
* mongoengine

### Installation

1. Make sure you have Python 3.x and pip installed.
2. Install the required libraries:

   ```bash
   pip install pymongo redis mongoengine
   ```

3. Configure your MongoDB connection details in the `config.ini` file. You'll need to specify the following:

   * `user`: Username for your MongoDB database
   * `pass`: Password for your MongoDB database
   * `db_name`: Database name
   * `domain`: Domain of your MongoDB cluster (if using AtlasDB)

4. (Optional) Populate your database with quotes using the provided sample data. Run the following command in the project directory:

   ```bash
   python seed.py
   ```

### Usage

1. Run the main script:

   ```bash
   python main.py
   ```

2. The program will display a help message with available commands.
3. Enter a command like `name: Albert Einstein` or `tag:love` to search for quotes.
4. Type `exit` or any of the listed exit commands to quit the program.

### Supported Commands

* `name:[author name]`: Find quotes by a specific author.
* `tag:[tag]`: Find quotes with a particular tag.
* `tags:[tag-1],[tag-2],...,[tag-n]`: Find quotes containing multiple tags (comma-separated).

### Data Model

The project uses a MongoDB database to store quotes, authors, and tags. The data model is defined in the `models.py` file:

* **Authors:** Stores author information like name, date of birth, location, and description.
* **Tags:** Stores individual tags associated with quotes.
* **Quotes:** Stores the quote content, author reference, and a list of tags.

### Caching

The `redis-lru` library is used to implement a basic caching mechanism. This helps improve performance by storing frequently accessed queries in Redis for faster retrieval.

### Running Tests

(Functionality for writing unit tests is not included in the provided code)

You can implement unit tests using a testing framework like `unittest` or `pytest` to ensure the functionality of different modules.
