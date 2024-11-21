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

URL = 'https://www.dropbox.com/scl/fi/31dx7lmf1qmzx5j42vaq6/Consolidated-Students-Loan-Scheme-Beneficiaries-for-the-AY2021-22.pdf?rlkey=js8bbo5rzrth6vyb9e3vfq4cu&dl=0'
PDF_PATH = ''
SAVE_FILE_PATH = ''

# Set up logging
log_file_path = os.path.join(SAVE_FILE_PATH, 'UG_HESFB_2021_successful_applicants.log')
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
                        row = ['S/No.', 'Application No.', 'Name of Applicant', 'Gender', 'District of Origin', 'Admitted University', 'Admitted Course', 'Course Duration', 'Course Type']
                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_successful_applicants')
                    else:
                        if text == '' or text[:4] == 'Page':
                            continue
                        row = transform_string(text)

                        if row is None:
                            continue

                        # Replace the commas to not mess up the .csv file
                        for k, column in enumerate(row):
                            row[k] = column.replace(',', '-')

                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_successful_applicants')
                continue

            for i, text in enumerate(page_text):
                    if i <= 2:
                        continue
                    row = []
                    if text == '' or text[:4] == 'Page':
                        continue
                    row = transform_string(text)

                    if row is None:
                        continue

                    # Replace the commas to not mess up the .csv file
                    for k, column in enumerate(row):
                        row[k] = column.replace(',', '-')

                    write_row_to_csv(row, SAVE_FILE_PATH, 'data_successful_applicants')

# Transforms the string into desired format for csv table
def transform_string(input_string):
    pattern = r'(\d+)\s+(HESFB/2021/\d+)\s+(.*?)\s+([FM])\s+([-A-Za-z]+)\s+(.*?)((?:BSc|Bsc|BSC|B\.|Diploma|Dip|B |Bachelor|BACHELOR|BA |NATIONAL HIGHER)(?:.*?))\s*(\d+.+years)\s+([A-Za-z]+)'
    match = re.match(pattern, input_string)
    
    # This line is messed up
    if input_string == '320 HESFB/2021/14805 COSMAS OJWANG M Soroti Gulu University Bachelof of Science Education (Physical, Biological, Economics, Sports Science, Technologica3l yEedaurcsation) Degree':
        return ['320', 'HESFB/2021/14805', 'COSMAS OJWANG', 'M', 'Soroti', 'Gulu University', 'Bachelof of Science Education (Physical, Biological, Economics, Sports Science, Technological Education)', '3 years', 'Degree']
    # This line is also messed up
    elif input_string == '1152 HESFB/2021/13555 OSCAR OWANI M Oyam Gulu University Bachelof of Science Education (Physical, Biological, Economics, Sports Science, Technologica3l yEedaurcsation) Degree':
        return ['1152', 'HESFB/2021/13555', 'OSCAR OWANI', 'M', 'Oyam', 'Gulu University', 'Bachelof of Science Education (Physical, Biological, Economics, Sports Science, Technological Education)', '3 years', 'Degree']
    elif match:
        return list(match.groups())
    else:
        print(input_string)
        return None
    

# Specify the path to the PDF and the desired output CSV file
if __name__ == "__main__":
    extract_data()
