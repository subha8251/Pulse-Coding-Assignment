# SaaS Review Scraper

A Python-based review scraping tool that collects product reviews from multiple sources including G2, Trustpilot, and mock data generation for testing. This project was developed as part of the Pulse Coding Assignment.

## Project Requirements Met

1. Successfully scrapes reviews from G2
2. Implements date range filtering
3. Handles anti-bot detection
4. Provides clean JSON output
5. Includes mock data fallback
6. Added Trustpilot as bonus source

## Features

- **Multi-Source Support**
  - G2 Reviews (with anti-bot protection)
  - Trustpilot Integration
  - Mock data generation for testing

- **Advanced Functionality**
  - Date range filtering
  - Customizable output formats
  - Automatic rate limiting
  - Proxy support (configurable)
  - Browser-like request headers
  - Robust error handling

- **Clean Output Format**
  - Review title and content
  - Rating scores
  - Reviewer information
  - Verification status
  - Company size (when available)
  - Pros and cons (when available)

## Requirements

```bash
# Python version
python >= 3.8

# Required packages (included in requirements.txt)
requests==2.32.4
beautifulsoup4==4.13.4
urllib3==2.5.0
```

## Project Structure

```
review_scraper/
│
├── review_scraper.py      # Main scraper script
├── requirements.txt       # Package dependencies
├── reviews.json          # Default output file
├── README.md            # This documentation
│
└── samples/             # Sample outputs
    ├── g2_reviews.json
    └── trustpilot_reviews.json
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/subha8251/Pulse-Coding-Assignment.git
cd Pulse-Coding-Assignment
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Basic G2 scraping with mock data
python review_scraper.py \
  --company "Salesforce" \
  --start-date "2024-06-01" \
  --end-date "2024-08-15" \
  --source "g2"

# Using Trustpilot as alternative source
python review_scraper.py \
  --company "Microsoft" \
  --start-date "2024-01-01" \
  --end-date "2024-12-31" \
  --source "trustpilot" \
  --output "microsoft_reviews.json"

# Specifying custom output file
python review_scraper.py \
  --company "Slack" \
  --start-date "2024-01-01" \
  --end-date "2024-12-31" \
  --source "g2" \
  --output "slack_reviews.json"
```

### Command Line Arguments

| Argument | Description | Required | Default |
|----------|-------------|----------|---------|
| --company | Company name to scrape reviews for | Yes | - |
| --start-date | Start date (YYYY-MM-DD) | Yes | - |
| --end-date | End date (YYYY-MM-DD) | Yes | - |
| --source | Source platform (g2, trustpilot) | Yes | - |
| --output | Output JSON file path | No | reviews.json |

## Sample Output

The scraper generates a JSON file with reviews. Here are sample outputs from different sources:

### G2 Review Sample
```json
[
  {
    "title": "Excellent Salesforce experience",
    "description": "We've been using Salesforce for over a year and it has significantly improved our productivity. The interface is intuitive and the features are comprehensive.",
    "date": "2024-08-15",
    "rating": 4.62,
    "reviewer_name": "Demo User 1",
    "reviewer_title": "Manager",
    "company_size": "51-200 employees",
    "source": "g2",
    "verified": true
  }
]
```

### Trustpilot Review Sample
```json
[
  {
    "title": "Great Microsoft Products",
    "description": "We've been using Microsoft products for years. Their cloud services are excellent and support is responsive.",
    "date": "2024-01-15",
    "rating": 4.5,
    "reviewer_name": "John Smith",
    "reviewer_title": "IT Director",
    "company_size": "201-500 employees",
    "source": "Trustpilot",
    "verified": true
  }
]
```

## Alternative Source (Bonus Feature)

### Trustpilot Integration

As a bonus feature, this scraper includes support for Trustpilot reviews. To use Trustpilot as a source:

1. Use the `--source trustpilot` parameter
2. The scraper will:
   - Search for the company on Trustpilot
   - Extract reviews within the specified date range
   - Include verification status and ratings
   - Follow the same output format as G2 reviews

Example:
```bash
python review_scraper.py \
  --company "Microsoft" \
  --start-date "2024-01-01" \
  --end-date "2024-12-31" \
  --source "trustpilot" \
  --output "microsoft_trustpilot.json"
```

## Anti-Bot Protection

The scraper implements several measures to avoid detection:
- Random delays between requests (2-10 seconds)
- Modern browser-like headers including:
  - Up-to-date User-Agent strings
  - Proper Accept headers
  - Sec-Fetch headers
- Cookie handling and management
- Referrer chain simulation
- SSL verification with fallback
- Automatic retry with exponential backoff
- Random query parameter addition

## Limitations

- Some websites may block automated access
- Rate limiting may affect scraping speed
- Review content might be truncated on some platforms
- Historical data might be limited

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Contact

Subhasish - [GitHub](https://github.com/subha8251)

Project Link: [https://github.com/subha8251/Pulse-Coding-Assignment](https://github.com/subha8251/Pulse-Coding-Assignment)

## 🙏 Acknowledgments

- Thanks to all contributors
- Inspired by various open-source scraping tools
- Built with Python and love ❤️