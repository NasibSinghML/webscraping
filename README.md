# Website Scraper

## Overview

This project is a web scraper designed to extract various pieces of information from a list of websites and store the results in a MySQL database. It extracts details such as meta titles, meta descriptions, social media links, tech stack, payment gateways, language, and category of the website. Certain social media links are ignored based on predefined patterns.

## Features

- Fetches website content using HTTP requests.
- Extracts meta titles and descriptions.
- Detects and extracts social media links while ignoring specific patterns.
- Identifies the technology stack used by the website.
- Extracts available payment gateways mentioned in the content.
- Determines the primary language of the website.
- Categorizes the website based on its content.
- Stores the extracted data in a MySQL database.

## Requirements

- Python 3.12.4
- Required Python libraries:
  - requests
  - beautifulsoup4
  - mysql-connector-python
  - pandas
  - python-dotenv
  - time
  - re

## Installation

1. Clone this repository:

    ```sh
    git clone https://github.com/your-username/website-scraper.git
    cd website-scraper
    ```

2. Install the required Python libraries:

    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the project directory with your MySQL database credentials:

    ```env
    DB_HOST=your_database_host
    DB_USER=your_database_username
    DB_PASSWORD=your_database_password
    DB_NAME=your_database_name
    ```

4. Create the necessary tables in your MySQL database by running the provided SQL script:



## Usage

1. Prepare a CSV file named `websites.csv` in the project directory containing a column `websitedomain` with the list of website URLs to be processed. The file can have comments starting with `#`.

2. Run the scraper:

    ```sh
    python scraper.py
    ```

3. The script will process the websites, extract the necessary information, and store the data in the MySQL database.

## Output

The extracted data will be stored in the `websites` table in your MySQL database. The table has the following schema:

```sql
CREATE TABLE IF NOT EXISTS websites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    social_media_links TEXT,
    tech_stack TEXT,
    meta_title TEXT,
    meta_description TEXT,
    payment_gateways TEXT,
    language VARCHAR(10),
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);




