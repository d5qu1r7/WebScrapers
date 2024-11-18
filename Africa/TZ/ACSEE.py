import asyncio
import logging
import os
import sys
from bs4 import BeautifulSoup
import concurrent.futures
from playwright.sync_api import sync_playwright

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_modules.scraping import timer, write_row_to_csv, get_html, screenshot_page

'''
pip install httpx
pip install beautifulsoup4
'''

BASE_URL_1 = 'https://maktaba.tetea.org/exam-results/ACSEE' #2010
BASE_URL_2 = '/alevel.htm'
BASE_URL_3 = '/index.htm'
BASE_LINK = 'https://maktaba.tetea.org/exam-results/ACSEE' #2010
SAVE_FILE_PATH = 'w:/papers/current/african_records/TZ_ACSEE/'
LIST_OF_YEARS = ['2005','2006','2007','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023','2024']

# Set up logging
log_file_path = os.path.join(SAVE_FILE_PATH, 'TZ_ACSEE.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
    
async def fetch_table_urls(html, i):
    links = []

    if i < 10:
        # Find the table of regions
        table = html.find_all('table')[0]
    else:
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

def process_school(school_url, school_name, year):
    school_html = get_html(school_url)
    tables = school_html.find_all('table')
    save_file_path = SAVE_FILE_PATH

    for i, table in enumerate(tables):
        file_path = f'{save_file_path}{year}/{school_name.replace(" ", "_")}/'
        file_name = f'table'

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
    global LIST_OF_YEARS, BASE_URL_1, BASE_URL_2, BASE_URL_3, SAVE_FILE_PATH

    for i, year in enumerate(LIST_OF_YEARS):

        # if i != 18: # This is for testing only
        #     continue
            
        
        if i > 3 and i < 9:
            html = get_html(f"{BASE_URL_1}{year}{BASE_URL_2}")
        elif i <= 3 or i == 9:
            html = get_html(f"{BASE_URL_1}{year}{BASE_URL_2}l")
        else:
            html = get_html(f"{BASE_URL_1}{year}{BASE_URL_3}")

        region_links = asyncio.run(fetch_table_urls(html, i))

        # 2005, 2007, and 2009 HTML is messed up
        if i <= 3:
            # Create new playwright instance
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless = True)
                context = browser.new_context()
                page = context.new_page()

                for link in region_links:
                    # If the list scraper breaks, the try catch block will restart it
                    try:
                        page.goto(f"{BASE_URL_1}{year}/{link[1]}")
                        tables = page.locator('table').all()
                        save_file_path = SAVE_FILE_PATH

                        for i, table in enumerate(tables):
                            file_path = f'{save_file_path}{year}/{link[0].replace(" ", "_")}/'
                            file_name = f'table'

                            # Get all the rows of the table
                            rows = table.locator('tr').all()

                            # Loop through the rows of the table
                            for row in rows:
                                row_data = []

                                columns = row.locator('td').all()
                                for column in columns:
                                    # Adding everything to a row and writing to .csv
                                    row_data.append(column.inner_text().replace("\n", " ").replace(",", " "))
                                write_row_to_csv(row_data, file_path, file_name)

                            # Put space in between the tables
                            write_row_to_csv(' ', file_path, file_name)
                            
                        logging.info(f"Processed school: {link[0]}")
                        print(f"Processed school: {link[0]}")
                    except:
                        # main(page)
                        print("Something went wrong, exiting program.")
                        screenshot_page(page, SAVE_FILE_PATH, 'problem', False)
                        raise Exception

                page.close()
                context.close()
                browser.close()
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                futures = [executor.submit(process_school, f'{BASE_LINK}{year}/{link[1]}', link[0], year) for link in region_links]
                concurrent.futures.wait(futures)

        print(f'Finished collecting data from {year}')

    print('Finished collecting data')

if __name__ == "__main__":
    main()
