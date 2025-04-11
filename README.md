# 🕷️ AFDB Scrapy Crawler

A Scrapy-based web crawler for extracting product data from [AFDB.fr](https://www.afdb.fr). This project scrapes detailed product information, including title, brand, stock status, images, and technical specifications.

---

## 📁 Project Structure

```
afdb/
├── afdb/
│   ├── __init__.py
│   ├── items.py           # Defines scraped data fields
│   ├── settings.py        # Scrapy settings (feeds, concurrency, etc.)
│   └── spiders/
│       ├── __init__.py
│       └── products.py    # CrawlSpider for product pages
```

---

## 🚀 How to Run the Spider

### 1. Install Requirements

```bash
pip install scrapy
```

### 2. Run the Spider

```bash
scrapy crawl products
```

This will generate a file named `afdb.json` in the project root containing the scraped data in JSON format.

---

## 📦 Output Example

Each product item includes:

```json
{
  "url": "https://www.afdb.fr/...SKU...",
  "title": "Product Name",
  "brand": "Brand Name",
  "description": "Product description here...",
  "category": "Category",
  "image_urls": "https://www.afdb.fr/images/product.jpg",
  "sku": "SKU12345",
  "type": "Some Type",
  "finition": "Matte",
  "stock": "En Stock",
  "details": {
    "Weight": "5kg",
    "Dimensions": "30x20x10cm"
  },
  "variure": "VAR1"
}
```

---

## ⚙️ Configuration (Highlights from `settings.py`)

- **Bot Name**: `afdb`
- **ROBOTSTXT_OBEY**: `False`
- **FEEDS**: JSON output saved as `afdb.json`

---

## 🕸️ Spider Behavior (`products.py`)

- Starts from: `https://www.afdb.fr`
- Follows links ending with `.html` or containing `SKU`
- Filters out `INTERSHOP` links
- Uses structured JSON-LD to extract SKUs
- Extracts stock data from a secondary AJAX call

---

## 📄 License

MIT License. This is an educational or research tool. Use responsibly and ethically.
