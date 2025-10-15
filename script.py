import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.amazon.com/Premier-Protein-Shake-Chocolate-11-5/dp/B07MJL8NXR/?th=1"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "lxml")

product_name_tag = soup.find("span", {"id": "productTitle"})
product_name = product_name_tag.get_text(strip=True) if product_name_tag else "Product name not found"

print(f"Product Name: {product_name}\n{'=' * 80}")

reviews = soup.find_all("span", {"data-hook": "review-body"})
data = []
first_row = True

for i, review in enumerate(reviews, start=1):
    text = review.get_text(strip=True)
    clean_text = text.replace("Read more", "").strip()
    print(f"⭐ Review {i}:")
    print(clean_text)
    print("-" * 80)
    data.append({
        'Product Name': product_name if i == 1 else '',
        'Review Title': f"Review {i}",
        'Review Body': clean_text
    })

csv_file = 'amazon_reviews.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Product Name', 'Review Title', 'Review Body'])
    writer.writeheader()
    writer.writerows(data)
print(f"Saved extracted data to {csv_file}")
