import asyncio
import csv
import json
import logging
import os
import random
import re
import string
import time
import httpx
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, expect
import concurrent.futures
import ollama

os.environ['OLLAMA_MAX_LOADED_MODELS'] = '3'
os.environ['OLLAMA_NUM_PARALLEL'] = '4'
os.environ['OLLAMA_MAX_QUEUE'] = '512'

'''
download ollama
ollama pull llama3.1 
pip install httpx beautifulsoup4 ollama
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
        logging.info(elapsed_time)
        return result
    return wrapper

MAIN_LINK_1 = 'https://news.harvard.edu/gazette/?s=gifts+to+harvard+%22' # Sept
MAIN_LINK_2 = '+' # 20
MAIN_LINK_3 = '%22#gsc.tab=0&gsc.q=gifts%20to%20harvard%20%22' # Sept
MAIN_LINK_4 = '%20' # 20
MAIN_LINK_5 = '%22&gsc.page=' # 1
SAVE_FILE_PATH = 'w:/RA_work_folders/Davis_Holdstock/Harvard/Harvard_gifts/January/' # FIXME: Change to the perminant file path the .csvs will be stored in

SAVED_DAY = 0
SAVED_PAGE = 10

# Set up logging
log_file_path = os.path.join(SAVE_FILE_PATH, 'Harvard_gifts_playwright_january.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_html(url):
    with httpx.Client() as client:
        time.sleep(2)
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

def get_urls(url, month, day):

    print(url)
    logging.info(url)

    article = get_html(url)

    try:
        article_title = article.find('body').find('div').find('main').find('h1')
        title_2 = article_title.text.strip()
    
        print(f'Processing {title_2}')

        title_2 = re.sub(' ,-', '_', title_2).lower()

        title = '"'
        # Remove multiple consecutive underscores
        title += re.sub(r'_+', '_', title_2)
        title += '"'

    except:
        print("No title found")
        logging.error("No title found")
        return

    article_main = article.find('body').find('div').find('main')

    paragraphs = article_main.find_all('p')

    text = '"'

    for paragraph in paragraphs:
        text += paragraph.text.strip()

    text += '"'

    # Remove new lines
    text = re.sub('\n', ' ', text)

    donor_name = '"'
    response_ollama = ollama.chat(model='llama3.1', messages=[{ 'role': 'user', 'content': f'Based on this article what was the name(s) of the individual(s) who gave the donation to harvard? Please only respond with his or her full name. If there is more than one donor please list them all seperated by commas. Please only respond with the name of the individual(s) names and nothing else. If this article is not about a donor or donation respond only with "No donor mentioned". Do not respond with a summary of the article or main points, but only the name of the donors if there are any. If this article is not about a donor or donation only respond with "No donor mentioned". Do not respond with a summary of the article or what it appears to be about. If the article is just "This page could not be found." please respond with "No donor mentioned".\n {text}. Do not provide a summary of the main points. Do not provide the topics covered. Only provide the name of the donor, if any.' }])
    donor_name += response_ollama['message']['content']
    donor_name += '"'

    # Remove new lines
    donor_name = re.sub('\n', ' ', donor_name)

    donation_amount = '"'
    response_ollama = ollama.chat(model='llama3.1', messages=[{ 'role': 'user', 'content': f'Based on this article what was the amount {donor_name} donated to harvard? Please only respond with The amount they donated. If they did not donate any money just respond with "Did not donate". If there is no donor respond with "$0". If the article consists of "This page could not be found." respond only with "$0". If there is no numerical answer based on the text respond only with "$0". Do not respond with a summary of the article or main points, but only the amount of the donation if any. If this article is not about a donor or donation only respond with "$0". Do not respond with a summary of the article or what it appears to be about.\n {text}' }])
    donation_amount += response_ollama['message']['content']
    donation_amount += '"'

    # Remove new lines
    donation_amount = re.sub('\n', ' ', donation_amount)

    alumni_year = '"'
    response_ollama = ollama.chat(model='llama3.1', messages=[{ 'role': 'user', 'content': f'Based on this article if {donor_name} is an alumni of harvard respond with the year they graduated from Harvard. Please respond with nothing else except the year they graduated. If there are multiple donors respond with the years respectively seperated by commas. If they are not an alumni of Harvard respond with nothing but the words "Did not go to Harvard". If there is no donor respond with "NA". If the article consists of "This page could not be found." only respond with "NA". Do not respond with a summary of the article or main points, but only the year the donor, if any, went to harvard if at all. If this article is not about a donor or donation only respond with "NA". Do not respond with a summary of the article or what it appears to be about.\n {text}' }])
    alumni_year += response_ollama['message']['content']
    alumni_year += '"'

    # Remove new lines
    alumni_year = re.sub('\n', ' ', alumni_year)

    row = [title, donor_name, donation_amount, alumni_year, url, text]
    # print(row)
    write_row_to_csv(row, SAVE_FILE_PATH, f'{month}_{day + 1}')

@timer
def main(browser):

    global SAVED_DAY, SAVED_PAGE

    main_url_1 = MAIN_LINK_1
    main_url_2 = MAIN_LINK_2
    main_url_3 = MAIN_LINK_3
    main_url_4 = MAIN_LINK_4
    main_url_5 = MAIN_LINK_5
    save_day = SAVED_DAY
    save_page = SAVED_PAGE
    months = ['Jan','Feb','March','April','May','June','July','Aug','Sept','Oct','Nov','Dec']

    for month in months[:1]:
        for day in range(31):

            if day < save_day:
                continue

            SAVED_DAY = day
            save_day = day

            for page in range(11):

                if page < save_page:
                    continue

                SAVED_PAGE = page
                save_page = page

                browser.goto(f'{main_url_1}{month}{main_url_2}{day + 1}{main_url_3}{month}{main_url_4}{day + 1}{main_url_5}{page + 1}')
                # browser.goto(f'{main_url_1}{month}{main_url_2}1{main_url_3}{month}{main_url_4}1{main_url_5}{page + 1}')

                # Wait for the page to load completely
                browser.wait_for_load_state('networkidle')
                time.sleep(2)

                print(f'{month} {day + 1}')

                if browser.locator('main').inner_text(timeout=50000) == 'Search the Harvard Gazette\nDisplaying results for:\nGO\nSort by:\nRelevance\nNo Results':
                    print("No results")
                    break

                main_content = browser.locator('#___gcse_0')
                links_div = main_content.locator('.gsc-wrapper')
                a_tags = links_div.locator('a').all()

                links = []

                for hyperlink in a_tags: # There are multiple links per article, so we must dedupe
                    if hyperlink.inner_text() != '':
                        # Get the href attribute using JavaScript 
                        href = hyperlink.evaluate("element => element.getAttribute('href')")
                        links.append(href)

                # Drop the last two elements because they are just for a google search
                new_list_links = []
                new_list_links = links[:-2]

                # Dedupe the list of links to not count any of them twice
                deduped_list = []
                deduped_list = list(set(new_list_links))

                for k, deduped_url in enumerate(deduped_list):
                    # print(k)
                    get_urls(deduped_url, month, day)

                print(f'Finished Processing {month} {day + 1} Page: {page + 1}')
                logging.info(f'Finished Processing {month} {day + 1} Page: {page + 1}')

                # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                #     futures = [executor.submit(get_urls, url, month, day) for url in deduped_list]
                #     concurrent.futures.wait(futures)
            
            SAVED_PAGE = 0
            save_page = 0

    # process_csv_files(starting_folder, output_file)
    
    print('Finished collecting data')

if __name__ == "__main__":
    # Create new playwright instance
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless = True)
        context = browser.new_context()
        page = context.new_page()

        # If the list scraper breaks, the try catch block will restart it
        try:
            main(page)
        except:
            main(page)
        #     # print("Something went wrong, exiting program.")
        #     raise Exception

        page.close()
        context.close()
        browser.close()
