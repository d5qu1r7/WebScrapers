import logging
import os
from playwright.sync_api import sync_playwright, expect
import time

# Set up logging
log_file_path = os.path.join(os.path.dirname(__file__), 'F5_admits.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

#------------------------------------------------ FIXME: The link is broken ------------------------------------------------#
# Where the archive is located.
baselink = 'https://selform.tamisemi.go.tz/Content/selection-and-allocation/2024/first-selection/index.html'
SAVE_FILE_PATH = '' # FIXME: Change to the perminant file path the .csv files will be stored in

def interact_with_page(page):
    # Going to the page with the archives
    page.goto(baselink)

    # Wait for the page to load completely
    page.wait_for_load_state('networkidle')
    time.sleep(4)

    # Wait for a table to be present
    expect(page.locator('tbody'))

    # Find the table
    table_region = page.locator('tbody')
    # Get all the rows of the table
    all_rows_region = table_region.locator('tr').all()

#----------------------------------------------------------- Loop Through Region -----------------------------------------------------------#

    # Create a variable to keep track of the Regions
    i = 0

    # Loop through the rows
    for row_region in all_rows_region:
        full_row_region = row_region.locator('td').all()
        for column_region in full_row_region:

            # if i != 0: #FIXME This is just for testing, and only clicks on the first link
            #     i += 1
            #     continue

            try:
                name_region = column_region.locator('a').inner_text(timeout=60000)
                logging.info(f"Processing region: {name_region}")
                print(f"Processing region: {name_region}")
            except:
                error_message = f"Error occurred while getting region name number {i}. Skipping this item."
                logging.error(error_message)
                print(error_message)
                continue
            
            # Check for a blank name
            if name_region == '':
                continue

            column_region.locator('a').click()
            
            # Wait for the page to load completely
            page.wait_for_load_state('networkidle')
            time.sleep(5)

            # Wait for a table to be present
            expect(page.locator('tbody'))

            # Find the table
            table_council = page.locator('tbody')
            # Get all the rows of the table
            all_rows_council = table_council.locator('tr').all()

#----------------------------------------------------------- Loop Through Council -----------------------------------------------------------#

            # Create a variable to keep track of the councils
            j = 0
            
            # Loop through the rows
            for row_council in all_rows_council:
                full_row_council = row_council.locator('td').all()
                for column_council in full_row_council:

                    if i == 0 and j < 2: #FIXME This is just for testing, and only clicks on the first link
                        j += 1
                        continue

                    try:    
                        name_council = column_council.locator('a').inner_text(timeout=60000)
                        logging.info(f"Processing council: {name_council}")
                        print(f"Processing council: {name_council}")
                    except:
                        error_message = f"Error occurred while getting region {name_region}, council name number {j}. Skipping this item."
                        logging.error(error_message)
                        print(error_message)
                        continue

                    # Check for a blank name
                    if name_council == '':
                        continue

                    column_council.locator('a').click()

                    # Wait for the page to load completely
                    page.wait_for_load_state('networkidle')
                    time.sleep(5)

                    # Wait for a table to be present
                    expect(page.locator('tbody'))

                    # Find the table
                    table_school = page.locator('tbody')
                    # Get all the rows of the table
                    all_rows_school = table_school.locator('tr').all()

                    # Next table has a blank first row, so we need to skip that by keeping track of the row in a variable
                    k = 0

#----------------------------------------------------------- Loop Through School -----------------------------------------------------------#
                    
                    # Create a variable to keep track of the councils
                    l = 0

                    # Loop through the rows
                    for row_school in all_rows_school:
                        if k == 0:
                            k += 1
                            continue
                        full_row_school = row_school.locator('td').all()
                        for column_school in full_row_school:

                            # ARUSHA - ARUSHA DC - S5556 - YAKINI SECONDARY SCHOOL did not work

                            # if i == 0 and j < 2 and l < 108: #FIXME This is just for testing, and only clicks on the first link
                            #     l += 1
                            #     continue

                            page.mouse.wheel(0, 10000)
                            page.mouse.wheel(0, 10000)
                            # name_school = column_school.locator('a').inner_text()
                            try:
                                name_school = column_school.locator('a').inner_text(timeout=60000)
                                logging.info(f"Processing school: {name_school}")
                                print(f"Processing school: {name_school}")
                            except:
                                error_message = f"Error occurred while getting region {name_region}, council {name_council}, school name number {l}. Skipping this item."
                                logging.error(error_message)
                                print(error_message)
                                continue

                            # Check for a blank name
                            if name_school == '':
                                continue

                            column_school.locator('a').click()

                            # Wait for the page to load completely
                            page.wait_for_load_state('networkidle')
                            time.sleep(5)

                            # Wait for a table to be present
                            expect(page.locator('tbody'))

                            # Find the table
                            table_admission_instructions = page.locator('tbody')
                            # Get all the rows of the table
                            all_rows_admission_instructions = table_admission_instructions.locator('tr').all()

                            # Create a variable to keep track of the rows in the table
                            m = 0
                            
#----------------------------------------------------------- Loop Through Admission Instructions -----------------------------------------------------------#

                            # Loop through the rows
                            for row_admission_instructions in all_rows_admission_instructions:
                                
                                row_data = []

                                full_row_admission_instructions = row_admission_instructions.locator('td').all()
                                for column_admission_instructions in full_row_admission_instructions:
                                    
                                    # name_admission_instructions = column_admission_instructions.locator('a').inner_text().replace(" ", "_")
                                    
                                    # # Check for a blank name
                                    # if name_admission_instructions == '':
                                    #     continue
                                    
                                    file_path = f'{SAVE_FILE_PATH}{name_region.replace(" ", "_")}/{name_council.replace(" ", "_")}/'
                                    file_name = f'{name_school.replace(" ", "_")}'

                                    # Adding everything to a row and writing to val_dOise.csv
                                    row_data.append(column_admission_instructions.inner_text().replace("\n", " ").replace(",", " "))
                                write_row_to_csv(row_data, file_path, file_name)

                                m += 1
                            # Use synchronous go_back() method to go back a page
                            page.go_back()
                            page.wait_for_load_state('networkidle')
                            l += 1
                        k += 1
                    # Use synchronous go_back() method to go back a page
                    page.go_back()
                    page.wait_for_load_state('networkidle')
                    j += 1
            # Use synchronous go_back() method to go back a page
            page.go_back()
            page.wait_for_load_state('networkidle')
            i += 1               

    print('Finished collecting CSVs')

def image_download(file_path, file_name, download_button):
    # Define the path for the downloaded file
    save_path = file_path + file_name

    # Create the directories for the file path
    # exist_ok=True means that no errors are raised if the file path is already there
    os.makedirs(file_path, exist_ok=True)

    # print(f"Path '{file_path}' created successfully!")

    # Download the pdf by clicking the link
    with page.expect_download() as download_info:
        download_button.click()
        download = download_info.value
    download.save_as(save_path)

# Append a single row to .csv
def write_row_to_csv(row, file_path, file_name):
    # Create the directories for the file path
    # exist_ok=True means that no errors are raised if the file path is already there
    os.makedirs(file_path, exist_ok=True)

    # print(f"Path '{file_path}' created successfully!")

    csv_file_path = f'{file_path}{file_name}.csv'
    with open(csv_file_path, 'a', encoding='utf-8') as work_file:
        row_text = ''
        # Each pipeline indicates the start of a new column in the .csv file
        for item in row:
            row_text += item + ','
        row_text = row_text[:-1]
        row_text = row_text + '\n'
        work_file.write(row_text)

# Create new playwright instance
with sync_playwright() as pw:
    browser = pw.firefox.launch(headless = True)
    context = browser.new_context()
    page = context.new_page()

    # If the list scraper breaks, the try catch block will restart it
    # try:
    interact_with_page(page)
    # except:
    #     print("Something went wrong, exiting program.")

    page.close()
    context.close()
    browser.close()
