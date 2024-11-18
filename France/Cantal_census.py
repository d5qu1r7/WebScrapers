import logging
import os
import re
import sys
import time

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import sync_playwright
from unidecode import unidecode

from my_modules.scraping import timer, write_row_to_csv, image_download, screenshot_page

'''
pip install playwright unidecode
python -m playwright install
'''

BASE_URL = 'https://archives.cantal.fr/rechercher/genealogie/listes-nominatives-de-recensement-numerisees?detail=1879632&positionResult=1&arko_default_5f9274ef15acf--filtreGroupes%5Bmode%5D=simple&arko_default_5f9274ef15acf--filtreGroupes%5Bop%5D=AND&arko_default_5f9274ef15acf--from=0&arko_default_5f9274ef15acf--resultSize=100&arko_default_5f9274ef15acf--contenuIds%5B0%5D=2890788&arko_default_5f9274ef15acf--modeRestit=arko_default_5f92759e26bf3&referrer=%2Frechercher%2Fgenealogie%2Flistes-nominatives-de-recensement-numerisees&previousReferrer=%2Frechercher%2Fgenealogie%2Flistes-nominatives-de-recensement-numerisees'
SAVE_FILE_PATH_STATE = 'w:/RA_work_folders/Davis_Holdstock/France/Cantal/Census/'
SAVE_FILE_PATH = 'w:/papers/current/french_records/french_record_images/Cantal/Census/'
TOTAL_PAGES = 270

# Set up logging
log_file_path = os.path.join(SAVE_FILE_PATH, 'census.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_page(page):
    global BASE_URL, SAVE_FILE_PATH, TOTAL_PAGES

    page.goto(BASE_URL)    

    for i in range(TOTAL_PAGES):

        if i < 4: # FIXME: This is for testing only
            # Wait for the page to load completely
            page.wait_for_load_state('networkidle')
            time.sleep(2)
            main_section = page.locator('article')
            next_button = main_section.locator('#nav_detail_container').locator('nav').locator('a.resultat_suivant')
            if i != TOTAL_PAGES:
                next_button.click()
            continue

        # Wait for the page to load completely
        page.wait_for_load_state('networkidle')
        time.sleep(2)

        meta_data = page.locator('div.champ_detail').all()
        cote = ''
        nom_geographique = ''

        for n, meta in enumerate(meta_data):
            if n == 1:
                cote = meta.locator('div.champ_contenu').inner_text()
            if n == (2 if len(meta_data) == 5 else 3):
                nom_geographique_elements = meta.locator('div.champ_contenu').locator('li').all()
                nom_geographique = nom_geographique_elements[0].inner_text()

        # Convert to English equivalents
        english_string_cote = unidecode(cote)
        english_string_nom_geographique = unidecode(nom_geographique)

        # Remove spaces and special characters
        clean_string_cote = re.sub(r'[^A-Za-z0-9/]', '_', english_string_cote)
        clean_string_nom_geographique = re.sub(r'[^A-Za-z0-9/]', '_', english_string_nom_geographique)

        save_page_path = f'{clean_string_cote}/{clean_string_nom_geographique}/'

        main_section = page.locator('article')

        figures = main_section.locator('figure').all()
        next_button = main_section.locator('#nav_detail_container').locator('nav').locator('a.resultat_suivant')

        if len(figures) > 1:
            figure = figures[0]
        else:
            figure = main_section.locator('figure')
            
        url = f'\"{BASE_URL}{figure.locator('button').get_attribute('data-visionneuse-url')}\"'
        caption = figure.locator('figcaption').inner_text()
        row = caption.split(', ')
        result = "/".join(row)

        # Convert to English equivalents
        english_string = unidecode(result)

        # Remove spaces and special characters
        clean_string = re.sub(r'[^A-Za-z0-9/]', '_', english_string)

        figure.scroll_into_view_if_needed()

        time.sleep(2)

        figure.locator('button').click()

        # Wait for the page to load completely
        page.wait_for_load_state('networkidle')
        time.sleep(2)

        try:
            if page.locator('.viewer-container').locator('h2').inner_text() == 'Licence clic':
                accept_button = page.locator('.viewer-container').locator('button')
                accept_button.click()
                time.sleep(5)
                storage = page.context.storage_state(path=f"{SAVE_FILE_PATH}/cantal_census_state.json")

            main_tab = page.locator('.visionneuse_arkotheque')
            more_tab = main_tab.locator('.bouton_volet')
            close_button = main_tab.locator('.close')
            more_tab.click()

            # Wait for the page to load completely
            page.wait_for_load_state('networkidle')
            time.sleep(1)

            pictures = main_tab.locator('section')
            nav_bar = pictures.locator('nav')
            tabs = nav_bar.locator('li').all()
            all_pics_tab = tabs[3]
            download_tab = tabs[4]

            # Move the mouse slightly (10 pixels to the right and 10 pixels down)
            page.mouse.move(10, 10)

            all_pics_tab.click()

            # Wait for the page to load completely
            page.wait_for_load_state('networkidle')
            time.sleep(4)

            individual_pictures = pictures.locator('div').locator('nav')

            # If the page has more than one image there is an options selector on the pdfs, if not there is not one
            if len(figures) > 1:

                options_selector = individual_pictures.locator('select')
                options = options_selector.locator('option').all()

                for l in range(len(options)):
                    # if l > 1:
                    #     continue

                    option = (options[l].inner_text())[6:]
                    row_option = option.split(', ')
                    result_option = "/".join(row_option)

                    # Convert to English equivalents
                    english_string_option = unidecode(result_option)

                    # Remove spaces and special characters
                    clean_string_option = re.sub(r'[^A-Za-z0-9/]', '_', english_string_option)

                    # Wait for the page to load completely
                    page.wait_for_load_state('networkidle')

                    # Select an option by its value
                    options_selector.select_option(f'{l}')

                    # Wait for the page to load completely
                    page.wait_for_load_state('networkidle')
                    time.sleep(5)

                    individual_pics = individual_pictures.locator('li').all()
                    
                    for m, pics in enumerate(individual_pics):
                        # if m != 0:
                        #     continue

                        pics.scroll_into_view_if_needed()
                        pics.click()
                        
                        # Wait for the page to load completely
                        page.wait_for_load_state('networkidle')
                        time.sleep(1)

                        download_tab.click()
                        time.sleep(1)

                        download_selector = pictures.locator('.contenu_onglet').locator('a').all()
                        download_button = download_selector[0]

                        print(f'Downloading image {m}')
                        image_download(page, f'{SAVE_FILE_PATH}{save_page_path}{clean_string_option}/', f'image_{m}.jpg', download_button)
                        time.sleep(1)

                        all_pics_tab.click()
                        time.sleep(1)

                    # Log the pdf that was processed
                    logging.info(f'Processed: {row_option}')
                    print(f'Processed: {row_option}')

                    url = f'\"{page.url}\"'

                    row_option.append(url)

                    row_option_final = [f'\"{cote}\"', f'\"{nom_geographique}\"']

                    for r_o in row_option:
                        row_option_final.append(r_o)

                    write_row_to_csv(row_option_final, SAVE_FILE_PATH, f'images')

                close_button.click()

            else:

                # Log the pdf being processed
                logging.info(f'Processing: {row}')
                print(f'Processing: {row}')

                individual_pics = individual_pictures.locator('li').all()
                    
                for m, pics in enumerate(individual_pics):
                    # if m > 1:
                    #     continue

                    pics.scroll_into_view_if_needed()
                    pics.click()
                    
                    # Wait for the page to load completely
                    page.wait_for_load_state('networkidle')
                    time.sleep(1)

                    download_tab.click()
                    time.sleep(1)

                    download_selector = pictures.locator('.contenu_onglet').locator('a').all()
                    download_button = download_selector[0]

                    print(f'Downloading image {m}')
                    image_download(page, f'{SAVE_FILE_PATH}{save_page_path}{clean_string}/', f'image_{m}.jpg', download_button)
                    time.sleep(1)

                    all_pics_tab.click()
                    time.sleep(1)

                # Convert to English equivalents
                english_row = unidecode(caption)

                row = english_row.split(', ')
                row.append(url)

                write_row_to_csv(row, SAVE_FILE_PATH, f'images')

                close_button.click()

            print(f'Finished Scraping page {i}')
            logging.info(f'Finished Scraping page {i}')
            
            if i != TOTAL_PAGES:
                next_button.click()
        except:
            main_tab = page.locator('.visionneuse_arkotheque')
            more_tab = main_tab.locator('.bouton_volet')
            close_button = main_tab.locator('.close')
            more_tab.click()

            # Wait for the page to load completely
            page.wait_for_load_state('networkidle')
            time.sleep(1)

            pictures = main_tab.locator('section')
            nav_bar = pictures.locator('nav')
            tabs = nav_bar.locator('li').all()
            all_pics_tab = tabs[3]
            download_tab = tabs[4]

            # Move the mouse slightly (10 pixels to the right and 10 pixels down)
            page.mouse.move(10, 10)

            all_pics_tab.click()

            # Wait for the page to load completely
            page.wait_for_load_state('networkidle')
            time.sleep(4)

            individual_pictures = pictures.locator('div').locator('nav')

            # If the page has more than one image there is an options selector on the pdfs, if not there is not one
            if len(figures) > 1:

                options_selector = individual_pictures.locator('select')
                options = options_selector.locator('option').all()

                for l in range(len(options)):
                    # if l > 1:
                    #     continue

                    option = (options[l].inner_text())[6:]
                    row_option = option.split(', ')
                    result_option = "/".join(row_option)

                    # Convert to English equivalents
                    english_string_option = unidecode(result_option)

                    # Remove spaces and special characters
                    clean_string_option = re.sub(r'[^A-Za-z0-9/]', '_', english_string_option)

                    # Wait for the page to load completely
                    page.wait_for_load_state('networkidle')

                    # Select an option by its value
                    options_selector.select_option(f'{l}')

                    # Wait for the page to load completely
                    page.wait_for_load_state('networkidle')
                    time.sleep(5)

                    individual_pics = individual_pictures.locator('li').all()
                    
                    for m, pics in enumerate(individual_pics):
                        # if m != 0:
                        #     continue

                        pics.scroll_into_view_if_needed()
                        pics.click()
                        
                        # Wait for the page to load completely
                        page.wait_for_load_state('networkidle')
                        time.sleep(1)

                        download_tab.click()
                        time.sleep(1)

                        download_selector = pictures.locator('.contenu_onglet').locator('a').all()
                        download_button = download_selector[0]

                        print(f'Downloading image {m}')
                        image_download(page, f'{SAVE_FILE_PATH}{save_page_path}{clean_string_option}/', f'image_{m}.jpg', download_button)
                        time.sleep(1)

                        all_pics_tab.click()
                        time.sleep(1)

                    # Log the pdf that was processed
                    logging.info(f'Processed: {row_option}')
                    print(f'Processed: {row_option}')

                    url = f'\"{page.url}\"'

                    row_option.append(url)

                    row_option_final = [f'\"{cote}\"', f'\"{nom_geographique}\"']

                    for r_o in row_option:
                        row_option_final.append(r_o)

                    write_row_to_csv(row_option_final, SAVE_FILE_PATH, f'images')

                close_button.click()

            else:

                # Log the pdf being processed
                logging.info(f'Processing: {row}')
                print(f'Processing: {row}')

                individual_pics = individual_pictures.locator('li').all()
                    
                for m, pics in enumerate(individual_pics):
                    # if m > 1:
                    #     continue

                    pics.scroll_into_view_if_needed()
                    pics.click()
                    
                    # Wait for the page to load completely
                    page.wait_for_load_state('networkidle')
                    time.sleep(1)

                    download_tab.click()
                    time.sleep(1)

                    download_selector = pictures.locator('.contenu_onglet').locator('a').all()
                    download_button = download_selector[0]

                    print(f'Downloading image {m}')
                    image_download(page, f'{SAVE_FILE_PATH}{save_page_path}{clean_string}/', f'image_{m}.jpg', download_button)
                    time.sleep(1)

                    all_pics_tab.click()
                    time.sleep(1)

                # Convert to English equivalents
                english_row = unidecode(caption)

                row = english_row.split(', ')
                row.append(url)

                write_row_to_csv(row, SAVE_FILE_PATH, f'images')

                close_button.click()

            print(f'Finished Scraping page {i}')
            logging.info(f'Finished Scraping page {i}')
            
            if i != TOTAL_PAGES:
                next_button.click()
@timer
def main():
    global SAVE_FILE_PATH, SAVE_FILE_PATH_STATE

    # Create new playwright instance
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless = True)
        context = browser.new_context(storage_state=f"{SAVE_FILE_PATH_STATE}/cantal_census_state.json")
        page = context.new_page()

        # If the list scraper breaks, the try catch block will restart it
        try:
            scrape_page(page)
        except:
            # main(page)
            print("Something went wrong, exiting program.")
            screenshot_page(page, SAVE_FILE_PATH, 'problem', False)
            raise Exception

        page.close()
        context.close()
        browser.close()

if __name__ == '__main__':
    main()
