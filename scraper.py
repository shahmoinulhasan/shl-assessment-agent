import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.shl.com/solutions/products/product-catalog/"

def scrape_catalog():
    print("Fetching catalog...")
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    catalog = []
    
    # SHL catalog items are currently contained in these specific divs
    items = soup.find_all('div', class_='module-product-catalog__product') 
    
    for item in items:
        # Extract the exact name, description, and link
        name_tag = item.find('h3', class_='module-product-catalog__product-title')
        desc_tag = item.find('p', class_='module-product-catalog__product-desc')
        link_tag = item.find('a', class_='module-product-catalog__product-link')
        
        name = name_tag.text.strip() if name_tag else "Unknown"
        desc = desc_tag.text.strip() if desc_tag else ""
        link = link_tag['href'] if link_tag else ""
        
        # Build the full URL and format the data
        full_url = f"https://www.shl.com{link}" if link.startswith('/') else link
        
        # We assume they are individual assessments as required
        catalog.append({
            "name": name,
            "description": desc,
            "url": full_url,
            "test_type": "Assessment" 
        })
    
    # Save it to a JSON file so our agent can read it later
    with open('catalog.json', 'w') as f:
        json.dump(catalog, f, indent=4)
        
    print(f"Success! Saved {len(catalog)} items to catalog.json")

if __name__ == "__main__":
    scrape_catalog()