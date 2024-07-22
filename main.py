import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from colorama import init, Fore, Style

# Initialize colorama
init()

# Base URL for Booking.com search results (you need to adjust the location and other search parameters)
base_url = "https://www.booking.com/searchresults.nl.html?label=01HP5400BCFTC1PQJ217EC9D3F_01J3BYHS22M3G6JQZK4DEHX580&sid=17ef3398ed3d81b34883dea49421a24a&aid=2375516&sb_lp=1&src=index&error_url=https%3A%2F%2Fwww.booking.com%2Findex.nl.html%3Faid%3D2375516%26label%3D01HP5400BCFTC1PQJ217EC9D3F_01J3BYHS22M3G6JQZK4DEHX580%26sid%3D17ef3398ed3d81b34883dea49421a24a%26sb_price_type%3Dtotal%26%26&ss=Nederland&is_ski_area=0&checkin_year=&checkin_month=&checkout_year=&checkout_month=&flex_window=0&group_adults=1&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&ss_raw=Nederlad&dest_id=&dest_type=&search_pageview_id=b8ac05a176450049&search_selected=false&nflt=ht_id%3D204%3Bht_id%3D226%3Bht_id%3D201%3Bht_id%3D228%3Bht_id%3D206%3Bht_id%3D216%3Bht_id%3D214%3Bht_id%3D212%3Bht_id%3D224%3Bht_id%3D215%3Bht_id%3D203%3Bht_id%3D205%3Bht_id%3D234%3Bht_id%3D225%3Bht_id%3D221"

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
def scrape_all_pages(base_url, max_hotels):
    all_hotels = []
    page_number = 0
    cooldown_attempts = 0

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
        url = f"{base_url}&offset={page_number * 25}"
        
        print(f"{Fore.CYAN}{'='*80}\nScraping page {page_number + 1}\nURL: {url}\n{'='*80}{Style.RESET_ALL}")
        hotels = scrape_page(url)
        
        if not hotels:
            if cooldown_attempts == 0:
                print(f"{Fore.RED}No more hotels found, starting 1-minute cooldown.{Style.RESET_ALL}")
                for i in range(60, 0, -1):
                    print(f"{Fore.BLUE}Cooldown: {i} seconds remaining...{Style.RESET_ALL}", end='\r')
                    time.sleep(1)
                cooldown_attempts += 1
                continue  # Retry scraping the same page after cooldown
            else:
                print(f"{Fore.RED}No more hotels found after cooldown, stopping scrape.{Style.RESET_ALL}")
                break
        
        all_hotels.extend(hotels)
        total_hotels = len(all_hotels)
        
        print(f"{Fore.YELLOW}{'-'*80}\nTotal hotels collected so far: {total_hotels}\n{'-'*80}{Style.RESET_ALL}")
        
        if total_hotels >= max_hotels:
            print(f"{Fore.GREEN}Reached the maximum limit of {max_hotels} hotels. Stopping scrape.{Style.RESET_ALL}")
            break
        
        page_number += 1
        cooldown_attempts = 0  # Reset cooldown attempts after successful scrape
        time.sleep(1)  # A bit of delay to avoid overloading the server

    return all_hotels

# User input for maximum number of hotels to scrape
max_hotels = int(input("Enter the maximum number of hotels to scrape: "))

# Scrape all pages
all_hotels = scrape_all_pages(base_url, max_hotels)

# Check if hotels were found
if all_hotels:
    # Put the collected data into a DataFrame
    df = pd.DataFrame(all_hotels)
    
    # Save the data to an Excel file
    df.to_excel('hotels.xlsx', index=False)
    
    print(f"{Fore.GREEN}\n{'='*80}\nData successfully saved in hotels.xlsx\n{'='*80}{Style.RESET_ALL}")
else:
    print(f"{Fore.RED}\n{'='*80}\nNo hotels found. Check the HTML structure of the page.\n{'='*80}{Style.RESET_ALL}")
