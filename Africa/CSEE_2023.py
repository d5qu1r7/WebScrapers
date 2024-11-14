import asyncio
import logging
import os
import random
import sys
import time
import httpx
from bs4 import BeautifulSoup
import concurrent.futures

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_modules.scraping import timer, write_row_to_csv, get_html

'''
pip install httpx
pip install beautifulsoup4
'''

BASE_URL = 'https://maktaba.tetea.org/exam-results/CSEE2023/index.htm'
BASE_LINK = 'https://maktaba.tetea.org/exam-results/CSEE2023/'
SAVE_FILE_PATH = ''

# Set up logging
log_file_path = os.path.join(SAVE_FILE_PATH, 'TZ_CSEE_2023.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
    
async def fetch_table_urls(html):
    links = []

    # Find the table of regions
    table = html.find_all('table')[2]

    # Get all the rows of the table
    all_rows = table.find_all('tr')


    # Loop through all the rows
    for i, row in enumerate(all_rows):
        full_row = row.find_all('td')
        for j, column in enumerate(full_row):
            link = column.find('a')
            if link == None:
                continue
            
            name = link.text.strip()
            if name == '':
                continue

            links.append([name, link.get('href')])

    return links

def process_school(school_url, school_name):
    school_html = get_html(school_url)
    # print(school_html)
    tables = school_html.find_all('table')
    save_file_path = SAVE_FILE_PATH

    for i, table in enumerate(tables):
        file_path = f'{save_file_path}/{school_name.replace(" ", "_")}/'
        file_name = f'table'

        if i == 1: # This skips the second table that is blank
            continue

        # Get all the rows of the table
        rows = table.find_all('tr')

        # Loop through the rows of the table
        for row in rows:
            row_data = []

            columns = row.find_all(['td', 'th'])
            for column in columns:
                # Adding everything to a row and writing to .csv
                row_data.append(column.text.strip().replace("\n", " ").replace(",", " "))
            write_row_to_csv(row_data, file_path, file_name)

        # Put space in between the tables
        write_row_to_csv(' ', file_path, file_name)
        
    logging.info(f"Processed school: {school_name}")
    print(f"Processed school: {school_name}")

@timer
def main():
    html = get_html(BASE_URL)
    region_links = asyncio.run(fetch_table_urls(html))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_school, f'{BASE_LINK}{link[1]}', link[0]) for link in region_links]
        concurrent.futures.wait(futures)

    print('Finished collecting data')

if __name__ == "__main__":
    main()
