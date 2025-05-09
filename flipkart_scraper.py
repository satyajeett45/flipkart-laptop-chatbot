import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
URL = os.getenv("FLIPKART_URL")
if not URL:
    print("Error: FLIPKART_URL not found in .env file")
    exit(1)

# Headers to mimic a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def scrape_product_description(product_url):
    try:
        response = requests.get(product_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        desc_tag = soup.find("ul", class_ = "G4BRas")
        description = desc_tag.text.strip() if desc_tag else "No description available"
        return description
    except (requests.RequestException, AttributeError) as e:
        print(f"Error fetching description for {product_url}: {e}")
        return "No description available"

def scrape_flipkart_laptops(url, max_pages=60):
    laptops = []
    for page in range(1, max_pages + 1):
        page_url = f"{url}&page={page}"
        print(f"Scraping page {page}: {page_url}")
        try:
            response = requests.get(page_url, headers=HEADERS)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            # Corrected listing class
            listings = soup.find_all("div", class_="tUxRFH")

            print(f"Found {len(listings)} listings on page {page}")
            if not listings:
                print(f"No listings found on page {page}. Check HTML structure or server response.")
                continue

            for listing in listings:
                try:
                    name_tag = listing.find("div", class_="KzDlHZ")
                    name = name_tag.text.strip() if name_tag else "N/A"
                    price_tag = listing.find("div", class_="Nx9bqj _4b5DiR")
                    price = price_tag.text.strip() if price_tag else "N/A"
                    rating_tag = listing.find("div", class_="XQDdHH")
                    rating = rating_tag.text.strip() if rating_tag else "N/A"
                    url_tag = listing.find("a", class_="CGtC98")
                    product_url = "https://www.flipkart.com" + url_tag["href"] if url_tag else "N/A"
                    description = scrape_product_description(product_url) if product_url != "N/A" else "No description available"

                    laptops.append({
                        "name": name,
                        "price": price,
                        "rating": rating,
                        "url": product_url,
                        "description": description
                    })
                    print(f"Scraped: {name}")
                    time.sleep(1)
                except AttributeError as e:
                    print(f"Error parsing listing on page {page}: {e}")
                    continue
        except requests.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break
    return laptops

def save_to_csv(data, filename="data/laptops.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    laptop_data = scrape_flipkart_laptops(URL, max_pages=60)
    print(f"Scraped {len(laptop_data)} laptops")
    save_to_csv(laptop_data)