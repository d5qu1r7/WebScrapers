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

URL = 'https://www.dropbox.com/scl/fi/d2hcmjh46mqwle44ovh9t/HESFB-Final-List-of-Successful-Applicants-2018-19_0.pdf?rlkey=6e4x7kbg6yf6wkbi7cexpudal&dl=0'
PDF_PATH = ''
SAVE_FILE_PATH = ''

# Set up logging
log_file_path = os.path.join(SAVE_FILE_PATH, 'UG_HESFB_2018_successful_applicants.log')
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
                    if i <= 2:
                        continue
                    row = []
                    if i == 3:
                        row = ['S/No', 'Application No.', 'Name of Applicant', 'Gender', 'Telephone', 'District of Origin', 'Admitted University', 'Admitted Course', 'Course Duration', 'Course Type', 'Region']
                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_successful_applicants')
                    else:
                        if text == '' or text == '.' or text[:4] == 'Page':
                            continue
                        row = transform_string(text)

                        # Replace the commas to not mess up the .csv file
                        for k, column in enumerate(row):
                            row[k] = column.replace(',', '-')

                        write_row_to_csv(row, SAVE_FILE_PATH, 'data_successful_applicants')
                continue

            for i, text in enumerate(page_text):
                    row = []
                    if text == '' or text == '.' or text[:4] == 'Page':
                        continue
                    row = transform_string(text)

                    # Replace the commas to not mess up the .csv file
                    for k, column in enumerate(row):
                        row[k] = column.replace(',', '-')

                    write_row_to_csv(row, SAVE_FILE_PATH, 'data_successful_applicants')

# Transforms the string into desired format for csv table
def transform_string(input_string):
    pattern = r'(\d+)\s+(HESFB/2018/\d+)\s+(.*?)([FM])\s+(\d+)\s+([A-Za-z]+)\s+((?:.*?)(?:School|Clinical Officers|Fortportal|INSTITUTE|Midwifery|Officers,Gulu|Comprehensive Nursing|BusinessSch|University|Technology|College|College Mulago|College,Lira|College, Bushenyi|College,Elgon|Mbale|Uganda|Management))(.*?)\s*(\d+.+years)\s+([A-Za-z]+)\s+([A-Za-z]+)'
    match = re.match(pattern, input_string)
    
    # This line is messed up
    if input_string == '554 HESFB/2018/04803 COLLIN MAGULU M 0702113835 Kamuli Kyambogo University Ordinary Diploma in Science Technology (Biology, Physics, Ch3e ymeiasrtsry) Diploma Eastern':
        return ['554', 'HESFB/2018/04803', 'COLLIN MAGULU', 'M', '0702113835', 'Kamuli', 'Kyambogo University', 'Ordinary Diploma in Science Technology (Biology, Physics, Chemistry)', '3 years', 'Diploma', 'Eastern']
    # This line is also messed up
    elif input_string == '1280 HESFB/2018/01574 HENRY SSEMPIJJA M 0700804347 Wakiso Ndejje University BSc. Information Technology (Student passed Mathematics/P3h yyesaicrss at A ‘LDeveeglr)ee Central':
        return ['1280', 'HESFB/2018/01574', 'HENRY SSEMPIJJA', 'M', '0700804347', 'Wakiso', 'Ndejje University', 'BSc. Information Technology (Student passed Mathematics Physics at A Level', '3 years', 'Degree', 'Central']
    elif match:
        return list(match.groups())
    else:
        print(input_string)
        return None
    

# Specify the path to the PDF and the desired output CSV file
if __name__ == "__main__":
    extract_data()
