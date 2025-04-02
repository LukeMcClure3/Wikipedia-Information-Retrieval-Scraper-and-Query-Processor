import requests
from bs4 import BeautifulSoup
def get_desc(url):
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page, 'lxml') # or 'html.parser'
    first_paragraph = soup.find('p').get_text(strip=False)
    return first_paragraph

