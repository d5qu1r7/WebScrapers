import asyncio
import logging
import os
import sys
import concurrent.futures
import urllib.parse

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_modules.scraping import timer, get_html, write_row_to_csv

'''
pip install httpx
pip install beautifulsoup4
'''

BASE_URL = 'https://maktaba.tetea.org/exam-results/HESLB2012/loans.htm'
SAVE_FILE_PATH = ''
BASE_LINK = 'https://maktaba.tetea.org/exam-results/HESLB2012/'

# Set up logging
log_file_path = os.path.join(SAVE_FILE_PATH, 'TZ_HESLB_2012.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

async def fetch_table_urls(html):
    links = []

    # Find the table of regions
    table = html.find('table')

    # Get all the rows of the table
    all_rows = table.find_all('tr')

    # Loop through all the rows
    for row in all_rows[2:]:
        full_row = row.find_all('td')
        for column in full_row:
            link = column.find('a')
            name = link.text.strip()

            if name == '':
                continue

            # hrefs are not url encoded so we need to fix that
            encoded_link = urllib.parse.quote(link.get('href'))

            links.append([name, encoded_link])

    return links

def process_university(university_url, university_name):
    global BASE_LINK

    university_html = get_html(f'{BASE_LINK}{university_url}')
    university_table = university_html.find('table')

    # Get all the rows of the table
    university_rows = university_table.find_all('tr')

    # Loop through the rows of the table
    for university_row in university_rows:
        row_data = []

        university_columns = university_row.find_all('td')
        for university_column in university_columns:
            # Adding everything to a row and writing to .csv
            row_data.append(university_column.text.strip().replace("\n", " ").replace(",", " "))
        write_row_to_csv(row_data, f'{SAVE_FILE_PATH}{university_name.replace(" ", "_").replace(":", "")}/', 'data')

@timer
def main():
    html = get_html(BASE_URL)
    links = asyncio.run(fetch_table_urls(html))

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(process_university, link[1], link[0]) for link in links]
        concurrent.futures.wait(futures)

    print('Finished collecting data')

if __name__ == "__main__":
    main()
