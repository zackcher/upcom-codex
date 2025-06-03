# Upcom Codex Utilities

This repository provides utilities to gather trending e-commerce products and collect client contact information.

## Trending Product Scraper

`product_scraper.py` fetches product names, images, and links from several external sources (Amazon Movers & Shakers, AliExpress Trending, and TikTok Made Me Buy It) and writes the data to a Google Sheet.

Steps to run:

1. Install dependencies:
   ```bash
   pip install requests beautifulsoup4 gspread oauth2client
   ```
2. Create a Google service account and download the credentials JSON as `service_account.json` in this directory.
3. Set `SHEET_ID` inside the script to your Google Sheet ID.
4. Execute the script:
   ```bash
   python product_scraper.py
   ```

The first worksheet named `TrendingProducts` will contain the collected items.

## Client Contact Form

`client_form.py` starts a small Flask application providing a form for email and phone number collection. Each submission is appended to another sheet tab named `ClientSubmissions` in the same Google Sheet.

Steps to run:

1. Install dependencies:
   ```bash
   pip install Flask gspread oauth2client
   ```
2. Ensure `service_account.json` is present and `SHEET_ID` is set in `client_form.py`.
3. Launch the server:
   ```bash
   python client_form.py
   ```
4. Visit `http://localhost:5000` in your browser to submit contact details.
