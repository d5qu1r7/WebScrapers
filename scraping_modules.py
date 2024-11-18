import logging
import os
import time
from bs4 import BeautifulSoup
import httpx
from urllib.parse import urlparse

async def can_scrape(url):
    # Parse the URL to get the domain
    parsed_url = urlparse(url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(robots_url)
            if response.status_code == 200:
                robots_txt = response.text
                # Check if the robots.txt file disallows scraping
                if "Disallow: /" in robots_txt:
                    return False
                else:
                    return True
            else:
                # If robots.txt is not found, assume scraping is allowed
                return True
        except httpx.RequestError as e:
            print(f"Error accessing {robots_url}: {e}")
            return False

# # Example usage
# import asyncio

# website_url = "https://example.com"
# result = asyncio.run(can_scrape(website_url))
# if result:
#     print(f"Web scraping is allowed on {website_url}")
# else:
#     print(f"Web scraping is not allowed on {website_url}")

def get_html(url):
    with httpx.Client() as client:
        time.sleep(1)
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

def screenshot_page(page, file_path, file_name, fullpage = False):
    """
    Screenshot the current page
    Args:
        page (playwright context): The playwright page
        file_path (str): Where to save the file
        file_name (str): The name of the file, with no file extension
        fullpage (bool): Whether or not to screenshot the full page (False by default)
    """

    # Create the directories for the file path
    # exist_ok=True means that no errors are raised if the file path is already there
    os.makedirs(file_path, exist_ok=True)

    print(f"Path '{file_path}' created successfully!")

    page.screenshot(path=f'{file_path}{file_name}.png', full_page=fullpage)

def image_download(page, file_path, file_name, download_button):
    # Define the path for the downloaded file
    save_path = file_path + file_name

    # Create the directories for the file path
    # exist_ok=True means that no errors are raised if the file path is already there
    os.makedirs(file_path, exist_ok=True)

    # Download the pdf by clicking the link
    with page.expect_download() as download_info:
        download_button.click()
        download = download_info.value
    download.save_as(save_path)
