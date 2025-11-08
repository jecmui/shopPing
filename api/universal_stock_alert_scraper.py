# universal_stock_alert_scraper.py
# Requirements: pip install selenium beautifulsoup4 webdriver-manager requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv

# ----------------------------
# Configuration
# ----------------------------
HEADERS = "Mozilla/5.0 (compatible; UniversalStockScraper/1.0; +mailto:rnarain@buffalo.edu)"
DELAY = 3  # seconds delay between requests

# Keywords for purchase buttons and generic stock detection
PURCHASE_BUTTON_KEYWORDS = ["add to cart", "add to bag", "buy now", "purchase"]
PAGE_STOCK_KEYWORDS = ["in stock", "available"]
PAGE_OUT_OF_STOCK_KEYWORDS = ["out of stock", "sold out", "currently unavailable"]

# ----------------------------
# Selenium driver setup
# ----------------------------
def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument(f"user-agent={HEADERS}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# ----------------------------
# Variant-aware stock detection
# ----------------------------
def detect_variant_stock(soup, variant_text=None):
    """
    Detect stock for a specific variant if provided (size/color). Falls back to generic stock detection.
    """
    in_stock = False

    # Check <select> dropdowns (common for sizes/colors)
    selects = soup.find_all("select")
    for sel in selects:
        options = sel.find_all("option")
        for opt in options:
            text = opt.get_text(strip=True).lower()
            if variant_text and variant_text.lower() in text:
                if not opt.has_attr("disabled") and "out of stock" not in text:
                    return "In Stock"
                else:
                    return "Out of Stock"

    # Check buttons/radio options for variants
    buttons = soup.find_all("button")
    for b in buttons:
        text = b.get_text(strip=True).lower()
        if variant_text and variant_text.lower() in text:
            if not b.has_attr("disabled") and "out of stock" not in text:
                return "In Stock"
            else:
                return "Out of Stock"

    # ------------------ Generic fallback ------------------
    # Check buttons for purchase keywords
    for b in buttons:
        text = b.get_text(strip=True).lower()
        if any(k in text for k in PURCHASE_BUTTON_KEYWORDS) and not b.has_attr("disabled"):
            in_stock = True
            break

    # Check page text
    if not in_stock:
        page_text = soup.get_text(separator=" ").lower()
        if any(k in page_text for k in PAGE_STOCK_KEYWORDS):
            in_stock = True
        elif any(k in page_text for k in PAGE_OUT_OF_STOCK_KEYWORDS):
            in_stock = False

    return "In Stock" if in_stock else "Out of Stock"

# ----------------------------
# Scrape a single URL
# ----------------------------
def scrape_url(url, variant=None):
    driver = get_driver()
    driver.get(url)
    time.sleep(DELAY)  # wait for JS to render
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    stock_status = detect_variant_stock(soup, variant_text=variant)

    # Gather recommendations (other links on page)
    recommendations = []
    for a in soup.find_all("a", href=True):
        t = a.get_text(strip=True)
        if t:
            recommendations.append({"title": t, "link": a["href"]})
        if len(recommendations) >= 5:
            break

    return {"url": url, "variant": variant, "stock_status": stock_status, "recommendations": recommendations}

# ----------------------------
# Main stock alert logic
# ----------------------------
def stock_alert(urls, variants=None):
    if variants is None:
        variants = [None] * len(urls)
    all_results = []

    for i, url in enumerate(urls):
        variant = variants[i] if i < len(variants) else None
        print(f"\nScraping: {url} | Variant: {variant if variant else 'Any'}")
        result = scrape_url(url, variant)
        print(f"Stock status: {result['stock_status']}")

        if result["stock_status"] == "Out of Stock":
            print("Recommendations:")
            for rec in result["recommendations"]:
                print(f"{rec['title']} → {rec['link']}")

        all_results.append(result)

    # Save CSV log
    with open("stock_alert_log.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "variant", "stock_status", "recommendations"])
        writer.writeheader()
        for r in all_results:
            writer.writerow({
                "url": r["url"],
                "variant": r["variant"] if r["variant"] else "",
                "stock_status": r["stock_status"],
                "recommendations": ", ".join([rec["title"] for rec in r["recommendations"]])
            })
    print("\n✅ Done! Log saved to stock_alert_log.csv")

# ----------------------------
# Run script
# ----------------------------
if __name__ == "__main__":
    urls = input("Enter shopping URLs (comma-separated): ").split(",")
    variants_input = input("Enter corresponding variant names (comma-separated, leave blank if none): ").split(",")

    urls = [u.strip() for u in urls]
    variants = [v.strip() if v.strip() != "" else None for v in variants_input]

    stock_alert(urls, variants)
