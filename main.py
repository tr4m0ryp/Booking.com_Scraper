import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from colorama import init, Fore, Style

# Initialize colorama
init()

# Base URL for Booking.com search results (you need to adjust the location and other search parameters)
base_url = "https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1BCAEoggI46AdIM1gEaCCIAQGYARyIAQzYAQPoAQGIAgGoAgO4Av-mtJIGwAIB0gIkZDY5YmU5NDYtNmRkMi00M2M3LWIwZDctZmJlZWI5MmFhYzMx2AIE4AIB&sid=34e1dd939a0c9ae00f135e59eb13be0f&aid=304142&dest_id=20088325&dest_type=city&group_adults=2&group_children=0&no_rooms=1&from_sf=1"

# Headers to make the scraping less suspicious
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Function to scrape a single page
def scrape_page(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    hotels = []
    for hotel in soup.find_all('div', attrs={'data-testid': 'property-card'}):
        try:
            name = hotel.find('div', attrs={'data-testid': 'title'}).text.strip()
        except AttributeError:
            name = 'N/A'
        
        try:
            location = hotel.find('span', attrs={'data-testid': 'address'}).text.strip()
        except AttributeError:
            location = 'N/A'

        try:
            price = hotel.find('span', attrs={'data-testid': 'price-and-discounted-price'}).text.strip()
        except AttributeError:
            price = 'N/A'
        
        hotels.append({
            'Name': name,
            'Location': location,
            'Price': price
        })
    
    return hotels

# Function to scrape all pages
def scrape_all_pages(base_url):
    all_hotels = []
    page_number = 0
    total_hotels = 0
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
        url = f"{base_url}&offset={page_number * 25}"
        
        print(f"{Fore.CYAN}{'='*80}\nScraping page {page_number + 1}\nURL: {url}\n{'='*80}{Style.RESET_ALL}")
        hotels = scrape_page(url)
        if not hotels:
            print(f"{Fore.RED}No more hotels found, stopping scrape.{Style.RESET_ALL}")
            break
        all_hotels.extend(hotels)
        total_hotels = len(all_hotels)
        
        print(f"{Fore.YELLOW}{'-'*80}\nTotal hotels collected so far: {total_hotels}\n{'-'*80}{Style.RESET_ALL}")
        
        page_number += 1
        time.sleep(1)  # A bit of delay to avoid overloading the server

    return all_hotels

# Scrape all pages
all_hotels = scrape_all_pages(base_url)

# Check if hotels were found
if all_hotels:
    # Put the collected data into a DataFrame
    df = pd.DataFrame(all_hotels)
    
    # Save the data to an Excel file
    df.to_excel('hotels.xlsx', index=False)
    
    print(f"{Fore.GREEN}\n{'='*80}\nData successfully saved in hotels.xlsx\n{'='*80}{Style.RESET_ALL}")
else:
    print(f"{Fore.RED}\n{'='*80}\nNo hotels found. Check the HTML structure of the page.\n{'='*80}{Style.RESET_ALL}")
