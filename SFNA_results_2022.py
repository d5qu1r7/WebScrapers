import os
from playwright.sync_api import sync_playwright, expect
import time

#------------------------------------------------ Working (change FIXME) ------------------------------------------------#
# Where the archive is located.
baselink = 'https://onlinesys.necta.go.tz/results/2022/sfna/sfna.htm'
SAVE_FILE_PATH = '' # FIXME: Change to the perminant file path the .csv files will be stored in

def interact_with_page(page):
    # Going to the page with the archives
    page.goto(baselink)

    # Wait for the page to load completely
    page.wait_for_load_state('networkidle')
    time.sleep(2)

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

            # if i != 0: #FIXME This is just for testing
            #     continue

            try:
                name_region = column_region.locator('a').inner_text(timeout=5000)
                print(f"Processing region: {name_region}")
            except TimeoutError:
                print(f"Timeout occurred while getting region name number {i}. Skipping this item.")
                continue
            
            # Check for a blank name
            if name_region == '':
                continue

            # print(name_region)
            column_region.locator('a').click()

            # Wait for the page to load completely
            page.wait_for_load_state('networkidle')
            time.sleep(2)

            # Wait for a table to be present
            expect(page.locator('tbody'))

            # Find the table
            table_province = page.locator('tbody')
            # Get all the rows of the table
            all_rows_province = table_province.locator('tr').all()

#----------------------------------------------------------- Loop Through Province -----------------------------------------------------------#

            # Create a variable to keep track of the provinces
            j = 0
            
            # Loop through the rows
            for row_province in all_rows_province:
                full_row_province = row_province.locator('td').all()
                for column_province in full_row_province:

                    # if j != 0: #FIXME This is just for testing
                    #     continue

                    try:    
                        name_province = column_province.locator('a').inner_text(timeout=5000)
                        print(f"Processing province: {name_province}")
                    except TimeoutError:
                        print(f"Timeout occurred while getting province name number {j}. Skipping this item.")
                        continue

                    # Check for a blank name
                    if name_province == '':
                        continue

                    # print(name_province)

                    column_province.locator('a').click()

                    # Wait for the page to load completely
                    page.wait_for_load_state('networkidle')
                    time.sleep(2)

                    # Wait for a table to be present
                    expect(page.locator('tbody'))

                    # Find the table
                    table_school = page.locator('tbody')
                    # Get all the rows of the table
                    all_rows_school = table_school.locator('tr').all()

#----------------------------------------------------------- Loop Through School -----------------------------------------------------------#
                    
                    # Create a variable to keep track of the councils
                    l = 0

                    # Loop through the rows
                    for row_school in all_rows_school:
                        full_row_school = row_school.locator('td').all()
                        for column_school in full_row_school:

                            # if l != 0: #FIXME This is just for testing, and only clicks on the first link
                            #     continue

                            try:
                                name_school = column_school.locator('a').inner_text(timeout=5000)
                                print(f"Processing school: {name_school}")
                            except TimeoutError:
                                print(f"Timeout occurred while getting school name number {l}. Skipping this item.")
                                continue

                            # Check for a blank name
                            if name_school == '':
                                continue

                            # print(name_school)

                            column_school.locator('a').click()

                            # Wait for the page to load completely
                            page.wait_for_load_state('networkidle')
                            time.sleep(2)

                            # Wait for a table to be present
                            expect(page.locator('tbody'))

                            # Find the table
                            table_school_tables = page.locator('tbody').all()

#----------------------------------------------------------- Loop Through Tables -----------------------------------------------------------#

                            # Create a variable to keep track of the tables
                            m = 0

                            for table_school_table in table_school_tables:

                                if m == 0: # This skips the first table that has another table inside of it
                                    all_rows_school_table = table_school_table.locator('tr').all()
                                    # Create a variable to keep track of the rows
                                    o = 0

                                    # This skips the first table that thas another table inside of it
                                    if o > 0:
                                        m += 1
                                        o += 1
                                        continue

                                    # Create a varable to only get the first row
                                    p = 0

                                    # Loop through the rows
                                    for row_school_table in all_rows_school_table:

                                        # This skips the first row
                                        if p > 0:
                                            p += 1
                                            o += 1
                                            continue

                                        row_data = []

                                        full_row_school_table = row_school_table.locator('td, th').all()
                                        for column_school_table in full_row_school_table:

                                            file_path = f'{SAVE_FILE_PATH}{name_region.replace(" ", "_")}/{name_province.replace(" ", "_")}/{name_school.replace(" ", "_")}/'
                                            file_name = f'table_{m}'

                                            # Adding everything to a row and writing to .csv
                                            row_data.append(column_school_table.inner_text().replace("\n", " ").replace(",", " "))
                                        write_row_to_csv(row_data, file_path, file_name)
                                        o += 1
                                        p += 1
                                    m += 1
                                    continue

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

                                        file_path = f'{SAVE_FILE_PATH}{name_region.replace(" ", "_")}/{name_province.replace(" ", "_")}/{name_school.replace(" ", "_")}/'
                                        file_name = f'table_{m}'

                                        # Adding everything to a row and writing to .csv
                                        row_data.append(column_school_table.inner_text().replace("\n", " ").replace(",", " "))
                                    write_row_to_csv(row_data, file_path, file_name)
                                    n += 1
                                m += 1

                            # Use synchronous go_back() method to go back a page
                            page.go_back()
                            page.wait_for_load_state('networkidle')
                            l += 1
                    # Use synchronous go_back() method to go back a page
                    page.go_back()
                    page.wait_for_load_state('networkidle')
                    j += 1
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
    browser = pw.chromium.launch(headless = True)
    context = browser.new_context()
    page = context.new_page()

    # If the list scraper breaks, the try catch block will restart it
    try:
        interact_with_page(page)
    except:
        print("Something went wrong, exiting program.")

    page.close()
    context.close()
    browser.close()
