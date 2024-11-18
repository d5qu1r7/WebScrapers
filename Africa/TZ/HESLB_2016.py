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

def separate_tables(text, output_folder):
    tables = re.split(r"\x0c", text)  # Splitting based on multiple newlines, adjust if needed
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, table in enumerate(tables):
        lines = table.strip().split("\n")
        if i == 0:
            continue
        elif i == len(tables) - 1:
            lines = lines[:-1]
        output_file = os.path.join(output_folder, f'table_{i}.csv')
        with open(output_file, 'w') as file:
            for j, line in enumerate(lines):
                line = line.replace('\r', '')
                line = line.replace('\n', '')
                if j == 0:
                    line = line.replace(', ', '-')
                    line = re.sub(r'\s\s+', ',', line)
                elif j == 2:
                    line = re.sub(r'\s\s+', '', line)
                elif j > 5 and j < 8:
                    line = re.sub(r'\s+=\s+', '==', line)
                    line = re.sub(r'==', ',', line)
                    line = re.sub(r'\s\s+', '', line)
                elif j > 10:
                    pattern = r'^\s+$'
                    pattern_2 = r'^(\s+)([A-Za-z0-9])(.+)'
                    
                    # Use re.match to check if the pattern matches the text 
                    match = re.match(pattern, line)
                    match_2 = re.match(pattern_2, line)
                    if match: 
                        continue
                    elif match_2:
                        all_groups_except_first = match_2.groups()[1:]
                        line = ''.join(all_groups_except_first)
                    line = re.sub(r'\s\s+', ',', line)
                else:
                    line = re.sub(r'\s\s+', '', line)
                file.write(line + "\n")

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
