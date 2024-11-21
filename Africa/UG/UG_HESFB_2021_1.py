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

URL = 'https://www.dropbox.com/scl/fi/m99nr7ay5e2qc1p04yqtz/Students-Loans-Scheme-Beneficiaries-List-for-the-AY-2020-21.pdf?rlkey=odpdg37uk6euo11de2lziqbmn&dl=0'
PDF_PATH = ''
SAVE_FILE_PATH = ''

# Set up logging
log_file_path = os.path.join(SAVE_FILE_PATH, 'UG_HESFB_2021_loan_awards_annex_5.log')
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
                        row = ['Application No.', 'Name of Applicant', 'Gender', 'Admitted University', 'Admitted Course', 'Course Duration']
                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_loan_awards_annex_5')
                    else:
                        if text == '' or text[:4] == 'Page':
                            continue
                        row = transform_string(text)

                        # Replace the commas to not mess up the .csv file
                        for k, column in enumerate(row):
                            row[k] = column.replace(',', '-')

                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_loan_awards_annex_5')
                continue

            for i, text in enumerate(page_text):
                    if i <= 2:
                        continue
                    row = []
                    if text == '' or text[:4] == 'Page':
                        continue
                    row = transform_string(text)

                    # Replace the commas to not mess up the .csv file
                    for k, column in enumerate(row):
                        row[k] = column.replace(',', '-')

                    write_row_to_csv(row, SAVE_FILE_PATH, 'data_loan_awards_annex_5')

# Transforms the string into desired format for csv table
def transform_string(input_string):
    pattern = r'(HESFB/2020/\d+)\s+(.*?)\s+([FM])\s+([A-Za-z]+)\s+(.*?)((?:BSc|Bsc|BSC|B\.|Diploma|Dip|B |Bachelor|BA )(?:.*?))\s*(\d+.+years)'
    match = re.match(pattern, input_string)
    
    # This line is messed up
    if input_string == 'HESFB/2020/05741 SARAH NANSASI F Uganda Institute of Allied Health and Management SDeirpvliocmesa, Minu Plhagaormacy 3 years':
        return ['HESFB/2020/05741', 'SARAH NANSASI', 'F', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Pharmacy', '3 years']
    # This line is also messed up
    elif input_string == 'HESFB/2020/08726 SHARON KAMULI F Uganda Institute of Allied Health and Management SDeirpvliocmesa, Minu Plhagaormacy 3 years':
        return ['HESFB/2020/08726', 'SHARON KAMULI', 'F', 'Uganda Institute of Allied Health and Management Services, Mulago', 'Diploma in Pharmacy', '3 years']
    elif match:
        return list(match.groups())
    else:
        print(input_string)
        return None
    

# Specify the path to the PDF and the desired output CSV file
if __name__ == "__main__":
    extract_data()
