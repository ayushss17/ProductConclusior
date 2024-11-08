import requests
from bs4 import BeautifulSoup



async def getReviews():
    url = "https://amzn.in/d/8NMSKWE"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    r = requests.get(url, headers=headers)
    htmlCont = r.content
    soup = BeautifulSoup(htmlCont, 'html.parser')

    reviews = soup.find_all("div", class_="card-padding")
    rev_data=""
    if reviews:
        for review in reviews:
            rev_data+=review.getText(strip=True)
    else:
        print("No reviews found.")

    print(rev_data.strip)
    
    return rev_data.strip()