import logging
import os
from playwright.sync_api import sync_playwright, expect
import time

#------------------------------------------------ Working (change FIXME) ------------------------------------------------#
# Where the archive is located.
baselink = 'https://onlinesys.necta.go.tz/results/2021/gatce/index.htm'
SAVE_FILE_PATH = ''

# Set up logging os.path.dirname(__file__)
log_file_path = os.path.join(SAVE_FILE_PATH, 'GATCE_2021.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def interact_with_page(page):
    # Going to the page with the archives
    page.goto(baselink)

    # Wait for the page to load completely
    page.wait_for_load_state('networkidle')
    time.sleep(2)

    # Wait for a table to be present
    expect(page.locator('tbody'))

    # Find the table
    tables_main = page.locator('tbody').all()

    # Create a variable for the number of tables
    i = 0

    # Loop through all the main page tables
    for table_main in tables_main:
        if i == 1:

#----------------------------------------------------------- Loop Through Letters -----------------------------------------------------------#

            # Create a variable to keep track of the Letters
            j = 0

            all_rows_letters = table_main.locator('tr').all()
            for row_letters in all_rows_letters:
                full_row_letters = row_letters.locator('td').all()
                for column_letters in full_row_letters:

                    # The first column needs to be clicked so that all schools are visable
                    if j == 0:
                        try:
                            name_letters = column_letters.locator('a').inner_text(timeout=5000)
                            logging.info(f"Processing letter: {name_letters}")
                            print(f"Processing letter: {name_letters}")
                        except:
                            error_message = f"Error occurred while getting letter name number {j}. Skipping this item."
                            logging.error(error_message)
                            print(error_message)
                            continue

                        # Check for a blank name
                        if name_letters == '':
                            continue

                        # Click on the letter
                        column_letters.locator('a').click()

                        # Wait for the page to load completely
                        page.wait_for_load_state('networkidle')
                        time.sleep(2)

                    j += 1
        elif i == 2:
                        
#----------------------------------------------------------- Loop Through School -----------------------------------------------------------#
                    
            # Create a variable to keep track of the councils
            k = 0

            all_rows_school = table_main.locator('tr').all()
            # Loop through the rows
            for row_school in all_rows_school:
                full_row_school = row_school.locator('td').all()
                for column_school in full_row_school:

                    # FIXME: For testing purposes only
                        # if k > 1:
                        #     k += 1
                        #     continue

                        try:
                            name_school = column_school.locator('a').inner_text(timeout=5000)
                            logging.info(f"Processing school: {name_school}")
                            print(f"Processing school: {name_school}")
                        except:
                            error_message = f"Error occurred while getting school name number {j}. Skipping this item."
                            logging.error(error_message)
                            print(error_message)
                            continue

                        # Check for a blank name
                        if name_school == '':
                            continue

                        # Click on the letter
                        column_school.locator('a').click()

                        # Wait for the page to load completely
                        page.wait_for_load_state('networkidle')
                        time.sleep(2)

                        # Wait for a table to be present
                        expect(page.locator('tbody'))

                        # Find the table
                        table_school_tables = page.locator('tbody').all()

#----------------------------------------------------------- Loop Through Tables In School Records -----------------------------------------------------------#

                        # Create a variable to keep track of the tables
                        m = 0

                        for table_school_table in table_school_tables:

                            # Get all the rows of the table
                            all_rows_school_table = table_school_table.locator('tr').all()

#----------------------------------------------------------- Loop Through Rows in school tables -----------------------------------------------------------#

                            # Create a variable to keep track of the rows
                            n = 0

                            # Loop through the rows
                            for row_school_table in all_rows_school_table:

                                row_data = []

                                full_row_school_table = row_school_table.locator('td, th').all()
                                for column_school_table in full_row_school_table:

                                    file_path = f'{SAVE_FILE_PATH}{name_school.replace(" ", "_")}/'
                                    
                                    file_name = f'table_{m}'

                                    # Adding everything to a row and writing to .csv
                                    row_data.append(column_school_table.inner_text().replace("\n", " ").replace(",", " "))
                                write_row_to_csv(row_data, file_path, file_name)
                                n += 1
                            m += 1
                        k += 1

                        # Use synchronous go_back() method to go back a page
                        page.go_back()
                        page.wait_for_load_state('networkidle')
        i += 1

    print('Finished collecting names')

# Screenshot the current page
def screenshot_page(file_path, file_name):

    # Create the directories for the file path
    # exist_ok=True means that no errors are raised if the file path is already there
    os.makedirs(file_path, exist_ok=True)

    print(f"Path '{file_path}' created successfully!")

    page.screenshot(path=f'{file_path}{file_name}.png', full_page=True)

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
    start_time = time.time()
    browser = pw.chromium.launch(headless = True)
    context = browser.new_context()
    page = context.new_page()

    # If the list scraper breaks, the try catch block will restart it
    try:
        interact_with_page(page)
    except:
        print("Something went wrong, exiting program.")

    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Convert the elapsed time to hours, minutes, and seconds
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)

    elapsed_time = f"--- {int(hours)} hours, {int(minutes)} minutes, {seconds:.2f} seconds ---"
    logging.info(elapsed_time)
    print(elapsed_time)

    page.close()
    context.close()
    browser.close()
