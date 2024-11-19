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

URL = 'https://www.dropbox.com/scl/fi/jzz3o7gmk7lromlenkujk/Loan-Beneficiairies-2017.18-for-Media-Degree-Report.pdf?rlkey=2xn0d9a340ywkgilup69lb1e5&dl=0'
PDF_PATH = ''
SAVE_FILE_PATH = ''

# Set up logging
log_file_path = os.path.join(SAVE_FILE_PATH, 'UG_HESFB_2017_undergraduate_beneficiaries.log')
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
                        row = ['S.No', 'Name of Applicant', 'Gender', 'District of Origin', 'Schools', 'Admitted Course', 'Course Duration']
                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_undergraduate_beneficiaries')
                    else:
                        if text == '' or text == '.' or text[:4] == 'Page':
                            continue
                        row = transform_string(text)

                        # Replace the commas to not mess up the .csv file
                        for k, column in enumerate(row):
                            if k == 0:
                                row[k] = column.replace(',', '')
                            else:
                                row[k] = column.replace(',', '-')

                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_undergraduate_beneficiaries')
                continue

            for i, text in enumerate(page_text):
                    if i <= 2:
                        continue
                    row = []
                    if text == '' or text == '.' or text[:4] == 'Page':
                        continue
                    row = transform_string(text)

                    # Replace the commas to not mess up the .csv file
                    for k, column in enumerate(row):
                        if k == 0:
                            row[k] = column.replace(',', '')
                        else:
                            row[k] = column.replace(',', '-')

                    write_row_to_csv(row, SAVE_FILE_PATH, 'data_undergraduate_beneficiaries')

# Transforms the string into desired format for csv table
def transform_string(input_string):
    pattern = r'(\d+)\s+(.*?)\s+([FM])\s+([A-Za-z]+)\s+((?:.*?)\s(?:University|Tech|College Mulago))\s+(.*?)\s*(\d+.+)'
    match = re.match(pattern, input_string)
    
    pattern_2_digit = r'(\d+)\s+(\d+)\s+(.*?)\s+([FM])\s+([A-Za-z]+)\s+((?:.*?)\s(?:University|Tech|College Mulago))\s+(.*?)\s*(\d+.+)'
    match_2_digit = re.match(pattern_2_digit, input_string)
    
    pattern_3_digit = r'(\d+)\s+(,\d+)\s+(.*?)\s+([FM])\s+([A-Za-z]+)\s+((?:.*?)\s(?:University|Tech|College Mulago))\s+(.*?)\s*(\d+.+)'
    match_3_digit = re.match(pattern_3_digit, input_string)
    
    if match_3_digit:
        return [f'{match_3_digit.group(1)}{match_3_digit.group(2)}', match_3_digit.group(3), match_3_digit.group(4), match_3_digit.group(5), match_3_digit.group(6), match_3_digit.group(7), match_3_digit.group(8)]
    elif match_2_digit:
        return [f'{match_2_digit.group(1)}{match_2_digit.group(2)}', match_2_digit.group(3), match_2_digit.group(4), match_2_digit.group(5), match_2_digit.group(6), match_2_digit.group(7), match_2_digit.group(8)]
    elif match:
        return list(match.groups())
    else:
        print(input_string)
        return None
    

# Specify the path to the PDF and the desired output CSV file
if __name__ == "__main__":
    extract_data()
