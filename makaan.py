import requests
from bs4 import BeautifulSoup
import csv
import sqlite3

def get_city_links(url, cities):
    # make the request to the URL and parse the HTML content
    # extract the city links from the HTML
    city_links = []
    for city in cities:
        # implementation for multiple pages
        '''city_page = 1
        while True:  
            city_url = f"{url}property-rates-for-buy-in-{city.lower()}?page{city_page}"
            response = requests.get(city_url)
            if response.status_code == 200:
                city_links.append(city_url)
                city_page += 1
            else:
                break'''
        #implementation for multiple pages
        for page in range(1, 2):
            city_url = f"{url}property-rates-for-buy-in-{city.lower()}?page={page}"
            city_links.append(city_url)
        print(city_links)
    return city_links

def extract_city_data(city_link):
    # make the request to the city link and parse the HTML content
    response = requests.get(city_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # extract the city name and URL from the HTML
    #city_name = soup.find("div", {"class": "thinput", })
    city_name = str(city_link[62:len(city_link)-7]).title()
    city_url = city_link
    
    # extract the locality-wise price information from the HTML
    localities = []
    for localityyy in soup.find_all("table", {"class": "tbl", "data-trend-type":"apartment"}):
        for localityy in localityyy.find_all("tbody"):
            for locality in localityy.find_all("tr"):
                #print(locality)
                #print("****************************************************************")
                locality_name = locality.find("span", {"itemprop":"name"}).string
                #min and max range prices
                min_price = locality.find("span", {"itemprop":"minPrice"})
                max_price = locality.find("span", {"itemprop":"maxPrice"})
                #check
                if min_price and max_price:
                    price_range = min_price.string + "-" + max_price.string
                else:
                    price_range = "Not Available"
                specific_avg = locality.find_all("td", {"class": "ta-r"})
                # accepting all the different ta-r in td tag 
                avg_price = str(specific_avg[1])[48: len(str(specific_avg[1]))-5]
                #checking for blank space
                price_rise_element = locality.find("span", {"class": "val"})
                if price_rise_element:
                    price_rise = price_rise_element.string
                else:
                    price_rise = "Not Available"
                
                localities.append({
                    "locality_name": locality_name,
                    "price_range_per_sq_ft": price_range,
                    "avg_price_per_sq_ft": avg_price,
                    "price_rise": price_rise,
                })
            break
        # total pages count
        #total_pages = localityyy.find("div", {"class": "pagination", "data-type":"pagination"}).string
    #print(localities)
    
    return city_name, city_url, localities

def write_to_csv(data, filename):
    # write the data to a CSV file
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["city_name", "city_url", "locality_name", "price_range_per_sq_ft", "avg_price_per_sq_ft", "price_rise"])
        writer.writeheader()
        
        for city in data:
            for locality in city["localities"]:
                writer.writerow({
                    "city_name": city["city_name"],
                    "city_url": city["city_url"],
                    "locality_name": locality["locality_name"],
                    "price_range_per_sq_ft": locality["price_range_per_sq_ft"],
                    "avg_price_per_sq_ft": locality["avg_price_per_sq_ft"],
                    "price_rise": locality["price_rise"]
                })

cities = ['Chennai', 'Mumbai', 'Pune', 'Puri', 'Bangalore']
# the URL for the city list
url = "https://www.makaan.com/price-trends/"

# get the city links from the URL
city_links = get_city_links(url, cities)

# extract the city data for each city link
city_data = []
for city_link in city_links:
    city_name, city_url, localities = extract_city_data(city_link)
    city_data.append({
        "city_name": city_name,
        "city_url": city_url,
        "localities": localities
    })
#print(city_data)

# write the city data to a CSV file
write_to_csv(city_data, "makaan_locality_prices.csv")

'''
    Creating the DataBase
'''

def save_csv_to_db(csv_file, db_file):
    data = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS locality_prices (
            city_name text,
            city_url text,
            locality_name text,
            price_range_per_sq_ft text,
            avg_price_per_sq_ft real,
            price_rise integer
        )
    ''')

    for row in data:
        c.execute("""
            INSERT INTO locality_prices (
                city_name,
                city_url,
                locality_name,
                price_range_per_sq_ft,
                avg_price_per_sq_ft,
                price_rise
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row['city_name'],
            row['city_url'],
            row['locality_name'],
            row['price_range_per_sq_ft'],
            row['avg_price_per_sq_ft'],
            row['price_rise']
        ))

    conn.commit()
    conn.close()
save_csv_to_db("makaan_locality_prices.csv", "makaan_locality_prices.db")