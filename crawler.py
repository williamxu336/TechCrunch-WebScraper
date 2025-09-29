import requests
from datetime import datetime as dt, timezone
from time import sleep as sleep
import re
from html import unescape
import os
from scraper import Scraper
from tech_crunch_parser import TechCrushParser
   
# Removes invalid characters from the filename string
def sanitize_filename(filename):
    invalid_characters = [':', '/', '\\', '\0', '\n', '\r', '\t', '*', '?', '"', '|', '>', '<']
    for char in invalid_characters:
        filename = filename.replace(char, ' ')
    return filename

# Creates a path to save the articles
def create_file_path(article_title, featured, published_time, type):
    # Adds [FEATURED] to the article name if the article is featured
    ft = '[FEATURED] 'if featured else ''

    # Get the current working directory
    current_directory = os.getcwd()

    # Create platform-indepent file name and path 
    directory_path = os.path.join(current_directory, 
                                  str(published_time.year), 
                                  str(published_time.month).zfill(2), 
                                  str(published_time.day).zfill(2), 
                                  type)
    file_path = os.path.join(directory_path, f'{ft}{sanitize_filename(article_title)}')
    
    # Create the directory if it doesn't exist
    os.makedirs(directory_path, exist_ok=True)
    return file_path

# Converts from UTC to Local Time 
def utc_to_local(utc_time):
    utc_tm = dt.strptime(utc_time,'%Y-%m-%dT%H:%M:%S%z')
    local_tm = utc_tm.replace(tzinfo=timezone.utc).astimezone(tz=None)
    return local_tm

def save_article(url):
    # Create an instance of MyHTMLParser
    parser = TechCrushParser()
    response = requests.get(url)

    # If response.ok is set to true the response code is 200 --  a successful response
    if response.ok:
        html_content = response.text

        # Parses through the URL
        parser.feed(html_content)

        # create file path
        article_title = parser.title[:-13]

        # Convert datetime from UTC to local timezone
        local_published_time = utc_to_local(parser.published_time)
        try:
            if parser.modified_time == '':
                local_modified_time = local_published_time
            else:
                local_modified_time = utc_to_local(parser.modified_time)
        except:
            print(f"Unknown time format: {parser.modified_time}")
            local_modified_time = local_published_time

        # Create the path for the article
        file_path = create_file_path(article_title, parser.featured, local_published_time, parser.type)

        # Open the file
        try:
            with open(file_path, 'w', encoding='utf-8') as file:

                # Write article title, url, author name, published date, and modified date
                file.write(
                    f'{article_title}\n\n'
                    f'URL: {url}\n\n'
                    f'Author: {parser.author}\n\n'
                    f'Published Date: {local_published_time.strftime("%Y-%m-%dT%H:%M:%S %Z")}, '
                    f'Modified Date: {local_modified_time.strftime("%Y-%m-%dT%H:%M:%S %Z")}\n\n'
                )

                # Write the paragraphs into the file
                for paragraph in parser.paragraphs:
                    file.write(f'{paragraph}\n\n')
        except Exception as e:
            print(f'An error occurred while writing to the file: {e}') 

        print(article_title)
    # If response is not set to 200
    else:
        # Response error
        raise RuntimeError(f'HTML response error {response.status_code}')

def main():
    # Define a parameters dictionary to be passed to class on construction
    params = {'wait_time' : 60, 'num_articles' : 50, 'start_page' : 1, 'pause' : 1}

    # Create a new instance of the Scraper class
    web_scraper = Scraper(params)

    # Call the run function
    article_urls = web_scraper.run()

    # Iterate through the urls in article_urls
    for url in article_urls:
        try:
            save_article(url)
        except Exception as err:
            print(f'Exception when reading {url}:{err}')
        # Pause between each URL request
        sleep(params.get('pause'))

    print('=============Completed=============')

if __name__ == '__main__':
    main()