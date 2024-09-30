import time
import json
import os
import re
from firecrawl import FirecrawlApp
from bs4 import BeautifulSoup
import markdown

class CrawlerAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        env = os.environ.get(
        "FIRECRAWL_LOGGING_LEVEL", "INFO"
        ).upper()
        self.app = FirecrawlApp(api_key=self.api_key)

    def crawl_website(self, website_url, format='markdown'):
        # Set up crawl parameters
        params = {
            'limit': 1,  # Maximum number of pages to crawl
            'scrapeOptions': {
                'formats': [format.lower()]
            },
            # Add other parameters as needed
        }

        try:
            # Start the crawl asynchronously on the server
            crawl_status = self.app.async_crawl_url(website_url, params=params)
            crawl_id = crawl_status.get('id')
            if not crawl_id:
                print("Failed to start crawl: No crawl ID returned.")
                return None
            print(f"Reading started!")

            # Poll for the crawl status
            while True:
                status = self.app.check_crawl_status(crawl_id)
                print(f"Reading status: {status.get('status')}")
                if status.get('status') == 'completed':
                    break
                elif status.get('status') == 'failed':
                    print("Reading failed.")
                    return None
                time.sleep(2.5)  # Wait 5 seconds before checking again

            # Retrieve the crawl results
            final_status = self.app.check_crawl_status(crawl_id)
            results = final_status.get('data')
            if results:
                return results
            else:
                print("Failed to retrieve reading results.")
                return None

        except Exception as e:
            print(f"An error occurred during reading: {e}")
            return None

    def process(self, website_url, format='markdown'):
        # Validate and set the format
        if format.lower() not in ['html', 'markdown']:
            print(f"Invalid format '{format}'. Defaulting to markdown.")
            format = 'markdown'

        # Crawl the website
        results = self.crawl_website(website_url, format)
        if results is None:
            print("Crawling failed.")
            return None

        return results
