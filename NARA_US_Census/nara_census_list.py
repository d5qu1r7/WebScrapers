from playwright.sync_api import sync_playwright, expect
import time
import re
import csv
import httpx
import json
import logging
import os
from bs4 import BeautifulSoup
import logging
import sys

MAX_PAGE_VIEW = 1000
#counties without counties so the code changes based on these elements. It also has the batch number for the images.
islands_without_counties = [['Midway Island', '469'],['Canton Island','None'],['Johnston Island','0468'], ['Overseas Island Possessions','0467'], ['Wake Island', 'None']]
# This dictionary of lists can be used to start the scraper where it left off in the case of it breaking
COMPLETED_DATA = {'Alabama': ['Autauga', 'Baldwin', 'Barbour']}
#completed_data = {'Alabama': ['Autauga', 'Baldwin', 'Barbour', 'Bibb', 'Birmingham, Jefferson', 'Blount', 'Bullock', 'Butler', 'Calhoun', 'Chambers', 'Cherokee', 'Chilton', 'Choctaw', 'Clarke', 'Clay', 'Cleburne', 'Coffee', 'Colbert', 'Conecuh', 'Coosa', 'Covington', 'Crenshaw', 'Cullman', 'Dale', 'Dallas', 'DeKalb', 'Elmore', 'Escambia', 'Etowah', 'Fayette', 'Franklin', 'Geneva', 'Greene', 'Hale', 'Henry', 'Houston', 'Jackson', 'Jefferson', 'Lamar', 'Lauderdale', 'Lawrence', 'Lee', 'Limestone', 'Lowndes', 'Macon', 'Madison', 'Marengo', 'Marion', 'Marshall', 'Mobile', 'Mobile, Mobile', 'Monroe', 'Montgomery', 'Montgomery, Montgomery', 'Morgan', 'Perry', 'Pickens', 'Pike', 'Randolph', 'Russell', 'Shelby', 'St. Clair', 'Sumter', 'Talladega', 'Tallapoosa', 'Tuscaloosa', 'Walker', 'Washington', 'Wilcox', 'Winston'], 'Alaska': ['First Judicial Division', 'Fourth Judicial Division', 'Second Judicial Division', 'Third Judicial Division']}
STARTING_COUNTY = "Bibb"
STARTING_VIEW = 5
# STARTING_PAGE = 40

# A list just in case there are territories or states that don't allow you to see the page count on the first county page. Normally it does though
states_with_weird_page_counters = ['American Samoa']

#Titles for the csv folder
title = ["Year","State","County","Link","Batch","ImageNumber"]

# Where the archive is located.
url = 'https://1950census.archives.gov/search/'
# Record details base_link
base_link = 'https://archives.paris.fr'
#file_path = 'W://RA_work_folders/Jason_Elzinga/NARA_US_Census/US_Census_1950'

file_path = 'W://papers/current/us_census/us_census_images/US_Census_1950'
#"W:\papers\current\us_census\us_census_images"
csv_file_path = os.path.join(file_path, 'nara_census_1950.csv')

records = {}


logging.basicConfig(
    filename='scraping_log.txt',  # Log file
    level=logging.INFO,            # Minimum logging level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log message format
)

def mark_as_completed(state, county='None'):
    global COMPLETED_DATA
    """Add the specified county to the completed list for the given state."""
    if state not in COMPLETED_DATA:
        COMPLETED_DATA[state] = []  # Initialize list if state is not in dictionary
    if county not in COMPLETED_DATA[state]:
        COMPLETED_DATA[state].append(county)
        logging.info(f'Marked as completed: {state} - {county}')

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

def is_in_list_of_lists(item, list_of_lists):
    for sublist in list_of_lists:
        if item in sublist:
            return True
    return False

def return_batch_number_for_islands(item, lst):
    for island in lst:
        if island[0] == item:
            return island[1]

#tracks the completed states and counties in the completed data dictionary
def is_completed(state, county):
    global COMPLETED_DATA
    """Check if the specified county for a given state is already completed."""
    if state in COMPLETED_DATA:
        return county in COMPLETED_DATA[state]
    else:
        return False

@timer
def scrape_page(page):
    global COMPLETED_DATA
    states_https = httpx.get('https://1950census.archives.gov/api/state')
    states = states_https.text
    states = json.loads(states)
    # Here is a list of the abbr and the states that it will loop through
    #states = [{"abbr":"AL","name":"Alabama"},{"abbr":"AK","name":"Alaska"},{"abbr":"AS","name":"American Samoa"},{"abbr":"AZ","name":"Arizona"},{"abbr":"AR","name":"Arkansas"},{"abbr":"CA","name":"California"},{"abbr":"CN","name":"Canton Island"},{"abbr":"CO","name":"Colorado"},{"abbr":"CT","name":"Connecticut"},{"abbr":"DE","name":"Delaware"},{"abbr":"DC","name":"District of Columbia"},{"abbr":"FL","name":"Florida"},{"abbr":"GA","name":"Georgia"},{"abbr":"GU","name":"Guam"},{"abbr":"HI","name":"Hawaii"},{"abbr":"ID","name":"Idaho"},{"abbr":"IL","name":"Illinois"},{"abbr":"IN","name":"Indiana"},{"abbr":"IA","name":"Iowa"},{"abbr":"JN","name":"Johnston Island"},{"abbr":"KS","name":"Kansas"},{"abbr":"KY","name":"Kentucky"},{"abbr":"LA","name":"Louisiana"},{"abbr":"ME","name":"Maine"},{"abbr":"MD","name":"Maryland"},{"abbr":"MA","name":"Massachusetts"},{"abbr":"MI","name":"Michigan"},{"abbr":"MW","name":"Midway Island"},{"abbr":"MN","name":"Minnesota"},{"abbr":"MS","name":"Mississippi"},{"abbr":"MO","name":"Missouri"},{"abbr":"MT","name":"Montana"},{"abbr":"NE","name":"Nebraska"},{"abbr":"NV","name":"Nevada"},{"abbr":"NH","name":"New Hampshire"},{"abbr":"NJ","name":"New Jersey"},{"abbr":"NM","name":"New Mexico"},{"abbr":"NY","name":"New York"},{"abbr":"NC","name":"North Carolina"},{"abbr":"ND","name":"North Dakota"},{"abbr":"OH","name":"Ohio"},{"abbr":"OK","name":"Oklahoma"},{"abbr":"OR","name":"Oregon"},{"abbr":"OI","name":"Overseas Island Possessions"},{"abbr":"PC","name":"Panama Canal Zone"},{"abbr":"PA","name":"Pennsylvania"},{"abbr":"PR","name":"Puerto Rico"},{"abbr":"RI","name":"Rhode Island"},{"abbr":"SC","name":"South Carolina"},{"abbr":"SD","name":"South Dakota"},{"abbr":"TN","name":"Tennessee"},{"abbr":"TX","name":"Texas"},{"abbr":"UT","name":"Utah"},{"abbr":"VT","name":"Vermont"},{"abbr":"VI","name":"Virgin Islands"},{"abbr":"VA","name":"Virginia"},{"abbr":"WK","name":"Wake Island"},{"abbr":"WA","name":"Washington"},{"abbr":"WV","name":"West Virginia"},{"abbr":"WI","name":"Wisconsin"},{"abbr":"WY","name":"Wyoming"}]

    for state in states:
        # Make the state_name and abbreviations
        state_name = state['name']
        state_abbr = state['abbr']

        # Make the state folder
        state_path = os.path.join(file_path, state_name)
        os.makedirs(state_path, exist_ok=True)

        # if state in islands_without_counties:
        if is_in_list_of_lists(state_name,islands_without_counties):
            logging.info(f"No counties to process for {state_name}.")
            # print(return_batch_number_for_islands(state_name,islands_without_counties))
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless = False)
                context = browser.new_context()
                page = context.new_page()


                if interact_with_page(page, return_batch_number_for_islands(state_name, islands_without_counties), state_abbr, state_name, state_path):
                    mark_as_completed(state_name)
                    print(COMPLETED_DATA)
                    logging.info(COMPLETED_DATA)
                else:
                    print(f"There is an error but This is the completed data: {COMPLETED_DATA}")
                    logging.error(f"Incomplete: {state_name} - {county}")
                    
                page.close()
                context.close()
                browser.close()


        else: # get the counties

            counties = httpx.get(f'https://1950census.archives.gov/api/county?state={state_abbr}')
            counties = json.loads(counties.text)
            #for all other states with counties (most of them)

            for county in counties:
                if is_completed(state_name, county):
                    logging.info(f"Skipping already completed county: {state_name} - {county}")
                    continue  # Skip this county if it’s already been completed
            
                county_path = os.path.join(state_path, county)
                os.makedirs(county_path, exist_ok=True)

                with sync_playwright() as pw:
                    browser = pw.chromium.launch(headless = False)
                    context = browser.new_context()
                    page = context.new_page()

                    if interact_with_page(page, county, state_abbr, state_name, county_path):
                        mark_as_completed(state_name, county)
                        logging.info(f"Successfully completed: {state_name} - {county}")
                        page.close()
                        context.close()
                        browser.close()
                    else:
                        print(f"There is an error but This is the completed data: {COMPLETED_DATA}")
                        logging.error(f"Incomplete: {state_name} - {county}")
                

def image_download(file_path, file_name, download_button, page, view_button, lst, three_dot_button, current_download_pending):
    # Define the path for the downloaded file
    save_path = os.path.join(file_path, file_name)

    # Create the directories for the file path
    os.makedirs(file_path, exist_ok=True)
    page.wait_for_load_state("networkidle")
    
    def retry_download():
        """Helper function to attempt the download with fresh context."""
        with page.expect_download(timeout=300000) as download_info:
            download_button.click()
            return download_info.value

    try:
        download = retry_download()

        # Check if download has completed successfully
        if download.failure() is None:
            download.save_as(save_path)
            logging.info(f'File downloaded and saved as {save_path}')
            return True
        else:
            # Retry logic upon failure
            logging.error(download)
            logging.error(f'Download failed with message: {download.failure()}')
            reload(page, view_button, lst, three_dot_button, download_button, current_download_pending)
            page.wait_for_load_state("networkidle")
            
            # Retry the download after reload
            download = retry_download()
            if download.failure() is None:
                download.save_as(save_path)
                logging.info(f'Retry successful, file saved as {save_path}')
                return True
            else:
                logging.error(f'Retry download failed with message: {download.failure()}')
                return False

    except Exception as e:
        logging.error(download_button)
        logging.error(page)
        logging.error(file_name)
        logging.error(file_path)
        logging.error(page.url)
        logging.error(f'Error during download: {str(e)}')
        return False
    

def interact_with_page(page, county, state, state_name, county_path):
    global states_with_weird_page_counters, MAX_PAGE_VIEW
    # go to each page and get the page count (set limit to MAX_PAGE_VIEW)
    if county != 'None':
        if state_name not in states_with_weird_page_counters:
            try:
                page.goto(f'https://1950census.archives.gov/search/?county={county}&page=1&size={MAX_PAGE_VIEW}&state={state}')
                #print(f'{county}')
                page.wait_for_selector('b')
                view_counter = int(page.locator('.stat b').first.inner_text())

            except:
                states_with_weird_page_counters.append(state_name)
                logging.info(f'These are the states or territories with weird page counters: {states_with_weird_page_counters}')
                page.goto(f'https://1950census.archives.gov/search/?page=1&size={MAX_PAGE_VIEW}&state={state}')
                view_counter = int(page.locator('.stat b').first.inner_text())
                page.goto(f'https://1950census.archives.gov/search/?county={county}&page=1&size={MAX_PAGE_VIEW}&state={state}')

        else:
            logging.info(f'These are the states or territories with weird page counters: {states_with_weird_page_counters}')
            page.goto(f'https://1950census.archives.gov/search/?page=1&size={MAX_PAGE_VIEW}&state={state}')
            view_counter = int(page.locator('.stat b').first.inner_text())
            logging.info(view_counter)
            #page.goto(f'https://1950census.archives.gov/search/?county={county}&page=1&size={MAX_PAGE_VIEW}&state={state}')

    else:
        page.goto(f'https://1950census.archives.gov/search/?page=1&size={MAX_PAGE_VIEW}&state={state}')
        # page.wait_for_selector('span.value')
        # page_counter = int(page.locator('span.value').nth(3).inner_text())
        view_counter = 1
    

    if view_counter > MAX_PAGE_VIEW:
        logging.info(f"Page count of {view_counter} exceeds {MAX_PAGE_VIEW} limit")
        page_changes = (view_counter//MAX_PAGE_VIEW)
        if view_counter % MAX_PAGE_VIEW != 0:
            page_changes +=1
        last_page_count = view_counter % MAX_PAGE_VIEW
    else:
        page_changes = 1

    success = True
    # Go through 1000 pages and then go to the next page if needed. If not just go through all of the views up to the page count.
    for i in range(page_changes):

        try:
            current_page = i+1
            time.sleep(1)
            # First page
            if current_page == 1:
                go_through_images(page, county,state,state_name,county_path, view_counter, current_page,page_changes)
            # All pages in between
            elif (current_page) < page_changes:
                page.goto(f'https://1950census.archives.gov/search/?county={county}&page={current_page}&size={MAX_PAGE_VIEW}&state={state}')
                go_through_images(page, county, state, state_name, county_path, MAX_PAGE_VIEW, current_page,page_changes)
            # Last page
            elif (current_page) == page_changes:
                page.goto(f'https://1950census.archives.gov/search/?county={county}&page={current_page}&size={MAX_PAGE_VIEW}&state={state}')
                go_through_images(page, county, state, state_name, county_path, last_page_count, current_page, page_changes)

        except:
                logging.warning(f"failed to interact_with_page for {state_name} - {county} - Image {current_page}")
                print(f"This is the completed data: {COMPLETED_DATA}")
                sys.exit()
                
                success = False  # Mark as unsuccessful if max retries are hit
    return success

def go_through_images(page, county, state, state_name, county_path, view_counter, current_page, page_changes, current_download_pending=0):
    global STARTING_COUNTY, STARTING_VIEW
    ran = view_counter
    page.wait_for_load_state("networkidle")
    print(f'This is the ran: {ran}')
    # Going through each view
    for i in range(ran):
        if county == STARTING_COUNTY and i < STARTING_VIEW:
            continue
        print("Entering the view loop")
        logging.info(f"\nOn page {current_page}/{page_changes}. On view {i+1}/{view_counter}. In {county} county in {state_name}")
        # print("It is in the view loop")
        page.wait_for_load_state("networkidle")
        view = page.locator(f'#result{i}')
        view.wait_for(state='visible')
        view_button = view.locator('button.btn.btn-primary.schedulebutton')
        view_button.click()

        #Click the button to allow the download button to be viewed
        page.wait_for_load_state("networkidle")
        three_dot_button = view.locator('button.MuiButtonBase-root.MuiIconButton-root')
        three_dot_button.nth(2).click()

        # Get the number of pages in each county downlaod view
        page.wait_for_load_state("networkidle")
        number_of_images_to_download = int(view.locator('span.value').nth(3).inner_text())
        # print(f'{number_of_images_to_download} pages to download')

        page.wait_for_load_state("networkidle")
        download_button = view.locator('li:has-text("Download")')
        download_button.wait_for(state='visible')

        #print(f'There are {number_of_images_to_download} images to go through')
        current_locator = view

        current_download_pending = 0
        list_of_page_button_clicked = []
        print(f'This loop will run {number_of_images_to_download} times')
        # Loop of the pages in each view
        for j in range(number_of_images_to_download):
            print("Trying to download")
            closing_fake_page(page)
            print("Checked if the page.url has the word search or not")
            logging.info(f"Downloading {j+1} image out of {number_of_images_to_download}")
            # Click on the image
            if j !=0:
                # print("Trying to find the next image")
                time.sleep(1)
                page.wait_for_load_state("networkidle")
                current_image_button = current_locator.locator(f'div[role="button"][data-canvas-index="{j}"]')
                current_image_button.wait_for(state='visible', timeout=5000)  # Wait for the image button to be visible
                current_image_button.scroll_into_view_if_needed()  # Ensure it's in view before clicking
                current_image_button.click()

                # print("Trying to click on the button with the three dots")
                three_dot_button = view.locator('button.MuiButtonBase-root.MuiIconButton-root')
                three_dot_button.nth(2).click()

                list_of_page_button_clicked.append(current_image_button)
                print(f'This is the list of page_buttons to click {list_of_page_button_clicked}')

            # Click the download button
            # print("Trying to click the download button")
            print("Trying to click the download button")
            page.wait_for_load_state("networkidle")
            page.wait_for_selector('li:has-text("Download")', state='visible')
            #download_button.scroll_into_view_if_needed() 
            download_button = view.locator('li:has-text("Download")')
            download_button.click()
            
            # just in case (we will make the batch and image_number)
            print("Finding the image download link")
            image_number = j+1
            page.wait_for_load_state("networkidle")
            page.wait_for_selector('a:has-text("Whole image")', state='visible', timeout=10000)
            download_link = view.locator('a:has-text("Whole image")').first.get_attribute('href')
            download_image_button = view.locator('a:has-text("Whole image")').first
                
            print("trying to write to csv and download images to file")
            batch,image_number =  extract_batch_and_image_number(download_link, state_name)
            row = [str(1950), state_name, county, str(download_link), batch, image_number]
            file_name = f'US_Census_1950_{state_name}_{county}_{batch}_{image_number}.jpg'
            # Try downloading if it doesn't work then just put the info in the csv so I can check it.
            
            #image_download(county_path, file_name, download_image_button, page)
            print("Trying to download")
            logging.info("Trying to download...")
            # file_path, file_name, download_button, page, view_button, lst, three_dot_button, current_download_pending
            if image_download(county_path, file_name, download_image_button, page, view_button, list_of_page_button_clicked, three_dot_button, current_download_pending):
                write_row_to_csv(row,state_name)
                logging.info('It is downloaded and written to the csv')
            else:
                print('Failed download... checking the page url')
                closing_fake_page(page)
                logging(f"Attempting to download image failed for {file_name}.")
                reload(page, view_button, list_of_page_button_clicked, three_dot_button, download_button, current_download_pending)
                print(f"It reloaded the page now it is... {page.url} is on the second attempt")
                    
                if image_download(county_path, file_name, download_image_button, page):
                    write_row_to_csv(row,state_name)
                    logging.info('It is downloading and writing to the csv')
                else:
                    print("It didn't work so raising a value error")
                    logging.error('Tried to reload the page again but still cound not download the image.')
                    sys.exit("Exiting program due to an error.")

            page.wait_for_load_state("networkidle")
            page.wait_for_selector('button.MuiButtonBase-root.MuiButton-root.MuiButton-text.MuiButton-textPrimary', state='visible')
            exit_out_of_image_download = view.locator("button.MuiButtonBase-root.MuiButton-root.MuiButton-text.MuiButton-textPrimary")
            exit_out_of_image_download.click()

            # logging.info(f"There is an error in {state} in {county} view: {view} page: {current_page} image: {image_number}")
            print('Exiting the second loop')

def reload(page, view_button, lst, three_dot_button, download_button, current_download_pending):
    logging.info(f'Trying to redownload {current_download_pending}')

    #Reload the page
    page.reload(wait_until="load")
    #Go to the current view
    view_button.wait_for_element_state("visible")
    view_button.click()
    #Go to the current image
    for i in range(len(lst)):
        page.wait_for_load_state("networkidle")
        lst[i].wait_for_element_state("visible")
        lst[i].click()
        
        if i == len(lst)-1:
            page.wait_for_load_state("networkidle")
            three_dot_button.wait_for_element_state("visible")
            three_dot_button.click()

            page.wait_for_load_state("networkidle")
            download_button.wait_for_element_state("visible")
            download_button.click()

def closing_fake_page(page):
    logging.info("Checking if the page is real...")
    page_url = page.url
    print(f"This is the page_url: {page_url}")
    logging.info(f'This is the page.url that it is checking--- {page.url}')
    if "search" in page_url:
        logging.info("This is a search URL. Continuing...")
        # Do something with the search URL

    elif page_url.endswith(".jpg"):
        logging.info("This is an image URL. Clsing the page.")
        page.close()
    

def extract_batch_and_image_number(url,state):
    # Use regular expressions to capture the two required numbers
    # The regex pattern captures a sequence of digits (\d+)
    if state not in islands_without_counties:
        #This part insures that names with spaces will still match it
        state_formatted = state.replace(" ", "_")
        pattern = rf'{state_formatted}.*?(\d+)-(\d+)\.jpg'
        match = re.search(pattern, url)
    
        if match:
            # match.group(1) captures the first number (095363)
            # match.group(2) captures the second number (0001)
            batch = match.group(1)
            image_number = match.group(2)
            return batch, image_number

    else:
        state_formatted = state.replace(" ", "_")
        pattern = rf'{state_formatted}-?(\d+)\.jpg'
        match = re.search(pattern, url)
        # ex: https://1950census.archives.gov/iiif/2/1950-Territories%2F5550637-Canton_Island%2F5550637-Canton_Island-0003.jpg/full/7332,/0/default.jpg?download=true
        if match:
            # match.group(1) captures the first number (095363)
            # match.group(2) captures the second number (0001)
            image_number = match.group(1)
            logging.info(f'The image number is: {image_number}')
            return 'None', image_number
        else:
            return 'None', image_number
    logging.info(f'This is the url: {url}')
    logging.info(f'This is the url: {state}')
    logging.error(f'Couldnt find the batch')
    return None, None

# Append a single row to .csv
def write_row_to_csv(row, state_name, error = False):
    state_formatted = state_name.replace(" ", "_")
    current_file_path = os.path.join(file_path, state_name)
    current_csv_file_path = os.path.join(current_file_path, f'nara_census_1950_{state_formatted}.csv')

    if error == False:
        
        with open(current_csv_file_path, 'a', encoding = 'utf-8') as work_file:
            row_text = ''
            # Each pipeline indicates the start of a new column in the .csv file
            for item in row:
                row_text += item + '|'
            row_text = row_text[:-1]
            row_text = row_text + '\n'
            work_file.write(row_text)
            #print("It is working and going through the file writing thing")
    else:
        logging.info(f'This is the error row: {row}')
        raise ValueError

def main():
    #write_row_to_csv(title)
    logging.info("Starting the web scraping process.")

    scrape_page(url)
    logging.info("Web scraping process completed.")

if __name__ == "__main__":
    main()
