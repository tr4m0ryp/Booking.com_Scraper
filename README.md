# Booking.com Hotel Scraper

Python based script scrapes hotel data from Booking.com and saves it into an Excel file. It uses BeautifulSoup for parsing HTML and colorama for colored terminal output.

## Features

- Scrapes hotel name, location, and price from Booking.com
- Saves the data into an Excel file
- Displays the progress in a user-friendly manner in the terminal

## Requirements

- Python 3.x
- Requests
- BeautifulSoup4
- Pandas
- Colorama

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/booking-scraper.git
cd booking-scraper
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the script using Python:

```bash
python scraper.py
```

The script will scrape the hotel data and save it into `hotels.xlsx`.
