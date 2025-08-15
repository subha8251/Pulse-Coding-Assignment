SaaS Review Scraper

A Python tool to scrape product reviews from G2, Capterra, and GetApp for a given company and date range, using Playwright to bypass JavaScript rendering and anti-bot protection.

Features

Multiple sources: G2, Capterra, GetApp

Date range filter: Only keep reviews between your start & end dates

Headless browser: Uses Playwright for full page rendering

JSON output: Clean, structured data with title, review, date, reviewer, rating, source, and URL

Installation
pip install playwright beautifulsoup4
playwright install

Usage
Real scraping (needs direct reviews URL)
python scrape_reviews_playwright.py \
  --company "Notion" \
  --start-date "2025-05-01" \
  --end-date "2025-07-31" \
  --source g2 \
  --url "https://www.g2.com/products/notion/reviews" \
  --outfile notion_g2.json

Demo mode with mock data (no internet)
python scrape_reviews_playwright.py \
  --company "Salesforce" \
  --start-date "2024-06-01" \
  --end-date "2024-08-15" \
  --source g2 \
  --mock

Parameters
Flag	Description
--company	Company/product name (for reference in output)
--start-date	Start date in YYYY-MM-DD format
--end-date	End date in YYYY-MM-DD format
--source	Review source: g2, capterra, getapp
--url	Direct reviews page URL (required for real scraping)
--outfile	Output JSON file name (default: reviews.json)
--mock	Use mock/demo reviews instead of scraping
Example Outputs
[
  {
    "title": "Amazing product for teams",
    "review": "We switched last year and love the integrations.",
    "date": "2025-05-10",
    "reviewer": "Priya S",
    "rating": 4.5,
    "source": "g2",
    "url": "https://www.g2.com/products/notion/reviews"
  }
]