import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import List, Dict, Tuple

# Helper to authorize Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

def get_sheet(sheet_id: str, worksheet_name: str):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'service_account.json', SCOPE)
    gc = gspread.authorize(credentials)
    sh = gc.open_by_key(sheet_id)
    try:
        worksheet = sh.worksheet(worksheet_name)
    except gspread.WorksheetNotFound:
        worksheet = sh.add_worksheet(title=worksheet_name, rows="100", cols="20")
    return worksheet

# Scraper functions

def scrape_amazon_movers_and_shakers() -> List[Tuple[str, str, str]]:
    """Scrape Amazon Movers & Shakers for product name, image, link."""
    url = "https://www.amazon.com/gp/movers-and-shakers"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    items = []
    for card in soup.select(".zg-grid-general-faceout")[:10]:
        title_tag = card.select_one(".p13n-sc-truncate")
        img_tag = card.select_one("img")
        link_tag = card.select_one("a")
        if not title_tag or not img_tag or not link_tag:
            continue
        title = title_tag.get_text(strip=True)
        img = img_tag["src"]
        link = "https://www.amazon.com" + link_tag["href"]
        items.append((title, img, link))
    return items


def scrape_aliexpress_trending() -> List[Tuple[str, str, str]]:
    """Scrape AliExpress trending products."""
    url = "https://www.aliexpress.com"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    items = []
    for card in soup.select(".list-item")[:10]:
        title_tag = card.select_one(".item-title")
        img_tag = card.select_one("img")
        link_tag = card.select_one("a")
        if not title_tag or not img_tag or not link_tag:
            continue
        title = title_tag.get_text(strip=True)
        img = img_tag["src"]
        link = link_tag["href"]
        items.append((title, img, link))
    return items


def scrape_tiktok_made_me_buy_it() -> List[Tuple[str, str, str]]:
    """Scrape TikTok 'Made Me Buy It' tag."""
    url = "https://www.tiktok.com/tag/tiktokmademebuyit"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    items = []
    for card in soup.select("div[data-e2e='search-video-item']")[:10]:
        title_tag = card.select_one("a")
        img_tag = card.select_one("img")
        link_tag = card.select_one("a")
        if not title_tag or not img_tag or not link_tag:
            continue
        title = title_tag.get_text(strip=True)
        img = img_tag["src"]
        link = "https://www.tiktok.com" + link_tag["href"]
        items.append((title, img, link))
    return items

SCRAPERS = {
    "amazon": scrape_amazon_movers_and_shakers,
    "aliexpress": scrape_aliexpress_trending,
    "tiktok": scrape_tiktok_made_me_buy_it,
}


def fetch_all_sources() -> List[Tuple[str, str, str, str]]:
    products = []
    for source, scraper in SCRAPERS.items():
        try:
            for title, img, link in scraper():
                products.append((source, title, img, link))
        except Exception as e:
            print(f"Failed to scrape {source}: {e}")
    return products


def save_products_to_sheet(sheet_id: str, worksheet_name: str, products: List[Tuple[str, str, str, str]]):
    ws = get_sheet(sheet_id, worksheet_name)
    ws.clear()
    ws.append_row(["Source", "Product Name", "Image", "Link"])
    for row in products:
        ws.append_row(list(row))


def main():
    SHEET_ID = "YOUR_SHEET_ID"  # replace with actual sheet id
    WORKSHEET_NAME = "TrendingProducts"
    products = fetch_all_sources()
    if products:
        save_products_to_sheet(SHEET_ID, WORKSHEET_NAME, products)


if __name__ == "__main__":
    main()
