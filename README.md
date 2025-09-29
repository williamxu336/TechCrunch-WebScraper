# TechCrunch Article Scraper
The crawler.py script allows you to scrape TechCrunch articles and save them locally. It utilizes the requests library for making HTTP requests, a custom Scraper class for handling the article URLs, and a TechCrushParser class for parsing the HTML content of each article. Successfully tested on both Windows and macOS using Python 3.9. Developed using Visual Studio Code.

**Prerequisites**
Make sure you have the following dependencies installed:
- Install requests library using `pip install requests`

**Usage**
1. Adjust Parameters (skip this step if running default parameters)
    Open `crawler.py` and modify the parameters in the `params` dictionary in main() to customize the scraper behavior:

    params = {'wait_time': 60, 'num_articles': 50, 'start_page': 1, 'pause': 1}
    
    - `wait_time`: Wait in seconds before getting response again if a request failed.
    - `num_articles`: Number of articles to scrape.
    - `start_page`: Page number to start scraping from.
    - `pause`: Pause in seconds between each request.
    
2. Run the Scraper
    Execute the main script to start scraping: python3 crawler.py

    - The script will fetch TechCrunch articles and save them to the current directory. 
    - The article will have a path based on CURRENT_DIRECTORY/YEAR/MONTH/DATE/TYPE/ARTICLE_NAME
        - The YEAR/MONTH/DATE is based on the published date and not the modified date. The times are local time.
        - The TYPE is the category of the article (e.g. AI, Apps, Startups, etc)
        - Articles that are categorized as 'Featured' articles will have '[FEATURED]' before the article name.
    
**File Structure**

- `crawler.py`: Main script to run the scraper. Saves articles to local directory.
- `scraper.py`: Scraper class for handling requests and processing responses. Stores the urls of the articles.
- `tech_crunch_parser.py`: HTML parser class for extracting information from TechCrunch articles.

**Future Improvements**
While the project requires saving to disk using directories and files, utilizing a database for storing articles can enhance accessibility. This approach supports querying by various parameters such as date, author, and category, facilitating concurrent retrieval by multiple users. Furthermore, preserving both the modified and original versions of an article upon modifications in database allows for easy identification of changes.