import requests
from bs4 import BeautifulSoup
import pandas as pd

# Basis URL voor Booking.com zoekresultaten (je moet de locatie en andere zoekparameters aanpassen)
base_url = "https://www.booking.com/searchresults.html?ss=Amsterdam&nflt=ht_id%3D204%3B&rows=50"

# Headers om het scrapen minder verdacht te maken
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Functie om een enkele pagina te scrapen
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

# Scrape de eerste pagina
url = base_url
hotels = scrape_page(url)

# Controleer of hotels zijn gevonden
if hotels:
    # Zet de verzamelde gegevens in een DataFrame
    df = pd.DataFrame(hotels)
    
    # Sla de gegevens op in een Excel-bestand
    df.to_excel('hotels.xlsx', index=False)
    
    print("Gegevens succesvol opgeslagen in hotels.xlsx")
else:
    print("Geen hotels gevonden. Controleer de HTML-structuur van de pagina.")

