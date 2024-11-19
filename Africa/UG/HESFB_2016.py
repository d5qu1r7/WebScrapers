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

URL = 'https://www.dropbox.com/scl/fi/tvrricq4qhzbk0ofgl8bo/successful-loan-beneficiaries-201617.pdf?rlkey=5ufj0hiy8xe0ea39tbgb7yuui&dl=0'
PDF_PATH = ''
SAVE_FILE_PATH = ''

# Set up logging
log_file_path = os.path.join(SAVE_FILE_PATH, 'HESFB_2016_loan_benficiaries.log')
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
                    if i <= 3:
                        continue
                    row = []
                    if i == 4:
                        row = ['S/No', 'Application No.', 'Name of Applicant', 'Gender', 'District of Origin', 'Admitted University', 'Admitted Course', 'Course Duration (in no. of yrs)']
                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_loan_benficiaries')
                    else:
                        if text == '' or text == '.' or text[:4] == "Page":
                            continue
                        row = transform_string(text)

                        # Replace the commas to not mess up the .csv file
                        for k, column in enumerate(row):
                            row[k] = column.replace(',', '-')

                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_loan_benficiaries')
                continue

            for i, text in enumerate(page_text):
                    if i <= 2:
                        continue
                    row = []
                    if text == '' or text == '.' or text[:4] == "Page":
                        continue
                    row = transform_string(text)

                    # Replace the commas to not mess up the .csv file
                    for k, column in enumerate(row):
                        row[k] = column.replace(',', '-')

                    write_row_to_csv(row, SAVE_FILE_PATH, 'data_loan_benficiaries')

# Transforms the string into desired format for csv table
def transform_string(input_string):
    pattern = r'(\d+)\s+(HESFB/2016/\d+)\s+(.*?)([FM])\s+([A-Za-z]+)\s+((?:.*?)\s(?:University|UNIVERSITY|College\sMulago|Technology|Uganda|Nursing))\s+(.*?)\s*(\d+)'
    match = re.match(pattern, input_string)
    
    pattern_2 = r'(\d+)\s+(HESFB/2016/\d+)\s+(.*?)([FM])\s+([A-Za-z]+)\s+(.*?)((?:Diploma|Ordinary Diploma|National Diploma|Higher Diploma)\s(?:.*?))\s*(\d+)'
    match_2 = re.match(pattern_2, input_string)
    
    pattern_missing_2 = r'(\d+)\s+(.*?)([FM])\s+([A-Za-z]+)\s+((?:.*?)\s(?:University|UNIVERSITY|College\sMulago|Technology|Uganda|Nursing))\s+(.*?)\s*(\d+)'
    match_missing_2 = re.match(pattern_missing_2, input_string)
    
    pattern_2_missing_2 = r'(\d+)\s+(.*?)([FM])\s+([A-Za-z]+)\s+(.*?)((?:Diploma|Ordinary Diploma|National Diploma|Higher Diploma)\s(?:.*?))\s*(\d+)'
    match_2_missing_2 = re.match(pattern_2_missing_2, input_string)
    
    pattern_missing_5 = r'(\d+)\s+(HESFB/2016/\d+)\s+(.*?)([FM])\s+((?:.*?)\s(?:University|UNIVERSITY|College\sMulago|Technology|Uganda|Nursing))\s+(.*?)\s*(\d+)'
    match_missing_5 = re.match(pattern_missing_5, input_string)
    
    if match:
        return list(match.groups())
    elif match_2:
        return list(match_2.groups())
    elif match_missing_2:
        return [match_missing_2.group(1), ' ', match_missing_2.group(2), match_missing_2.group(3), match_missing_2.group(4), match_missing_2.group(5), match_missing_2.group(6), match_missing_2.group(7)]
    elif match_2_missing_2:
        return [match_2_missing_2.group(1), ' ', match_2_missing_2.group(2), match_2_missing_2.group(3), match_2_missing_2.group(4), match_2_missing_2.group(5), match_2_missing_2.group(6), match_2_missing_2.group(7)]
    elif match_missing_5:
        return [match_missing_5.group(1), match_missing_5.group(2), match_missing_5.group(3), match_missing_5.group(4), ' ', match_missing_5.group(5), match_missing_5.group(6), match_missing_5.group(7)]
    else:
        print(input_string)
        return None
    

# Specify the path to the PDF and the desired output CSV file
if __name__ == "__main__":
    extract_data()
