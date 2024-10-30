import asyncio
import logging
import os
import random
import time
import httpx
from bs4 import BeautifulSoup
import concurrent.futures

'''
pip install httpx
pip install beautifulsoup4
'''

# Timer decorator
def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        # Convert the elapsed time to hours, minutes, and seconds
        hours, rem = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(rem, 60)

        elapsed_time = f"--- {int(hours)} hours, {int(minutes)} minutes, {seconds:.2f} seconds ---"
        print(elapsed_time)
        return result
    return wrapper

BASE_URL = 'https://onlinesys.necta.go.tz/results/2023/sfna/sfna.htm'
SAVE_FILE_PATH = '' 

# Set up logging
log_file_path = os.path.join(SAVE_FILE_PATH, 'SFNA_results_2023.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_html(url):
    with httpx.Client() as client:
        response = client.get(url)

        if response.status_code != 200:
            logging.error(f"Non-200 response: {url} - Status Code: {response.status_code}")
        
        return BeautifulSoup(response.text, 'html.parser')
    
# Append a single row to .csv
def write_row_to_csv(row, file_path, file_name):
    # Create the directories for the file path
    # exist_ok=True means that no errors are raised if the file path is already there
    os.makedirs(file_path, exist_ok=True)

    csv_file_path = f'{file_path}{file_name}.csv'
    with open(csv_file_path, 'a', encoding='utf-8') as work_file:
        row_text = ''
        # Each pipeline indicates the start of a new column in the .csv file
        for item in row:
            row_text += item + ','
        row_text = row_text[:-1]
        row_text = row_text + '\n'
        work_file.write(row_text)
    
async def fetch_table_urls(html):
    links = []

    # Find the table of regions
    table = html.find('table')

    # Get all the rows of the table
    all_rows = table.find_all('tr')

    # Loop through all the rows
    for row in all_rows:
        full_row = row.find_all('td')
        for column in full_row:
            link = column.find('a')
            name = link.text.strip()

            if name == '':
                continue

            links.append([name, link.get('href')])

    return links

def process_school(school_url, region_name, province_name, school_name):
    school_html = get_html(school_url)
    # print(school_html)
    tables = school_html.find_all('table')
    save_file_path = SAVE_FILE_PATH

    for i, table in enumerate(tables):
        file_path = f'{save_file_path}{region_name.replace(" ", "_")}/{province_name.replace(" ", "_")}/{school_name.replace(" ", "_")}/'
        file_name = f'table'

        if i == 0: # This skips the first table that has another table inside of it FIXME: This is broken
            row = list(table.find_all('tr'))[0]
            row_data = []
            row_data.append(row.text.strip().replace("\n", " ").replace(",", " "))
            write_row_to_csv(row_data, file_path, file_name)

            # Put space in between the tables
            write_row_to_csv(' ', file_path, file_name)
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

def process_province(province_url, region_name, province_name):
    province_html = get_html(province_url)
    school_links = asyncio.run(fetch_table_urls(province_html))
    # province_link = [region_name, province_name, school_links]
    # print(province_link)
    # print()

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(process_school, f'https://onlinesys.necta.go.tz/results/2023/sfna/results/{link[1]}', region_name, province_name, link[0]) for link in school_links]
        # futures = [executor.submit(process_school, f'https://onlinesys.necta.go.tz/results/2023/sfna/results/{link[1]}', region_name, province_name, link[0]) for link in school_links[:8]] # For testing only, limiting the number of loops
        concurrent.futures.wait(futures)

    logging.info(f"Processed province: {province_name}")
    print(f"Processed province: {province_name}")

def process_region(region_url, region_name):
    region_html = get_html(region_url)
    province_links = asyncio.run(fetch_table_urls(region_html))
    # region_links = [region_name, province_links]
    # print(region_links)
    # print()

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_province, f'https://onlinesys.necta.go.tz/results/2023/sfna/results/{link[1]}', region_name, link[0]) for link in province_links]
        # futures = [executor.submit(process_province, f'https://onlinesys.necta.go.tz/results/2023/sfna/results/{link[1]}', region_name, link[0]) for link in province_links[:4]] # For testing only, limiting the number of loops
        concurrent.futures.wait(futures)

    logging.info(f"Processed region: {region_name}")
    print(f"Processed region: {region_name}")

@timer
def main():
    html = get_html(BASE_URL)
    region_links = asyncio.run(fetch_table_urls(html))

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(process_region, f'https://onlinesys.necta.go.tz/results/2023/sfna/{link[1]}', link[0]) for link in region_links]
        # futures = [executor.submit(process_region, f'https://onlinesys.necta.go.tz/results/2023/sfna/{link[1]}', link[0]) for link in region_links[:2]] # For testing only, limiting the number of loops
        concurrent.futures.wait(futures)

    print('Finished collecting data')

if __name__ == "__main__":
    main()
