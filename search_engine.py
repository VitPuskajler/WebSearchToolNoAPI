import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

class SearchEngine:
    def __init__(self):
        # Initialize any variables or configurations here
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.3"
        }

    def google_search(self, query):
        url = f"https://www.google.sk/search?q={query}"
        
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            # Check if the response contains the consent page
            if "Before you continue to Google" in response.text:
                print("Google is showing a consent page.")
                return None

            # Parse the results to extract useful information
            parsed_results = self.parse_results(response.text)
            return parsed_results  # Return the parsed results
        else:
            print(f"Error: Received response code {response.status_code}")
            return None

    def parse_results(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []

        # Find all search result containers
        for g in soup.find_all('div', class_='tF2Cxc'):
            # Extract title
            title_element = g.find('h3')
            title = title_element.text if title_element else ''

            # Extract link
            link_element = g.find('a')
            link = link_element['href'] if link_element else ''

            results.append({
                'title': title,
                'link': link,
            })

        return results

    def save_to_json(self, data, filename='results.json'):
        with open(f"/path/{filename}", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def save_to_csv(self, data, filename='results.json'):
        self.df = pd.DataFrame(data)
        self.df.to_csv(f"/path/{filename}",  encoding="utf-8-sig", index=False)