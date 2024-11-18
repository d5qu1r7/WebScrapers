import logging
import os
import re
import sys
from bs4 import BeautifulSoup
import concurrent.futures

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_modules.scraping import timer, get_html, write_row_to_csv

'''
pip install httpx
pip install beautifulsoup4
'''

BASE_URL = 'https://web.archive.org/web/20161119150111/http://olas.heslb.go.tz:80/index.php/defaulters/lst/CBE'
SAVE_FILE_PATH = ''

# Set up logging
log_file_path = os.path.join(SAVE_FILE_PATH, 'TZ_HESLB_2016.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

@timer
def main():
    global BASE_URL, SAVE_FILE_PATH

    html = get_html(BASE_URL)
    table = html.find('table')

    # Get all the rows of the table
    rows = table.find_all('tr')

    # Loop through the rows of the table
    for row in rows:
        row_data = []

        columns = row.find_all('td')
        for column in columns:
            # Adding everything to a row and writing to .csv
            row_data.append(column.text.strip().replace("\n", " ").replace(",", " "))
        write_row_to_csv(row_data, SAVE_FILE_PATH, 'data')

if __name__ == "__main__":
    main()
