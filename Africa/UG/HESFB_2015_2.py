import logging
import os
import re
import sys
import pdfplumber

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_modules.scraping import timer, write_row_to_csv

'''
pip install pdfplumber
'''

URL = 'https://www.dropbox.com/scl/fi/r4cdl7ipyu40xkslciwze/HESFB-2015-16-List-of-Successful-Approved-Beneficiaries-Diploma.pdf?dl=0&e=1&rlkey=l3y0bwdttxdak57c22y8k6yg0'
PDF_PATH = ''
SAVE_FILE_PATH = ''

# Set up logging
log_file_path = os.path.join(SAVE_FILE_PATH, 'UG_HESLB_2015_2.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

@timer
def extract_data():
    with pdfplumber.open(PDF_PATH) as pdf:
        pdf_length = len(pdf.pages)

        for j in range(pdf_length):
            
            page_text = pdf.pages[j].extract_text().split('\n')

            if j == 0:
                for i, text in enumerate(page_text):
                    if i <= 1:
                        continue
                    row = []
                    if i == 2:
                        row = ['S/No', 'Name of Applicant', 'Gender', 'District of Origin', 'University', 'Course', 'Duration']
                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_2')
                    else:
                        if text == '' or text == '.':
                            continue
                        row = transform_string(text)

                        # Replace the commas to not mess up the .csv file
                        for k, column in enumerate(row):
                            row[k] = column.replace(',', '-')

                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_2')
                continue

            for i, text in enumerate(page_text):
                    if i <= 1:
                        continue
                    row = []
                    if text == '' or text == '.':
                        continue
                    row = transform_string(text)

                    # Replace the commas to not mess up the .csv file
                    for k, column in enumerate(row):
                        row[k] = column.replace(',', '-')

                    write_row_to_csv(row, SAVE_FILE_PATH, 'data_2')

# Transforms the string into desired format for csv table
def transform_string(input_string):
    pattern = r'(\d+)\s+(.*?)\s+([FM])\s+(.*?)\s+((?:.*?)\s(?:University|College\sMulago))\s+(.*?)\s*(\d+.+)'
    match = re.match(pattern, input_string)
    
    if match:
        return list(match.groups())
    else:
        print(input_string)
        return None
    

# Specify the path to the PDF and the desired output CSV file
if __name__ == "__main__":
    extract_data()
