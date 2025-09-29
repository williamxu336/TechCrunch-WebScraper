from time import sleep as sleep
import requests
import json
from datetime import datetime as dt

class Scraper:
    def __init__(self, params):
        self.wait_time = params.get('wait_time')
        self.num_articles = params.get('num_articles')
        self.start_page = params.get('start_page')
        self.pause=params.get('pause')
        self.urls = []

    # Request data from a specific page number
    def request(self, page_number):
        headers = {
            'authority': 'techcrunch.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json; charset=utf-8',
            'referer': 'https://techcrunch.com/',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'x-tc-ec-auth-token': '',
            'x-tc-uuid': '',
        }

        # Go to that specific page number for the request
        params = {
            'page': f'{page_number}',
        }

        # Update user with terminal window prints
        print_update = lambda x: print(f'>>> Time: {dt.now().strftime("%H:%M %d-%h")},\tResponse Code: {x},\tPage: {page_number}          \n', end='\r')

        # While loop that breaks when a getting a successful response from the server
        while True:
            # Using try except to catch any possible errors
            try:
                # Data from request to the server 
                response = requests.get('https://techcrunch.com/wp-json/tc/v1/magazine', params=params, headers=headers)

                # If response.ok is set to true the response code is 200 --  a successful response
                if response.ok:
                    # Print update to terminal
                    print_update(response.status_code)

                    # Convert the retrieved response from JSON to a python dictionary
                    response = json.loads(response.text)
                    return response                
                # If response is not set to 200
                else:
                    # Print update to terminal
                    print_update(response.status_code)
                    # Sleep for wait_time seconds before try again, set in params
                    sleep(self.wait_time)      
            except:
                # Print Error to terminal
                print_update('Error')
                # Sleep for wait_time seconds before try again, set in params
                sleep(self.wait_time)

    # Process the data response retrieved from the server
    def process(self, response):
        # Create an empty list to store the article urls
        articles = []

        for article in response:
            # Append article url to the 
            articles.append(article.get('canonical_url'))

        return articles

    # Run function that loops through the page numbers and calls request to process
    def run(self):
        # Start from page 1
        curr_page = self.start_page

        # While loop that iterate through the pages collecting urls
        while len(self.urls) < self.num_articles:
            # Get a response from the Server
            response = self.request(curr_page)

            # Process the response into a list of urls on current page
            curr_urls = self.process(response)
            self.urls += curr_urls

            # Go to next page
            curr_page += 1

            # Pause between requests
            sleep(self.pause)
        
        return self.urls[:self.num_articles]