import sys
import requests
from bs4 import BeautifulSoup

def has_class_but_no_id(tag):
    return tag.has_attr('class')

# Send a GET request to the website you want to scrape
url = 'https://www.amazon.ca/s?k=gaming+laptops'
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')
sys.stdout.reconfigure(encoding="utf-8")

# Find the elements you want to extract data from
print(soup.find_all(has_class_but_no_id))

## Shits broke..