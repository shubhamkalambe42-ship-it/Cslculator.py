import requests
from bs4 import BeautifulSoup

# Example: Scraping headlines from BBC News
url = "https://www.bbc.com/news"
response = requests.get(url)

# Check response
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # BBC headlines are usually inside <h2> or <h3> tags
    headlines = soup.find_all(["h2", "h3"], limit=15)  # get top 15
    print("Latest BBC News Headlines:\n")
    for idx, h in enumerate(headlines, 1):
        text = h.get_text(strip=True)
        if text:  # avoid empty ones
            print(f"{idx}. {text}")
else:
    print("Failed to fetch page:", response.status_code)
